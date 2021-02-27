import logging
import os
import unittest
import warnings


# from chalicelib.boot import init, register_vendor

# This is your Project Root
# from chalicelib.config import get_config
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# init()
# register_vendor()


class BaseFunctionalTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    """
    Classe base para testes funcionais
    """

    def setUp(self):
        log_name = 'functional_test'
        log_filename = None
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=log_format, filename=log_filename, level=logging.DEBUG)
        self.logger = logging.getLogger(log_name)

        # ignora falso positivos
        # https://github.com/boto/boto3/issues/454
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")