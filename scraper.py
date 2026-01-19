#!/usr/bin/env python3
"""
tw.live 監控點爬蟲程式
爬取全站監控點資訊並建立資料庫
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from urllib.parse import urljoin
from datetime import datetime


class TWLiveScraper:
    def __init__(self):
        self.base_url = "https://tw.live"
        self.cameras = []
        self.categories = {}
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

    def fetch_page(self, url):
        """抓取頁面並處理錯誤"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"❌ 抓取失敗 {url}: {e}")
            return None

    def extract_youtube_id(self, html):
        """從 HTML 提取 YouTube ID"""
        patterns = [
            r"youtube\.com/embed/([a-zA-Z0-9_-]+)",
            r"youtube\.com/vi/([a-zA-Z0-9_-]+)",
            r"img\.youtube\.com/vi/([a-zA-Z0-9_-]+)",
            r'youtubeId[\'"]?\s*[:=]\s*[\'"]([a-zA-Z0-9_-]+)[\'"]',
        ]
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                return match.group(1)
        return None

    def extract_hls_url(self, html):
        """從 HTML 提取 HLS URL"""
        pattern = r'(https?://[^\s"\']+\.m3u8[^\s"\']*)'
        match = re.search(pattern, html)
        if match:
            return match.group(1)
        return None

    def extract_static_image_url(self, html):
        """從 HTML 提取靜態圖片 URL"""
        patterns = [
            r'(https?://cctv[^\s"\']+\.(?:jpg|jpeg|png))',
            r'(https?://[^\s"\']+/abs2jpg\.php[^\s"\']*)',
        ]
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                return match.group(1)
        return None

    def scrape_camera_detail(self, camera_url, camera_id):
        """爬取單個監控點詳細資訊"""
        print(f"  📹 抓取: {camera_id}")
        html = self.fetch_page(camera_url)
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")

        # 提取基本資訊
        camera = {"id": camera_id, "url": camera_url}

        # 提取標題
        h1 = soup.find("h1")
        if h1:
            camera["name"] = h1.text.strip().replace("即時影像", "").strip()

        # 提取描述
        h2 = soup.find("h2")
        if h2:
            camera["description"] = h2.text.strip()

        # 提取影像來源
        figcaption = soup.find("figcaption")
        if figcaption:
            source_link = figcaption.find("a")
            if source_link:
                camera["source"] = source_link.text.strip()

        # 判斷監控類型
        youtube_id = self.extract_youtube_id(html)
        if youtube_id:
            camera["type"] = "youtube"
            camera["youtubeId"] = youtube_id
        else:
            hls_url = self.extract_hls_url(html)
            if hls_url:
                camera["type"] = "hls"
                camera["hlsUrl"] = hls_url
            else:
                image_url = self.extract_static_image_url(html)
                if image_url:
                    camera["type"] = "image"
                    camera["imageUrl"] = image_url
                else:
                    camera["type"] = "unknown"

        return camera

    def scrape_category_page(self, category_url, category_name):
        """爬取分類頁面的所有監控點"""
        print(f"🗂️  抓取分類: {category_name}")
        html = self.fetch_page(category_url)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        cameras = []

        # 找到所有監控點連結
        cctv_stacks = soup.find_all("div", class_="cctv-stack")

        for stack in cctv_stacks:
            link = stack.find("a")
            if not link:
                continue

            camera_url = urljoin(self.base_url, link.get("href", ""))

            # 提取 camera ID
            match = re.search(r"id=([a-zA-Z0-9_-]+)", camera_url)
            if not match:
                continue

            camera_id = match.group(1)

            # 提取名稱（從縮圖頁面）
            name_tag = stack.find("p")
            name = name_tag.text.strip() if name_tag else "未知監控點"

            # 提取縮圖 URL
            img = stack.find("img")
            thumbnail = img.get("data-src", "") if img else ""

            # 建立基本資料
            camera = {
                "id": camera_id,
                "name": name,
                "category": category_name,
                "url": camera_url,
                "thumbnail": thumbnail,
            }

            # 判斷類型（從縮圖 URL）
            if "youtube.com" in thumbnail:
                # YouTube 類型
                yt_id_match = re.search(r"/vi/([a-zA-Z0-9_-]+)/", thumbnail)
                if yt_id_match:
                    camera["type"] = "youtube"
                    camera["youtubeId"] = yt_id_match.group(1)
                    camera["description"] = f"{category_name} YouTube 直播"

            cameras.append(camera)

            # 避免過度請求
            time.sleep(0.5)

        print(f"  ✅ 找到 {len(cameras)} 個監控點")
        return cameras

    def scrape_all_categories(self):
        """爬取所有主要分類"""
        categories = {
            "國道": [
                ("/national-highway/1/", "國道一號"),
                ("/national-highway/3/", "國道三號"),
                ("/national-highway/5/", "國道五號"),
            ],
            "景點": [
                ("/yms/", "陽明山"),
                ("/hhs/", "合歡山"),
                ("/np/sheipa/", "雪霸國家公園"),
                ("/np/alishan/", "阿里山"),
                ("/sunmoonlake/", "日月潭"),
            ],
            "市區": [
                ("/city/taipeicity/", "台北市"),
                ("/city/newtaipeicity/", "新北市"),
                ("/city/taichungcity/", "台中市"),
                ("/city/tainancity/", "台南市"),
                ("/city/kaohsiungcity/", "高雄市"),
            ],
            "省道": [
                ("/beiyi/", "北宜公路"),
                ("/provincial-highway/suhua/", "蘇花改"),
                ("/provincial-highway/newtaipei/", "新北市省道"),
            ],
            "快速道路": [
                ("/provincial-highway/64/", "台64線"),
                ("/provincial-highway/61/", "台61線"),
                ("/provincial-highway/66/", "台66線"),
            ],
        }

        all_cameras = []

        for cat_name, urls in categories.items():
            self.categories[cat_name] = []

            for url, sub_name in urls:
                full_url = urljoin(self.base_url, url)
                cameras = self.scrape_category_page(full_url, sub_name)

                all_cameras.extend(cameras)
                self.categories[cat_name].extend(cameras)

                # 避免過度請求
                time.sleep(1)

        self.cameras = all_cameras
        return all_cameras

    def save_database(self, filename="cameras_database.json"):
        """儲存資料庫"""
        database = {
            "cameras": self.cameras,
            "categories": self.categories,
            "metadata": {
                "totalCount": len(self.cameras),
                "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version": "1.0.0",
                "source": "https://tw.live",
            },
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(database, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 資料庫已儲存: {filename}")
        print(f"📊 總共 {len(self.cameras)} 個監控點")
        print(f"📁 分類數: {len(self.categories)}")

        return filename


def main():
    print("🚀 開始爬取 tw.live 監控點資料...")
    print("=" * 60)

    scraper = TWLiveScraper()

    # 爬取所有分類
    cameras = scraper.scrape_all_categories()

    # 儲存資料庫
    scraper.save_database()

    # 顯示統計資訊
    print("\n📈 統計資訊:")
    print("=" * 60)
    for cat_name, cams in scraper.categories.items():
        print(f"  {cat_name}: {len(cams)} 個")

    # 顯示樣本
    print("\n📋 樣本資料 (前 3 個):")
    print("=" * 60)
    for cam in cameras[:3]:
        print(json.dumps(cam, ensure_ascii=False, indent=2))
        print("-" * 40)


if __name__ == "__main__":
    main()
