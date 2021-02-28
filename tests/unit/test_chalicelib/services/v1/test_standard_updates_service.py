import unittest

from unittest_data_provider import data_provider

from chalicelib.config import get_config
from chalicelib.http_resources.request import ApiRequest
from chalicelib.logging import get_logger
from chalicelib.services.v1.standard_updates_service import StandardUpdatesService
from tests import ROOT_DIR
from tests.functional.functionaltestutils import BaseFunctionalTestCase
from tests.functional.helpers.connection_helper import ConnectionHelper, DynamoDBHelper
from tests.unit.mocks.boto3_mocks import table_mock
from tests.unit.mocks.database_mock import get_connection
from tests.unit.testutils import get_function_name


def get_request():
    request = ApiRequest()
    request.limit = 2

    request2 = ApiRequest()
    request2.limit = 2
    request2.offset = 1

    return (request,), (request2,),


class StandardUpdatesServiceTestCase(BaseFunctionalTestCase):

    def setUp(self):
        super().setUp()
        # sobrescreve o mock
        self.connection = get_connection()
        self.config = get_config()

        data = {
            'Items': [
                {
                    "uuid": "067d914c-cb19-4f3f-8755-584e0eafe344",
                    "identification": "ISO 9001:2015",
                    "publication_date": "2015-09-30",
                    "title": "Sistemas de gestão da qualidade - Requisitos",
                    "description": "This document reached stage 30.60 on 2021-02-26, TC/SC: ISO/TC 42, ICS: 37.040.20",
                    "link": "http://www.iso.org/cms/render/live/en/sites/isoorg/contents/data/standard/03/19/31944.html",
                    "synchronized": True
                },
                {
                    "uuid": "fd214a67-1ad9-4152-87b8-b1e0f7d12cb9",
                    "identification": "ISO/DTS 18950.2",
                    "publication_date": "2021-02-26",
                    "title": "ISO/DTS 18950.2 - Imaging materials — Reflection colour photographic images — Indoor light stability specifications for museum display",
                    "description": "This document reached stage 30.60 on 2021-02-26, TC/SC: ISO/TC 42, ICS: 37.040.20",
                    "link": "http://www.iso.org/cms/render/live/en/sites/isoorg/contents/data/standard/03/19/31944.html",
                    "synchronized": False
                },
            ],
            'Count': 2,
            'ScannedCount': 2,
            'ResponseMetadata': {'RequestId': 'ebe11a2f-1b8f-472b-8507-c9aadeb3a379', 'HTTPStatusCode': 200,
                                 'HTTPHeaders': {'date': 'Sun, 28 Feb 2021 03:06:49 GMT',
                                                 'content-type': 'application/x-amz-json-1.0',
                                                 'x-amz-crc32': '2132082689',
                                                 'x-amzn-requestid': 'ebe11a2f-1b8f-472b-8507-c9aadeb3a379',
                                                 'content-length': '1130', 'server': 'Jetty(9.4.18.v20190429)'},
                                 'RetryAttempts': 0}}
        # Mock returns
        table_mock.scan.side_effect = lambda: data
        table_mock.item_count = data['Count']

    @data_provider(get_request)
    def test_list(self, request):
        self.logger.info('Running test: %s', get_function_name(__name__))
        service = StandardUpdatesService(logger=self.logger, config=self.config, connection=self.connection)
        data = service.list(request)
        # print(len(data))
        self.assertIsNotNone(data)
        # self.assertTrue(len(data) == request.limit)

    @data_provider(get_request)
    def test_count(self, request):
        """

        :param (ApiRequest) request:
        :return:
        """
        self.logger.info('Running test: %s', get_function_name(__name__))
        service = StandardUpdatesService(logger=self.logger, config=self.config, connection=self.connection)
        data = service.count(request)

        self.assertIsNotNone(data)
        self.assertTrue(data > 0)


if __name__ == '__main__':
    unittest.main()
