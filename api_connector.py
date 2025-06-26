import requests

class APIConnector:
    """Simple API connector that performs GET requests."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    def get(self, endpoint: str, **kwargs):
        """Send a GET request to the specified endpoint and return the JSON response."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, **kwargs)
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    # Example usage; replace 'https://api.example.com' and '/data' as needed
    connector = APIConnector("https://api.example.com")
    try:
        data = connector.get("/data")
        print(data)
    except requests.exceptions.RequestException as exc:
        print(f"API request failed: {exc}")
