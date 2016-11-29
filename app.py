from datetime import datetime

import logging
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin

from smart_client import poaching_data, human_activity_data
from metadata import api_schema


app = Flask(__name__)
CORS(app)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.route('/poaching', methods=['GET'])
def poaching_endpoint(event=None, context=None):
    logger.info('Lambda function invoked /poaching')
    limit = int(request.args.get('limit', 1000))
    raw_categories = request.args.get('categories')
    start_date = _cleanup_time(request.args.get('start_date'))
    end_date = _cleanup_time(request.args.get('end_date'))

    if raw_categories:
        categories = raw_categories.split(',')
    else:
        categories = []
    return jsonify(poaching_data(max_rows=limit, categories=categories, start_date=start_date, end_date=end_date))


@app.route('/human_activity', methods=['GET'])
def human_activity_endpoint(event=None, context=None):
    logger.info('Lambda function invoked /human_activity')
    limit = int(request.args.get('limit', 1000))
    start_date = _cleanup_time(request.args.get('start_date'))
    end_date = _cleanup_time(request.args.get('end_date'))

    return jsonify(human_activity_data(max_rows=limit, start_date=start_date, end_date=end_date))


@app.route('/metadata', methods=['GET'])
def metadata(event=None, context=None):
    return jsonify(api_schema)


@app.route('/', methods=['GET'])
def index(event=None, context=None):
    logger.info('Lambda function invoked /')
    return jsonify({'ok': True})

def _cleanup_time(time_string):
    if not time_string:
        return None
    return datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S")


if __name__ == '__main__':
    app.run(debug=True)
