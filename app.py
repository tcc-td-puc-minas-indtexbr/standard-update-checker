import base64
import json
import os

import yaml

from chalicelib.boot import register_vendor

# execute before other codes of app
from chalicelib.helper import open_vendor_file
from chalicelib.http_helper import CUSTOM_DEFAULT_HEADERS
from chalicelib.openapi import spec, generate_openapi_yml
from chalicelib.services.v1.standard_updates_service import StandardUpdatesService
from chalicelib.services.v1.update_synchronizer_service import UpdateSynchronizerService

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
    """
        get:
            summary: Ping method
            responses:
                200:
                    description: Success response
                    content:
                        application/json:
                            schema: PingSchema

        """
    body = {"message": "PONG"}
    return http_helper.create_response(body=body, status_code=200)


@app.route('/alive', cors=True)
def alive():
    """
            get:
                summary: Service Health Method
                responses:
                    200:
                        description: Success response
                        content:
                            application/json:
                                schema: AliveSchema

            """
    body = {"app": "I'm alive!"}
    return http_helper.create_response(body=body, status_code=200)


@app.route('/favicon-32x32.png')
def favicon():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "image/png"
    data = base64.b64decode(
        'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAkFBMVEUAAAAQM0QWNUYWNkYXNkYALjoWNUYYOEUXN0YaPEUPMUAUM0QVNUYWNkYWNUYWNUUWNUYVNEYWNkYWNUYWM0eF6i0XNkchR0OB5SwzZj9wyTEvXkA3az5apTZ+4C5DgDt31C9frjU5bz5uxTI/eDxzzjAmT0IsWUEeQkVltzR62S6D6CxIhzpKijpJiDpOkDl4b43lAAAAFXRSTlMAFc304QeZ/vj+ECB3xKlGilPXvS2Ka/h0AAABfklEQVR42oVT2XaCMBAdJRAi7pYJa2QHxbb//3ctSSAUPfa+THLmzj4DBvZpvyauS9b7kw3PWDkWsrD6fFQhQ9dZLfVbC5M88CWCPERr+8fLZodJ5M8QJbjbGL1H2M1fIGfEm+wJN+bGCSc6EXtNS/8FSrq2VX6YDv++XLpJ8SgDWMnwqznGo6alcTbIxB2CHKn8VFikk2mMV2lEnV+CJd9+jJlxXmMr5dW14YCqwgbFpO8FNvJxwwM4TPWPo5QalEsRMAcusXpi58/QUEWPL0AK1ThM5oQCUyXPoPINkdd922VBw4XgTV9zDGWWFrgjIQs4vwvOg6xr+6gbCTqE+DYhlMGX0CF2OknK5gQ2JrkDh/W6TOEbYDeVecKbJtyNXiCfGmW7V93J2hDus1bDfhxWbIZVYDXITA7Lo6E0Ktgg9eB4KWuR44aj7ppBVPazhQH7/M/KgWe9X1qAg8XypT6nxIMJH+T94QCsLvj29IYwZxyO9/F8vCbO9tX5/wDGjEZ7vrgFZwAAAABJRU5ErkJggg==')
    return http_helper.create_response(body=data, status_code=200, headers=headers)


@app.route('/docs')
def docs():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "text/html"
    html_file = open_vendor_file('./public/swagger/index.html', 'r')
    html = html_file.read()
    return http_helper.create_response(body=html, status_code=200, headers=headers)


@app.route('/openapi.json')
def docs():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "text/json"
    html_file = open_vendor_file('./public/swagger/openapi.json', 'r')
    html = html_file.read()
    return http_helper.create_response(body=html, status_code=200, headers=headers)


@app.route('/openapi.yml')
def docs():
    headers = CUSTOM_DEFAULT_HEADERS.copy()
    headers['Content-Type'] = "text/yaml"
    html_file = open_vendor_file('./public/swagger/openapi.yml', 'r')
    html = html_file.read()
    return http_helper.create_response(body=html, status_code=200, headers=headers)


@app.route('/v1/updates', methods=['GET'], cors=True)
def updates_list():
    """
            get:
                summary: List the updates
                responses:
                    200:
                        description: Success response
                        content:
                            application/json:
                                schema: StandardUpdatesListResponseSchema

            """

    service = StandardUpdatesService()
    request = ApiRequest().parse_request(app)
    response = ApiResponse(request)
    status_code = 200

    try:
        data = service.list(request)
        total = service.count(request)

        response.set_data(data)
        response.set_total(total)

    except Exception as err:
        logger.error(err)

        if isinstance(err, ApiException):
            api_ex = err
            status_code = 404
        else:
            api_ex = ApiException(MessagesEnum.LIST_ERROR)
            status_code = 500

        response.set_exception(api_ex)

    return response.get_response(status_code)


@app.route('/v1/updates/{uuid}', methods=['GET'], cors=True)
def updates_get(uuid):
    """
    get:
        summary: Get Standard Update
        parameters:
            - in: path
              name: uuid
              description: "Standard Update uuid"
              required: true
              schema:
                type: string
                format: UUID
        responses:
            200:
                description: Success response
                content:
                    application/json:
                        schema: StandardUpdatesGetResponseSchema

            """

    service = StandardUpdatesService()
    request = ApiRequest().parse_request(app)
    response = ApiResponse(request)
    status_code = 200

    try:

        data = service.get(request, uuid)
        response.set_data(data)

    except Exception as err:
        logger.error(err)

        if isinstance(err, ApiException):
            api_ex = err
            status_code = 404
        else:
            api_ex = ApiException(MessagesEnum.FIND_ERROR)
            status_code = 500

        response.set_exception(api_ex)

    return response.get_response(status_code)


@app.route('/v1/updates/check', methods=['GET'], cors=True)
def updates_check():
    """
            get:
                summary: Check for updates
                responses:
                    200:
                        description: Success response
                        content:
                            application/json:
                                schema: UpdatesCheckResponseSchema

            """

    service = UpdateCheckerService()
    request = ApiRequest().parse_request(app)
    response = ApiResponse(request)
    status_code = 200

    try:
        service.execute()

        total = len(service.updates)
        data = service.get_updates()

        print(total)
        print(data)
        response.set_data(data)
        response.set_total(total)

    except Exception as err:
        logger.error(err)

        if isinstance(err, ApiException):
            api_ex = err
            status_code = 404
        else:
            api_ex = ApiException(MessagesEnum.LIST_ERROR)
            status_code = 500

        response.set_exception(api_ex)

    return response.get_response(status_code)


@app.route('/v1/updates/sync', methods=['GET'], cors=True)
def updates_sync():
    """
    get:
                summary: Synchronize the updates
                responses:
                    200:
                        description: Success response
                        content:
                            application/json:
                                schema: UpdatesSyncResponseSchema

            """
    service = UpdateSynchronizerService()
    request = ApiRequest().parse_request(app)
    response = ApiResponse(request)
    status_code = 200

    try:

        raise ApiException(MessagesEnum.METHOD_NOT_IMPLEMENTED_ERROR)

    except Exception as err:
        logger.error(err)
        status_code = 501
        if isinstance(err, ApiException):
            api_ex = err
        else:
            api_ex = ApiException(MessagesEnum.METHOD_NOT_IMPLEMENTED_ERROR)

        response.set_exception(api_ex)

    return response.get_response(status_code)


@app.schedule('rate(1 day)')
def every_day(event):
    service = UpdateCheckerService()
    result = service.execute()
    body = {
        "count": len(service.updates),
        "data": service.get_updates()
    }

    logger.info("Event: {}".format(event.to_dict()))
    print("Result: {}".format(json.dumps(body)))

    return result


# doc
spec.path(view=ping, path="/alive", operations=yaml.safe_load(alive.__doc__))
spec.path(view=ping, path="/ping", operations=yaml.safe_load(ping.__doc__))
spec.path(view=updates_check, path="/v1/updates/check", operations=yaml.safe_load(updates_check.__doc__))
spec.path(view=updates_sync, path="/v1/updates/sync", operations=yaml.safe_load(updates_sync.__doc__))
spec.path(view=updates_list, path="/v1/updates", operations=yaml.safe_load(updates_list.__doc__))
spec.path(view=updates_get, path="/v1/updates/{uuid}", operations=yaml.safe_load(updates_get.__doc__))
# spec.path(view=standard_get, path="/v1/standard/{uuid}", operations=yaml.safe_load(standard_get.__doc__))
# spec.path(view=standard_update, path="/v1/standard/{uuid}", operations=yaml.safe_load(standard_update.__doc__))
# spec.path(view=standard_delete, path="/v1/standard/{uuid}", operations=yaml.safe_load(standard_delete.__doc__))

helper.print_routes(app, logger)
logger.info('Running at {}'.format(os.environ['APP_ENV']))

# generate de openapi.yml
generate_openapi_yml(spec, logger)
