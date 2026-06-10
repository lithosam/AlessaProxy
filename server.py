import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)
# The client initializes here. If GEMINI_API_KEY is missing, it will fail.
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
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
    # This ensures it runs on the port Render provides
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

