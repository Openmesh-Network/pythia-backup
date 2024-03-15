# -*- coding: utf-8 -*-
"""sagemaker-falcon7b.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cf-Z-NFnNEuioe5aWstgFFMci6iuEjGs

### 0 - Configuration
"""

import sagemaker
import boto3

import os
from dotenv import load_dotenv

"""### 1 - AWS Session"""

# environment variables
# Option 1
# os.environ["aws_access_key_id"]='aws_access_key_id'
# os.environ["aws_secret_access_key"]='aws_secret_access_key'

# Option 2
load_dotenv()

"""  [Secret keys](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html)"""

REGION_NAME = "us-east-1"
os.environ["AWS_DEFAULT_REGION"] = REGION_NAME
ROLE_NAME =  'Sagemaker-ExecutionRole'

auth_arguments = {
    'aws_access_key_id':os.environ["AWS_S3_ACCESS_KEY"],
    'aws_secret_access_key':os.environ["AWS_S3_KEY_SECRET"],
    'region_name':REGION_NAME
}

"""[IAM rol](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html)"""

iam = boto3.client('iam', **auth_arguments)
role = iam.get_role(RoleName=ROLE_NAME)['Role']['Arn']

session = sagemaker.Session(boto3.Session(**auth_arguments))

"""### 2 - Deployment"""

from sagemaker.huggingface import get_huggingface_llm_image_uri

# image uri
llm_image = get_huggingface_llm_image_uri("huggingface")

print(f"image uri: {llm_image}")

from sagemaker.huggingface import HuggingFaceModel

# Falcon 7b
hub = {'HF_MODEL_ID':'tiiuae/falcon-7b'}
print('hugging face')

# Hugging Face Model Class
huggingface_model = HuggingFaceModel(
   env=hub,
   role=role,  # iam role from AWS
   image_uri=llm_image,
   sagemaker_session=session
)
print('going to predictor')
# deploy model to SageMaker
predictor = huggingface_model.deploy(
	initial_instance_count=1, # number of instances
	instance_type='ml.g5.16xlarge',
 	container_startup_health_check_timeout=300
)

"""### 3 - Inference"""

print('this is the predictor fist')
print(predictor)

exit()