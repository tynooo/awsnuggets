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

        function = _lambda.Function(self, "Function",
            code=_lambda.Code.from_asset("lambda",
                bundling={
                    "image": _lambda.Runtime.PYTHON_3_6.bundling_docker_image,
                    "command": ["bash", "-c", " echo CONTAINER && pip install -r requirements.txt -t /asset-output && rsync -r . /asset-output && echo DONE "]
                }
            ),
            runtime=_lambda.Runtime.PYTHON_3_6,
            timeout=core.Duration.seconds(10),
            handler="update-ipranges.main"
        )
        function.add_to_role_policy(iam.PolicyStatement(
            resources=["*"],
            actions=["ec2:DescribeManagedPrefixLists",
                "ec2:ModifyManagedPrefixList",
                "ec2:GetManagedPrefixListEntries"]
            )
        )
        
        topic = sns.Topic.from_topic_arn(self, "iprangesTopic", topic_arn="arn:aws:sns:us-east-1:806199016981:AmazonIpSpaceChanged")
        function.add_event_source(SnsEventSource(topic))
