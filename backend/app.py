from flask import Flask
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


if __name__ == "__main__":
    app.run(debug=True)
