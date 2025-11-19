import requests

def get_slugs(url: str):
    try:
        response = requests.get(f"{url}/api/v1/tournaments")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to make request.")
    if response.status_code != 200:
        raise RuntimeError(f"[{response.status_code}] unwanted response: {response.reason}")
    
    data = response.json()
    return [comp["slug"] for comp in data]
    
    