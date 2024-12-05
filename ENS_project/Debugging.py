from Properties import *

# used to silence the warnings
import warnings
warnings.filterwarnings("ignore")

# used for debugging zeep response, uncomment for debugging
import logging
if debug:
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('zeep').setLevel(logging.DEBUG)
    logging.getLogger('requests').setLevel(logging.DEBUG)

# used to get full xml content of request and response
from zeep.plugins import HistoryPlugin
from lxml import etree
if xml:
    history = HistoryPlugin()
else:
    history = ""

def print_soap_history(history):
    # Get the last request and response
    last_request = history.last_sent
    last_response = history.last_received
    # Convert them to pretty-printed XML strings
    request_str = etree.tostring(last_request['envelope'], pretty_print=True).decode('utf-8')
    print(f"last request: {request_str}")
    if last_response != None:
        response_str = etree.tostring(last_response['envelope'], pretty_print=True).decode('utf-8')
        print(f"last response: {response_str}")
    else:
        print(f"last response: {last_response}")

