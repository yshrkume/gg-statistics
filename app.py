from flask import Flask, request
from flask_restful import Api, Resource
from datetime import datetime, timedelta

app = Flask(__name__)
api = Api(app)


class WateringFrequencyCountResource(Resource):
    def post(self):
        plants = request.json.get("plants", [])
        freq_map = {
            "daily": 1,
            "every 3 days": 3,
            "weekly": 7,
            "bi-weekly": 14,
            "monthly": 30,
        }

        freq_counts = {freq: 0 for freq in freq_map.keys()}

        for plant in plants:
            watering_freq = plant["watering_frequency"]
            if watering_freq in freq_map:
                freq_counts[watering_freq] += 1

        return freq_counts, 200


class UpcomingTasksCountResource(Resource):
    def post(self):
        plants = request.json.get("plants", [])
        upcoming_watering_count = 0
        upcoming_fertilizing_count = 0
        today = datetime.utcnow().date()

        for plant in plants:
            # Calculate watering schedule
            watering_interval = {
                "daily": 1,
                "every 3 days": 3,
                "weekly": 7,
                "bi-weekly": 14,
                "monthly": 30,
            }.get(plant["watering_frequency"], 7)

            last_watering_date = datetime.strptime(
                plant["purchase_date"], "%Y-%m-%d"
            ).date()

            # 現在から1週間先までの水やり回数をカウント
            while last_watering_date <= (today + timedelta(days=7)):
                next_watering_date = last_watering_date + timedelta(
                    days=watering_interval
                )
                if today <= next_watering_date <= (today + timedelta(days=7)):
                    upcoming_watering_count += 1
                last_watering_date = next_watering_date

            # Calculate fertilizing schedule
            fertilizing_interval = {"weekly": 7, "bi-weekly": 14, "monthly": 30}.get(
                plant["fertilizing_frequency"], 30
            )

            last_fertilizing_date = datetime.strptime(
                plant["purchase_date"], "%Y-%m-%d"
            ).date()

            # 現在から1週間先までの肥料やり回数をカウント
            while last_fertilizing_date <= (today + timedelta(days=7)):
                next_fertilizing_date = last_fertilizing_date + timedelta(
                    days=fertilizing_interval
                )
                if today <= next_fertilizing_date <= (today + timedelta(days=7)):
                    upcoming_fertilizing_count += 1
                last_fertilizing_date = next_fertilizing_date

        return {
            "upcoming_watering_tasks": upcoming_watering_count,
            "upcoming_fertilizing_tasks": upcoming_fertilizing_count,
        }, 200


api.add_resource(WateringFrequencyCountResource, "/watering_frequency_count")
api.add_resource(UpcomingTasksCountResource, "/upcoming_tasks_count")

if __name__ == "__main__":
    app.run()
