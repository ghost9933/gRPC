import grpc
import petadoption_pb2
import petadoption_pb2_grpc
import os
import base64

def register_pet(client, name, gender, age, breed, picture_path):
    try:
        with open(picture_path, "rb") as f:
            picture = f.read()

        pet = petadoption_pb2.Pet(name=name, gender=gender, age=age, breed=breed, picture=picture)
        response = client.RegisterPet(pet)
        print(response.message)
    except FileNotFoundError:
        print(f"Error: The file '{picture_path}' was not found.")
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
            print(f"Picture (base64): {picture_encoded}")


def update_pet(client, pet_id, name, gender, age, breed, picture_path):
    try:
        with open(picture_path, "rb") as f:
            picture = f.read()

        pet = petadoption_pb2.Pet(id=pet_id, name=name, gender=gender, age=age, breed=breed, picture=picture)
        response = client.UpdatePet(pet)
        print(response.message)
    except FileNotFoundError:
        print(f"Error: The file '{picture_path}' was not found.")
    except Exception as e:
        print(f"An error occurred while updating the pet: {e}")

def remove_pet(client, pet_id):
    request = petadoption_pb2.RemoveRequest(id=pet_id)
    response = client.RemovePet(request)
    print(response.message)

def run():
    client_ip = os.environ.get('CLIENT_IP')
    server_ip = os.environ.get('SERVER_IP', 'pet_adoption_server')  # Use the service name
    server_ip='127.0.0.1'
    print(f"Client running at IP: {client_ip}")
    print(f"Connecting to server at: {server_ip}:50051")

    with grpc.insecure_channel(f"{server_ip}:50051") as channel:
        client = petadoption_pb2_grpc.PetAdoptionServiceStub(channel)

        while True:
            print("\nMenu:")
            print("1. Register a Pet")
            print("2. Search for a Pet")
            # print("3. Update a Pet")
            # print("4. Remove a Pet")
            print("5. Exit")
            choice = input("Choose an option (1-5): ")

            if choice == '1':
                name = input("Enter pet name: ")
                gender = input("Enter pet gender (Male/Female): ")
                age = int(input("Enter pet age: "))
                breed = input("Enter pet breed: ")
                picture_path = input("Enter path to pet picture: ")
                register_pet(client, name, gender, age, breed, picture_path)

            elif choice == '2':
                query = input("Enter pet name, gender, age, or breed to search: ")
                search_pet(client, query)

            # elif choice == '3':
            #     pet_id = input("Enter pet ID to update: ")
            #     name = input("Enter new pet name: ")
            #     gender = input("Enter new pet gender (Male/Female): ")
            #     age = int(input("Enter new pet age: "))
            #     breed = input("Enter new pet breed: ")
            #     picture_path = input("Enter path to new pet picture: ")
            #     update_pet(client, pet_id, name, gender, age, breed, picture_path)

            # elif choice == '4':
            #     pet_id = input("Enter pet ID to remove: ")
            #     remove_pet(client, pet_id)

            elif choice == '5':
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == '__main__':
    run()