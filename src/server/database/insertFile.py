import pandas as pd
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def load_excel_to_mongodb(excel_path: str, db_name: str, collection_name: str) -> bool:
    try:
        df = pd.read_excel(excel_path)

        columns_to_drop = df.columns[-3:]
        df_dropped = df.drop(columns=columns_to_drop)
        
        rename_mapping = {
        'วันและเวลาที่เผยแพร่': 'datetime',
        'หัวข้อข่าว': 'title',
        'เนื้อหาข่าว': 'description',
        'ลิงค์ข่าว': 'link',
        'หน่วยงานที่ตรวจสอบ': 'verified_by',
        'ประเภทข่าว': 'category'
        }

        df_renamed = df_dropped.rename(columns=rename_mapping)
        categories_to_keep = ["ข่าวจริง", "ข่าวปลอม", "ข่าวบิดเบือน"]

        df = df_renamed[df_renamed['category'].isin(categories_to_keep)]

        image_urls = []
        
        for url in tqdm(df['link'], desc="Scraping Progress"):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')
                image_tag = soup.find('meta', property='og:image')

                if image_tag:
                    image_urls.append(image_tag['content'])
                else:
                    image_urls.append(None)

            except requests.RequestException as e:
                print(f"\nCould not fetch URL {url}: {e}")
                image_urls.append(None)
            except Exception as e:
                print(f"\nAn error occurred for URL {url}: {e}")
                image_urls.append(None)

        df['image_url'] = image_urls

    except FileNotFoundError:
        print(f"❌ Error: The file was not found at '{excel_path}'.")
        return False
    except Exception as e:
        print(f"❌ An error occurred while preparing the Excel file: {e}")
        return False

    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PROJECT_NAME = os.getenv('DB_PROJECT_NAME')

    if not all([DB_USERNAME, DB_PASSWORD, DB_PROJECT_NAME]):
        print("❌ Error: Database credentials not found in .env file.")
        return False

    connection_string = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_PROJECT_NAME}.0prwqib.mongodb.net/"
    client = None 

    try:
        client = MongoClient(connection_string)
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB Atlas. Error: {e}")
        return False

    try:
        db = client[db_name]
        collection = db[collection_name]
        
        data_to_insert = df.to_dict('records')

        if data_to_insert:
            collection.delete_many({})
            print(f"Cleared existing documents in '{collection_name}'.")
            
            result = collection.insert_many(data_to_insert)
            print(f"✅ Successfully inserted {len(result.inserted_ids)} documents into '{db_name}.{collection_name}'.")
        else:
            print("ℹ️ The DataFrame is empty. Nothing to insert.")
        
        return True

    except Exception as e:
        print(f"❌ An error occurred during data insertion: {e}")
        return False
    finally:
        if client:
            client.close()
            print("🔌 Connection to MongoDB closed.")

if __name__ == "__main__":
    load_dotenv() 

    EXCEL_FILE_PATH = 'src/database/AFNC_Opendata_export_20250819102926.xlsx'
    DATABASE_NAME = 'UDetectionNews'
    COLLECTION_NAME = 'LinkNews'

    success = load_excel_to_mongodb(
        excel_path=EXCEL_FILE_PATH,
        db_name=DATABASE_NAME,
        collection_name=COLLECTION_NAME
    )
