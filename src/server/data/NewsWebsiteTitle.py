from selenium import webdriver
from selenium.webdriver.common.by import By # ◀️ เพิ่ม import
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def NewsWebsiteTitle(url: str) -> str:
    """
    ดึง Title ของหน้าเว็บโดยใช้ Selenium เพื่อควบคุมเบราว์เซอร์จริง
    สามารถผ่านระบบป้องกันที่ใช้ JavaScript ได้
    """
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.1 Safari/537.36")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        
        print(f"กำลังใช้ Selenium เข้าไปยัง: {url}")
        driver.get(url)

        # --- จุดที่แก้ไข ---
        # รอให้หน้าเว็บโหลดจนมี tag <body> ปรากฏขึ้นมา (รอสูงสุด 15 วินาที)
        print("กำลังรอให้หน้าเว็บโหลดสมบูรณ์...")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # --- ดึง Title ออกมา ---
        title = driver.title
        print("ดึง Title สำเร็จ!")
        return title.strip()

    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการทำงานของ Selenium: {e}")
        return f"เกิดข้อผิดพลาดจาก Selenium: {e}"
        
    finally:
        if driver:
            print("กำลังปิดเบราว์เซอร์...")
            driver.quit()