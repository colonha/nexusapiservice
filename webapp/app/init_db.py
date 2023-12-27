from flask_pymongo import PyMongo
import random
import time
from flask import Flask
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://mongo:27017/myDatabase")
mongo = PyMongo(app)

# Service Class/Methods
class Service:
    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def insert(self):
        self.creation_date = datetime.utcnow()
        return mongo.db.services.insert_one(self.__dict__).inserted_id
    
    @staticmethod
    def convert_service(service):
        return {k: str(v) if isinstance(v, ObjectId) else v for k, v in service.items()}
    
    @classmethod
    def get_all(cls):
        services = mongo.db.services.find()
        # Use list comprehension to convert each document
        return jsonify([cls.convert_service(service) for service in services])
    @classmethod
    def get_services(cls, args):
        if args["name"]:
            filtered_services = cls.apply_filters(args)
            return jsonify({"services": [service for service in filtered_services]})
        elif args["page"] and args["limit"]:
            paginated_services = cls.apply_pagination(args)
            return paginated_services
        else:
            return cls.get_all()
    @classmethod
    def apply_filters(cls, filters):
        filter_dict = {}
        for key, value in filters.items():
            if value:
                filter_dict[key] = value
        services = mongo.db.services.find(filter_dict)
        return [cls.convert_service(service) for service in services]
    @classmethod
    def apply_pagination(cls, pagination_data):
        page = pagination_data.get('page', 1)
        print("Page is:", page)
        limit = pagination_data.get('limit', 5)
        skip_amount = limit * (page - 1)

        paginated_services = mongo.db.services.find().skip(skip_amount).limit(limit)
        services_count = mongo.db.services.count_documents({})

        return jsonify({
            "total_number": services_count,
            "page": page,
            "showing": limit,
            "services": [cls.convert_service(service) for service in paginated_services]
        })
    @staticmethod
    def get_by_id(service_id):
        try:
            service = mongo.db.services.find_one({"_id": ObjectId(service_id)})
            if service:
                service['_id'] = str(service['_id'])
                return service
        except Exception as e:
            print("An error occurred:", e)
            return None


# Version Class/Methods
class Version:
    def __init__(self, service_id, version_number, additional_info):
        self.service_id = service_id
        self.version_number = version_number
        self.additional_info = additional_info

    def insert(self):
        mongo.db.versions.insert_one(self.__dict__)

    @staticmethod
    def get_by_service_id(service_id):
        try:
            versions=mongo.db.versions.find({'service_id': ObjectId(service_id)})
            if versions:
                return [{k: str(v) if isinstance(v, ObjectId) else v for k, v in version.items()} for version in versions]
        except Exception as e:
            print("An error occurred:", e)
            return None

def is_db_ready():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://mongo:27017/myDatabase")
    mongo = PyMongo(app)
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
