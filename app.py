from chalicelib.boot import register_vendor

# execute before other codes of app
register_vendor()

# registra a pasta vendor (antes de tudo)
from chalicelib.enums.messages import MessagesEnum
from chalicelib.exceptions import ApiException
from chalicelib.http_resources.request import ApiRequest
from chalicelib.http_resources.response import ApiResponse
from chalicelib.services.v1.update_checker_service import UpdateCheckerService

from chalicelib.config import get_config
from chalicelib.logging import get_logger, get_log_level
from chalicelib import APP_NAME, helper, http_helper, APP_VERSION
from chalice import Chalice

# config
config = get_config()
# debug
debug = helper.debug_mode()
# logger
logger = get_logger()
# chalice app
app = Chalice(app_name=APP_NAME, debug=debug)
# override the log configs
if not debug:
    # override to the level desired
    logger.level = get_log_level()
# override the log instance
app.log = logger


@app.route('/', cors=True)
def index():
    body = {"app": '%s:%s' % (APP_NAME, APP_VERSION)}
    return http_helper.create_response(body=body, status_code=200)


@app.route('/ping', cors=True)
def ping():
    body = {"message": "PONG"}
    return http_helper.create_response(body=body, status_code=200)


@app.route('/alive', cors=True)
def alive():
    body = {"app": "I'm alive!"}
    return http_helper.create_response(body=body, status_code=200)


@app.route('/update_checker', methods=['GET'], cors=True)
def update_checker():
    service = UpdateCheckerService()
    # service.execute()

    body = {
        "count": 0,
        "data": []
    }
    return http_helper.create_response(body=body, status_code=200)

    # status_code = 500
    # data = MessagesEnum.METHOD_NOT_IMPLEMENTED_ERROR.message
    # return http_helper.create_response(body=data, status_code=status_code)


@app.schedule('rate(1 day)')
def every_hour(event):
    service = UpdateCheckerService()
    service.execute()

    print(event.to_dict())


helper.print_routes(app, logger)
