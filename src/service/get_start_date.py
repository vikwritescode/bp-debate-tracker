from utils import correct_url
import requests
from models import TabAuthError, StartNotFoundError
def get_start_date(tab_url, slug):
    """
    Gets the start date for a tournament
    
    :param tab_url: Description
    :param slug: Description
    """
    url = correct_url(tab_url)
    try:
        response = requests.get(f"{url}/api/v1/tournaments/{slug}/rounds/1")
        if not response.ok:
            raise RuntimeError("Error Fetching data!")
        round_data = response.json()
        
        if round_data.get("starts_at", None) is None:
            raise StartNotFoundError
        return round_data["starts_at"].split("T")[0]
    except requests.HTTPError as e:
        if e.response.status_code == 401:
            raise TabAuthError
    except Exception as e:
        raise