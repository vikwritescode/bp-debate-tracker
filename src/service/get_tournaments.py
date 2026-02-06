import requests
from models import SlugRef, TabAuthError
from utils import correct_url
def get_tournaments(url: str) -> list:
    """
    Docstring for get_tournaments
    
    :param url: tab URL
    :type url: str
    :return: list of tournaments
    :rtype: list
    """
    fixed_url = correct_url(url)
    print(f"{fixed_url}/api/v1/tournaments")
    try:
        response = requests.get(f"{fixed_url}/api/v1/tournaments")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        if e.response.status_code == 401:
            raise TabAuthError
        raise RuntimeError(f"Failed to make request.")

    
    data = response.json()
    return [SlugRef(name=comp["name"], slug=comp["slug"]) for comp in data]