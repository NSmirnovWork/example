# Useful tools
- [gRPC UI](https://github.com/fullstorydev/grpcui)

    Command for run
    ```shell
    grpcui -plaintext localhost:50051
    ```

- grpclib_tools generate code
    ```python -m grpc_tools.protoc \
        -I./protocols \
        --python_out=./protocols \
        --grpclib_python_out=./protocols \
        ./protocols/*.proto 
    ``` 

- [protoc installation](https://grpc.io/docs/protoc-installation/)
