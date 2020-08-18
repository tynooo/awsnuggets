# AWSnuggets
Repo to contain tiny utility type things to run in AWS using AWS CDK and Python


# Update Managed Prefix Lists

This is a lambda function that's triggered by an update to the AWS ipranges.json
SNS topic. It grabs the latest ipranges.json file and maintains a prefix list
based on the data in it. 

Right now, it's basic and you need to modify the code to change the region and 
service it grabs the prefixes for. When I get time, I'll clean it up and 
parameterise it.

```
cdk deploy update-managed-prefix-lists
```

## Getting it running

Assuming you have Python3 and CDK installed

Clone this repo and get your environment ready

```
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
npm -g upgrade
```

To list the stacks in the repo, run ``` cdk list```

Then run ```cdk deploy <stackname> ``` to deploy to your account.

When you're done run ```cdk destroy <stackname>``` to tear it all down.