import requests
from models import SlugRef
def get_tournaments(url: str) -> list:
    """
    Docstring for get_tournaments
    
    :param url: tab URL
    :type url: str
    :return: list of tournaments
    :rtype: list
    """
    print(f"{url}/api/v1/tournaments")
    try:
        response = requests.get(f"{url}/api/v1/tournaments")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to make request.")
    if response.status_code != 200:
        raise RuntimeError(f"[{response.status_code}] unwanted response from tab: {response.reason}")
    
    data = response.json()
    return [SlugRef(name=comp["name"], slug=comp["slug"]) for comp in data]