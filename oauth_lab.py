from flask import Flask, redirect, request
import requests, json, os

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

app = Flask(__name__)

@app.route("/")
def index():
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=https://mail.google.com/ https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/userinfo.email"
        f"&access_type=offline&prompt=consent"
    )

    return f'''
    <html>
    <head>
    <style>
    .login-btn {{
        display: inline-flex;
        align-items: center;
        background-color: white;
        color: #444;
        border: 1px solid #ccc;
        padding: 10px 20px;
        font-size: 16px;
        font-family: Arial, sans-serif;
        text-decoration: none;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}
    .login-btn:hover {{
        background-color: #f5f5f5;
    }}
    .login-btn img {{
        height: 20px;
        margin-right: 10px;
    }}
    body {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: #f0f2f5;
    }}
    </style>
    </head>
    <body>
        <a class="login-btn" href="{auth_url}">
            <img src="https://developers.google.com/identity/images/g-logo.png" alt="Google Logo">
            Login with Google
        </a>
    </body>
    </html>
    '''

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    r = requests.post(token_url, data=data)
    tokens = r.json()

    print("TOKENS:", json.dumps(tokens, indent=2))

    with open("tokens.json", "w") as f:
        json.dump(tokens, f, indent=2)

    return f"<pre>{json.dumps(tokens, indent=2)}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
