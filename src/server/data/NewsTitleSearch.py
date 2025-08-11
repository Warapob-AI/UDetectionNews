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
        print(f"เกิดข้อผิดพลาดในการดึงข้อมูลจาก URL: {url} - {e}")
        # หากดึงข้อมูลไม่ได้ ก็จะคืนค่าพื้นฐานที่ตั้งไว้ตอนแรก
        return metadata
    except Exception as e:
        print(f"เกิดข้อผิดพลาดที่ไม่คาดคิดระหว่างประมวลผล URL: {url} - {e}")
        return metadata


def NewsSearch(task: str):
    """
    ค้นหาข่าวโดยใช้ SERPER API, จากนั้นเข้าไปดึงข้อมูลจากแต่ละลิงก์
    และคืนค่าเป็น List ของ Dictionary ที่มี title, description, imageUrl, link
    """
    api_keys = [
        os.getenv('SERPER_API_KEY_1'),
        os.getenv('SERPER_API_KEY_2'),
        os.getenv('SERPER_API_KEY_3'),
        os.getenv('SERPER_API_KEY_4'),
        os.getenv('SERPER_API_KEY_5'),
        os.getenv('SERPER_API_KEY_6'),
        os.getenv('SERPER_API_KEY_7')
    ]

    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": f"{task}"})

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

            # --- ส่วนที่ปรับปรุงใหม่ ---
            # วนลูปเพื่อดึงข้อมูล metadata จากแต่ละลิงก์
            enriched_results = []
            # ประมวลผลแค่ 5 ลิงก์แรกเพื่อความรวดเร็ว (ปรับแก้ได้ตามต้องการ)
            for result in organic_results[:5]: 
                link = result.get('link')
                if link:
                    print(f"กำลังดึงข้อมูลจาก: {link}")
                    metadata = _scrape_website_metadata(link)
                    enriched_results.append(metadata)
            
            print(enriched_results)
            return enriched_results
            # --- จบส่วนที่ปรับปรุง ---

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

search = NewsSearch("กัมพูชางัด 'ข่าวปลอม' ถล่มไทย ทำลายภาพลักษณ์ตัวเองในเวทีโลก - มติชนสุดสัปดาห์")
print(search)
