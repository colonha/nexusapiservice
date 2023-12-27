from flask import Flask, jsonify, request
from flask_restful import reqparse
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
import os
import time
import logging

pagination_data = reqparse.RequestParser()
pagination_data.add_argument('page', type=int, required=True, help='Page number is required', location='args')
pagination_data.add_argument('limit', type=int, required=True, help='Limit is required', location='args')
filter_parser = reqparse.RequestParser()
filter_parser.add_argument('name', type=str, required=False, help='Filter by service name', location='args')



app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://mongo:27017/myDatabase")
mongo = PyMongo(app)


def is_db_ready():
    try:
        # Attempt a simple operation like a server info command to check DB connection
        mongo.db.command('ismaster')
        return True
    except Exception as e:
        print(f"Database check failed: {e}")
        return False

def wait_for_db(max_retries=5, delay=3):
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

# services and versions documents structure
# {
#   "_id": "unique_service_id",
#   "name": "Service Name",
#   "description": "..."
# }
#
# {
#   "_id": "unique_version_id",
#   "service_id": "unique_service_id",
#   "version_number": "1.0",
#   "additional_info": "..."
# }

# Service Class/Methods
class Service:
    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def insert(self):
        self.creation_date = datetime.utcnow()
        return mongo.db.services.insert_one(self.__dict__).inserted_id

    @staticmethod
    def get_all():
        services = mongo.db.services.find()
        # Use list comprehension to convert each document
        return [{k: str(v) if isinstance(v, ObjectId) else v for k, v in service.items()} for service in services]

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
        
    

@app.route('/')
def index():
    if not wait_for_db():
        return "Database is not ready", 503
    return "Hello, World!"

@app.route('/api/service', methods=['POST'])
def add_service():
    data = request.json
    service = Service(data['name'])
    service_id = service.insert()
    return jsonify({'service_id': str(service_id)})


@app.route('/api/version', methods=['POST'])
def add_version():
    data = request.json
    version = Version(data['service_id'], data['version_number'], data['additional_info'])
    version.insert()
    return jsonify({"message": "Version added successfully"})

@app.route('/api/service/<service_id>/versions', methods=['GET'])
def get_versions(service_id):
    versions = Version.get_by_service_id(service_id)
    return jsonify({"versions": [version for version in versions]})


@app.route('/api/service/<service_id>', methods=['GET'])
def get_service(service_id):
    service = Service.get_by_id(service_id)
    print(service)
    return jsonify({"service": service})

@app.route('/api/services', methods=['GET'])
def get_services():

    args = filter_parser.parse_args()
    filters = {}

    if args['name']:
        filters['name'] = args['name']
        services = mongo.db.services.find(filters)
        services_list = [{k: str(v) if isinstance(v, ObjectId) else v for k, v in service.items()} for service in services]
        return jsonify({"services": [service for service in services_list]})

    # Add other filters to the dictionary as needed

    args = pagination_data.parse_args()
    page = args['page']
    #page = 2
    print(page)
    print("Hola PEPE")
    limit = args['limit']
    #limit = 3

    services_count = mongo.db.services.count_documents({})
    print(services_count)
    services = mongo.db.services.find().skip(limit * (page - 1)).limit(limit)
    services_list = [{k: str(v) if isinstance(v, ObjectId) else v for k, v in service.items()} for service in services]

    return jsonify({
        "total_number": services_count, 
        "page": page, 
        "showing": limit, 
        "services": services_list
    })
    # services = Service.get_all()
    # return jsonify({"services": [service for service in services]})


if __name__ == "__main__":
    wait_for_db()
    app.run(debug=True)

