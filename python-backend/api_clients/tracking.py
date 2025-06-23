import requests

class Tracking:
    @staticmethod
    def get_tracking_data(tracking_code: str) -> dict | None:
        try:
            url = f'http://localhost:3001/tracking/{tracking_code}'
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json() 
        except requests.RequestException as e:
            return None
