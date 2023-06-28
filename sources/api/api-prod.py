import json

from flask import Flask, request

from src.endpoints import Endpoints
from src.utils import obtain_logger

# Init
app = Flask(__name__)
endpoints = Endpoints()
logger = obtain_logger("API")


@app.route('/community')
def community():
    """Returns the averages of the community"""
    return endpoints.community_endpoint()


@app.route('/user_data', methods=["POST"])
def user_data():
    """Save user data from the app"""
    request_data = request.json
    logger.info('A request has been received')
    return endpoints.user_data_endpoint(request_data)


@app.route('/daily_questionnaires', methods=["POST"])
def daily_questionnaires():
    """Save user daily questionnaires data from the app"""
    request_data = request.json
    logger.info('A request has been received')
    return endpoints.daily_questionnaires_endpoint(request_data)


@app.route('/one_off_questionnaires', methods=["POST"])
def one_off_questionnaires():
    """Save user one_off questionnaires data from the app"""
    request_data = request.json
    logger.info('A request has been received')
    return endpoints.one_off_questionnaires_endpoint(request_data)


@app.route('/bg_data', methods=["POST"])
def user_databg():
    """Save user background data from the app"""
    request_databg0 = request.json
    request_databg = json.loads(request_databg0)
    logger.info(f'A request has been received with the following data: {request_databg}')
    return endpoints.user_databg_endpoint(request_databg)


# If this script is being executed and not imported, deploy the API
if __name__ == '__main__':
    app.run(host="0.0.0.0")
