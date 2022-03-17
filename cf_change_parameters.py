import boto3
from pprint import pprint
import sys


def change_parameter_of_cloudformation(StackNameStartsWith, ParameterKey, ParameterValue):
    successfully_updated_stacks = []
    unsuccessfully_updated_stacks = []

    ######## Parameter Key and Value which will be modified #########
    parameters_to_be_modified = [
        {'key': ParameterKey, 'value': ParameterValue}]

    state_stack = ['CREATE_COMPLETE',
                   'ROLLBACK_FAILED',
                   'ROLLBACK_COMPLETE',
                   'UPDATE_COMPLETE',
                   'UPDATE_FAILED',
                   'UPDATE_ROLLBACK_FAILED',
                   'UPDATE_ROLLBACK_COMPLETE'
                   ]

    cfn_client = boto3.client('cloudformation', region_name='us-east-1')
    waiter = cfn_client.get_waiter('stack_update_complete')

    stacks_list = cfn_client.list_stacks(
        StackStatusFilter=state_stack
    )

    while True:
        token = stacks_list["NextToken"] if "NextToken" in stacks_list else None
        if stacks_list['StackSummaries']:
            for stack in stacks_list['StackSummaries']:
                if "ParentId" not in stack:
                    if stack['StackName'].startswith(StackNameStartsWith):
                        print("Stack Name {} starts with {}".format(
                            stack['StackName'], StackNameStartsWith))

            ################# Describing Stack ########################################
                        stack_details = cfn_client.describe_stacks(
                            StackName=stack['StackName'])
                        print("\nFetching Parmeters from stack {}".format(
                            stack['StackName']))
                        parameters = stack_details["Stacks"][0]["Parameters"]
                        pprint(parameters)
                        print("\nUpdating Parmeters for stack {}".format(
                            stack['StackName']))

                        ################ Modifying  parameters ###############
                        for index, param in enumerate(parameters):
                            for to_be_alter in parameters_to_be_modified:
                                if param["ParameterKey"] == to_be_alter["key"]:
                                    parameters[index]["ParameterValue"] = to_be_alter["value"]

                        pprint(parameters)
                        ############## Updating Stack ########################
                        try:
                            cfn_client.update_stack(
                                StackName=stack['StackName'], UsePreviousTemplate=True,
                                Parameters=parameters,
                                Capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_AUTO_EXPAND', 'CAPABILITY_IAM'])

                            print(
                                "********************************************************************")
                            waiter.wait(StackName=stack['StackName'],
                                        WaiterConfig={
                                'Delay': 20,
                                'MaxAttempts': 5

                            })
                            print("\nStack {} updated successfully".format(
                                stack['StackName']))
                            successfully_updated_stacks.append(
                                stack['StackName'])
                        except Exception as e:
                            print(e)
                            unsuccessfully_updated_stacks.append(
                                stack['StackName'])
            print("Stacks updated successfully")
            print(successfully_updated_stacks)

            print("Stacks not updated ")
            print(unsuccessfully_updated_stacks)

        else:
            print("No stack found")

        if token is not None:
            stacks_list = cfn_client.list_stacks(
                NextToken=token,
                StackStatusFilter=state_stack
            )
        else:
            break


if len(sys.argv) == 4:
    change_parameter_of_cloudformation(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    print("Please provide the correct number of arguments")
