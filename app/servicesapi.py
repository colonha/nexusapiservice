from flask import Flask, jsonify, request
from flask_restful import reqparse
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
import os
import time
from prometheus_flask_exporter import PrometheusMetrics
import logging

parser = reqparse.RequestParser()
# Pagination parameters
parser.add_argument('page', type=int, required=False, help='Page number of the results', location='args', default=None)
parser.add_argument('limit', type=int, required=False, help='Number of results per page', location='args', default=None)

# Filtering parameters
parser.add_argument('name', type=str, required=False, help='Filter by name', location='args', default=None)
# Add other filter parameters as needed...




app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://mongo:27017/myDatabase")
mongo = PyMongo(app)
metrics = PrometheusMetrics(app)


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
        
    

@app.route('/')
def index():
    if not wait_for_db():
        return "Database is not ready", 503
    return "Hello, welcome to API services!"

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
def api_services():
    args = parser.parse_args()
    services = Service.get_services(args)
    return services        

if __name__ == "__main__":
    wait_for_db()
    app.run(debug=True)

