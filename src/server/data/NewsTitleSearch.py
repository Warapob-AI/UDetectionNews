import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()
from dotenv import load_dotenv
load_dotenv()
import requests
from bs4 import BeautifulSoup
import json
import os

def _scrape_website_metadata(url: str):
    """
    ฟังก์ชันเสริม: เข้าไปดึงข้อมูล title, description, และ image URL จากหน้าเว็บ
    โดยจะพยายามหาจาก OG (Open Graph) tags ก่อน แล้วค่อยหาจาก HTML tags ทั่วไป
    """
    metadata = {
        "title": "ไม่พบหัวข้อ",
        "description": "ไม่พบคำอธิบาย",
        "imageUrl": None,
        "link": url
    }
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')

        # --- หา Title ---
        og_title = soup.find("meta", property="og:title")
        if og_title:
            metadata["title"] = og_title.get("content")
        else:
            title_tag = soup.find("title")
            if title_tag:
                metadata["title"] = title_tag.string

        # --- หา Description ---
        og_description = soup.find("meta", property="og:description")
        if og_description:
            metadata["description"] = og_description.get("content")
        else:
            meta_description = soup.find("meta", attrs={"name": "description"})
            if meta_description:
                metadata["description"] = meta_description.get("content")

        # --- หา Image URL ---
        og_image = soup.find("meta", property="og:image")
        if og_image:
            metadata["imageUrl"] = og_image.get("content")

        return metadata

    except requests.exceptions.RequestException as e:
        # หากดึงข้อมูลไม่ได้ ก็จะคืนค่าพื้นฐานที่ตั้งไว้ตอนแรก
        return metadata
    except Exception as e:
        print(f"เกิดข้อผิดพลาดที่ไม่คาดคิดระหว่างประมวลผล URL: {url} - {e}")
        return metadata

def NewsSearch(task: str):
    """
    ค้นหาข่าวโดยใช้ SERPER API และดึงข้อมูล metadata จนกว่าจะได้ผลลัพธ์
    ที่สมบูรณ์ (มี title, description, imageUrl) ครบ 3 รายการแล้วจึงหยุด
    """
    api_keys = [
        os.getenv('SERPER_API_KEY_1'),
        os.getenv('SERPER_API_KEY_2'),
        os.getenv('SERPER_API_KEY_3'),
        os.getenv('SERPER_API_KEY_4'),
        os.getenv('SERPER_API_KEY_5'),
        os.getenv('SERPER_API_KEY_6'),
        os.getenv('SERPER_API_KEY_7'),
        os.getenv('SERPER_API_KEY_8'),
        os.getenv('SERPER_API_KEY_9'),
    ]

    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": f"{task}", "num": 30})

    for i, key in enumerate(api_keys):
        if not key:
            continue

        print(f"กำลังลองใช้ SERPER API Key #{i+1}...")

        headers = {
            'X-API-KEY': key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status()
            
            print(f"SERPER API Key #{i+1} ใช้งานได้สำเร็จ!")
            data = response.json()
            organic_results = data.get('organic', [])

            enriched_results = []
            
            # --- ✨ ส่วนที่ปรับแก้ลอจิก ---
            # วนลูปไปเรื่อยๆ ไม่จำกัดจำนวนลิงก์
            for result in organic_results: 
                link = result.get('link')
                if not link:
                    continue

                metadata = _scrape_website_metadata(link)
                
                # คัดกรองผลลัพธ์ที่ไม่สมบูรณ์ออก
                if (metadata.get('title') == 'ไม่พบหัวข้อ' or
                    metadata.get('description') == 'ไม่พบคำอธิบาย' or
                    metadata.get('imageUrl') is None):
                    continue

                # เพิ่มข้อมูลที่สมบูรณ์ลงในลิสต์
                enriched_results.append(metadata)
                
                # ตรวจสอบว่าได้ครบ 5 รายการแล้วหรือยัง?
                if len(enriched_results) >= 5:
                    print("\n*** ได้ผลลัพธ์ครบ 5 รายการแล้ว หยุดการค้นหา ***")
                    break # ถ้าครบแล้ว ให้ออกจาก for loop ทันที
            # --- จบส่วนที่ปรับแก้ ---
            
            print("\n--- ผลลัพธ์สุดท้าย (แบบสวยๆ) ---")
            print(json.dumps(enriched_results, indent=4, ensure_ascii=False))
            print("----------------------------------------\n")

            return enriched_results

        except requests.exceptions.HTTPError as e:
            if e.response.status_code in [401, 403]:
                print(f"API Key #{i+1} ใช้งานไม่ได้, กำลังลองคีย์ถัดไป...")
            else:
                print(f"เกิดข้อผิดพลาดร้ายแรงจากเซิร์ฟเวอร์: {e}")
                return {"error": f"เกิดข้อผิดพลาดจากเซิร์ฟเวอร์: {e}"}
        except Exception as e:
            print(f"เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")
            return {"error": f"เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}"}
            
    return {"error": "API Keys ทั้งหมดใช้งานไม่ได้"}

# --- การเรียกใช้งาน ---
task = "Ambatukam ช่วยตัวเองบนรถ"

search_results = NewsSearch(task)