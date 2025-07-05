import json, os

def _load():
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f: json.dump({}, f)
    with open("users.json", "r") as f:
        return json.load(f)

def _save(data):
    with open("users.json", "w") as f:
        json.dump(data, f, indent=2)

def save_user_cookie(user_id, cookie):
    data = _load()
    if str(user_id) not in data: data[str(user_id)] = {}
    data[str(user_id)]["cookie"] = cookie
    _save(data)

def save_target_user(user_id, username):
    data = _load()
    if str(user_id) not in data: data[str(user_id)] = {}
    data[str(user_id)]["username"] = username
    _save(data)

def get_user_data(user_id):
    data = _load()
    return data.get(str(user_id))
