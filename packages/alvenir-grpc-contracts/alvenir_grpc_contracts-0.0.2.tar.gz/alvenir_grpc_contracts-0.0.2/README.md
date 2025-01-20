# Alvenir GRPC Contracts

This package provides methods for interacting with the alvenir gRPC api.

To see more about gRPC look here: https://grpc.io/

Package on pypi: https://pypi.org/project/alvenir-grpc-contracts/

## Installation
```py
pip install alvenir-grpc-contracts
```

## Usage example
```py
import grpc
from pathlib import Path
from alvenir_grpc_contracts.summary.v1 import summary_pb2_grpc
from alvenir_grpc_contracts.types.v1 import ping_pb2

# Endpoint needs to be provided by alvenir
ENDPOINT = "<grpc_endpoint>:443"
# Required if server uses tls
ROOT_CERT = Path("<path to alvenir ca.crt>").read_bytes()

# If server does not use tls, replace credentials and with statement with:
# with grpc.insecure_channel(ENDPOINT) as channel:
credentials = grpc.ssl_channel_credentials(root_certificates=ROOT_CERT)
with grpc.secure_channel(ENDPOINT, credentials=credentials) as channel:
    stub = summary_pb2_grpc.SummaryServiceStub(channel)
    response: ping_pb2.PingResponse = stub.Ping(
        ping_pb2.PingRequest(wait_time=1)
    )
    print(response.requests_received_utc, response.response_sent_utc)
```
