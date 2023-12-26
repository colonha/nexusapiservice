from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime


app = Flask(__name__)
# Configure the SQLAlchemy part of the app instance
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

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
        print (type(service_id))
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
        return mongo.db.versions.find({'service_id': service_id})
    


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
    services = Service.get_all()
    return jsonify({"services": [service for service in services]})


if __name__ == "__main__":
    app.run(debug=True)

