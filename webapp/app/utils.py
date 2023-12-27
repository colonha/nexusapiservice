import time
#from app import mongo
from flask import current_app

def is_db_ready():
    from app import mongo
    try:
        # Attempt a simple operation like a server info command to check DB connection
        #mongo = current_app.extensions['pymongo']
        # pymongo_extension = current_app.extensions.get('pymongo')
        # mongo = pymongo_extension.db if pymongo_extension else None   
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