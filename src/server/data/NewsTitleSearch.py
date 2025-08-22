import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()

def NewsSearch(task: str): 
    SEARCH_ENGINE_ID = os.getenv('search_engine_id')
    
    api_keys = [
        # 100 per day
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
    
    valid_api_keys = [key for key in api_keys if key]

    task_with_filter = f"{task} -site:wikipedia.org"
    
    for i, api_key in enumerate(valid_api_keys):
        print(f"--- Attempting with API Key #{i + 1} ---")
        
        try:
            url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={SEARCH_ENGINE_ID}&q={task_with_filter}"
            
            response = requests.get(url)
            # หากมีข้อผิดพลาด (เช่น 429 Quota Exceeded) บรรทัดนี้จะโยน exception
            response.raise_for_status()
            
            print(f"API Key #{i + 1} successful!")
            search_results = response.json()
            results_list = []
            
            if "items" in search_results:
                for item in search_results.get("items", []):
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
            
            print(results_list)
            return results_list
            
        except requests.exceptions.HTTPError as err:
            print(f"API Key #{i + 1} failed: {err}. Trying next key...")
        
        except Exception as e:
            print(f"An unexpected error occurred with Key #{i + 1}: {e}. Trying next key...")
            
    print("All API keys failed.")
    return json.dumps([], indent=4, ensure_ascii=False) # return เป็น JSON array ว่าง


NewsSearch("ทำเนียบขาวมีบัญชี  TikTok แล้ว ต่อต้านไม่ได้ก็เข้าร่วม ! ทำเนียบขาวสมัครบัญชี TikTok เลื่อนการแบนออกไป ให้มีเวลาขายธุรกิจให้สหรัฐ") 