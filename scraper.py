import requests
from bs4 import BeautifulSoup
import re
import json
import os

def load_cookies():
    try:
        with open("cookies.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print("⚠️ Failed to load cookies.json:", e)
        return {}

def get_latest_pin(username, cookie=None):
    url = f"https://www.pinterest.com/{username}/_saved/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    cookies = load_cookies()  # load full cookies from cookies.json

    # If a specific _pinterest_sess cookie is passed (e.g. via bot), override it
    if cookie:
        cookies["_pinterest_sess"] = cookie

    try:
        print(f"🔍 Scraping {username} with cookie: {url}")
        res = requests.get(url, headers=headers, cookies=cookies, timeout=10)

        if res.status_code == 403 or "login" in res.url:
            print("❌ Invalid or expired cookie – login required.")
            return {"error": "invalid_cookie"}

        if res.status_code != 200:
            print(f"❌ Request failed: {res.status_code}")
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        scripts = soup.find_all("script")

        for script in scripts:
            if "pinimg.com/originals" in script.text:
                match = re.search(r'https://i\.pinimg\.com/originals/[^"]+', script.text)
                if match:
                    image_url = match.group(0)
                    return {
                        "image": image_url,
                        "title": "Pinterest Pin",
                        "link": url
                    }

        print("⚠️ No image pin found")
        return None

    except Exception as e:
        print(f"❌ Scraper error:", e)
        return None
