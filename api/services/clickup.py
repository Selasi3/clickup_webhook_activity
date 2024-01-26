import httpx

CLICKUP_API_KEY = ''
CLICKUP_TEAM_ID=''
WEBHOOK_ENDPOINT = ""

class ClickUpServices:
    def __init__(self):
        self.api_key = CLICKUP_API_KEY

    def get_space(self, space_id: str):
        url = "https://api.clickup.com/api/v2/space/" + space_id

        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = httpx.get(url, headers=headers)

            if response.status_code == 200:
                print("Space retrieved successfully")
                return response.json()
        except Exception as e:
            print(f"Request failed: {str(e)}")

    def get_task(self, task_id: str,):
        url = "https://api.clickup.com/api/v2/task/" + task_id

        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = httpx.get(url, headers=headers)

            if response.status_code == 200:
                print("Task data retrieved successfully")
                return response.json()
        except Exception as e:
            print(f"Request failed: {str(e)}")

    def create_webhook(
        self,
        team_id: str = CLICKUP_TEAM_ID
    ):
        webhook_endpoint = WEBHOOK_ENDPOINT

        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }
        body = {
            "endpoint": webhook_endpoint,
            "events": [
                "taskCreated",
                "taskUpdated",
                "taskDeleted",
                "taskPriorityUpdated",
                "taskStatusUpdated",
                "taskAssigneeUpdated",
                "taskDueDateUpdated",
                "taskTagUpdated",
                "taskMoved",
                "taskCommentPosted",
                "taskCommentUpdated",
                "taskTimeEstimateUpdated",
                "taskTimeTrackedUpdated"
            ]
        }
        url = "https://api.clickup.com/api/v2/team/" + team_id + "/webhook"

        try:
            response = httpx.post(url, headers=headers, json=body)

            if response.status_code == 200:
                print("Webhook created successfully")
                return response.json()
        except Exception as e:
            print(f"Request failed: {str(e)}")

    def get_webhooks(
        self,
        team_id: str = CLICKUP_TEAM_ID,
    ):
        url = "https://api.clickup.com/api/v2/team/" + team_id + "/webhook"

        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = httpx.get(url, headers=headers)

            if response.status_code == 200:
                print("Webhooks retrieved successfully")
                return response.json()
        except Exception as e:
            print(f"Request failed: {str(e)}")

    def delete_webhook(
        self,
        webhook_id: str
    ):
        url = "https://api.clickup.com/api/v2/webhook/" + webhook_id

        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = httpx.delete(url, headers=headers)
            print(f"DEBUGPRINT[2]: clickup.py:82: response={response}")

            if response.status_code == 200:
                print("Webhook deleted successfully")
                return response.json()
        except Exception as e:
            print(f"Request failed: {str(e)}")


