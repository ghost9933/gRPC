import grpc
import main_pb2
import main_pb2_grpc

def print_todos(todos):
    """Utility function to print all todos."""
    print("Current Todos:")
    for item in todos:
        print(f"{item.id}: {item.title} (Completed: {item.completed})")

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = main_pb2_grpc.TodoServiceStub(channel)

        while True:
            print("\nOptions:")
            print("1. Create Todo")
            print("2. List Todos")
            print("3. Update Todo")
            print("4. Delete Todo")
            print("5. Exit")

            choice = input("Choose an option (1-5): ")

            if choice == '1':
                title = input("Enter the title of the Todo item: ")
                response = stub.CreateTodo(main_pb2.TodoRequest(item=main_pb2.TodoItem(title=title)))
                print(response.message)

            elif choice == '2':
                response = stub.ListTodos(main_pb2.Empty())
                print_todos(response.items)

            elif choice == '3':
                todo_id = input("Enter the ID of the Todo item to update: ")
                title = input("Enter the new title of the Todo item: ")
                completed = input("Is the Todo item completed? (yes/no): ")
                completed = True if completed.lower() == 'yes' else False
                response = stub.UpdateTodo(main_pb2.TodoRequest(item=main_pb2.TodoItem(id=todo_id, title=title, completed=completed)))
                print(response.message)

            elif choice == '4':
                todo_id = input("Enter the ID of the Todo item to delete: ")
                response = stub.DeleteTodo(main_pb2.TodoId(id=todo_id))
                print(response.message)

            elif choice == '5':
                print("Exiting...")
                break

            else:
                print("Invalid option, please try again.")

if __name__ == '__main__':
    run()
