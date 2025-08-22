import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()
from NewsTitleCheck import NewsCheck

def NewsSearch(task: str): 
    SEARCH_ENGINE_ID = os.getenv('search_engine_id')
    
    api_keys = [
        os.getenv('GOOGLE_SEARCH_API_KEY_1'),
        os.getenv('GOOGLE_SEARCH_API_KEY_2'),
        os.getenv('GOOGLE_SEARCH_API_KEY_3'),
        os.getenv('GOOGLE_SEARCH_API_KEY_4'),
        os.getenv('GOOGLE_SEARCH_API_KEY_5'),
        os.getenv('GOOGLE_SEARCH_API_KEY_6'),
        os.getenv('GOOGLE_SEARCH_API_KEY_7'),
        os.getenv('GOOGLE_SEARCH_API_KEY_8'),
        os.getenv('GOOGLE_SEARCH_API_KEY_9'),
        os.getenv('GOOGLE_SEARCH_API_KEY_10'),
        os.getenv('GOOGLE_SEARCH_API_KEY_11'),
        os.getenv('GOOGLE_SEARCH_API_KEY_12'),
        os.getenv('GOOGLE_SEARCH_API_KEY_13'),
        os.getenv('GOOGLE_SEARCH_API_KEY_14'),
        os.getenv('GOOGLE_SEARCH_API_KEY_15'),
        os.getenv('GOOGLE_SEARCH_API_KEY_16'),
        os.getenv('GOOGLE_SEARCH_API_KEY_17'),
        os.getenv('GOOGLE_SEARCH_API_KEY_18'),
        os.getenv('GOOGLE_SEARCH_API_KEY_19'),
        os.getenv('GOOGLE_SEARCH_API_KEY_20'),
        os.getenv('GOOGLE_SEARCH_API_KEY_21'),
        os.getenv('GOOGLE_SEARCH_API_KEY_22'),
        os.getenv('GOOGLE_SEARCH_API_KEY_23'),
        os.getenv('GOOGLE_SEARCH_API_KEY_24'),
        os.getenv('GOOGLE_SEARCH_API_KEY_25'),
        os.getenv('GOOGLE_SEARCH_API_KEY_26'),
        os.getenv('GOOGLE_SEARCH_API_KEY_27'),
        os.getenv('GOOGLE_SEARCH_API_KEY_28'),
        os.getenv('GOOGLE_SEARCH_API_KEY_29'),
        os.getenv('GOOGLE_SEARCH_API_KEY_30')
    ]
    
    # กรองเอาเฉพาะ Key ที่มีค่า (ไม่เป็น None) ออกมาใช้งาน
    valid_api_keys = [key for key in api_keys if key]

    task_with_filter = f"{task} -site:wikipedia.org"
    
    # 🔄 วนลูปเพื่อลองใช้ API Key แต่ละอัน
    for i, api_key in enumerate(valid_api_keys):
        print(f"--- Attempting with API Key #{i + 1} ---")
        
        try:
            url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={SEARCH_ENGINE_ID}&q={task_with_filter}"
            
            response = requests.get(url)
            # หากมีข้อผิดพลาด (เช่น 429 Quota Exceeded) บรรทัดนี้จะโยน exception
            response.raise_for_status()

            # ✅ ถ้าโค้ดทำงานมาถึงตรงนี้ได้ หมายความว่า "สำเร็จ"
            print(f"API Key #{i + 1} successful!")
            search_results = response.json()
            results_list = []
            
            if "items" in search_results:
                for item in search_results.get("items", []):
                    print(item)
                    title = item.get("title")
                    link = item.get("link")
                    snippet = item.get("snippet")
                    
                    image_url = None
                    if 'pagemap' in item and 'cse_image' in item.get('pagemap', {}) and len(item['pagemap']['cse_image']) > 0:
                        image_url = item['pagemap']['cse_image'][0].get('src')
                    
                    if image_url is None: 
                        continue

                    result_item = {
                        "title": title,
                        "description": snippet,
                        "imageUrl": image_url,
                        "link": link
                    }
                    results_list.append(result_item)
            
            json_output = json.dumps(results_list, indent=4, ensure_ascii=False)
            
            print(json_output)
            # เมื่อสำเร็จแล้วให้ return ผลลัพธ์และออกจากฟังก์ชันทันที
            return json_output
            
        except requests.exceptions.HTTPError as err:
            # ❌ ถ้าล้มเหลว (เช่นโควต้าหมด) จะเข้ามาทำงานในส่วนนี้
            print(f"API Key #{i + 1} failed: {err}. Trying next key...")
            # Loop จะทำงานต่อไปเพื่อลอง Key อันถัดไปโดยอัตโนมัติ
        
        except Exception as e:
            print(f"An unexpected error occurred with Key #{i + 1}: {e}. Trying next key...")

    # ถ้าวนลูปจนจบแล้วยังไม่สำเร็จเลย (ทุก Key ใช้ไม่ได้)
    print("All API keys failed.")
    return json.dumps([], indent=4, ensure_ascii=False) # return เป็น JSON array ว่าง

# --- การเรียกใช้งาน ---
task = "สำนักงานคณะกรรมการกำกับหลักทรัพย์และตลาดหลักทรัพย์ เปิดเว็บไซต์ใหม่"

search_results = NewsSearch(task)
NewsCheck(task, search_results)