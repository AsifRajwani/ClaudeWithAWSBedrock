# Claude With Amazon Bedrock - Course Code Repository

This repository contains code and notebooks for the Skilljar course **Claude with Amazon Bedrock**.

- Course link: https://anthropic.skilljar.com/claude-in-amazon-bedrock
- Goal: keep all course examples, exercises, and related experiments in one place

## Project Origin

This repository was created from the `PythonStarter` template:

- https://github.com/AsifRajwani/PythonStarter

## Prerequisites

- Python 3.11+
- `uv` installed: https://docs.astral.sh/uv/getting-started/installation/
- An AWS account with Amazon Bedrock access

## Local Environment Setup

From the repository root, run:

```bash
# verify uv is installed
uv --version

# install dependencies from pyproject and create/update virtual environment
uv sync

# bootstrap pip in the uv env
uv run python -m ensurepip --upgrade

# upgrade pip itself (optional but recommended)
uv run python -m pip install --upgrade pip

# now install boto (or boto3, etc.)
uv run python -m pip install boto

# install boto3
uv run python -m pip install boto3
```

## Validating the Setup

Use this complete setup and validation guide for Claude on Amazon Bedrock to follow along with the Skilljar course.

### Step 1: Choose Your AWS Region

Go to the **AWS Console** and switch your region to **us-east-1 (N. Virginia)** or **us-west-2 (Oregon)**. These have the broadest Claude model availability.

### Step 2: Enable Anthropic Model Access

Anthropic models are enabled by default on Bedrock, but they still require a one-time usage form before first use:

1. Go to **Amazon Bedrock** in the AWS Console
2. In the left nav, find **Model catalog**
3. Search for **Claude** and click on a model (for example, Claude Sonnet)
4. Click **Submit use case details**
5. Fill out a brief form (for example: "Learning and experimenting with Anthropic models via a Skilljar course")

> Do not skip this step. Without completing the FTU form, first API calls may temporarily succeed but then fail with a `403` error.

### Step 3: Create an IAM User with Bedrock Permissions

For a course/dev setup, create a dedicated IAM user with programmatic access:

1. Go to **IAM -> Users -> Create user**
2. Give it a name like `bedrock-course-user`
3. Attach an inline or managed policy with these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListFoundationModels",
        "bedrock:ListInferenceProfiles",
        "aws-marketplace:Subscribe",
        "aws-marketplace:ViewSubscriptions"
      ],
      "Resource": "*"
    }
  ]
}
```

4. After creating the user, go to **Security credentials -> Create access key**
5. Choose **Local code** as the use case
6. Save the **Access Key ID** and **Secret Access Key** (the secret is shown only once)

### Step 4: Install and Configure the AWS CLI

Install the AWS CLI if needed: https://aws.amazon.com/cli/

Then configure it:

```bash
aws configure
```

Enter when prompted:

- **AWS Access Key ID**: from Step 3
- **AWS Secret Access Key**: from Step 3
- **Default region**: `us-east-1`
- **Default output format**: `json`

Verify it works:

```bash
aws bedrock list-foundation-models --region us-east-1 | grep claude
```

### Step 5: Install the Python SDK (Boto3)

The course examples use Boto3:

```bash
uv run python -m pip install boto3
```

Run the setup validation script:

```bash
uv run python src/validate_bedrock_setup.py
```

Optional: run with an explicit inference profile ID:

```bash
BEDROCK_MODEL_ID=us.anthropic.claude-3-5-sonnet-20241022-v2:0 \
uv run python src/validate_bedrock_setup.py
```

If you get a Claude response back, your setup is working.

### Quick Troubleshooting

| Error | Fix |
|-------|-----|
| `403 / AccessDeniedException` | Complete the Anthropic FTU form in the Bedrock console |
| `ValidationException` mentioning inference profile | Use an inference profile ID in `BEDROCK_MODEL_ID` (example: `us.anthropic.claude-3-5-sonnet-20241022-v2:0`) |
| `ResourceNotFoundException` with "Legacy" model message | Pick an ACTIVE Claude model in Bedrock Model Catalog and set `BEDROCK_MODEL_ID` to its inference profile ID |
| `No credentials found` | Re-run `aws configure` and verify your keys |
| Model not available in region | Switch to `us-east-1` or `us-west-2` |
