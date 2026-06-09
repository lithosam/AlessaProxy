    # Add this in server.py
    print(f"DEBUG: I see header 'x-api-key' as: {request.headers.get('x-api-key')}")

import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
    # Security check
    if request.headers.get("x-api-key") != os.environ.get("APP_SECRET_PASSWORD"):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    try:
        response = client.models.generate_content(
            model=data["model"],
            contents=data["contents"]
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
