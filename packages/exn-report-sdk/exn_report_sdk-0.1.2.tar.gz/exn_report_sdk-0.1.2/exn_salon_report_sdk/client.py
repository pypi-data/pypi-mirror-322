import requests
from .config import BASE_URL, TIMEOUT
from .exceptions import AuthenticationError, RequestError
from .utils import generate_signature, get_timestamp

class ReportClient:
    def __init__(self, api_key, secret_key, base_url=None):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url or BASE_URL

    def _generate_headers(self, payload):
        """Generate headers for authentication."""
        timestamp = get_timestamp()
        signature_payload = f"{self.api_key}{timestamp}{payload}"
        signature = generate_signature(self.secret_key, signature_payload)

        return {
            "Content-Type": "application/json",
            "API-Key": self.api_key,
            "Signature": signature,
            "Timestamp": timestamp,
        }

    def get_report(self, report_id):
        """Fetch a report by ID."""
        url = f"{self.base_url}/reports/{report_id}"
        headers = self._generate_headers("")
        
        try:
            response = requests.get(url, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key or secret key.") from e
            raise RequestError(f"HTTP error: {response.status_code}") from e
        except requests.exceptions.RequestException as e:
            raise RequestError("Request failed.") from e

    # def create_report(self, data):
    #     """Create a new report."""
    #     url = f"{self.base_url}/reports"
    #     payload = json.dumps(data)
    #     headers = self._generate_headers(payload)
        
    #     try:
    #         response = requests.post(url, headers=headers, data=payload, timeout=TIMEOUT)
    #         response.raise_for_status()
    #         return response.json()
    #     except requests.exceptions.HTTPError as e:
    #         if response.status_code == 401:
    #             raise AuthenticationError("Invalid API key or secret key.") from e
    #         raise RequestError(f"HTTP error: {response.status_code}") from e
    #     except requests.exceptions.RequestException as e:
    #         raise RequestError("Request failed.") from e
