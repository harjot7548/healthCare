from flask import Blueprint, request, jsonify
import os
from .utils import transcribe_audio, summarize_text, analyze_for_diseases_and_tests, getTestsForDiseases

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'app/static/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

disease_analysis_store = []


@main.route('/')
def home():
    return "Welcome to the HealthCare Backend API!"


@main.route('/getSummary', methods=['POST'])
def upload_audio():
    global disease_analysis_store

    if 'audio' not in request.files:
        print("No file part in request")
        return jsonify({"error": "No file part"}), 400

    file = request.files['audio']
    if file.filename == '':
        print("No selected file")
        return jsonify({"error": "No selected file"}), 400

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        print(f"File saved to {file_path}")

        transcribed_text = transcribe_audio(file_path)
        print(f"Transcribed Text: {transcribed_text}")

        summary = summarize_text(transcribed_text)
        print(f"Summary: {summary}")

        raw_disease_analysis = analyze_for_diseases_and_tests(transcribed_text)

        # Correctly update the global variable
        disease_analysis_store = [{"id": i + 1, "name": disease} for i, disease in enumerate(raw_disease_analysis)]
        print(f"Disease Analysis: {disease_analysis_store}")

        return jsonify({
            "transcription": transcribed_text,
            "summary": summary,
            "disease_analysis": disease_analysis_store
        })


@main.route('/getPrescription/<int:disease_id>', methods=['GET'])
def tests_for_disease(disease_id):
    global disease_analysis_store

    disease = next((disease for disease in disease_analysis_store if disease["id"] == disease_id), None)

    if not disease:
        return jsonify({"error": "disease not found"}), 404

    tests = getTestsForDiseases(disease["name"])
    return jsonify({
        "disease": disease,
        "tests": tests
    })




@main.route('/submit-patient-info', methods=['POST'])
def submit_patient_info():
    data = request.get_json()
    # Process patient info
    return jsonify({"status": "Patient information submitted successfully"})


@main.route('/doctor-diagnosis', methods=['POST'])
def doctor_diagnosis():
    data = request.get_json()
    # Process doctor's diagnosis
    return jsonify({"status": "Doctor's diagnosis submitted successfully"})


@main.route('/generate-prescription', methods=['POST'])
def generate_prescription():
    data = request.get_json()
    # Generate and return prescription based on diagnosis and tests
    return jsonify({"prescription": "Prescription details..."})
