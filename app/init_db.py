# from servicesapi import app, mongo, Service, Version
# import json
# import random
# import time

# def generate_dummy_data():
#     # Read and insert services
#     with open('sample_services.json') as f:
#         sample_services = json.load(f)
#     for service_data in sample_services:
#         service = Service(name=service_data['name'], description=service_data['description'])
#         service_id = service.insert()
#         print(service_data['name'])
        

#     # Read and insert versions for each service
#         with open('sample_versions.json') as fv:
#             sample_versions = json.load(fv)
#             json_object_len = len(sample_versions)
#         for version_data in range(3):
#             item=random.randint(0, json_object_len - 1)
#             version = Version(service_id=service_id, version_number=sample_versions[item]['version_number'], additional_info=sample_versions[item]['additional_info'])
#             version.insert()
#             print(sample_versions[item]['version_number'])
#         time.sleep(3)

# if __name__ == '__main__':
#     generate_dummy_data()

from servicesapi import app, mongo, Service, Version
import json
import random
import time

def is_db_ready():
    try:
        # Perform a simple operation like a ping to check DB connection
        mongo.db.command('ismaster')
        
        return True
    except:
        return False

def wait_for_db(max_retries=3, delay=3):
    retries = 0
    while retries < max_retries:
        if is_db_ready():
            print("Database is ready.")
            return True
        else:
            print(f"Waiting for database... retry {retries + 1}/{max_retries}")
            time.sleep(delay)
            retries += 1
    raise Exception("Database is not ready after maximum retries.")

def generate_dummy_data():
    # Ensure DB is ready before proceeding
    wait_for_db()

    # Read and insert services
    with open('sample_services.json') as f:
        sample_services = json.load(f)
    for service_data in sample_services:
        service = Service(name=service_data['name'], description=service_data['description'])
        service_id = service.insert()
        print(service_data['name'])

        # Read and insert versions for each service
        with open('sample_versions.json') as fv:
            sample_versions = json.load(fv)
            json_object_len = len(sample_versions)
        for version_data in range(3):
            item = random.randint(0, json_object_len - 1)
            version = Version(service_id=service_id, version_number=sample_versions[item]['version_number'], additional_info=sample_versions[item]['additional_info'])
            version.insert()
            print(sample_versions[item]['version_number'])
        time.sleep(3)

if __name__ == '__main__':
    generate_dummy_data()
