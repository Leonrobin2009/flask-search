from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SERPAPI_KEY = "d6cd1205e4db34500a172a94978a1a6cf789b39620adb07090f9aabc4dcb2c97"  # replace with your key

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    serp_url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "hl": "en",
        "gl": "in",
        "num": 1
    }

    response = requests.get(serp_url, params=params)
    result = response.json()

    answer = None
    if "answer_box" in result:
        answer = result["answer_box"].get("answer") or result["answer_box"].get("snippet")
    if not answer and "organic_results" in result:
        first = result["organic_results"][0]
        answer = first.get("snippet") or f"{first.get('title')}\n{first.get('link')}"

    return jsonify({"result": answer or "No result found."})

# Host config
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
