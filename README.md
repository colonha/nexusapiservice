Services API Project
====================

Overview
--------

This is my implementation of the Services API project. It is a RESTful API that provides information about services and their versions. It is written in Python and uses the Flask framework.

Features
--------

List the key features of the API, such as:

*   Retrieving a list of services from the database.
    *  WIP - with options for filtering, sorting, and pagination.
    
*   Fetching details of a specific service, including available versions.
    
*   WIP - Observability features for monitoring the service.

Technologies Used
-----------------

*   **Flask:** Used for building the API.
    
*   **MongoDB:** Database system for storing data.
    
*   **PyMongo:** Library for MongoDB interaction.
    
*   **Python:** Programming language for backend development.
    
*   **JSON:** Data representation and storage format.
    
*   **Git:** Version control system.
    
*   **Docker:** Platform for developing, shipping, and running applications in containers.
    
*   **Docker Compose:** Tool for defining and running multi-container Docker applications.
    
Data model
----------

*   **Type**: NoSQL DB
    
*   **Suggested NoSQL**: MongoDB, Cassandra, redis
    
*   **Reasoning**
    
    *   **Dynamic Schema:** NoSQL databases like MongoDB have a flexible schema
        
    *   **Ease of Scaling:** NoSQL databases are designed for horizontal scaling.
        
    *   **High Throughput:** They can handle high levels of read and write traffic.
        
    *   **Native JSON Support:** MongoDB uses BSON (Binary JSON).
        

### Schema Design
#### Table: **Services**

| Syntax      | Description |
| ----------- | ----------- |
| service\_id      | Primary Key, ObjectId.       |
| name   | str, Indexed for quick search.        |
| description   | str, to store detailed information about the service.        |
| creation\_date   | ISOdate, to store creation date of the service.        |

    

#### Table: **Versions**
| Syntax      | Description |
| ----------- | ----------- |
| version\_id      | Primary Key, ObjectId.       |
| service\_id   | Foreign Key, ObjectId, References **Services.service\_id**.        |
| version\_number   | str, represents the version of the service.        |
| additional\_info   | str, to store additional information about the version.        |




Getting Started
---------------

To be run the project locally, you need to have git, Docker and Docker Compose installed on your machine. Then, follow the steps below:

Clone the repository
```console
git clone git@github.com:colonha/nexus.git
```
activate the virtual environment
```console
source venv/bin/activate
```

Docker compose
```console
docker compose up -d
```

    

API Endpoints
-------------

Document the available API endpoints with their methods, path, request parameters, and a brief description of what they do. For example:

*   **GET /api/services**: Retrieves a list of services.
    
*   **GET /api/services/:id**: Fetches details of a specific service.
    

    

Testing
-------

WIP

Observability
-------------

WIP