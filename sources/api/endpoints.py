from typing import Dict

from flask import Response, jsonify

from src.database import Database
from src.response.daily_questionnaires_response import build_daily_questionnaires_response
from src.response.one_off_questionnaires_response import build_one_off_questionnaires_response
from src.response.user_data_response import build_user_data_response
from src.time import get_timestamps_yesterday, get_timestamps_current_week, get_timestamps_last_seven_days
from src.response.user_databg_response import build_user_databg_response
from src.utils import data_not_empty
from src.validator.daily_questionnaires_validator import DailyQuestionnairesValidator
from src.validator.one_off_questionnaires_validator import OneOffQuestionnairesValidator
from src.validator.user_data_validator import UserDataValidator
from src.validator.user_databg_validator import UserDataBgValidator


class Endpoints:
    def __init__(self, **kwargs):
        self.udv = UserDataValidator()
        self.dqv = DailyQuestionnairesValidator()
        self.ooqv = OneOffQuestionnairesValidator()
        self.udbgv = UserDataBgValidator()

        if "database" in kwargs:
            self.database = Database(database=kwargs["database"])
        else:
            self.database = Database()

    def user_data_endpoint(self, request_data: Dict) -> Response:
        if self.udv.validate(request_data):
            if data_not_empty(request_data["data"]):
                self.database.insert_user_data(request_data)
            response = build_user_data_response(request_data["data"])
            return jsonify(response)
        else:
            return Response("Bad request", 400)

    def daily_questionnaires_endpoint(self, request_data: Dict) -> Response:
        if self.dqv.validate(request_data):
            if data_not_empty(request_data["data"]):
                self.database.insert_daily_questionnaires(request_data)
            response = build_daily_questionnaires_response(request_data["data"])
            return jsonify(response)
        else:
            return Response("Bad request", 400)

    def one_off_questionnaires_endpoint(self, request_data: Dict) -> Response:
        if self.ooqv.validate(request_data):
            if data_not_empty(request_data["data"]):
                self.database.insert_one_off_questionnaires(request_data)
            response = build_one_off_questionnaires_response(request_data["data"])
            return jsonify(response)
        else:
            return Response("Bad request", 400)

    def community_endpoint(self) -> Response:
        response = {}

        # Obtain all timestamps
        yesterday_timestamps = get_timestamps_yesterday()
        current_week_timestamps = get_timestamps_current_week()
        last_seven_days_timestamps = get_timestamps_last_seven_days()

        # Yesterday average
        response["yesterday"] = self.database.get_daily_questionnaires_average(
            yesterday_timestamps[0],
            yesterday_timestamps[1]
        )

        # Current week average by day
        response["current_week"] = [
            self.database.get_daily_questionnaires_average(day[0], day[1]) for day in current_week_timestamps
        ]

        # Last seven days average
        response["last_seven_days"] = self.database.get_daily_questionnaires_average(
            last_seven_days_timestamps[0],
            last_seven_days_timestamps[1]
        )

        return jsonify(response)
    
    def user_databg_endpoint(self, request_databg: Dict) -> Response:
        if self.udbgv.validate(request_databg):
            if data_not_empty(request_databg["databg"]):
                self.database.insert_user_databg(request_databg)
            response = build_user_databg_response(request_databg["databg"])
            return jsonify(response)
        else:
            return Response("Bad request", 400)
