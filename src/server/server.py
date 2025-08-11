from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

from data.NewsWebsiteTitle import NewsWebsiteTitle 
from data.NewsTitleSearch import NewsSearch 
from data.NewsTitleCheck import NewsCheck 

app = FastAPI(title="Fastapi is Running ..")

from fastapi.middleware.cors import CORSMiddleware  # 👈 1. Import

# 👇 2. กำหนด Origins ที่อนุญาต
origins = [
    "http://localhost",
    "http://localhost:5173",  #  <-- ใส่ Port ของ React ของคุณที่นี่
    "http://localhost:3000",
    # ใส่ URL ของ frontend อื่นๆ ที่ต้องการอนุญาต
]

# 👇 3. เพิ่ม CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # อนุญาตทุก Methods (GET, POST, etc.)
    allow_headers=["*"],
)


# =======================================================
# News Website Title
# =======================================================
class NewsWebsiteTitleRequest(BaseModel):
    url: str

@app.post("/production/news-website-title")
async def news_website_title(request: NewsWebsiteTitleRequest):
    newsWebsiteTitle = NewsWebsiteTitle(url = request.url)
    return newsWebsiteTitle 

# =======================================================
# News Title Search 
# =======================================================
class NewsTitleSearchRequest(BaseModel):
    task: str

@app.post("/production/news-title-search")
async def news_title_search(request: NewsTitleSearchRequest):
    newsSearch = NewsSearch(task = request.task)
    return newsSearch 

# =======================================================
# News Title Check 
# =======================================================
class NewsTitleCheckRequest(BaseModel):
    task: str
    search: str

@app.post("/production/news-title-check")
async def news_title_check(request: NewsTitleCheckRequest):
    newsCheck = NewsCheck(task = request.task, search = request.search)
    return newsCheck

