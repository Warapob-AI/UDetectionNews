import os
from pymongo import MongoClient
from dotenv import load_dotenv

def delete_all_documents_in_collection(db_name: str, collection_name: str):
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PROJECT_NAME = os.getenv('DB_PROJECT_NAME')

    if not all([DB_USERNAME, DB_PASSWORD, DB_PROJECT_NAME]):
        print("❌ Error: Database credentials not found in .env file.")
        return

    connection_string = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_PROJECT_NAME}.0prwqib.mongodb.net/"
    client = None

    try:
        client = MongoClient(connection_string)
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")

        db = client[db_name]
        collection = db[collection_name]

        print(f"\n🗑️ Deleting all documents from the '{collection_name}' collection in the '{db_name}' database...")
        
        result = collection.delete_many({})
        
        print(f"✅ Success! Deleted {result.deleted_count} documents.")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        if client:
            client.close()
            print("🔌 Connection to MongoDB closed.")

if __name__ == "__main__":
    load_dotenv()

    DATABASE_TO_CLEAR = 'UDetectionNews'
    COLLECTION_TO_CLEAR = 'LinkNews'

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!! WARNING !!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(f"You are about to permanently delete ALL documents from the following location:")
    print(f"Database:   {DATABASE_TO_CLEAR}")
    print(f"Collection: {COLLECTION_TO_CLEAR}")
    print("This action CANNOT be undone.")
    
    confirm = input("Type the name of the collection to confirm: ")
    
    if confirm == COLLECTION_TO_CLEAR:
        print("Confirmation received. Proceeding with deletion...")
        delete_all_documents_in_collection(DATABASE_TO_CLEAR, COLLECTION_TO_CLEAR)
    else:
        print("Confirmation failed. Deletion cancelled.")