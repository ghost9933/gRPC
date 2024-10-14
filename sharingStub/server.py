import grpc
from concurrent import futures
import time
import main_pb2
import main_pb2_grpc

class TodoService(main_pb2_grpc.TodoServiceServicer):
    def __init__(self):
        self.todos = {}  # In-memory database for todo items

    def CreateTodo(self, request, context):

        todo_id = str(len(self.todos) + 1)
        todo_item = main_pb2.TodoItem(id=todo_id, title=request.item.title, completed=False)
        self.todos[todo_id] = todo_item
        print('request recived to create',request.item.id,request.item)
        return main_pb2.TodoResponse(message="Todo created successfully", item=todo_item)

    def DeleteTodo(self, request, context):
        print('request recived to delete',request.id)
        if request.id in self.todos:
            del self.todos[request.id]
            return main_pb2.TodoResponse(message="Todo deleted successfully")
        return main_pb2.TodoResponse(message="Todo not found")

    def UpdateTodo(self, request, context):
        print('request recived to update',request.item.id,request.item)
        if request.item.id in self.todos:
            self.todos[request.item.id] = request.item
            return main_pb2.TodoResponse(message="Todo updated successfully", item=request.item)
        return main_pb2.TodoResponse(message="Todo not found")

    def ListTodos(self, request, context):
        
        items = list(self.todos.values())
        print('seding this data to client',items)
        return main_pb2.TodoListResponse(items=items)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    main_pb2_grpc.add_TodoServiceServicer_to_server(TodoService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started, listening on port 50051")
    print("Server started at port 50051.")
    try:
        while True:
            time.sleep(86400)  # Keep the server running for a day
    except KeyboardInterrupt:
        print('TODO server stopping')
        server.stop(0)

if __name__ == '__main__':
    print('starting TODO server')
    serve()
    
