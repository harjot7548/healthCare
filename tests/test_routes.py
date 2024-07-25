import unittest
from app import create_app

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_upload_audio(self):
        response = self.client.post('/uploads', data={
            'file': (open('tests/speech2.m4a', 'rb'), 'speech2.m4a')
        })
        self.assertEqual(response.status_code, 200)

    def test_transcription_summary(self):
        response = self.client.post('/transcription-summary', json={
            'transcribed_text': 'This is a test transcription.'
        })
        self.assertEqual(response.status_code, 200)

    def test_analyze_diseases(self):
        response = self.client.post('/analyze-diseases', json={
            'transcribed_text': 'This is a test transcription.'
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
