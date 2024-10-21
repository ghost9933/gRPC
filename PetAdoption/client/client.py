import grpc
import petadoption_pb2
import petadoption_pb2_grpc
import os
import base64


def validate_pet_registration(name, gender, age, breed, picture_path):
    if not isinstance(name, str) or not name:
        raise ValueError("Pet name must be a non-empty string.")
    if gender not in ["Male", "Female"]:
        raise ValueError("Pet gender must be either 'Male' or 'Female'.")
    if not isinstance(age, int) or age < 0:
        raise ValueError("Pet age must be a non-negative integer.")
    if not isinstance(breed, str) or not breed:
        raise ValueError("Pet breed must be a non-empty string.")
    if not os.path.isfile(picture_path):
        raise ValueError(f"Picture path '{picture_path}' does not point to a valid file.")

def register_pet(client, name, gender, age, breed, picture_path):
    try:
        validate_pet_registration(name, gender, age, breed, picture_path)  # Validate inputs
        
        with open(picture_path, "rb") as f:
            picture = f.read()

        pet = petadoption_pb2.Pet(name=name, gender=gender, age=age, breed=breed, picture=picture)
        response = client.RegisterPet(pet)
        print(response.message)
    except FileNotFoundError:
        print(f"Error: The file '{picture_path}' was not found.")
    except ValueError as ve:
        print(f"Validation error: {ve}")
    except Exception as e:
        print(f"An error occurred while registering the pet: {e}")

def search_pet(client, query):
    request = petadoption_pb2.SearchRequest(query=query)
    response = client.SearchPet(request)
    print("Matching Pets:")
    for pet in response.pets:
        print(f"ID: {pet.id}, Name: {pet.name}, Gender: {pet.gender}, Age: {pet.age}, Breed: {pet.breed}")
        if pet.picture:
            picture_encoded = base64.b64encode(pet.picture).decode('utf-8')
            truncated_picture = picture_encoded[:50] + '...' if len(picture_encoded) > 50 else picture_encoded
            print(f"Picture (base64): {truncated_picture}")

def run():
    client_ip = os.environ.get('CLIENT_IP')
    server_address = os.getenv('SERVER_ADDRESS', 'server:50052')# Use the service name
    # server_ip='127.0.0.1'
    options = [
        ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50 MB for incoming messages
        ('grpc.max_send_message_length', 50 * 1024 * 1024),     # 50 MB for outgoing messages
    ]
    print(f"Client running at IP: {client_ip}")
    print(f"Connecting to server at: {server_address}")

    # server_address = '127.0.0.1:50051'
    print(f"Client running at IP: {client_ip}")
    print(f"Connecting to server at: {server_address}")

    with grpc.insecure_channel(f"{server_address}",options=options) as channel:
        client = petadoption_pb2_grpc.PetAdoptionServiceStub(channel)

        while True:
            print("\nMenu:")
            print("1. Register a Pet")
            print("2. Search for a Pet")
            print("5. Exit")
            choice = input("Choose an option (1-5): ")

            if choice == '1':
                name = input("Enter pet name: ")
                gender = input("Enter pet gender (Male/Female): ")
                try:
                    age = int(input("Enter pet age: "))
                except ValueError:
                    print("Age must be a valid integer.")
                    continue
                breed = input("Enter pet breed: ")
                picture_path = input("Enter path to pet picture: ")
                register_pet(client, name, gender, age, breed, picture_path)

            elif choice == '2':
                query = input("Enter pet name, gender, age, or breed to search: ")
                search_pet(client, query)

            elif choice == '5':
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")




if __name__ == '__main__':
    run()


