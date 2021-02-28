import unittest

from chalicelib.services.v1.update_synchronizer_service import UpdateSynchronizerService
from tests.functional.functionaltestutils import BaseFunctionalTestCase
from tests.functional.helpers.connection_helper import ConnectionHelper
from tests.unit.testutils import get_function_name


def get_connection():
    connection = ConnectionHelper().get_dynamodb_local_connection()
    return connection


class UpdateSynchronizerServiceTestCase(BaseFunctionalTestCase):
    CONFIG = None

    def test_execute(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        service = UpdateSynchronizerService(logger=self.logger, config=self.CONFIG, connection=get_connection())
        result = service.execute()

        self.assertIsNotNone(result)
        # self.logger.info("Total of updates: {}".format(len(service.updates)))
        # self.assertGreater(len(service.updates), 0)


if __name__ == '__main__':
    unittest.main()
