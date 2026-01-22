#!/usr/bin/env python3
"""
tw.live 分類發現器
遍歷全站並收集所有監控點分類頁面
版本：2.0.1
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin


class TWLiveCategoryDiscoverer:
    def __init__(self):
        self.base_url = "https://tw.live"
        self.categories = {}
        self.endpoints = []  # 實際有監控點的終點頁面
        self.visited = set()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

    def fetch_page(self, url):
        """抓取頁面並處理錯誤"""
        if url in self.visited:
            return None
        self.visited.add(url)

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"❌ 抓取失敗 {url}: {e}")
            return None

    def extract_main_categories(self, html):
        """從主頁提取主要分類"""
        soup = BeautifulSoup(html, "html.parser")
        categories = {}

        # 從 nav-scroller 提取分類連結
        nav = soup.find("div", class_="nav-scroller")
        if nav:
            links = nav.find_all("a", class_="nav-link")
            for link in links:
                href = link.get("href")
                if href and not href.startswith("#"):
                    text = link.get_text(strip=True)
                    if text and href != "/":
                        categories[text] = urljoin(self.base_url, href)

        return categories

    def extract_menu_categories(self, html):
        """從頁面提取 cctv-menu 中的分類連結"""
        soup = BeautifulSoup(html, "html.parser")
        categories = []

        menus = soup.find_all("div", class_="cctv-menu")
        for menu in menus:
            links = menu.find_all("a")
            for link in links:
                href = link.get("href")
                if href and not href.startswith("#"):
                    text = link.get_text(strip=True)
                    if text:
                        full_url = urljoin(self.base_url, href)
                        categories.append((text, full_url))

        return categories

    def extract_button_categories(self, html):
        """從頁面提取按鈕類型的分類連結（用於國道等）"""
        soup = BeautifulSoup(html, "html.parser")
        categories = []

        buttons = soup.find_all("a", class_="btn")
        for btn in buttons:
            if btn.get_text(strip=True) == "即時影像":
                href = btn.get("href")
                if href:
                    # 從按鈕附近的文字提取名稱
                    container = btn.find_parent("div", class_="col-md-4")
                    if container:
                        h2 = container.find("h2")
                        if h2:
                            text = h2.get_text(strip=True)
                            full_url = urljoin(self.base_url, href)
                            categories.append((text, full_url))

        return categories

    def is_endpoint_page(self, html):
        """判斷頁面是否為終點頁面（有 cctv-stack）"""
        soup = BeautifulSoup(html, "html.parser")
        stacks = soup.find_all("div", class_="cctv-stack")
        return len(stacks) > 0

    def discover_categories(self):
        """發現所有分類"""
        print("🏠 抓取主頁...")
        html = self.fetch_page(self.base_url)
        if not html:
            return

        # 提取主要分類
        main_categories = self.extract_main_categories(html)
        print(f"📂 找到 {len(main_categories)} 個主要分類")

        all_categories = {}

        for name, url in main_categories.items():
            print(f"\n🗂️  處理分類: {name} ({url})")
            html = self.fetch_page(url)
            if not html:
                continue

            if self.is_endpoint_page(html):
                # 直接是終點頁面
                print(f"  ✅ 終點頁面: {url}")
                self.endpoints.append({"name": name, "url": url, "type": "direct"})
            else:
                # 總覽頁面，提取子分類
                sub_categories = self.extract_menu_categories(html)
                if not sub_categories:
                    sub_categories = self.extract_button_categories(html)
                print(f"  📋 找到 {len(sub_categories)} 個子分類")
                all_categories[name] = sub_categories

                # 檢查子分類是否為終點
                for sub_name, sub_url in sub_categories:
                    html = self.fetch_page(sub_url)
                    if html:
                        if self.is_endpoint_page(html):
                            print(f"    ✅ 終點頁面: {sub_name} ({sub_url})")
                            self.endpoints.append(
                                {
                                    "name": f"{name} - {sub_name}",
                                    "url": sub_url,
                                    "type": "sub",
                                    "parent": name,
                                }
                            )
                        else:
                            # 進一步檢查是否有子子分類
                            sub_sub = self.extract_menu_categories(html)
                            if sub_sub:
                                print(f"    📋 {sub_name} 有 {len(sub_sub)} 個子子分類")
                                for ss_name, ss_url in sub_sub[:3]:  # 只檢查前3個
                                    html_ss = self.fetch_page(ss_url)
                                    if html_ss and self.is_endpoint_page(html_ss):
                                        print(
                                            f"      ✅ 終點頁面: {ss_name} ({ss_url})"
                                        )
                                        self.endpoints.append(
                                            {
                                                "name": f"{name} - {sub_name} - {ss_name}",
                                                "url": ss_url,
                                                "type": "sub_sub",
                                                "parent": name,
                                                "sub_parent": sub_name,
                                            }
                                        )

            time.sleep(0.5)  # 避免過度請求

        self.categories = all_categories
        return all_categories

    def save_blueprint(self, filename="scraper_blueprint.json"):
        """儲存分類藍圖"""
        blueprint = {
            "categories": self.categories,
            "endpoints": self.endpoints,
            "metadata": {
                "total_categories": len(self.categories),
                "total_endpoints": len(self.endpoints),
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
                "source": "https://tw.live",
            },
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(blueprint, f, ensure_ascii=False, indent=2)

        print(f"\n✅ 分類藍圖已儲存: {filename}")
        print(f"📂 分類數: {len(self.categories)}")
        print(f"🎯 終點頁面數: {len(self.endpoints)}")

        return filename


def main():
    print("🔍 開始發現 tw.live 分類結構...")
    print("=" * 60)

    discoverer = TWLiveCategoryDiscoverer()
    categories = discoverer.discover_categories()
    discoverer.save_blueprint()

    # 顯示摘要
    print("\n📊 分類摘要:")
    print("=" * 60)
    for cat_name, subs in categories.items():
        print(f"  {cat_name}: {len(subs)} 個子分類")

    print("\n🎯 終點頁面摘要:")
    print("=" * 60)
    for endpoint in discoverer.endpoints[:10]:  # 只顯示前10個
        print(f"  {endpoint['name']} ({endpoint['url']})")
    if len(discoverer.endpoints) > 10:
        print(f"  ... 還有 {len(discoverer.endpoints) - 10} 個終點頁面")


if __name__ == "__main__":
    main()
