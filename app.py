from flask import Flask, jsonify, Response
import requests
import os
# from functools import lru_cache


app = Flask(__name__)
GITHUB_API = "https://api.github.com"


# @lru_cache(maxsize=128)
def fetch_gists(username):
    url = f"{GITHUB_API}/users/{username}/gists"
    headers = {}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return [
        {
            "id": g.get("id"),
            "html_url": g.get("html_url"),
            "description": g.get("description"),
            "files": list(g.get("files", {}).keys()),
            "created_at": g.get("created_at"),
        }
        for g in data
    ]


@app.route("/<username>", methods=["GET"])
def get_gists(username):
    try:
        gists = fetch_gists(username)
        return jsonify({"user": username, "count": len(gists), "gists": gists})
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else 502
        return jsonify({"error": "GitHub API error", "details": str(e)}), status
    except Exception as e:
        return jsonify({"error": "internal error", "details": str(e)}), 500


@app.route("/", methods=["GET"])
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome to the GitHub Gist API!</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(120deg, #f8fafc 0%, #e0e7ef 100%);
                margin: 0;
                padding: 0;
                min-height: 100vh;
            }
            .container {
                max-width: 600px;
                margin: 60px auto;
                background: #fff;
                border-radius: 16px;
                box-shadow: 0 4px 24px rgba(0,0,0,0.08);
                padding: 40px 32px 32px 32px;
            }
            h1 {
                color: #2d3748;
                margin-bottom: 8px;
            }
            p {
                color: #4a5568;
            }
            form {
                margin: 24px 0;
                display: flex;
                gap: 8px;
            }
            input[type="text"] {
                flex: 1;
                padding: 10px 12px;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                font-size: 1rem;
            }
            button {
                background: #2563eb;
                color: #fff;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 1rem;
                cursor: pointer;
                transition: background 0.2s;
            }
            button:hover {
                background: #1e40af;
            }
            .gist-list {
                margin-top: 24px;
            }
            .gist {
                background: #f1f5f9;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 16px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            }
            .gist a {
                color: #2563eb;
                text-decoration: none;
                font-weight: 500;
            }
            .gist small {
                color: #64748b;
            }
            .error {
                color: #dc2626;
                margin-top: 16px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the GitHub Gist API!</h1>
            <h3>(This API allows you to fetch public gists for any GitHub user.</h3>
            <p>Enter a GitHub username to fetch their public gists:</p>
            <form id="gistForm" onsubmit="return fetchGists();">
                <input type="text" id="username" placeholder="e.g. octocat" required>
                <button type="submit">Fetch Gists</button>
            </form>
            <div id="result"></div>
            <div style="margin-top:32px;">
                <h3>API Usage</h3>
                <ul>
                    <li>GET <code>/&lt;github-username&gt;</code></li>
                </ul>
                <p><strong>Example:</strong> <a href="/octocat">/octocat</a></p>
            </div>
        </div>
        <script>
            function fetchGists() {
                const username = document.getElementById('username').value.trim();
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = '';
                if (!username) return false;
                resultDiv.innerHTML = '<p>Loading...</p>';
                fetch('/' + encodeURIComponent(username))
                    .then(res => res.json())
                    .then(data => {
                        if (data.error) {
                            resultDiv.innerHTML = '<div class="error"><strong>Error:</strong> ' + data.details + '</div>';
                        } else if (data.gists && data.gists.length > 0) {
                            let html = '<div class="gist-list">';
                            data.gists.forEach(gist => {
                                html += `<div class="gist">
                                    <a href="${gist.html_url}" target="_blank">${gist.description || '(No description)'}</a><br>
                                    <small>Files: ${gist.files.join(', ')}</small><br>
                                    <small>Created: ${new Date(gist.created_at).toLocaleString()}</small>
                                </div>`;
                            });
                            html += '</div>';
                            resultDiv.innerHTML = html;
                        } else {
                            resultDiv.innerHTML = '<div class="gist-list"><em>No gists found for this user.</em></div>';
                        }
                    })
                    .catch(err => {
                        resultDiv.innerHTML = '<div class="error"><strong>Error:</strong> Could not fetch gists.</div>';
                    });
                return false; // Prevent form submit
            }
        </script>
    </body>
    </html>
    """
    return Response(html, mimetype="text/html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))