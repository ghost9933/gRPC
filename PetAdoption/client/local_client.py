import grpc
import petadoption_pb2
import petadoption_pb2_grpc
import threading
import time
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
    server_address = os.getenv('SERVER_ADDRESS', 'server:50051')  # Use the service name
    server_address = '127.0.0.1:50051'
    print(f"Client running at IP: {client_ip}")
    print(f"Connecting to server at: {server_address}")

    with grpc.insecure_channel(f"{server_address}") as channel:
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
    validate_pet_registration(name, gender, age, breed, picture_path)  # Validate inputs
    with open(picture_path, "rb") as f:
        picture = f.read()

    pet = petadoption_pb2.Pet(name=name, gender=gender, age=age, breed=breed, picture=picture)
    response = client.RegisterPet(pet)
    return response.message

def search_pet(client, query):
    request = petadoption_pb2.SearchRequest(query=query)
    response = client.SearchPet(request)
    return response.pets

def test_input_validation(client):
    try:
        register_pet(client, "Invalid Pet", "Male", -1, "Dog", "img/farm.jpg")  # Invalid age
        assert False, "Test failed: Validation did not raise error for invalid age."
    except ValueError:
        pass  # Expected exception

def test_search_other_client(client):
    register_pet(client, "Buddy", "Male", 2, "Labrador", "img/farm.jpg")
    time.sleep(1)  # Ensure registration is complete
    pets = search_pet(client, "Buddy")
    assert len(pets) == 1 and pets[0].name == "Buddy", "Test failed: Buddy not found."

def test_edge_cases_search(client):
    register_pet(client, "Charlie", "Male", 3, "Beagle", "img/farm.jpg")
    register_pet(client, "Daisy", "Female", 5, "Poodle", "img/farm.jpg")
    time.sleep(1)  # Ensure registrations are complete

    assert len(search_pet(client, "Charlie")) == 1, "Test failed: Charlie not found."
    assert len(search_pet(client, "Poodle")) == 1, "Test failed: Daisy not found."
    assert len(search_pet(client, "3")) == 1, "Test failed: Charlie not found by age."
    assert len(search_pet(client, "Female")) == 1, "Test failed: Daisy not found by gender."

def test_multi_thread_edge_cases_search(client):
    print("\nTesting edge cases for search...")

    def register_multiple_pets():
        pets_to_register = [
            ("Charlie", "Male", 3, "Beagle", "img/farm.jpg"),
            ("Daisy", "Female", 5, "Poodle", "img/farm.jpg"),
            ("Buddy", "Male", 2, "Labrador", "img/farm.jpg"),
            ("Max", "Male", 4, "Golden Retriever", "img/farm.jpg"),
            ("Bella", "Female", 1, "Shih Tzu", "img/farm.jpg"),
            ("Lucy", "Female", 7, "Beagle", "img/farm.jpg"),
        ]
        for name, gender, age, breed, picture_path in pets_to_register:
            register_pet(client, name, gender, age, breed, picture_path)
            time.sleep(0.1)  # Slight delay to avoid race conditions

    registration_threads = []
    for _ in range(3):  # Start 3 threads to register pets concurrently
        t = threading.Thread(target=register_multiple_pets)
        t.start()
        registration_threads.append(t)

    for t in registration_threads:
        t.join()

    time.sleep(1)

    def perform_search(query):
        return search_pet(client, query)

    search_queries = ["Beagle", "Female", "3", "Labrador"]
    search_threads = []
    for query in search_queries:
        t = threading.Thread(target=perform_search, args=(query,))
        t.start()
        search_threads.append(t)

    for t in search_threads:
        t.join()

def test_simultaneous_requests(client):
    print("\nTesting simultaneous requests...")
    
    def register_multiple_pets():
        for i in range(4):
            register_pet(client, f"Pet-{i}", "Male" if i % 2 == 0 else "Female", 2 + i, "Breed", "img/farm.jpg")
            time.sleep(0.1)

    threads = []
    for _ in range(4):  # Four threads for registration
        t = threading.Thread(target=register_multiple_pets)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()  # Wait for all threads to finish

def run_tests():
    server_address = '127.0.0.1:50051'
    options = [
        ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50 MB for incoming messages
        ('grpc.max_send_message_length', 50 * 1024 * 1024),     # 50 MB for outgoing messages
    ]
    print(f"Connecting to server at: {server_address}")
    failed_tests = []

    with grpc.insecure_channel(f"{server_address}",options=options) as channel:
        client = petadoption_pb2_grpc.PetAdoptionServiceStub(channel)

        try:
            test_input_validation(client)
        except AssertionError:
            failed_tests.append("test_input_validation")

        try:
            test_search_other_client(client)
        except AssertionError:
            failed_tests.append("test_search_other_client")

        try:
            test_edge_cases_search(client)
        except AssertionError:
            failed_tests.append("test_edge_cases_search")

        try:
            test_simultaneous_requests(client)
        except AssertionError:
            failed_tests.append("test_simultaneous_requests")

        try:
            test_multi_thread_edge_cases_search(client)
        except AssertionError:
            failed_tests.append("test_multi_thread_edge_cases_search")

    if failed_tests:
        print("The following tests failed:")
        for test in failed_tests:
            print(f"- {test}")
    else:
        print("All tests passed successfully.")



if __name__ == '__main__':
    run_tests()
    run()
