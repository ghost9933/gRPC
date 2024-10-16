import grpc
from concurrent import futures
import petadoption_pb2
import petadoption_pb2_grpc
import time
import threading
import logging
import os
import pickle

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(message)s')

DATA_DIR = "data"

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

class PetAdoptionService(petadoption_pb2_grpc.PetAdoptionServiceServicer):
    def __init__(self):
        self.locks = {}  # Locks for individual pet records

    def get_lock(self, pet_id):
        if pet_id not in self.locks:
            self.locks[pet_id] = threading.Lock()
        return self.locks[pet_id]

    def save_pet_to_file(self, pet):
        pet_file_path = os.path.join(DATA_DIR, f"{pet.id}.pkl")
        with open(pet_file_path, "wb") as f:
            pickle.dump({
                'id': pet.id,
                'name': pet.name,
                'gender': pet.gender,
                'age': pet.age,
                'breed': pet.breed,
                'picture': pet.picture
            }, f)

    def load_pet_from_file(self, pet_id):
        pet_file_path = os.path.join(DATA_DIR, f"{pet_id}.pkl")
        if os.path.exists(pet_file_path):
            with open(pet_file_path, "rb") as f:
                pet_data = pickle.load(f)
                return petadoption_pb2.Pet(
                    id=pet_data['id'],
                    name=pet_data['name'],
                    gender=pet_data['gender'],
                    age=pet_data['age'],
                    breed=pet_data['breed'],
                    picture=pet_data['picture']
                )
        return None

    def RegisterPet(self, request, context):
        lock = self.get_lock(request.id)
        with lock:  # Ensure thread safety for the specific pet ID
            self.save_pet_to_file(request)
            logging.info(f"Registered pet: {request.name} with name: {request.name},id:{request.id},gender:{request.gender},breed:{request.breed},age:{request.age},image:{request.image} by {threading.current_thread().name}")
            return petadoption_pb2.Response(message="Pet registered successfully.")

    def SearchPet(self, request, context):
        matching_pets = []
        for pet_file in os.listdir(DATA_DIR):
            pet_id, ext = os.path.splitext(pet_file)
            if ext == ".pkl":
                pet = self.load_pet_from_file(pet_id)
                if pet and (
                    request.query.lower() in pet.name.lower() or
                    request.query.lower() in pet.gender.lower() or
                    request.query == str(pet.age) or
                    request.query.lower() in pet.breed.lower()
                ):
                    matching_pets.append(pet)
        logging.info(f"Search request for '{request.query}' served by {threading.current_thread().name}")
        return petadoption_pb2.SearchResponse(pets=matching_pets)

    def UpdatePet(self, request, context):
        lock = self.get_lock(request.id)
        with lock:  # Ensure thread safety for the specific pet ID
            pet = self.load_pet_from_file(request.id)
            if pet:
                self.save_pet_to_file(request)
                logging.info(f"Updated pet: {request.name} by {threading.current_thread().name}")
                return petadoption_pb2.Response(message="Pet updated successfully.")
            else:
                return petadoption_pb2.Response(message="Pet not found.")

    def RemovePet(self, request, context):
        lock = self.get_lock(request.id)
        with lock:  # Ensure thread safety for the specific pet ID
            pet_file_path = os.path.join(DATA_DIR, f"{request.id}.pkl")
            if os.path.exists(pet_file_path):
                os.remove(pet_file_path)
                logging.info(f"Removed pet with ID: {request.id} by {threading.current_thread().name}")
                return petadoption_pb2.Response(message="Pet removed successfully.")
            else:
                return petadoption_pb2.Response(message="Pet not found.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    petadoption_pb2_grpc.add_PetAdoptionServiceServicer_to_server(PetAdoptionService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info(f"Server started and listening on port 50051")
    try:
        while True:
            time.sleep(86400)  # Keep the server running for a day
    except KeyboardInterrupt:
        logging.info('Stopping server...')
        server.stop(0)

if __name__ == '__main__':
    serve()