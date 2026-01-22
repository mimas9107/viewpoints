#!/usr/bin/env python3
"""
tw.live 監控點抓取器 v2
基於分類藍圖的完整抓取
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from urllib.parse import urljoin


class TWLiveScraper2:
    def __init__(self):
        self.base_url = "https://tw.live"
        self.cameras = []
        self.seen_ids = set()
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

    def extract_camera_from_stack(self, stack, category_name):
        """從 cctv-stack 提取監控點資訊"""
        link = stack.find("a")
        if not link:
            return None

        camera_url = urljoin(self.base_url, link.get("href", ""))

        # 提取 camera ID
        match = re.search(r"id=([a-zA-Z0-9_-]+)", camera_url)
        if not match:
            return None

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
            "location": category_name,  # 預設使用分類名稱作為地點
            "url": camera_url,
            "thumbnail": thumbnail,
            "type": "image",  # 預設類型
            "imageUrl": thumbnail,  # 預設圖片網址
        }

        # 判斷類型（從縮圖 URL）
        if "youtube.com" in thumbnail:
            # YouTube 類型
            yt_id_match = re.search(r"/vi/([a-zA-Z0-9_-]+)/", thumbnail)
            if yt_id_match:
                camera["type"] = "youtube"
                camera["youtubeId"] = yt_id_match.group(1)
                camera["description"] = f"{category_name} YouTube 直播"
                # YouTube 不需要 imageUrl
                del camera["imageUrl"]
        elif thumbnail.startswith("https://tw.live/assets/thumbnail.png"):
            # 佔位符圖片，可能需要從詳細頁面提取 HLS
            hls_url = self.extract_hls_from_detail_page(camera_url)
            if hls_url:
                camera["type"] = "hls"
                camera["hlsUrl"] = hls_url
                # HLS 不需要 imageUrl
                del camera["imageUrl"]

        return camera

    def extract_hls_from_detail_page(self, detail_url):
        """從詳細頁面提取 HLS URL"""
        html = self.fetch_page(detail_url)
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")

        # 查找 HLS 來源
        source = soup.find("source", {"type": "application/x-mpegURL"})
        if source and source.get("src"):
            return source["src"]

        return None

    def scrape_endpoint_page(self, endpoint_info):
        """從終點頁面抓取所有監控點"""
        url = endpoint_info["url"]
        name = endpoint_info["name"]

        print(f"📹 抓取終點: {name}")
        html = self.fetch_page(url)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        cameras = []

        # 找到所有監控點連結
        cctv_stacks = soup.find_all("div", class_="cctv-stack")

        for stack in cctv_stacks:
            camera = self.extract_camera_from_stack(stack, name)
            if camera and camera["id"] not in self.seen_ids:
                cameras.append(camera)
                self.seen_ids.add(camera["id"])
                time.sleep(0.1)  # 短延遲

        print(f"  ✅ 找到 {len(cameras)} 個監控點")
        return cameras

    def load_blueprint(self, filename="scraper_blueprint.json"):
        """載入分類藍圖"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                blueprint = json.load(f)
            return blueprint
        except Exception as e:
            print(f"❌ 載入藍圖失敗: {e}")
            return None

    def scrape_from_blueprint(self):
        """從藍圖抓取所有監控點"""
        blueprint = self.load_blueprint()
        if not blueprint:
            return []

        endpoints = blueprint.get("endpoints", [])
        print(f"🎯 開始從 {len(endpoints)} 個終點頁面抓取監控點...")

        all_cameras = []

        # 測試只處理前 5 個終點
        for endpoint in endpoints[:5]:
            cameras = self.scrape_endpoint_page(endpoint)
            all_cameras.extend(cameras)
            time.sleep(0.5)  # 避免過度請求

        self.cameras = all_cameras
        return all_cameras

    def save_test_output(self, filename="testoutput.json"):
        """儲存測試輸出"""
        output = {
            "cameras": self.cameras,
            "metadata": {
                "totalCount": len(self.cameras),
                "lastUpdated": time.strftime("%Y-%m-%d %H:%M:%S"),
                "version": "2.0.0",
                "source": "https://tw.live",
                "method": "blueprint-based",
            },
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 測試輸出已儲存: {filename}")
        print(f"📊 總共 {len(self.cameras)} 個監控點")


def main():
    print("🚀 開始抓取 tw.live 監控點 (v2)...")
    print("=" * 60)

    scraper = TWLiveScraper2()
    cameras = scraper.scrape_from_blueprint()
    scraper.save_test_output()

    # 顯示樣本
    print("\n📋 樣本資料 (前 5 個):")
    print("=" * 60)
    for cam in cameras:
        print(json.dumps(cam, ensure_ascii=False, indent=2))
        print("-" * 40)


if __name__ == "__main__":
    main()
