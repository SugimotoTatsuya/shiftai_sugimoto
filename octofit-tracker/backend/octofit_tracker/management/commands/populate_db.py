from django.core.management.base import BaseCommand
from django.conf import settings
from pymongo import MongoClient

from django.contrib.auth import get_user_model
from django.apps import apps

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating octofit_db with test data...'))
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Teams
        teams = [
            {"name": "Marvel", "description": "Team Marvel"},
            {"name": "DC", "description": "Team DC"}
        ]
        team_ids = db.teams.insert_many(teams).inserted_ids

        # Users
        users = [
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
            {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
            {"name": "Superman", "email": "superman@dc.com", "team": "DC"}
        ]
        db.users.insert_many(users)
        db.users.create_index([("email", 1)], unique=True)

        # Activities
        activities = [
            {"user": "Iron Man", "activity": "Running", "duration": 30},
            {"user": "Captain America", "activity": "Cycling", "duration": 45},
            {"user": "Batman", "activity": "Swimming", "duration": 60},
            {"user": "Superman", "activity": "Flying", "duration": 120}
        ]
        db.activities.insert_many(activities)

        # Workouts
        workouts = [
            {"name": "Morning Cardio", "suggested_for": "Marvel"},
            {"name": "Strength Training", "suggested_for": "DC"}
        ]
        db.workouts.insert_many(workouts)

        # Leaderboard
        leaderboard = [
            {"team": "Marvel", "points": 150},
            {"team": "DC", "points": 180}
        ]
        db.leaderboard.insert_many(leaderboard)

        self.stdout.write(self.style.SUCCESS('octofit_db test data population complete.'))
