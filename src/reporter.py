import traceback

import mqtt_common

import paho.mqtt.subscribe as subscribe

import structlog

log = structlog.get_logger()


def print_averages(client, userdata, message):
    log.msg("Result:", result=message.payload)


if __name__ == "__main__":
    log.msg("Hi from reporter")
    connected = False
    while not connected:
        try:
            rc = subscribe.callback(
                print_averages,
                mqtt_common.REPORTER_TOPIC,
                hostname=mqtt_common.BROKER_HOSTNAME,
            )
            log.msg("Subscribe Response", response=rc)
            connected = True
        except Exception as e:
            log.error("Aggregator Subscribe Error", traceback=traceback.format_exc())
