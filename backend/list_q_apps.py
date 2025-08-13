import boto3

client = boto3.client(
    'qbusiness',
    region_name='us-east-1',
    aws_access_key_id='XXX',
    aws_secret_access_key='XXXX+XX'
)

response = client.list_applications()
for app in response['applications']:
    print("App ID:", app['applicationId'], "| Name:", app.get('name', 'N/A'))
