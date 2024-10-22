# gRPC Tutorial, Todo App and Pet Adoption System

This repository provides an implementation of a gRPC-based Todo application and a Pet Adoption system using Python and Java. Follow the instructions below to set up, run, and test the code for both applications.

## Directory Structure


## How It Works

1. **Define Service**: Create a `.proto` file with service definitions.
2. **Generate Code**: Use the gRPC compiler to generate server and client code.
3. **Implement Server**: Write the logic for the defined methods in your preferred language.
4. **Invoke Client**: Use the generated client code to make remote procedure calls to the server.

---

## Question 1: GRPC Tutorial

### Setting Up

1. **Install gRPC**:
   Ensure you have `gRPC` installed for Python:
   ```bash
   pip install grpcio grpcio-tools
   ```
2. **quick start**:
     ```bash
   $ git clone -b v1.66.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc
    cd grpc/examples/python/helloworld

    python -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/helloworld.proto
    
    python greeter_server.py

    python greeter_client.py
   ```

3. **Basic Guide** :
   ```bash
   $ git clone -b v1.66.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc
   cd grpc/examples/python/route_guide


   ```
---

---

## Question 2: Todo Service Definition

### Creating the Stub Codes

1. **Generate the Python Stub Code**:
   After writing your `.proto` file, generate the stub codes using:
   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. todo.proto
   ```

### Running the Todo Application Again

1. **Start the Server**:
   - In one terminal, run:
   ```bash
   python server.py
   ```

2. **Run the Client**:
   - In a separate terminal, run:
   ```bash
   python client.py
   ```

---

# Question 3
# Running the gRPC Server and Client

This section provides instructions for setting up and running the gRPC server and client for both Java and Python implementations.

## Starting the gRPC Server

1. **Navigate to the Java gRPC directory**:
   ```bash
   cd Grpc-Java/grpc-java
   ```

2. **Build and start the Docker containers**:
   ```bash
   docker-compose up --build
   ```

## Testing the Client

1. **Navigate to the Python Pet Adoption client directory**:
   ```bash
   cd Grpc-python/gRPC/PetAdoption/client
   ```

2. **Run the client in a Docker container**:
   ```bash
   docker-compose run client bash
   ```

3. **Execute the test and client scripts**:
   ```bash
   python test.py & python client.py
   ```
---

### Testing the Client

1. **Connect to the Server**: Ensure the client connects to the gRPC server correctly.
2. **Run Functional Tests**: Test various functionalities such as pet registration and search.


