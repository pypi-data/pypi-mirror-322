import io
import json
import os
import shutil
import subprocess
import sys
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout
from glob import glob
from io import BytesIO
from itertools import product
from pathlib import Path
from shutil import which
from tempfile import TemporaryDirectory
from typing import List, Optional
from unittest import TestCase
from unittest.mock import MagicMock, patch

import boto3

from daggerml_cli import api
from daggerml_cli.repo import Resource
from tests.util import SimpleApi


class MockStreamingBody:
    def __init__(self, response_data):
        self.response_data = response_data
    def read(self):
        return json.dumps(self.response_data).encode('utf-8')

def create_mock_lambda_response(response_data, status_code=200):
    mock_response = MagicMock()
    mock_response['StatusCode'] = status_code
    mock_response['Payload'] = MockStreamingBody(response_data)
    mock_response['ResponseMetadata'] = {
        'RequestId': 'mock-request-id',
        'HTTPStatusCode': status_code
    }
    return mock_response

def mock_lambda_invoke(mocker, response_data, status_code=200):
    mock_response = create_mock_lambda_response(response_data, status_code)
    mock_client = MagicMock()
    mock_client.invoke.return_value = mock_response
    mocker.patch('boto3.client', return_value=mock_client)
    return mock_client

TEST_BUCKET = "bucket-does-not-exist"
ROLE_NAME = "role-does-not-exist"
_HERE_ = Path(__file__).parent


def create_test_role() -> str:
    """Create an IAM role for testing with moto."""
    iam = boto3.client('iam')
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    try:
        response = iam.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        return response['Role']['Arn']
    except iam.exceptions.EntityAlreadyExistsException:
        response = iam.get_role(RoleName=ROLE_NAME)
        return response['Role']['Arn']

def add_to_zip(local_dir, zip_file):
    for root, _, files in os.walk(local_dir):
        for file in files:
            if file.endswith(('.py', '.so', '.pyd', '.pyc')):
                file_path = os.path.join(root, file)
                archive_path = os.path.relpath(file_path, local_dir)
                zip_file.write(file_path, archive_path)

def create_lambda(code_path, function_name="fn"):
    build_dir = f'{_HERE_}/fn/lambda_build'
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)
    with open(f"{build_dir}/.gitignore", "w") as f:
        f.write("*")
    try:
        py = f"python{sys.version_info.major}.{sys.version_info.minor}"
        # subprocess.check_call([
        #     sys.executable, '-m', 'venv', 
        #     os.path.join(build_dir, 'venv')
        # ])
        # pip_path = os.path.join(build_dir, 'venv', 'bin', 'pip')
        # subprocess.check_call([pip_path, 'install', str(_HERE_.parent)])
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            with open(code_path, 'rb') as file:
                zip_file.writestr('index.py', file.read())
            # add_to_zip(str(_HERE_), zip_file)
            # add_to_zip(f"{build_dir}/venv/lib/{py}/site-packages", zip_file)
        lambda_client = boto3.client('lambda')
        try:
            response = lambda_client.create_function(
                FunctionName=function_name,
                Runtime=py,
                Role=f'arn:aws:iam::123456789012:role/{ROLE_NAME}',
                Handler='index.lambda_handler',
                Code={'ZipFile': zip_buffer.getvalue()},
                Timeout=30,
                MemorySize=128,
                Publish=True
            )
            return response
        except Exception as e:
            print(f"Error creating Lambda function: {e}")
            raise
    finally:
        shutil.rmtree(build_dir)


class TestApiCreate(TestCase):

    def setUp(self):
        # clear out env variables for safety
        for k in sorted(os.environ.keys()):
            if k.startswith("AWS_"):
                del os.environ[k]
        os.environ["AWS_ACCESS_KEY_ID"] = "foobar"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "foobar"
        os.environ["AWS_REGION"] = os.environ["AWS_DEFAULT_REGION"] = "us-west-2"
        # this loads env vars, so import after clearing
        from moto.server import ThreadedMotoServer
        super().setUp()
        self.server = ThreadedMotoServer(port=0)
        with redirect_stderr(None), redirect_stdout(None):
            self.server.start()
        self.moto_host, self.moto_port = self.server._server.server_address
        self.endpoint = f"http://{self.moto_host}:{self.moto_port}"
        os.environ["AWS_ENDPOINT_URL"] = self.endpoint
        boto3.client("s3", region_name="us-east-1").create_bucket(Bucket=TEST_BUCKET)

    def tearDown(self):
        self.server.stop()
        super().tearDown()

    def test_lambda_basic(self):
        args = list(range(10))
        with SimpleApi.begin('d0') as d0:
            create_test_role()
            resp = create_lambda(_HERE_/"fn/lambda_.py")
            resp = boto3.client("lambda").invoke(
                FunctionName=resp["FunctionArn"],
                InvocationType='RequestResponse',
                LogType='Tail',
                Payload=json.dumps({"test": "data"}).encode(),
            )
            assert resp is None
            resource = Resource(resp["FunctionArn"], adapter="dml-lambda-adapter")
            n0 = d0.put_literal(resource, name='n0', doc='This is my data.')
            nodes = [d0.put_literal(i) for i in args]
            resp = d0.unroll(d0.start_fn(n0, *nodes))
            assert resp is None
