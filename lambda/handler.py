import boto3

ec2 = boto3.client(
    "ec2",
    region_name="us-east-1",
    endpoint_url="http://10.0.2.237:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

def handler(event, context):
    action = event.get("action", "status")
    instance_id = event.get("instance_id")
    if action == "start":
        ec2.start_instances(InstanceIds=[instance_id])
        return {"statusCode": 200, "body": f"started {instance_id}"}
    elif action == "stop":
        ec2.stop_instances(InstanceIds=[instance_id])
        return {"statusCode": 200, "body": f"stopped {instance_id}"}
    elif action == "status":
        r = ec2.describe_instances(InstanceIds=[instance_id])
        state = r["Reservations"][0]["Instances"][0]["State"]["Name"]
        return {"statusCode": 200, "body": f"{instance_id} : {state}"}
    return {"statusCode": 400, "body": "action invalide"}
