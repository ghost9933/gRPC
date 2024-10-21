import grpc
import petadoption_pb2
import petadoption_pb2_grpc
import os
import threading
import time

# Function to register a pet
def register_pet(client, name, gender, age, breed, picture_path):
    try:
        with open(picture_path, "rb") as f:
            picture = f.read()

        pet = petadoption_pb2.Pet(name=name, gender=gender, age=age, breed=breed, picture=picture)
        response = client.RegisterPet(pet)
        print(f"Registered pet: {name} - {response.message}")
    except FileNotFoundError:
        print(f"Error: The file '{picture_path}' was not found.")
    except Exception as e:
        print(f"An error occurred while registering the pet: {e}")

# Function to search for a pet
def search_pet(client, query):
    request = petadoption_pb2.SearchRequest(query=query)
    response = client.SearchPet(request)
    print(f"Search results for '{query}':")
    for pet in response.pets:
        print(f"ID: {pet.id}, Name: {pet.name}, Gender: {pet.gender}, Age: {pet.age}, Breed: {pet.breed}")

# Function to simulate multiple registrations
def simulate_register_pet(client, pet_data):
    for data in pet_data:
        name, gender, age, breed, picture_path = data
        register_pet(client, name, gender, age, breed, picture_path)
        time.sleep(1)  # Sleep to simulate delay between requests

# Function to simulate multiple searches
def simulate_search_pet(client, queries):
    for query in queries:
        search_pet(client, query)
        time.sleep(1)  # Sleep to simulate delay between requests

def run():
    server_address = '127.0.0.1:50051'  # Update if needed
    print(f"Connecting to server at: {server_address}")

    with grpc.insecure_channel(server_address) as channel:
        client = petadoption_pb2_grpc.PetAdoptionServiceStub(channel)

        # Pet data for registration
        pet_data = [
            ("Buddy", "Male", 3, "dog", "img/goldy.jpeg"),
            ("Bella", "Female", 2, "cat", "img/grumpy.jpg"),
        ]

        # Queries for searching
        queries = ["Buddy", "Bella"]

        # Create threads for registration
        register_threads = [
            threading.Thread(target=simulate_register_pet, args=(client, pet_data))
            for _ in range(2)  # Simulate two clients registering pets
        ]

        # Create threads for searching
        search_threads = [
            threading.Thread(target=simulate_search_pet, args=(client, queries))
            for _ in range(2)  # Simulate two clients searching for pets
        ]

        # Start all threads
        for thread in register_threads + search_threads:
            thread.start()

        # Wait for all threads to complete
        for thread in register_threads + search_threads:
            thread.join()

        print("All operations completed.")

if __name__ == '__main__':
    run()
