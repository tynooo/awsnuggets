from aws_cdk import (
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_sns as sns,
    core
)
from aws_cdk.aws_lambda_event_sources import SnsEventSource


class UpdateManagedPrefixListsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        function = _lambda.Function(
            self, 'Function',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('update_managed_prefix_lists/lambda'),
            handler='update-ipranges.main',
        )

        function.add_to_role_policy(iam.PolicyStatement(
            resources=["*"],
            actions=["ec2:DescribeManagedPrefixLists",
                     "ec2:ModifyManagedPrefixList",
                     "ec2:GetManagedPrefixListEntries",
                     "ec2:CreateManagedPrefixList"]
            )
        )

        topic = sns.Topic.from_topic_arn(self, "iprangesTopic", topic_arn="arn:aws:sns:us-east-1:806199016981:AmazonIpSpaceChanged")
        function.add_event_source(SnsEventSource(topic))
