from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)
app.config['DEBUG'] = True
load_dotenv()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/groups')
def groups():
    return render_template('groups.html')

@app.route('/channels')
def channels():
    return render_template('channels.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/helpcenter')
def helpcenter():
    return render_template('helpcenter.html')

@app.route('/changelog')
def changelog():
    return render_template('changelog.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')


# MEMBERSHIP CHECK

BOT_TOKEN = os.getenv("BOT_TOKEN")

GROUPS = {
    "-1003274034865": "Test GC 01",
    "@testgc02": "Test GC 02"
}

def get_user_by_id(user_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChat?chat_id={user_id}"
    r = requests.get(url).json()

    if r.get("ok"):
        return r["result"]
    return None
    

def check_membership(user_id):
    results = []
    for group_id, group_name in GROUPS.items():
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={group_id}&user_id={user_id}"
        r = requests.get(url).json()

        if not r.get("ok"):
            results.append({
                "group": group_name,
                "status": "Tidak dapat mengambil data"
            })
            continue

        status = r["result"]["status"]

        if status in ["member", "administrator", "creator"]:
            status_text = "Member"
        elif status == "kicked":
            status_text = "Banned"
        elif status == "restricted":
            status_text = "Muted"
        elif status == "left":
            status_text = "Already Left"
        else:
            status_text = "Not Joined"

        results.append({
            "group": group_name,
            "status": status_text
        })

    return results


@app.route("/membershipcheck", methods=["GET", "POST"])
def check():
    # Permintaan pertama kali (GET) → tampilkan halaman HTML
    if request.method == "GET":
        return render_template("membership.html")

    # Permintaan dari WebApp (POST) → proses cek membership
    data = request.get_json()
    user_id = data.get("user_id")

    user = get_user_by_id(user_id)
    membership_data = check_membership(user_id)

    return {
        "user_id": user_id,
        "full_name": user.get("first_name", "-"),
        "username": user.get("username", "-"),
        "membership_data": membership_data
    }

if __name__ == '__main__':
    app.run()