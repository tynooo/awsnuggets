#!/usr/bin/env python3

from aws_cdk import core


from update_managed_prefix_lists.update_managed_prefix_lists_stack import UpdateManagedPrefixListsStack


app = core.App()
UpdateManagedPrefixListsStack(app, "update-managed-prefix-lists")

app.synth()
