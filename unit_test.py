import json
import unittest

from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_health(self):
        response = self.app.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Welcome to Rossmann Sales API!!")

    def test_predict(self):
        input_data = {
            "Store": 1111,
            "DayOfWeek": 4,
            "Date": "2014-07-10",
            "Customers": 4100,
            "Open": 1,
            "Promo": 1,
            "StateHoliday": "a",
            "SchoolHoliday": 1,
        }
        input_json = json.dumps(input_data)
        response = self.app.post(
            "/predict", data=input_json, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.data)
        self.assertIn("sales", response_json)
        self.assertIsInstance(response_json["sales"], float)


if __name__ == "__main__":
    unittest.main()
