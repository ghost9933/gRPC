import grpc
from concurrent import futures
import services_pb2
import services_pb2_grpc
# Ensure that the generated services_pb2_grpc.py file is in the same directory or in the Python path

class TodoService(services_pb2_grpc.ToDoServiceServicer):
    def __init__(self):
        self.todos = []
        self.next_id = 1

    def AddTodo(self, request, context):
        todo = services_pb2.Todo(id=self.next_id, task=request.task)
        self.todos.append(todo)
        self.next_id += 1
        return services_pb2.TodoResponse(success=True, message=f"Added todo: {request.task}")

    def ListTodos(self, request, context):
        return services_pb2.TodoList(todos=self.todos)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services_pb2_grpc.add_ToDoServiceServicer_to_server(TodoService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Python gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
