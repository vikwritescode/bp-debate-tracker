import requests
from models import SlugRef
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
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to make request.")
    if response.status_code != 200:
        raise RuntimeError(f"[{response.status_code}] unwanted response from tab: {response.reason}")
    
    data = response.json()
    return [SlugRef(name=comp["name"], slug=comp["slug"]) for comp in data]