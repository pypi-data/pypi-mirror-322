---
parent: Connecting to LLMs
nav_order: 560
---

# Amazon Bedrock

Llmcode can connect to models provided by Amazon Bedrock.
You will need to have an AWS account with access to the Bedrock service.

To configure Llmcode to use the Amazon Bedrock API, you need to set up your AWS credentials.
This can be done using the AWS CLI or by setting environment variables.

## AWS CLI Configuration

If you haven't already, install the [AWS CLI](https://aws.amazon.com/cli/) and configure it with your credentials:

```bash
aws configure
```

This will prompt you to enter your AWS Access Key ID, Secret Access Key, and default region.

## Environment Variables

Alternatively, you can set the following environment variables:

```bash
export AWS_REGION=your_preferred_region

# For user authentication
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key

# For profile authentication
export AWS_PROFILE=your-profile
```

You can add these to your 
[.env file](/docs/config/dotenv.html).

## Install boto3

The AWS Bedrock provider requires the `boto3` package in order to function correctly:

```bash
pip install boto3
```

To use llmcode installed via `pipx` with AWS Bedrock, you must add the `boto3` dependency to llmcode's virtual environment by running

```bash
pipx inject llmcode-chat boto3
```

You must install `boto3` dependency to llmcode's virtual environment installed via one-liner or uv by running

```bash
uv tool run --from llmcode-chat pip install boto3
```


## Running Llmcode with Bedrock

Once your AWS credentials are set up, you can run Llmcode with the `--model` command line switch, specifying the Bedrock model you want to use:

```bash
llmcode --model bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0
```

Sometimes it seems to help if you prefix the model name with "us.":

```bash
llmcode --model bedrock/us.anthropic.claude-3-5-sonnet-20240620-v1:0
```


## Available Models

To see some models available via Bedrock, run:

```bash
llmcode --list-models bedrock/
```

Make sure you have access to these models in your AWS account before attempting to use them with Llmcode.

# More info

For more information on Amazon Bedrock and its models, refer to the [official AWS documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html).

Also, see the 
[litellm docs on Bedrock](https://litellm.vercel.app/docs/providers/bedrock).
