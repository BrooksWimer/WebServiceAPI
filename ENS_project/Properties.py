
# Required constants
# url given by ISO NE
ENDPOINT_URL = r"insert URL here"

# path to CA CERT on your computer
CA_CERT_PATH = r"insert\path\to\ca\certificate\here"

# path to client CERT on your computer (given by ISO NE)
CLIENT_CERT_PATH = r"insert\path\to\client\certificate\here"

# private password for certificate
CERT_PASSWORD = r"insert password here"


# Set to True to display debugging
debug = False
# Set to True to display xml
xml = False

# used to get current directory
import os
# get current working directory
cwd = os.getcwd()
# path to the combined certificate (this is a file you will be creating in the Conversion step)
COMBINED_CERT_PATH = f"{cwd}\combined_certs.pem"























