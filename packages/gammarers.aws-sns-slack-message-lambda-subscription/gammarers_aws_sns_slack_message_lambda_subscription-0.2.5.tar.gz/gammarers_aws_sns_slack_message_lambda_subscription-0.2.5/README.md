# AWS SNS Slack Message Lambda Subscription

[![GitHub](https://img.shields.io/github/license/gammarers/aws-sns-slack-message-lambda-subscription?style=flat-square)](https://github.com/gammarers/aws-sns-slack-message-lambda-subscription/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarers/aws-sns-slack-message-lambda-subscription?style=flat-square)](https://www.npmjs.com/package/@gammarers/aws-sns-slack-message-lambda-subscription)
[![PyPI](https://img.shields.io/pypi/v/gammarers.aws-sns-slack-message-lambda-subscription?style=flat-square)](https://pypi.org/project/gammarers.aws-sns-slack-message-lambda-subscription/)
[![Nuget](https://img.shields.io/nuget/v/Gammarers.CDK.AWS.SNSSlackMessageLambdaSubscription?style=flat-square)](https://www.nuget.org/packages/Gammarers.CDK.AWS.SNSSlackMessageLambdaSubscription/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/gammarers/aws-sns-slack-message-lambda-subscription/release.yml?branch=main&label=release&style=flat-square)](https://github.com/gammarers/aws-sns-slack-message-lambda-subscription/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/gammarers/aws-sns-slack-message-lambda-subscription?sort=semver&style=flat-square)](https://github.com/gammarers/aws-sns-slack-message-lambda-subscription/releases)

This AWS CDK Construct is designed to post messages sent from an SNS topic to a Slack Webhook via a Lambda function. The Lambda function accepts JSON text as a message, formats it for Slack, and sends it to the Slack Webhook API.

## Sample Message

![](./images/example.png)

```json
{
    "text": ":mega: *TEST*",
    "attachments": [{
        "color": "#2eb886",
        "title": "CodePipeline pipeline execution *SUCCEED*",
        "title_link": "http://github.com/yicr",
        "fields": [
            {
                "title": "Pipeline",
                "value": "pipeline-name"
            }
        ]
    }]
}
```
