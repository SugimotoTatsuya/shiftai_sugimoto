from django.test import TestCase
from rest_framework.test import APIClient
from .models import User, Team, Activity, Workout, Leaderboard

class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        Team.objects.create(name="Marvel", description="Team Marvel")
        Team.objects.create(name="DC", description="Team DC")
        User.objects.create(name="Iron Man", email="ironman@marvel.com", team="Marvel")
        User.objects.create(name="Batman", email="batman@dc.com", team="DC")
        Activity.objects.create(user="Iron Man", activity="Running", duration=30)
        Workout.objects.create(name="Morning Cardio", suggested_for="Marvel")
        Leaderboard.objects.create(team="Marvel", points=100)

    def test_api_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('users', response.data)

    def test_users_list(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_teams_list(self):
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_activities_list(self):
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_workouts_list(self):
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_leaderboard_list(self):
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
