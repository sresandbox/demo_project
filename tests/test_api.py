import multiprocessing
import time
import requests
import app

def run_server():
    # Start the Flask app (not via gunicorn) for test
    app.app.run(host="0.0.0.0", port=8080)

def test_octocat_gists():
    p = multiprocessing.Process(target=run_server)
    p.start()
    time.sleep(1) # give server a moment to start
    try:
        resp = requests.get("http://127.0.0.1:8080/octocat", timeout=10)
        assert resp.status_code == 200
        data = resp.json()
        assert "gists" in data
        assert isinstance(data["gists"], list)
    finally:
        p.terminate()
        p.join()