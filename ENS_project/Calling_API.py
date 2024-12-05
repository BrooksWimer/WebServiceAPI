# used for api interaction
from zeep import Client, Transport
from requests import Session

# import api functions
from API_Functions import *

# import debugging tools
from Debuging import *





############ Setting up session and client for API interaction #################
# Set up a session to persist certain parameters and cookies across requests and configure the session to use the
# combined client certificate and to verify against the GeoTrust CA
session = Session()
# Path to the CA certificate for server verification
session.verify = CA_CERT_PATH
# Path to combined certificate and private key in PEM format
session.cert = COMBINED_CERT_PATH
# configure transport for zeep client
transport = Transport(session=session)
# Create a Zeep client that uses this transport
# if you want to display xml history
if xml:
    if ENDPOINT_URL == "https://smd.iso-ne.com/wpfmui/webservices/WindPlantLeadParticipant/1_0/?wsdl":
        logging.warning("You are using the production link. Are you sure you want to proceed?")
        confirmation = input("Type 'yes' to confirm submission to production, or anything else to cancel: ")
        if confirmation.lower() != "yes":
            raise RuntimeError("Submission to production was canceled by the user.")
        else:
            client = Client(wsdl=ENDPOINT_URL, transport=transport, plugins=[history])

    else:
        client = Client(wsdl=ENDPOINT_URL, transport=transport, plugins=[history])
else:
    if ENDPOINT_URL == "https://smd.iso-ne.com/wpfmui/webservices/WindPlantLeadParticipant/1_0/?wsdl":
        logging.warning("You are using the production link. Are you sure you want to proceed?")
        confirmation = input("Type 'yes' to confirm submission to production, or anything else to cancel: ")
        if confirmation.lower() != "yes":
            raise RuntimeError("Submission to production was canceled by the user.")
        else:
            client = Client(wsdl=ENDPOINT_URL, transport=transport)

    else:
        client = Client(wsdl=ENDPOINT_URL, transport=transport)


####### Assigning Variables ######

categoryID = "insert the selected category's Identifier here"
entityAssetID = "insert the selected entity's Asset Identifier here"
scheduleID_query = "insert the selected schedule's identifier here for querying data"
scheduleID_submitHourly = "insert the selected schedule's identifier here for submitting hourly data"
scheduleID_submitDaily = "insert the selected schedule's identifier here for submitting daily data"






####################### Making API Calls (uncomment functions to run) ###############################
#
# # # Query Categories
# make_request_categories(client)
# print()
#
# # # Query Entities
# make_request_entities(client, categoryID=categoryID)
# print()
#
# # # Query Schedules
# make_request_schedules(client)
# print()
#
# # # Query Forecasts
# make_request_forecasts(client, entityAssetID=entityAssetID, scheduleID=scheduleID_query)
# print()
#
# # # Submit hourly forecast
# power_values_hourly = []
# time_values_hourly = []
# submit_forecast(client, categoryID=categoryID, scheduleID=scheduleID_submitHourly, entityAssetID=entityAssetID,
#                 powerValues=power_values_hourly, forecastType=time_values_hourly)
# print()
#
# # # Submit daily forecast
# power_values_daily = []
# time_values_daily = []
# submit_forecast(client, categoryID=categoryID, scheduleID=scheduleID_submitDaily, entityAssetID=entityAssetID,
#                 powerValues=power_values_daily, forecastType=time_values_daily)
# print()


# prints xml request
if xml:
    try:
        print_soap_history(history)
    except:
        print("soap history not available")

