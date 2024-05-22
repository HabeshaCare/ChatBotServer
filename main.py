import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from src.DB import (
    create_doctor,
    delete_doctor,
    reset_database,
    search_doctor,
    update_doctor,
)
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
    def search():
        if "query" not in request.json:
            response = jsonify(
                {
                    "success": False,
                    "message": "Please make sure to add query parameter",
                    "statusCode": 400,
                    "data": None,
                    "errors": ["Missing query to search"],
                }
            )
            return response, 400
        query = request.json.get("query")
        return search_doctor(query)

    @app.route("/doctor/", methods=["POST"])
    def add_doctor():
        if "doctor" not in request.json:
            response = jsonify(
                {
                    "success": False,
                    "message": "Doctor data not provided",
                    "statusCode": 400,
                    "data": None,
                    "errors": ["Missing doctor to add"],
                }
            )
            return response, 400

        doctor = request.json.get("doctor")
        return create_doctor(doctor)

    @app.route("/doctor/<string:doctor_id>", methods=["PUT", "DELETE"])
    def doctor(doctor_id):
        if request.method == "PUT":
            if "doctor" not in request.json:
                response = jsonify(
                    {
                        "success": False,
                        "message": "Doctor data not provided",
                        "statusCode": 400,
                        "data": None,
                        "errors": ["Missing doctor data to update"],
                    }
                )
            if not doctor_id:
                response = {
                    "success": False,
                    "message": "Doctor id not provided",
                    "statusCode": 400,
                    "data": None,
                    "errors": ["Missing doctor_id to update"],
                }

                return jsonify(response), 400
            updated_doctor = request.json.get("doctor")
            return update_doctor(doctor_id, updated_doctor)
        elif request.method == "DELETE":
            if not doctor_id:
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "Doctor id not provided",
                            "statusCode": 400,
                            "data": None,
                            "errors": ["Missing doctor_id to delete"],
                        }
                    ),
                    400,
                )
            return delete_doctor(doctor_id)
        else:
            abort(502, "Unsupported request method")

    @app.route("/doctor/reset")
    def reset():
        return reset_database()

    return app


app = create_app()
