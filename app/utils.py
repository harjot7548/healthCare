import time
import whisper
import openai

# Load the Whisper model
model = whisper.load_model("base")

# Set your OpenAI API key
openai.api_key = "sk-proj-yvJiXyFlAmv2X1VEsCPtT3BlbkFJm7vAO1324yTnTSJOeBgC"


def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]


def summarize_text(text, retries=5, delay=5):
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user",
                     "content": f"Summarize the following text highlighting the key points and symptoms of the patient that are mentioned in the conversation:\n\n{text}"}
                ],
                max_tokens=100,
                temperature=0.7,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            summary = response.choices[0].message["content"].strip()
            return summary
        except Exception as e:
            if attempt < retries - 1:
                print(f"Error occurred: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise


def analyze_for_diseases_and_tests(text, retries=5, delay=5):
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful medical assistant."},
                    {"role": "user",
                     "content": f"Based on the following medical transcription, i just want the list of the possible diseases and i just want the list of diseases and nothing else in the output according to the transcription the diseases should be in bullet points:\n\n{text}"}
                ],
                max_tokens=200,
                temperature=0.7,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            analysis = response.choices[0].message["content"].strip()

            diseases = [disease.strip() for disease in analysis.split('\n') if disease.strip()]
            return diseases
        except Exception as e:
            if attempt < retries - 1:
                print(f"error occured: {e}. retrying in {delay} seconds..")
                time.sleep(delay)


def getTestsForDiseases(disease, retries=5, delay=5):
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "you are a helpful medical assistant."},
                    {"role": "user",
                     "content": f"list the possible tests required for diagnosing the following disease put the possible tests in bullet points not numbers:\n\n{disease}"}
                ],
                max_tokens=200,
                temperature=0.7,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            tests = response.choices[0].message["content"].strip()
            test_list = [test.strip() for test in tests.split('\n') if test.strip()]
            return test_list

        except Exception as e:
            if attempt < retries - 1:
                print(f"Error occurred: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise
