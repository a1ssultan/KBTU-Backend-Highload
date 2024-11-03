import json
import requests
import logging


class LokiHandler(logging.Handler):
    def __init__(self, url, tags=None):
        super().__init__()
        self.url = url
        self.tags = tags or {}

    def emit(self, record):
        log_entry = self.format(record)
        payload = {
            "streams": [
                {
                    "stream": self.tags,
                    "values": [
                        [str(int(record.created * 1000000000)), log_entry]  # время в наносекундах
                    ],
                }
            ]
        }

        try:
            requests.post(self.url, json=payload)
        except Exception as e:
            print(f"Failed to send log to Loki: {e}")

