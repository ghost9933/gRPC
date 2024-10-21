import grpc
from concurrent import futures
import petadoption_pb2
import petadoption_pb2_grpc
import time
import threading
import logging
import base64
import uuid  # Import UUID for generating unique IDs

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(message)s')

class PetAdoptionService(petadoption_pb2_grpc.PetAdoptionServiceServicer):
    def __init__(self):
        self.pets = {}  # In-memory storage for pets
        self.locks = {}  # Locks for individual pet records

    def get_lock(self, pet_id):
        if pet_id not in self.locks:
            self.locks[pet_id] = threading.Lock()
        return self.locks[pet_id]

    def RegisterPet(self, request, context):
        lock = self.get_lock(request.name)  # Use name or ID
        with lock:  # Ensure thread safety
            pet_id = str(uuid.uuid4())  # Generate a unique ID for each pet
            self.pets[pet_id] = {
                'id': pet_id,
                'name': request.name,
                'gender': request.gender,
                'age': request.age,
                'breed': request.breed,
                'picture': request.picture
            }
            logging.info(f"Registered pet: {request.name} with id: {pet_id}, gender: {request.gender}, breed: {request.breed}, age: {request.age} by {threading.current_thread().name}")
            print("end of register")
            return petadoption_pb2.Response(message="Pet registered successfully.")

    def SearchPet(self, request, context):
        matching_pets = []
        for pet_id, pet_data in self.pets.items():
            if (
                request.query.lower() == pet_data['name'].lower() or  # Exact match for name
                request.query.lower() == pet_data['gender'].lower() or  # Exact match for gender
                request.query == str(pet_data['age']) or  # Exact match for age
                request.query.lower() == pet_data['breed'].lower()  # Exact match for breed
            ):
                matching_pets.append(petadoption_pb2.Pet(
                    id=pet_data['id'],
                    name=pet_data['name'],
                    gender=pet_data['gender'],
                    age=pet_data['age'],
                    breed=pet_data['breed'],
                    picture=pet_data['picture']
                ))

        logging.info(f"Search request for '{request.query}' served by {threading.current_thread().name}")
        
        # Logging current pets
        print("end of search")
        return petadoption_pb2.SearchResponse(pets=matching_pets)

def serve():
    options = [
        ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 10 MB
        ('grpc.max_send_message_length', 50 * 1024 * 1024),     # 10 MB
    ]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)
    petadoption_pb2_grpc.add_PetAdoptionServiceServicer_to_server(PetAdoptionService(), server)
    server.add_insecure_port('0.0.0.0:50051')
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
