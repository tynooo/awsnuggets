#!/usr/bin/env python3

from aws_cdk import core

from awsnuggets.awsnuggets_stack import AwsnuggetsStack


app = core.App()
AwsnuggetsStack(app, "awsnuggets")

app.synth()
