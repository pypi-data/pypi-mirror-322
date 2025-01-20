# File: desync_search/core.py

import requests
import json
import time

class DesyncClient:
    """
    A high-level client for the Desync Search API.
    This handles search (stealth/test), retrieving previously collected search data,
    and pulling the user's credit balance.
    """

    def __init__(self, user_api_key):
        """
        Initialize the client with a user_api_key.
        The base URL is fixed to the current production endpoint.
        """
        self.user_api_key = user_api_key
        self.base_url = "https://nycv5sx75joaxnzdkgvpx5mcme0butbo.lambda-url.us-east-1.on.aws/"

    def search(
        self,
        url,
        search_type="stealth_search",
        scrape_full_html=False,
        remove_link_duplicates=True
    ):
        """
        Performs a search. By default, does a 'stealth_search' (cost: 10 credits),
        but you can supply 'test_search' for a cheaper test operation (cost: 1 credit).

        :param url: The URL to scrape.
        :param search_type: Either "stealth_search" (default) or "test_search".
        :param scrape_full_html: If True, returns full HTML. Default False.
        :param remove_link_duplicates: If True, deduplicate discovered links. Default True.

        Returns the API response dict if success. Raises RuntimeError if the API returns success=False.
        """
        payload = {
            "user_api_key": self.user_api_key,
            "timestamp": int(time.time()),
            "operation": "search",
            "flags": {
                "search_type": search_type,
                "target_list": [url],
                "scrape_full_html": scrape_full_html,
                "remove_link_duplicates": remove_link_duplicates
            },
            "metadata": {
                "api_version": "v1.0"
            }
        }
        return self._post_and_parse(payload)

    def list_available(self):
        """
        Lists minimal data about previously collected search results (IDs, domains, timestamps...).
        """
        payload = {
            "user_api_key": self.user_api_key,
            "timestamp": int(time.time()),
            "operation": "retrieval",
            "flags": {
                "retrieval_type": "list_available"
            },
            "metadata": {
                "api_version": "v1.0"
            }
        }
        return self._post_and_parse(payload)

    def pull_data(self, record_id):
        """
        Pulls full data for a specific record, including text_content, html_content, etc.
        """
        payload = {
            "user_api_key": self.user_api_key,
            "timestamp": int(time.time()),
            "operation": "retrieval",
            "flags": {
                "retrieval_type": "pull",
                "id": record_id
            },
            "metadata": {
                "api_version": "v1.0"
            }
        }
        return self._post_and_parse(payload)

    def pull_credits_balance(self):
        """
        Checks the user's own credit balance.
        """
        payload = {
            "user_api_key": self.user_api_key,
            "timestamp": int(time.time()),
            "operation": "retrieval",
            "flags": {
                "retrieval_type": "pull_credits_balance"
            },
            "metadata": {
                "api_version": "v1.0"
            }
        }
        return self._post_and_parse(payload)

    def _post_and_parse(self, payload):
        """
        Internal helper to POST the payload to self.base_url, parse JSON,
        and raise RuntimeError if success=False or there's an HTTP error.
        """
        try:
            resp = requests.post(self.base_url, json=payload, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            if not data.get("success", False):
                raise RuntimeError(
                    data.get("error", "Unknown error from API"),
                    data
                )
            return data
        except requests.RequestException as e:
            raise RuntimeError(f"HTTP error: {e}")
