from flask import jsonify, request
from .models import Service, Version
from .utils import wait_for_db
from flask_restful import reqparse



def configure_routes(app):
    
    parser = reqparse.RequestParser()
    # Pagination parameters
    parser.add_argument('page', type=int, required=False, help='Page number of the results', location='args', default=None)
    parser.add_argument('limit', type=int, required=False, help='Number of results per page', location='args', default=None)

    # Filtering parameters
    parser.add_argument('name', type=str, required=False, help='Filter by name', location='args', default=None)
    # Add other filter parameters as needed...

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