"""
app.py  —  NUST FAQ Chatbot Server
Run from project root:  python app.py
Browser opens automatically at http://localhost:5000
"""

import sys
import os
import webbrowser
import threading
import time

# Make src/ importable when running from root
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from flask import Flask, request, jsonify, send_from_directory
from chatbot import ask_bot

app = Flask(__name__, static_folder=".")


@app.route("/")
def index():
    return send_from_directory(".", "chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    if not data or not data.get("message", "").strip():
        return jsonify({"error": "Empty message"}), 400
    try:
        reply = ask_bot(data["message"].strip())
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"⚠️ Server error: {str(e)}"}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok", "offline": True})


def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://localhost:5000")


if __name__ == "__main__":
    print("\n" + "─" * 50)
    print("  NUST FAQ Chatbot  —  Starting up...")
    print("  URL : http://localhost:5000")
    print("  Stop: Ctrl+C")
    print("─" * 50 + "\n")
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
