import grpc
import petadoption_pb2
import petadoption_pb2_grpc
import unittest

class TestPetAdoption(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.channel = grpc.insecure_channel('localhost:50051')
        cls.client = petadoption_pb2_grpc.PetAdoptionServiceStub(cls.channel)

    @classmethod
    def tearDownClass(cls):
        cls.channel.close()

    def test_register_pet_success(self):
        pet = petadoption_pb2.Pet(name="Buddy", gender="Male", age=3, breed="Golden Retriever", picture=b"dummy_data")
        response = self.client.RegisterPet(pet)
        self.assertEqual(response.message, "Pet registered successfully.")

    def test_search_registered_pet(self):
        request = petadoption_pb2.SearchRequest(query="Buddy")
        response = self.client.SearchPet(request)
        self.assertEqual(len(response.pets), 1)
        self.assertEqual(response.pets[0].name, "Buddy")

    def test_search_non_existing_pet(self):
        request = petadoption_pb2.SearchRequest(query="NonExistent")
        response = self.client.SearchPet(request)
        self.assertEqual(len(response.pets), 0)

    def test_register_multiple_pets(self):
        pets = [
            petadoption_pb2.Pet(name="Max", gender="Male", age=2, breed="Labrador", picture=b"dummy_data"),
            petadoption_pb2.Pet(name="Bella", gender="Female", age=1, breed="Poodle", picture=b"dummy_data"),
        ]
        for pet in pets:
            response = self.client.RegisterPet(pet)
            self.assertEqual(response.message, "Pet registered successfully.")

    def test_search_pet_by_breed(self):
        request = petadoption_pb2.SearchRequest(query="Poodle")
        response = self.client.SearchPet(request)
        self.assertEqual(len(response.pets), 1)
        self.assertEqual(response.pets[0].breed, "Poodle")

    def test_search_pet_by_gender(self):
        request = petadoption_pb2.SearchRequest(query="Female")
        response = self.client.SearchPet(request)
        self.assertGreater(len(response.pets), 0)  # Expect at least one female pet

    def test_register_pet_with_empty_name(self):
        pet = petadoption_pb2.Pet(name="", gender="Male", age=3, breed="Beagle", picture=b"dummy_data")
        response = self.client.RegisterPet(pet)
        self.assertEqual(response.message, "Pet registered successfully.")

    def test_register_pet_with_special_characters(self):
        pet = petadoption_pb2.Pet(name="Buddy#1", gender="Male", age=3, breed="Beagle", picture=b"dummy_data")
        response = self.client.RegisterPet(pet)
        self.assertEqual(response.message, "Pet registered successfully.")

    def test_search_pet_with_numeric_query(self):
        request = petadoption_pb2.SearchRequest(query="3")  # Searching by age
        response = self.client.SearchPet(request)
        self.assertGreater(len(response.pets), 0)  # Expect at least one pet with age 3

    def test_search_pet_with_empty_query(self):
        request = petadoption_pb2.SearchRequest(query="")
        response = self.client.SearchPet(request)
        self.assertGreater(len(response.pets), 0)  # Expect some results with an empty query

if __name__ == "__main__":
    unittest.main()
