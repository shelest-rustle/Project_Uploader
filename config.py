import os
import logging

from dotenv import load_dotenv
from base64 import b64encode

load_dotenv()

CRED = os.environ.get('CRED')
URL_AUTH = os.environ.get('URL_AUTH')
URL_AGENT1_TEST = os.environ.get('URL_AGENT1_TEST')
URL_AGENT2_TEST = os.environ.get('URL_AGENT2_TEST')
URL_AGENT3_TEST = os.environ.get('URL_AGENT3_TEST')
URL_AGENT4_TEST = os.environ.get('URL_AGENT4_TEST')

NAMES = {
    '0': 'преколлекты',
    '1': 'коллект 1',
    '2': 'коллект 2'
}

logging.basicConfig(
    level=logging.INFO,
    filemode='w',
    filename='autom_log'
)

encoded_cred = CRED.encode('ascii')
cred_base64 = b64encode(encoded_cred)
cred = cred_base64.decode('ascii')
