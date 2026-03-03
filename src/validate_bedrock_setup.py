"""Validate AWS Bedrock + Claude access for this repository.

Run:
    uv run python src/validate_bedrock_setup.py
"""

from __future__ import annotations

import json
import os
import sys

import boto3
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError


def choose_active_anthropic_model(bedrock_client) -> str | None:
    """Return a likely active Anthropic model ID, or None if unavailable."""
    response = bedrock_client.list_foundation_models(byProvider="Anthropic")
    summaries = response.get("modelSummaries", [])

    active_text_models: list[str] = []
    for summary in summaries:
        model_id = summary.get("modelId", "")
        lifecycle = summary.get("modelLifecycle", {})
        status = lifecycle.get("status", "")
        input_modalities = summary.get("inputModalities", [])
        supports_text = "TEXT" in input_modalities
        if status == "ACTIVE" and supports_text and model_id:
            active_text_models.append(model_id)

    # Prefer Sonnet-style models for course compatibility.
    sonnet = [m for m in active_text_models if "sonnet" in m.lower()]
    candidates = sonnet or active_text_models
    return sorted(candidates)[-1] if candidates else None


def invoke_with_profile_fallback(client, model_id: str, body: dict) -> tuple[dict, str]:
    """Invoke model and retry with an inference profile when required."""
    serialized = json.dumps(body)
    try:
        response = client.invoke_model(modelId=model_id, body=serialized)
        return response, model_id
    except ClientError as exc:
        error = exc.response.get("Error", {})
        code = error.get("Code", "")
        message = error.get("Message", "")
        needs_profile = (
            code == "ValidationException" and "inference profile" in message.lower()
        )
        has_geo_prefix = model_id.startswith(("us.", "eu.", "apac."))
        if not needs_profile or has_geo_prefix:
            raise

        fallback_model_id = f"us.{model_id}"
        print(
            "On-demand invocation is not supported for this model in this account/region."
        )
        print(f"Retrying with inference profile ID: {fallback_model_id}")
        response = client.invoke_model(modelId=fallback_model_id, body=serialized)
        return response, fallback_model_id


def main() -> int:
    region = os.getenv("AWS_REGION", "us-east-1")
    model_id = os.getenv(
        "BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0"
    )

    runtime_client = boto3.client("bedrock-runtime", region_name=region)
    bedrock_client = boto3.client("bedrock", region_name=region)

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 120,
        "messages": [{"role": "user", "content": "Say hello in one short sentence."}],
    }

    try:
        response, invoked_model_id = invoke_with_profile_fallback(
            runtime_client, model_id, body
        )
        payload = json.loads(response["body"].read())
        text = payload["content"][0]["text"]
        print("Setup validation succeeded.")
        print(f"Region: {region}")
        print(f"Model: {invoked_model_id}")
        print(f"Claude response: {text}")
        return 0
    except NoCredentialsError:
        print(
            "No AWS credentials found. Run `aws configure` and verify your key/secret."
        )
        return 1
    except ClientError as exc:
        error = exc.response.get("Error", {})
        code = error.get("Code", "Unknown")
        message = error.get("Message", str(exc))

        # If default model is legacy, auto-select an active Anthropic model and retry.
        is_legacy_error = (
            code == "ResourceNotFoundException" and "legacy" in message.lower()
        )
        if is_legacy_error:
            try:
                replacement = choose_active_anthropic_model(bedrock_client)
                if replacement:
                    replacement_profile = (
                        replacement
                        if replacement.startswith(("us.", "eu.", "apac."))
                        else f"us.{replacement}"
                    )
                    print(
                        "Requested model is legacy for this account. "
                        f"Retrying with active model: {replacement_profile}"
                    )
                    response = runtime_client.invoke_model(
                        modelId=replacement_profile, body=json.dumps(body)
                    )
                    payload = json.loads(response["body"].read())
                    text = payload["content"][0]["text"]
                    print("Setup validation succeeded.")
                    print(f"Region: {region}")
                    print(f"Model: {replacement_profile}")
                    print(f"Claude response: {text}")
                    return 0
            except ClientError as retry_exc:
                error = retry_exc.response.get("Error", {})
                code = error.get("Code", code)
                message = error.get("Message", message)

        print(f"AWS client error ({code}): {message}")
        print(
            "Check Bedrock model access form completion, IAM permissions, "
            "selected AWS region, and inference profile requirements."
        )
        print(
            "Tip: set BEDROCK_MODEL_ID to an inference profile ID if needed "
            "(example: us.anthropic.claude-3-5-sonnet-20241022-v2:0)."
        )
        print(
            "If you see a legacy-model message, choose an ACTIVE model in the Bedrock "
            "Model Catalog and set BEDROCK_MODEL_ID to its inference profile ID."
        )
        return 1
    except (BotoCoreError, KeyError, json.JSONDecodeError) as exc:
        print(f"Unexpected Bedrock response error: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
