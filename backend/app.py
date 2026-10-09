from flask import Flask, request, jsonify
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


@app.route("/")
def home():
    return "Research Opportunity Portal API is running"


@app.route("/test-db")
def test_db():
    connection = get_db_connection()
    connection.close()

    return "Database connection successful"


@app.route("/api/opportunities", methods=["POST"])
def create_opportunity():
    data = request.get_json()

    required_fields = [
        "title",
        "description",
        "research_area",
        "faculty_name",
        "department",
        "required_skills",
        "available_positions",
        "application_deadline",
        "status"
    ]

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    for field in required_fields:
        if field not in data or data[field] == "":
            return jsonify({"error": f"{field} is required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO research_opportunities
        (
            title,
            description,
            research_area,
            faculty_name,
            department,
            required_skills,
            available_positions,
            application_deadline,
            status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data["title"],
        data["description"],
        data["research_area"],
        data["faculty_name"],
        data["department"],
        data["required_skills"],
        data["available_positions"],
        data["application_deadline"],
        data["status"]
    )

    cursor.execute(query, values)
    connection.commit()

    opportunity_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Research opportunity created successfully",
        "id": opportunity_id
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
