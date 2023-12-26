from servicesapi import app, mongo, Service, Version
import json
import random
import time

def generate_dummy_data():
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
            item=random.randint(0, json_object_len - 1)
            version = Version(service_id=service_id, version_number=sample_versions[item]['version_number'], additional_info=sample_versions[item]['additional_info'])
            version.insert()
            print(sample_versions[item]['version_number'])
        time.sleep(3)

if __name__ == '__main__':
    generate_dummy_data()