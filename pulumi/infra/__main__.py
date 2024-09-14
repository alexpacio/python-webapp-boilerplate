import json
import pulumi
import pulumi_aws as aws
import pulumi_kubernetes as k8s
import os

s3_bucket_name = os.environ.get("S3_BUCKET")
dynamodb_table_name = os.environ.get("DYNAMODB_TABLE")
iam_user_name = os.environ.get("IAM_USER_NAME")
iam_access_key_obj_name = os.environ.get("IAM_USER_ACCESS_KEY_OBJ_NAME")
k8s_secret_name = os.environ.get("K8S_AWS_SECRET_NAME")
k8s_namespace_id = os.environ.get("K8S_NAMESPACE_ID")

# Get the AWS account ID
current = aws.get_caller_identity()

bucket = aws.s3.Bucket(s3_bucket_name, bucket=s3_bucket_name)

dynamo = aws.dynamodb.Table(dynamodb_table_name, 
    name=dynamodb_table_name,
    billing_mode="PROVISIONED",
    read_capacity=1,
    write_capacity=1,
    hash_key="name",
    attributes=[
        {
            "name": "name",
            "type": "S",
        }
    ]
)

# Create an IAM User for the application running on Kubernetes
app_user = aws.iam.User(iam_user_name, name=iam_user_name)

# Define policies for DynamoDB access
dynamo_db_policy = aws.iam.UserPolicy("dynamoDbPolicy",
    user=app_user.name,
    policy=pulumi.Output.all().apply(lambda _: {
        "Version": "2012-10-17",
        "Statement": [{
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteItem",
            ],
            "Effect": "Allow",
            "Resource": f"arn:aws:dynamodb:{aws.config.region}:{current.account_id}:table/{dynamodb_table_name}"
        }]
    })
)

# Define policies for S3 access
s3_policy = aws.iam.UserPolicy("s3Policy",
    user=app_user.name,
    policy=pulumi.Output.all().apply(lambda _: {
        "Version": "2012-10-17",
        "Statement": [{
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
            ],
            "Effect": "Allow",
            "Resource": f"arn:aws:s3::{current.account_id}:{s3_bucket_name}/*"
        }]
    })
)

# Generate access keys for the IAM user
app_access_key = aws.iam.AccessKey(iam_access_key_obj_name, user=app_user.name)

# Define the Kubernetes Secret
aws_credentials_secret = k8s.core.v1.Secret(
    k8s_secret_name,
    metadata={
        "name": k8s_secret_name,
        "namespace": k8s_namespace_id,
    },
    string_data={
        "AWS_ACCESS_KEY_ID": app_access_key.id,
        "AWS_SECRET_ACCESS_KEY": app_access_key.secret,
    }
)

# Export the name of the secret
pulumi.export("aws_credentials_secret_name", aws_credentials_secret.metadata["name"])

# Export the access key and secret (ensure you store them securely)
pulumi.export("aws_access_key_id", app_access_key.id)
pulumi.export("aws_secret_access_key", app_access_key.secret)