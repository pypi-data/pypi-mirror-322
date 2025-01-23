# aws-sig

[![PyPi version](https://badge.fury.io/py/aws-signature.svg)](https://pypi.org/project/aws-signature/)
[![Code Coverage](https://img.shields.io/codecov/c/github/fcusson/aws-sig)](https://app.codecov.io/gh/fcusson/aws-sig)

A Python Library to Authenticate Request to the AWS API using the AWS Signatures.

---

## Features

- 🔒 AWS Signature Version 4 signing for `requests` library.  
- ⚡ Lightweight and fast.  
- 📦 Simple integration with the [requests](https://requests.readthedocs.io/en/latest/)

---

## Installation

Install the package using pip:

```bash
pip install aws-signature
```

## Usage

```python
import requests
from aws_sig import SigV4

# Configure AWS credentials and region
aws_access_key = "your-access-key"
aws_secret_key = "your_secret_key"
aws_region = "your_region"

# Create an authenticated session
auth = SigV4(aws_access_key, aws_secret_key, aws_region, "execute-api")

# make signed request
response = requests.get("https://service-name.region.amazonaws.com", auth=auth)

print(response.json())
```
