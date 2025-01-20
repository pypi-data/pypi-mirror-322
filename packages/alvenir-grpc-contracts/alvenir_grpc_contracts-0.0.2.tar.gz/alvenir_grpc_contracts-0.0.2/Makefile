.PHONY: generate build push

generate:
	python -m grpc_tools.protoc \
		--proto_path=./protos \
		--python_out=./src \
		--grpc_python_out=./src \
		--pyi_out=./src \
		protos/alvenir_grpc_contracts/asr/v1/*.proto \
		protos/alvenir_grpc_contracts/assistance/v1/*.proto \
		protos/alvenir_grpc_contracts/guidance/v1/*.proto \
		protos/alvenir_grpc_contracts/summary/v1/*.proto \
		protos/alvenir_grpc_contracts/types/v1/*.proto

build:
	python3 -m build

push:
	python3 -m twine upload dist/*
