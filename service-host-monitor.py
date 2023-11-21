#!/usr/bin/python3

#Jenkins monitoring script

import time
import requests
import logging

# Jenkins URL and Slack Web URL
JENKINS_URL = "https://jenkins.sonos.com/main/"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/workflows/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"

MAX_RETRIES = 6

# Logging
logging.basicConfig(filename='jenkins_monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def send_slack_alert(message):
    payload = {
        "jenkins": "Main Jenkins",
        "message": message
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        logging.error(f"Failed to send Slack alert: {response.status_code} - {response.text}")
    else:
        logging.info("Slack alert sent successfully.")

def check_jenkins():
    retries = 0

    while retries < MAX_RETRIES:
        try:
            response = requests.get(JENKINS_URL)
            response_code = response.status_code

            if response_code == 200:
                logging.info("Jenkins is up and running at %s", JENKINS_URL)
            else:
                logging.warning("Jenkins is down (HTTP response code: %d) - Retrying (attempt %d of %d)", response_code, retries + 1, MAX_RETRIES)
                send_slack_alert(f"Don't panic it's a testing: Jenkins {JENKINS_URL} is down (HTTP response code: {response_code}, Please take a look asap)")
                return
            retries += 1
            time.sleep(30)
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to connect to Jenkins: {e}")
            time.sleep(60)

if __name__ == "__main__":
    logging.info("Jenkins monitoring started.")
    check_jenkins()
