import grpc
import petadoption_pb2
import petadoption_pb2_grpc
import time
import os


def register_pet(client, name, gender, age, breed, picture_path):
    """
    Register a pet with the provided details.
    
    Args:
        client: The gRPC client stub.
        name (str): Name of the pet.
        gender (str): Gender of the pet ("Male" or "Female").
        age (int): Age of the pet.
        breed (str): Breed of the pet.
        picture_path (str): Path to the pet's picture.
        
    Returns:
        str: Response message from the server.
    """
    try:
        with open(picture_path, "rb") as f:
            picture = f.read()
    except FileNotFoundError:
        return f"Error: The file '{picture_path}' was not found."

    pet = petadoption_pb2.Pet(
        name=name,
        gender=gender,
        age=age,
        breed=breed,
        picture=picture
    )
    try:
        response = client.RegisterPet(pet)
        return response.message
    except grpc.RpcError as e:
        return f"gRPC Error: {e.details()}"


def build_dataset(client):
    """
    Build a dataset of pets for testing by registering predefined pets.
    
    Args:
        client: The gRPC client stub.
    """
    print("Building dataset...")
    pets_to_register = [
        ("Buddy", "Male", 2, "Labrador", "img/farm.jpg"),
        ("Charlie", "Male", 3, "Beagle", "img/farm.jpg"),
        ("Daisy", "Female", 5, "Poodle", "img/farm.jpg"),
        ("Max", "Male", 4, "Golden Retriever", "img/farm.jpg"),
        ("Bella", "Female", 1, "Shih Tzu", "img/farm.jpg"),
        ("Lucy", "Female", 7, "Beagle", "img/farm.jpg"),
    ]
    for name, gender, age, breed, picture_path in pets_to_register:
        message = register_pet(client, name, gender, age, breed, picture_path)
        print(f"Registering {name}: {message}")
        time.sleep(0.1)  # Slight delay to ensure registration is processed
    print("Dataset built successfully.\n")


def search_pet(client, query):
    """
    Search for pets matching the query.
    
    Args:
        client: The gRPC client stub.
        query (str): The search query based on name, gender, age, or breed.
        
    Returns:
        list: List of matching Pet objects.
    """
    request = petadoption_pb2.SearchRequest(query=query)
    try:
        response = client.SearchPet(request)
        return response.pets
    except grpc.RpcError as e:
        print(f"gRPC Error during search: {e.details()}")
        return []


def test_register_pet(client):
    """
    Test registering a new pet.
    
    Args:
        client: The gRPC client stub.
    """
    print("Testing pet registration...")
    name = "Rocky"
    gender = "Male"
    age = 4
    breed = "Boxer"
    picture_path = "img/farm.jpg"
    
    message = register_pet(client, name, gender, age, breed, picture_path)
    assert "successfully" in message.lower() or "registered" in message.lower(), "Pet registration failed."
    print(f"Passed test_register_pet: {message}\n")


def test_search_pet(client):
    """
    Test searching for a pet by name.
    
    Args:
        client: The gRPC client stub.
    """
    print("Testing pet search by name...")
    query = "Buddy"
    pets = search_pet(client, query)
    assert len(pets) >= 1, f"No pets found with query '{query}'."
    assert any(pet.name == "Buddy" for pet in pets), "Buddy not found in search results."
    print(f"Passed test_search_pet: Found {len(pets)} pet(s) with name '{query}'.\n")


def test_search_by_gender(client):
    """
    Test searching for pets by gender.
    
    Args:
        client: The gRPC client stub.
    """
    print("Testing pet search by gender...")
    query = "Female"
    pets = search_pet(client, query)
    expected_count = 3  # Based on the initial dataset (Daisy, Bella, Lucy)
    assert len(pets) >= expected_count, f"Expected at least {expected_count} female pets, found {len(pets)}."
    assert all(pet.gender == "Female" for pet in pets), "Not all returned pets are female."
    print(f"Passed test_search_by_gender: Found {len(pets)} female pet(s).\n")


def test_search_by_age(client):
    """
    Test searching for pets by age.
    
    Args:
        client: The gRPC client stub.
    """
    print("Testing pet search by age...")
    query = "3"
    pets = search_pet(client, query)
    expected_pets = ["Charlie"]  # Based on the initial dataset
    found_pets = [pet.name for pet in pets]
    for pet_name in expected_pets:
        assert pet_name in found_pets, f"Expected to find pet '{pet_name}' with age 3."
    print(f"Passed test_search_by_age: Found pets with age '{query}': {found_pets}\n")


def test_search_by_breed(client):
    """
    Test searching for pets by breed.
    
    Args:
        client: The gRPC client stub.
    """
    print("Testing pet search by breed...")
    query = "Beagle"
    pets = search_pet(client, query)
    expected_pets = ["Charlie", "Lucy"]  # Based on the initial dataset
    found_pets = [pet.name for pet in pets]
    for pet_name in expected_pets:
        assert pet_name in found_pets, f"Expected to find pet '{pet_name}' with breed 'Beagle'."
    print(f"Passed test_search_by_breed: Found pets with breed '{query}': {found_pets}\n")


def test_register_multiple_pets(client):
    """
    Test registering multiple pets and ensure all are searchable.
    
    Args:
        client: The gRPC client stub.
    """
    print("Testing registering multiple pets...")
    multiple_pets = [
        ("Molly", "Female", 3, "Bulldog", "img/farm.jpg"),
        ("Oscar", "Male", 5, "Terrier", "img/farm.jpg"),
        ("Lola", "Female", 2, "Pomeranian", "img/farm.jpg"),
    ]
    for name, gender, age, breed, picture_path in multiple_pets:
        message = register_pet(client, name, gender, age, breed, picture_path)
        assert "successfully" in message.lower() or "registered" in message.lower(), f"Failed to register pet '{name}'."
        print(f"Registered {name}: {message}")
    print("Passed test_register_multiple_pets.\n")
    
    # Verify that all newly registered pets can be searched
    for name, _, _, _, _ in multiple_pets:
        pets = search_pet(client, name)
        assert len(pets) >= 1 and any(pet.name == name for pet in pets), f"Pet '{name}' not found in search."
        print(f"Verified search for {name}: Found {len(pets)} pet(s).")
    print("Passed verification for test_register_multiple_pets.\n")


def test_search_with_multiple_criteria(client):
    """
    Test searching for pets using multiple criteria.
    
    Args:
        client: The gRPC client stub.
    """
    print("Testing pet search with multiple criteria...")
    # Since the server likely treats the query as a single string, perform separate searches and cross-validate
    name_query = "Buddy"
    breed_query = "Labrador"
    
    pets_by_name = search_pet(client, name_query)
    pets_by_breed = search_pet(client, breed_query)
    
    # Find intersection based on pet attributes
    matching_pets = [pet for pet in pets_by_name if pet in pets_by_breed]
    
    # Assert that Buddy with breed Labrador exists in the intersection
    assert any(pet.name == "Buddy" and pet.breed == "Labrador" for pet in matching_pets), \
        "Buddy Labrador not found in search results."
    
    print(f"Passed test_search_with_multiple_criteria: Found {len(matching_pets)} pet(s) matching '{name_query}' and '{breed_query}'.\n")


def run_tests():
    """
    Connect to the server, build the dataset, and run all functional tests.
    """
    server_address = os.getenv('SERVER_ADDRESS', 'server:50051')  # Ensure this matches your Docker Compose port
    options = [
        ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50 MB for incoming messages
        ('grpc.max_send_message_length', 50 * 1024 * 1024),     # 50 MB for outgoing messages
    ]
    print(f"Connecting to server at: {server_address}")
    failed_tests = []

    with grpc.insecure_channel(f"{server_address}", options=options) as channel:
        client = petadoption_pb2_grpc.PetAdoptionServiceStub(channel)

        # Build the dataset first
        build_dataset(client)

        # List of functional test functions to run
        test_functions = [
            test_register_pet,
            test_search_pet,
            test_search_by_gender,
            test_search_by_age,
            test_search_by_breed,
            test_register_multiple_pets,
            test_search_with_multiple_criteria,
        ]

        # Run each test
        for test in test_functions:
            try:
                test(client)
            except AssertionError as ae:
                failed_tests.append(test.__name__)
                print(f"Failed {test.__name__}: {ae}")
            except Exception as e:
                failed_tests.append(test.__name__)
                print(f"Error in {test.__name__}: {e}")

    if failed_tests:
        print("\nThe following tests failed:")
        for test in failed_tests:
            print(f"- {test}")
    else:
        print("\nAll functional tests passed successfully.")


if __name__ == '__main__':
    run_tests()
