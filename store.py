import os, json

def _load():
    if not os.path.exists("users.json"):
        json.dump({}, open("users.json","w"))
    return json.load(open("users.json"))

def _save(u):
    json.dump(u, open("users.json","w"), indent=2)

def save_user_cookie(uid, cookie):
    u = _load()
    u.setdefault(str(uid), {})["cookie"] = cookie
    _save(u)

def save_target_user(uid, username):
    u = _load()
    u.setdefault(str(uid), {})["username"] = username
    _save(u)

def get_user_data(uid):
    return _load().get(str(uid))
