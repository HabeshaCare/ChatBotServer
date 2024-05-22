import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import requests
from src.DB import search_doctor
from src.LLM import generate, loadMessagesToMemory


def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/ask", methods=["POST", "HEAD"])
    def generate_response():
        if request.method == "POST":
            query = request.json.get("query", "")
            patient_history = request.json.get("history", [])

            if not any(char.isalpha() for char in query):
                # Query doesn't have any alpha characters
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "Question must contain alpha characters",
                        }
                    ),
                    400,
                )

            response, _ = generate(query, patient_history)
            data = {"Response": response}

            print(f"Sending back data")
            return jsonify(data)

        else:
            return jsonify({"success": True, "message": "Message received"})

    @app.route("/loadcontext", methods=["POST"])
    def load_context():
        if request.method == "POST":
            messages = request.json["messages"]
            loadMessagesToMemory(messages)
            return jsonify({"success": True})
        else:
            abort(502, "Unsupported request method")

    @app.route("/wake", methods=["GET", "HEAD"])
    def wake():
        return jsonify({"success": True})

    @app.route("/doctor/search", methods=["POST"])
    def search(query):
        return search_doctor(query)

    return app


app = create_app()
