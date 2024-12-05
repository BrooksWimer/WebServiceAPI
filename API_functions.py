# used for dummy data creation
import numpy as np
import pandas as pd
import random

# used for date and time alignment
from datetime import timedelta, datetime
import pytz




def make_request_categories(client):
    try:
        response = (client.service.QueryCategories())
        print("Response from QueryCategories:", response)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")


def make_request_schedules(client):
    try:
        response = (client.service.QuerySchedules())
        print("Response from QuerySchedules:", response)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")


def make_request_entities(client, categoryID = None):
    category = {
        'identifier': categoryID,
        'name': None,
        'description': None
    }
    try:
        if categoryID == None:
            response = (client.service.QueryEntities())
        else:
            response = (client.service.QueryEntities(Category=category))
        print("Response from QueryEntities:", response)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")


def make_request_forecasts(client, entityAssetID, scheduleID):
    schedule_request_data = {
        'Schedule': {
            'identifier': scheduleID
        },
        'Entities': {
            'Entity': {
                'identifier': None,
                'assetIdentifier': entityAssetID,
            }
        }
    }
    try:
        response = client.service.QueryForecast(ScheduleRequest=schedule_request_data)
        print("Response from QueryForcasts:", response)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")


def validate_and_format_time_values(time_values):
    """
    Validates and reformats time values to the required format: "%Y-%m-%dT%H:%M:%S%z".
    If reformatting fails, raises an exception.
    """
    formatted_times = []
    for time_value in time_values:
        try:
            # Try parsing the time value
            parsed_time = datetime.strptime(time_value, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            try:
                # Attempt to handle missing timezone or incorrect format
                if "+" in time_value or "-" in time_value:
                    time_value = time_value[:-3] + time_value[-2:]  # Adjust timezone formatting if needed
                parsed_time = datetime.strptime(time_value, "%Y-%m-%dT%H:%M:%S")
                # Add UTC timezone as a default if missing
                parsed_time = parsed_time.replace(tzinfo=pytz.utc)
            except ValueError:
                raise ValueError(f"Invalid time format: {time_value}")

        # Format the time to the correct format
        formatted_time = parsed_time.strftime("%Y-%m-%dT%H:%M:%S%z")
        formatted_time = formatted_time[:-2] + ":" + formatted_time[-2:]  # Adjust timezone format
        formatted_times.append(formatted_time)

    return formatted_times


def submit_forecast(client, categoryID, scheduleID, entityAssetID, powerValues, timeValues):
    """
    Submits the forecast data after validating the time and power value lists.
    Ensures that the lists are the same length and that time values are formatted correctly.
    """
    # Ensure timeValues and powerValues have the same length
    if len(timeValues) != len(powerValues):
        raise ValueError("Time values and power values must have the same length.")

    # Validate and format time values
    timeValues = validate_and_format_time_values(timeValues)

    # Create power entries by pairing time values with power values
    power_entries = [{'time': time, 'value': value} for time, value in zip(timeValues, powerValues)]

    forecast_data = {
        'CreateSchedule': {
            'Category': {
                'identifier': categoryID,
            },
            'Schedule': {
                'identifier': scheduleID,
            },
            'Entities': {
                'Entity': [
                    {
                        'assetIdentifier': entityAssetID,
                        'Power': power_entries
                    }
                ]
            }
        }
    }

    print(power_entries)

    try:
        response = client.service.SubmitForecast(CreateSchedule=forecast_data['CreateSchedule'])
        print("Response from SubmitForecast:", response)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        raise


def generate_sample_power_data(entities):
    # Parameters
    start_time = datetime.utcnow().replace(hour=7, minute=0, second=0, microsecond=0) + timedelta(days=1)
    num_rows = 500
    min_mw = 30.0
    max_mw = 70.0
    time_index = [(start_time + timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M:%S%z") for i in range(num_rows)]
    data = {
        'Time': time_index
    }

    for i in range(len(entities)):
        data[entities[i]] = np.round(np.random.uniform(min_mw, max_mw, num_rows), 1)

    df = pd.DataFrame(data)
    df.to_csv("SampleData.csv", index=False)
    print("Sample data successfully created")
    return df





