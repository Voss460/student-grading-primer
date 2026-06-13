from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)


@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    students = db.get_all_students()
    return jsonify(students), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    student_data = request.json
    if not student_data:
        return jsonify({"error": "No data provided"}), 404

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark", 0)

    if not name or not course:
        return jsonify({"error": "Name and course are required"}), 404

    if not isinstance(mark, int) or mark < 0 or mark > 100:
        return jsonify({"error": "Mark must be an integer between 0 and 100"}), 404

    student = db.insert_student(name, course, mark)
    return jsonify(student), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    student_data = request.json
    if not student_data:
        return jsonify({"error": "No data provided"}), 404

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark")

    if mark is not None and (not isinstance(mark, int) or mark < 0 or mark > 100):
        return jsonify({"error": "Mark must be an integer between 0 and 100"}), 404

    student = db.update_student(student_id, name=name, course=course, mark=mark)
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    result = db.delete_student(student_id)
    if result is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(result), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()
    marks = [s["mark"] for s in students if s["mark"] is not None]

    if not marks:
        return jsonify({"count": 0, "average": None, "min": None, "max": None}), 200

    return jsonify({
        "count": len(marks),
        "average": sum(marks) / len(marks),
        "min": min(marks),
        "max": max(marks)
    }), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
