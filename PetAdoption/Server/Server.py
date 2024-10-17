import grpc
from concurrent import futures
import petadoption_pb2
import petadoption_pb2_grpc
import time
import threading
import logging
# from PIL import Image
# import io

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
        lock = self.get_lock(request.id)
        with lock:  # Ensure thread safety for the specific pet ID
            self.pets[request.id] = {
                'id': request.id,
                'name': request.name,
                'gender': request.gender,
                'age': request.age,
                'breed': request.breed,
                'picture': request.picture
            }
            # image = Image.open(io.BytesIO(request.picture))
            logging.info(f"Registered pet: {request.name} with name: {request.name},id:{request.id},gender:{request.gender},breed:{request.breed},age:{request.age} by {threading.current_thread().name}")
            # image.show()
            return petadoption_pb2.Response(message="Pet registered successfully.")

    def SearchPet(self, request, context):
        matching_pets = []
        for pet_id, pet_data in self.pets.items():
            if (
                request.query.lower() in pet_data['name'].lower() or
                request.query.lower() in pet_data['gender'].lower() or
                request.query == str(pet_data['age']) or
                request.query.lower() in pet_data['breed'].lower()
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
        return petadoption_pb2.SearchResponse(pets=matching_pets)

    def UpdatePet(self, request, context):
        lock = self.get_lock(request.id)
        with lock:  # Ensure thread safety for the specific pet ID
            if request.id in self.pets:
                self.pets[request.id] = {
                    'id': request.id,
                    'name': request.name,
                    'gender': request.gender,
                    'age': request.age,
                    'breed': request.breed,
                    'picture': request.picture
                }
                logging.info(f"Updated pet: {request.name} by {threading.current_thread().name}")
                return petadoption_pb2.Response(message="Pet updated successfully.")
            else:
                return petadoption_pb2.Response(message="Pet not found.")

    def RemovePet(self, request, context):
        lock = self.get_lock(request.id)
        with lock:  # Ensure thread safety for the specific pet ID
            if request.id in self.pets:
                del self.pets[request.id]
                logging.info(f"Removed pet with ID: {request.id} by {threading.current_thread().name}")
                return petadoption_pb2.Response(message="Pet removed successfully.")
            else:
                return petadoption_pb2.Response(message="Pet not found.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
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
