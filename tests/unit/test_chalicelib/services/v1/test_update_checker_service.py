import unittest
from tests.unit.testutils import BaseUnitTest, get_function_name
from chalicelib.services.v1.update_checker_service import UpdateCheckerService


class UpdateCheckerServiceTestCase(BaseUnitTest):
    def test_get_datasource(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        service = UpdateCheckerService()
        datasources = service.get_datasources()
        self.assertIsNotNone(datasources)

    def test_execute(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        service = UpdateCheckerService()
        result = service.execute()
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
