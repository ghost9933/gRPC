# import grpc
# import services_pb2_grpc
# import services_pb2

# def run():
#     with grpc.insecure_channel('localhost:50051') as channel:
#         stub = services_pb2_grpc.ToDoServiceStub(channel)
        
#         # Add a todo task
#         task = "Learn gRPC in Python"
#         response = stub.CreateToDo(services_pb2.todo(task=task))
#         print(f"AddTodo response: {response.message}")
        
#         # List all todo tasks
#         todos = stub.GetToDo(services_pb2.Empty())
#         print("Todo List:")
#         for todo in todos.todos:
#             print(f"{todo.id}. {todo.task}")

# if __name__ == '__main__':
#     run()


import grpc
import services_pb2_grpc
import services_pb2

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = services_pb2_grpc.ToDoServiceStub(channel)
        
        # Add a todo task (call AddTodo instead of CreateToDo)
        task = "Learn gRPC in Python"
        response = stub.CreateToDo(services_pb2.CreateToDoRequest(task=task))
        print(f"AddTodo response: {response.message}")
        
        # List all todo tasks
        todos = stub.GetToDo(services_pb2.Empty())
        print("Todo List:")
        for todo in todos.todos:
            print(f"{todo.id}. {todo.task}")

if __name__ == '__main__':
    run()
