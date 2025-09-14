from locust import task, HttpUser

"测试脚本"
class WebsiteUser(HttpUser):
    @task
    def index(self):
        self.client.get("/")