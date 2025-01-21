# AWS SNS Slack Message Lambda Subscription

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
