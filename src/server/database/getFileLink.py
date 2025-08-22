import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# --- ส่วนของฟังก์ชันดึงข้อมูลจาก MongoDB (เหมือนเดิม) ---
def fetch_link_news():
    """
    Fetches the latest 7 news links from the MongoDB database 
    and formats them with the key 'imageUrl'.
    """
    load_dotenv()
    
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PROJECT_NAME = os.getenv('DB_PROJECT_NAME')

    if not all([DB_USERNAME, DB_PASSWORD, DB_PROJECT_NAME]):
        print("❌ Error: Database credentials or DB_NAME not found in .env file.")
        return None

    connection_string = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_PROJECT_NAME}.0prwqib.mongodb.net/"
    COLLECTION_NAME = 'LinkNews'
    
    client = None
    try:
        print("Connecting to MongoDB...")
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ Connection successful!")
        
        db = client[DB_PROJECT_NAME]
        collection = db[COLLECTION_NAME]

        projection = {
            '_id': 0, 'title': 1, 'description': 1, 
            'link': 1, 'image_url': 1
        }

        documents = list(collection.find({}, projection).limit(7))
        print(f"Found {len(documents)} documents.")

        formatted_results = [
            {
                'title': doc.get('title'),
                'description': doc.get('description'),
                'link': doc.get('link'),
                'imageUrl': doc.get('image_url')
            }
            for doc in documents
        ]
        
        return formatted_results

    except ConnectionFailure as e:
        print(f"❌ Connection failed: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if client:
            client.close()
            print("Connection closed.")