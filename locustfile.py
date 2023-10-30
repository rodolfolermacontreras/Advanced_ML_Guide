import random

from locust import HttpUser, constant_pacing, task


class UnitPriceUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = constant_pacing(1)

    @task
    def unit_price(self):
        self.client.post(
            "/unitprice",
            json={"Distance": 1.0 + random.random() * 6499.0},
        )