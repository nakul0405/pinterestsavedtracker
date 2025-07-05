import requests
from bs4 import BeautifulSoup
import json
from store import get_user_data

def extract_pins(html, username):
    soup = BeautifulSoup(html, "html.parser")
    boards = soup.find_all("a", href=True)
    links = []
    for a in boards:
        href = a["href"]
        if href.startswith(f"/{username}/") and "/pin/" in href:
            links.append("https://www.pinterest.com" + href)
    return links

async def check_new_pins(user_id):
    user_data = get_user_data(user_id)
    if not user_data: return "⚠️ Please set cookie and target user."
    cookie = user_data["cookie"]
    username = user_data["username"]
    url = f"https://www.pinterest.com/{username}/saved/"
    headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
    except: return "❌ Failed to fetch data."
    if "login" in res.url: return "❌ Invalid or expired cookie."

    new_links = extract_pins(res.text, username)
    if not new_links: return "No saved pins found."

    if not os.path.exists("data.json"):
        with open("data.json", "w") as f: json.dump({}, f)

    with open("data.json", "r") as f:
        old_data = json.load(f)

    old_links = old_data.get(str(user_id), [])
    fresh_links = [l for l in new_links if l not in old_links]
    if fresh_links:
        old_data[str(user_id)] = new_links
        with open("data.json", "w") as f:
            json.dump(old_data, f, indent=2)
        return "📌 New Pins Saved:\n" + "\n".join(fresh_links[:5])
    else:
        return "No new pins found."
