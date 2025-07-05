import requests, os, json
from bs4 import BeautifulSoup
from store import get_user_data

def extract_pins(html, username):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith(f"/{username}/") and "/pin/" in href:
            full = "https://www.pinterest.com" + href
            if full not in links:
                links.append(full)
    return links

async def check_new_pins(user_id):
    ud = get_user_data(user_id)
    if not ud or not ud.get("cookie") or not ud.get("username"):
        return None
    headers = {"Cookie": ud["cookie"], "User-Agent": "Mozilla/5.0"}
    url = f"https://www.pinterest.com/{ud['username']}/saved/"
    r = requests.get(url, headers=headers, timeout=10)
    if "login" in r.url or r.status_code != 200:
        return f"❌ Invalid/expired cookie or can't access saved page for @{ud['username']}."
    new = extract_pins(r.text, ud["username"])
    os.makedirs("data", exist_ok=True)
    df = "data.json"
    if not os.path.exists(df):
        with open(df, "w") as f: json.dump({}, f)
    data = json.load(open(df))
    seen = data.get(str(user_id), [])
    fresh = [l for l in new if l not in seen]
    if fresh:
        data[str(user_id)] = new
        json.dump(data, open(df, "w"), indent=2)
        return "📌 New Pins:\n" + "\n".join(fresh[:5])
    return None
