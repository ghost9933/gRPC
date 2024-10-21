import grpc
import petadoption_pb2
import petadoption_pb2_grpc
import threading
import time
import os
import base64


def register_pet(client, name, gender, age, breed, picture_path):
    """Register a pet with the provided details."""
    with open(picture_path, "rb") as f:
        picture = f.read()

    pet = petadoption_pb2.Pet(name=name, gender=gender, age=age, breed=breed, picture=picture)
    response = client.RegisterPet(pet)
    return response.message


def build_dataset(client):
    """Build a dataset of pets for testing."""
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
        register_pet(client, name, gender, age, breed, picture_path)
        time.sleep(0.1)  # Slight delay to avoid race conditions
    print("Dataset built successfully.")


def search_pet(client, query):
    """Search for pets matching the query."""
    request = petadoption_pb2.SearchRequest(query=query)
    response = client.SearchPet(request)
    return response.pets


def test_search_other_client(client):
    """Test the search functionality for registered pets."""
    time.sleep(1)  # Ensure registration is complete
    pets = search_pet(client, "Buddy")
    assert len(pets) == 1 and pets[0].name == "Buddy", "Test failed: Buddy not found."


def test_edge_cases_search(client):
    """Test edge cases in the search functionality."""
    assert len(search_pet(client, "Charlie")) == 1, "Test failed: Charlie not found."
    assert len(search_pet(client, "Poodle")) == 1, "Test failed: Daisy not found."
    assert len(search_pet(client, "3")) == 1, "Test failed: Charlie not found by age."
    assert len(search_pet(client, "Female")) == 2, "Test failed: Daisy and Lucy not found by gender."


def test_multi_thread_edge_cases_search(client):
    """Test multi-threaded edge cases in the search functionality."""
    print("\nTesting edge cases for search...")

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
    """Test handling of simultaneous registration requests."""
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
    server_address = os.getenv('SERVER_ADDRESS', 'server:50052')  # Use the service name
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

        # Run tests
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
