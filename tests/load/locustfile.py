# locustfile.py
from locust import HttpUser, task
import json

class LLMAppUser(HttpUser):
    
    @task(1) # Weight 1: This task will be picked by users
    def get_health(self):
        self.client.get("/v1/health", name="/v1/health (GET)") # 'name' groups stats in UI

    @task(2) # Weight 2: This task will be picked twice as often as get_health
    def post_chat_completions(self):
        payload = {
            "messages": [
                {"role": "user", "content": "Who won the Stanley Cup in 2020?"}
            ],
            "temperature": 0.7,
            "max_tokens": 50
        }
        headers = {"Content-Type": "application/json"}
        
        # 'name' groups requests in Locust's stats
        self.client.post("/v1/chat/completions",
                         data=json.dumps(payload),
                         headers=headers,
                         name="/v1/chat/completions (POST)")

    def on_start(self):
        """
        on_start is called when a Locust start before any task is scheduled.
        Can be used for login or other setup.
        """
        print("A new Locust user is starting...")

    def on_stop(self):
        """
        on_stop is called when the Locust user is stopping.
        """
        print("A Locust user is stopping...")
        