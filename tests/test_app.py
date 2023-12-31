"""Tests for Flask app"""
import copy
import datetime
import unittest

from app import app


class RouteTests(unittest.TestCase):
    """Test class for Flask routes"""

    valid_task = {
        "description": "Clean House",
        "eta": "2020-06-20T14:00:00",
        "status": "OPEN",
    }

    basic_auth = {"Authorization": "Basic dGFza19tYXN0ZXI6TWFzdGVyT2ZUYXNrcw=="}

    def setUp(self):
        """Setup of application"""
        app.testing = True
        self.app = app.test_client()

    def get_tasks_with_empty_data(self):
        """testing get returns no data"""
        response = self.app.get("/tasks", headers=self.basic_auth)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [])

    def post_task_successful_and_get_task_by_id(self):
        """Test post route and get task by id"""
        response = self.app.post("/task", json=self.valid_task, headers=self.basic_auth)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        assert "_id" in data
        assert data["description"] == "Clean House"
        assert data["eta"] == "2020-06-20T14:00:00"
        assert data["status"] == "OPEN"
        assert response.headers.get("content-type") == "application/json"

        self.valid_task["_id"] = data["_id"]

        response = self.app.get(
            f"/task/{self.valid_task['_id']}", headers=self.basic_auth
        )
        data = response.get_json()[0]

        self.assertEqual(response.status_code, 200)
        assert data["_id"] == self.valid_task["_id"]
        assert data["description"] == "Clean House"
        assert data["eta"] == "2020-06-20T14:00:00"
        assert data["status"] == "OPEN"
        assert response.headers.get("content-type") == "application/json"

    def get_tasks_should_return_data(self):
        """Test get tasks should return data"""
        response = self.app.get("/tasks", headers=self.basic_auth)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        data = data[0]
        assert data["_id"] == self.valid_task["_id"]
        assert data["description"] == "Clean House"
        assert data["eta"] == "2020-06-20T14:00:00"
        assert data["status"] == "OPEN"
        assert response.headers.get("content-type") == "application/json"

    def delete_task(self):
        """Step to delete task"""
        response = self.app.delete(
            f"/task/{self.valid_task['_id']}", headers=self.basic_auth
        )

        self.assertEqual(response.status_code, 204)

    def put_task_and_check_result(self):
        """Step to update task"""
        self.valid_task["description"] = "Watching TV"
        response = self.app.put(
            f"/task/{self.valid_task['_id']}",
            json=self.valid_task,
            headers=self.basic_auth,
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        assert "_id" in data
        assert data["description"] == "Watching TV"
        assert data["eta"] == "2020-06-20T14:00:00"
        assert data["status"] == "OPEN"
        assert response.headers.get("content-type") == "application/json"

        response = self.app.get(
            f"/task/{self.valid_task['_id']}", headers=self.basic_auth
        )
        data = response.get_json()[0]

        self.assertEqual(response.status_code, 200)
        assert data["_id"] == self.valid_task["_id"]
        assert data["description"] == "Watching TV"
        assert data["eta"] == "2020-06-20T14:00:00"
        assert data["status"] == "OPEN"
        assert response.headers.get("content-type") == "application/json"

    def complete_task_and_get_result(self):
        """Test step for complete task"""
        response = self.app.patch(
            f"/task/{self.valid_task['_id']}/complete", headers=self.basic_auth
        )
        data = response.get_json()

        assert data["status"] == "DONE"

        get_response = self.app.get(
            f"/task/{self.valid_task['_id']}", headers=self.basic_auth
        )
        data = response.get_json()

        assert data["_id"] == self.valid_task["_id"]
        assert data["description"] == "Watching TV"
        assert data["eta"] == "2020-06-20T14:00:00"
        assert data["status"] == "DONE"
        assert get_response.headers.get("content-type") == "application/json"

    def post_future_task_and_get_due_tasks_and_delete(self):
        """Test GET due tasks"""
        future_task = copy.deepcopy(self.valid_task)
        future_date = (
            (datetime.datetime.now() + datetime.timedelta(days=5))
            .isoformat()
            .split(".")[0]
        )
        future_task["eta"] = future_date

        future_task_response = self.app.post(
            "/task", json=future_task, headers=self.basic_auth
        )
        future_task_response_data = future_task_response.get_json()

        due_tasks_response = self.app.get("/tasks/due", headers=self.basic_auth)
        due_tasks_response_data = due_tasks_response.get_json()

        assert len(due_tasks_response_data) == 1
        assert due_tasks_response_data[0] == self.valid_task

        self.app.delete(
            f"/task/{future_task_response_data['_id']}", headers=self.basic_auth
        )

    def test_get_and_post(self):
        """Test script for Flask API"""
        self.get_tasks_with_empty_data()
        self.post_task_successful_and_get_task_by_id()
        self.post_future_task_and_get_due_tasks_and_delete()
        self.get_tasks_should_return_data()
        self.put_task_and_check_result()
        self.complete_task_and_get_result()
        self.delete_task()
        self.get_tasks_with_empty_data()
