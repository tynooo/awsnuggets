#!/usr/bin/env python
import requests
import boto3

def main(event, context):
    max_prefixes = 100
    ip_ranges = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json').json()['prefixes']
    ec2_ips = [item['ip_prefix'] for item in ip_ranges if item["service"] == "EC2" and item["region"] == "ap-southeast-2"]
    
    
    ec2 = boto3.client('ec2')
    
    filters = [{'Name':'prefix-list-name', 'Values': ['EC2-SYD']}]
    response = ec2.describe_managed_prefix_lists(Filters=filters)
    
    entry_list = []
    
    if response['PrefixLists'] ==[]:
        print("No existing Prefix List. Creating new one")
    
        for ip in ec2_ips:
            entry_list.append({'Cidr': ip})
        ec2.create_managed_prefix_list(
            DryRun=False,
            PrefixListName='EC2-SYD',
            MaxEntries=max_prefixes,
            Entries=entry_list,
            AddressFamily='IPv4'
            )
        return {
            'statusCode': 200,
            'body': "Created new Prefix List"
        }
    
    else:
        print("Prefix List exists. Updating prefixes")
        to_remove=[]
        prefix_list_id = response['PrefixLists'][0]['PrefixListId']
        prefix_list_version = response['PrefixLists'][0]['Version']
        # if it exists, iterate through the list and add the new IPs
        existing_entries = ec2.get_managed_prefix_list_entries(PrefixListId=prefix_list_id)['Entries']
        for entry in existing_entries:
            if entry['Cidr'] in ec2_ips:
                ec2_ips.remove(entry['Cidr'])
            else:
                to_remove.append(entry)
        if ec2_ips != [] or to_remove != []:
            for ip in ec2_ips:
                entry_list.append({'Cidr': ip})
            print("MODIFYING")
            print("ADDING", entry_list)
            print("REMOVING", to_remove)
            ec2.modify_managed_prefix_list(
                DryRun=False,
                PrefixListId=prefix_list_id,
                AddEntries=entry_list,
                RemoveEntries=to_remove,
                CurrentVersion=prefix_list_version
                )
            return {
                'statusCode': 200,
                'body': "Updated prefixlist"
            }
        else:
            print("Nothing to modify")
            return {
                'statusCode': 200,
                'body': "Nothing to modify"
            }