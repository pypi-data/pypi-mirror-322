# File: desync_search/core.py

import requests
import json
import time
from desync_search.data_structures import PageData  # or .core if you keep them in same file

API_VERSION = "v0.2.3"

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
    ) -> PageData:
        """
        Performs a search. By default, does a 'stealth_search' (cost: 10 credits),
        but you can supply 'test_search' for a cheaper test operation (cost: 1 credit).

        :param url: The URL to scrape.
        :param search_type: Either "stealth_search" (default) or "test_search".
        :param scrape_full_html: If True, returns full HTML. Default False.
        :param remove_link_duplicates: If True, deduplicate discovered links. Default True.

        :return: A single PageData object representing the newly scraped page record.
                 Raises RuntimeError if the API returns success=False or on HTTP error.
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
                "api_version": API_VERSION
            }
        }
        resp = self._post_and_parse(payload)  # a dict with "data" inside
        # Typically: {"success": True, "data": {...}}
        data_dict = resp.get("data", {})
        return PageData.from_dict(data_dict)

    def list_available(self) -> list:
        """
        Lists minimal data about previously collected search results (IDs, domain, timestamps, etc.).
        Returns a list of PageData objects (with limited fields).
        """
        payload = {
            "user_api_key": self.user_api_key,
            "timestamp": int(time.time()),
            "operation": "retrieval",
            "flags": {
                "retrieval_type": "list_available"
            },
            "metadata": {
                "api_version": API_VERSION
            }
        }
        resp = self._post_and_parse(payload)  # e.g. { "success": True, "data": [ {...}, {...} ] }
        data_list = resp.get("data", [])
        # Each item is a minimal record: id, url, domain, etc.
        return [PageData.from_dict(item) for item in data_list]

    def pull_data(self, record_id=None, url_filter=None) -> list:
        """
        Pulls full data for one or more records (including text_content, html_content, etc.).
        :param record_id: Filter by specific record ID.
        :param url_filter: (Optional) If you want to filter by 'url' instead.
        :return: A list of PageData objects, in case multiple records match the filters.
        """
        flags = {
            "retrieval_type": "pull"
        }
        if record_id is not None:
            flags["id"] = record_id
        if url_filter is not None:
            flags["url"] = url_filter

        payload = {
            "user_api_key": self.user_api_key,
            "timestamp": int(time.time()),
            "operation": "retrieval",
            "flags": flags,
            "metadata": {
                "api_version": API_VERSION
            }
        }
        resp = self._post_and_parse(payload)
        # resp["data"] is a list of dict
        data_list = resp.get("data", [])
        return [PageData.from_dict(d) for d in data_list]

    def pull_credits_balance(self) -> dict:
        """
        Checks the user's own credit balance.
        Returns a dict: e.g. {"success": True, "credits_balance": 240}
        """
        payload = {
            "user_api_key": self.user_api_key,
            "timestamp": int(time.time()),
            "operation": "retrieval",
            "flags": {
                "retrieval_type": "pull_credits_balance"
            },
            "metadata": {
                "api_version": API_VERSION
            }
        }
        return self._post_and_parse(payload)  # e.g. { "success": True, "credits_balance": 240 }

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
