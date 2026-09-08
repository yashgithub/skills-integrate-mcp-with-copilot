import copy
import unittest

from fastapi import HTTPException

from src import app


class CapacityTests(unittest.TestCase):
    def setUp(self):
        self.original_activities = copy.deepcopy(app.activities)
        app.activities["Full Activity"] = {
            "description": "A full activity",
            "schedule": "Mondays, 3:00 PM - 4:00 PM",
            "max_participants": 1,
            "participants": ["existing@mergington.edu"],
        }

    def tearDown(self):
        app.activities.clear()
        app.activities.update(self.original_activities)

    def test_signup_rejects_full_activity(self):
        with self.assertRaises(HTTPException) as context:
            app.signup_for_activity("Full Activity", "new@mergington.edu")

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Activity is full")
        self.assertEqual(
            app.activities["Full Activity"]["participants"],
            ["existing@mergington.edu"],
        )

    def test_signup_succeeds_after_unregistering(self):
        app.unregister_from_activity("Full Activity", "existing@mergington.edu")

        response = app.signup_for_activity("Full Activity", "new@mergington.edu")

        self.assertEqual(response["message"], "Signed up new@mergington.edu for Full Activity")
        self.assertEqual(
            app.activities["Full Activity"]["participants"],
            ["new@mergington.edu"],
        )