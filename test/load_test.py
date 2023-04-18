from locust import HttpUser, task, between


class Testing(HttpUser):
    wait_time = between(1, 3)

    @task
    def predict_endpoint(self):
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

        self.client.post("/predict", json=input_data)
