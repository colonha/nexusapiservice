from bson import ObjectId
from datetime import datetime
from flask import jsonify
#from . import mongo
#from app import mongo



class Service:
    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def insert(self):
        from app import mongo
#        mongo = current_app.extensions['pymongo']
        self.creation_date = datetime.utcnow()
        return mongo.db.services.insert_one(self.__dict__).inserted_id
    
    @staticmethod
    def convert_service(service):
        return {k: str(v) if isinstance(v, ObjectId) else v for k, v in service.items()}
    
    @classmethod
    def get_all(cls):
        from app import mongo
#        mongo = current_app.extensions['pymongo']
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
        from app import mongo
        filter_dict = {}        
#        mongo = current_app.extensions['pymongo']
        for key, value in filters.items():
            if value:
                filter_dict[key] = value
        services = mongo.db.services.find(filter_dict)
        return [cls.convert_service(service) for service in services]
    @classmethod
    def apply_pagination(cls, pagination_data):
        from app import mongo
        page = pagination_data.get('page', 1)   
        limit = pagination_data.get('limit', 5)
        
#        mongo = current_app.extensions['pymongo']
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
        from app import mongo
        try:
    #        mongo = current_app.extensions['pymongo']
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
        from app import mongo
#        mongo = current_app.extensions['pymongo']
        mongo.db.versions.insert_one(self.__dict__)

    @staticmethod
    def get_by_service_id(service_id):
        from app import mongo
        try:
    #        mongo = current_app.extensions['pymongo']
            versions=mongo.db.versions.find({'service_id': ObjectId(service_id)})
            if versions:
                return [{k: str(v) if isinstance(v, ObjectId) else v for k, v in version.items()} for version in versions]
        except Exception as e:
            print("An error occurred:", e)
            return None