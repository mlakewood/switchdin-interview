from time import time
import mqtt_common
from sys import stdout
import traceback
import json
from datetime import datetime, timedelta

import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import pandas as pd

import structlog

log = structlog.get_logger()

timestamp_format = '%Y-%m-%d%H:%M:%S'
DATAFRAMESTORE = pd.DataFrame(columns=["Datetime", "value"])

def one_minute_average(dataframe):
    now = datetime.utcnow()
    one_minute_ago = now - timedelta(minutes=1)
    df = dataframe.loc[(dataframe.Datetime <= now) & (dataframe.Datetime >= one_minute_ago)]
    log.msg("1 min avg", avg=df['value'].mean())
    return df['value'].mean()

def five_minute_average(dataframe):
    now = datetime.utcnow()
    five_minutes_ago = now - timedelta(minutes=5)
    df = dataframe.loc[(dataframe.Datetime <= now) & (dataframe.Datetime >= five_minutes_ago)]
    log.msg("5 min avg", avg=df['value'].mean())

    return df['value'].mean()

def thirty_minute_average(dataframe):
    now = datetime.utcnow()
    thirty_minutes_ago = now - timedelta(minutes=30)
    df = dataframe.loc[(dataframe.Datetime <= now) & (dataframe.Datetime >= thirty_minutes_ago)]
    log.msg("30 min avg", avg=df['value'].mean())
    return df['value'].mean()

def store_message(client, userdata, message):
    global DATAFRAMESTORE
    log.msg(f"Message recieved", payload=message.payload)
    payload = json.loads(message.payload)
    timestamp = datetime.fromisoformat(payload[mqtt_common.PAYLOAD_TIMESTAMP_KEY])
    tmp_df = pd.DataFrame(
        [[pd.to_datetime(timestamp.strftime(timestamp_format), format=timestamp_format), payload[mqtt_common.PAYLOAD_NUMBER_KEY]]],
        columns=["Datetime", "value"],
    )

    DATAFRAMESTORE = pd.concat([tmp_df, DATAFRAMESTORE])

    one_minute = one_minute_average(DATAFRAMESTORE)
    five_minute = five_minute_average(DATAFRAMESTORE)
    thirty_minute = thirty_minute_average(DATAFRAMESTORE)

    payload = json.dumps(
        {
            mqtt_common.PAYLOAD_ONE_MINUTE_KEY: one_minute,
            mqtt_common.PAYLOAD_FIVE_MINUTE_KEY: five_minute,
            mqtt_common.PAYLOAD_THIRTY_MINUTE_KEY: thirty_minute,
        }
    )

    try:
        response = publish.single(
            mqtt_common.REPORTER_TOPIC, payload, hostname=mqtt_common.BROKER_HOSTNAME
        )
        log.msg("Publish Response", response=response)
    except Exception as e:
        log.error("Publish Traceback", traceback=traceback.format_exc())
    
    # redact data after a certain time for memory constraints
    now = datetime.utcnow()
    redact_period = now - timedelta(minutes=45) # give a bit of leeway
    DATAFRAMESTORE = DATAFRAMESTORE.loc[(DATAFRAMESTORE.Datetime <= now) & (DATAFRAMESTORE.Datetime >= redact_period)]


if __name__ == "__main__":
    print("Hi from aggregator")
    connected = False
    while not connected:
        try:
            rc = subscribe.callback(
                store_message,
                mqtt_common.GENERATOR_TOPIC,
                hostname=mqtt_common.BROKER_HOSTNAME,
            )
            log.msg("Subscribe Response", response=rc)
            connected = True
        except Exception as e:
            log.error("Aggregator Subscribe Error", traceback=traceback.format_exc())
