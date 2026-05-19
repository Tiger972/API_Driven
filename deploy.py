import boto3, json, zipfile, os

ENDPOINT = os.environ.get("AWS_ENDPOINT", "http://localhost:4566")
REGION = "us-east-1"
kwargs = dict(region_name=REGION, endpoint_url=ENDPOINT, aws_access_key_id="test", aws_secret_access_key="test")

ec2   = boto3.client("ec2", **kwargs)
lmb   = boto3.client("lambda", **kwargs)
apigw = boto3.client("apigateway", **kwargs)

print("1. Création EC2...")
r = ec2.run_instances(ImageId="ami-00000000", MinCount=1, MaxCount=1, InstanceType="t2.micro")
instance_id = r["Instances"][0]["InstanceId"]
print(f"   ✅ Instance : {instance_id}")

print("2. Package Lambda...")
with zipfile.ZipFile("/tmp/lambda.zip", "w") as z:
    z.write("lambda/handler.py", "handler.py")
with open("/tmp/lambda.zip", "rb") as f:
    zip_bytes = f.read()

print("3. Création Lambda...")
lmb.create_function(
    FunctionName="ec2-controller",
    Runtime="python3.11",
    Role="arn:aws:iam::000000000000:role/lambda-role",
    Handler="handler.handler",
    Code={"ZipFile": zip_bytes},
    Environment={"Variables": {"AWS_ENDPOINT": ENDPOINT}},
    Timeout=10
)
print("   ✅ Lambda : ec2-controller")

print("4. Création API Gateway...")
api = apigw.create_rest_api(name="ec2-api")
api_id = api["id"]
root_id = apigw.get_resources(restApiId=api_id)["items"][0]["id"]
res = apigw.create_resource(restApiId=api_id, parentId=root_id, pathPart="ec2")
res_id = res["id"]
apigw.put_method(restApiId=api_id, resourceId=res_id, httpMethod="POST", authorizationType="NONE")
lambda_arn = f"arn:aws:lambda:{REGION}:000000000000:function:ec2-controller"
apigw.put_integration(
    restApiId=api_id, resourceId=res_id, httpMethod="POST",
    type="AWS_PROXY", integrationHttpMethod="POST",
    uri=f"arn:aws:apigateway:{REGION}:lambda:path/2015-03-31/functions/{lambda_arn}/invocations"
)
apigw.create_deployment(restApiId=api_id, stageName="prod")

url = f"{ENDPOINT}/restapis/{api_id}/prod/_user_request_/ec2"
print(f"\n✅ Tout est déployé !")
print(f"   Instance ID : {instance_id}")
print(f"   API URL     : {url}")
print(f"\ncurl -X POST '{url}' -d '{{\"action\":\"status\",\"instance_id\":\"{instance_id}\"}}'")
print(f"curl -X POST '{url}' -d '{{\"action\":\"start\",\"instance_id\":\"{instance_id}\"}}'")
print(f"curl -X POST '{url}' -d '{{\"action\":\"stop\",\"instance_id\":\"{instance_id}\"}}'")
