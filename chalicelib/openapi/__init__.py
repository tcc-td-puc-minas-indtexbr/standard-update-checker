import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from chalicelib import APP_NAME, APP_VERSION
# Create an APISpec
from chalicelib.config import get_config
from chalicelib.helper import open_vendor_file
from chalicelib.logging import get_logger
from chalicelib.openapi.schemas import PingSchema
from chalicelib.openapi import api_schemas

servers = [
    {
        "url": os.environ["API_SERVER"] if "API_SERVER" in os.environ else None,
        "description": os.environ["API_SERVER_DESCRIPTION"] if "API_SERVER_DESCRIPTION" in os.environ else None
    }
]

if get_config().APP_ENV == "development":
    servers.append({
        "url": "http://localhost:8000",
        "description": "Development server"
    })

spec = APISpec(
    title=APP_NAME,
    openapi_version='3.0.2',
    version=APP_VERSION,
    plugins=[
        MarshmallowPlugin()
    ],
    servers=servers

)


def generate_openapi_yml(spec_object, logger, force=False):
    openapi_data = spec_object.to_yaml()

    if os.environ['APP_ENV'] == 'development' or force:
        stream = open_vendor_file("./public/swagger/openapi.yml", "w")

        if stream:
            stream.write(openapi_data)
            stream.close()
