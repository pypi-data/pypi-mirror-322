import dis
import requests
import pandas as pd

class Unifier:
    """A class to interact with the Unifier API."""
    
    url = 'https://unifier.exponential-tech.ai/unifier'
    user = ''
    token = ''

    __version__ = '0.1.6'

    @classmethod
    def get_asof_dates(cls, name):
        """Get a list of available asof dates for a given name."""
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            'name': name,
            'user': cls.user,
            'token': cls.token,
        }

        _url = cls.url + '/get_asof_date'
        try:
            response = requests.post(_url, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()
            if 'error' in response_data:
                print("Error:", response_data['error'])
                return []
            return pd.DataFrame(response_data)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []


    @classmethod
    def query(cls, name, user=None, token=None, key=None, keys=None, as_of=None, back_to=None, up_to=None, asof_date=None, limit=None, disable_view=False):
        """Query the Unifier API and return the response data."""
        
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            'name': name,
            'user': cls.user,
            'token': cls.token,
            'disable_view': disable_view,
        }

        if limit:
            payload['limit'] = limit
        
        if key is not None:
            payload['key'] = key
        if keys is not None:
            payload['keys'] = keys
        if token is not None:
            payload['token'] = token
        if user is not None:
            payload['user'] = user
        
        # as_of param is deprecated and will be removed in future
        if as_of is not None:
            payload['asof_date'] = as_of
        if back_to is not None:
            payload['back_to'] = back_to
        if up_to is not None:
            payload["up_to"] = up_to
        if asof_date is not None:
            payload['asof_date'] = asof_date

        try:
            response = requests.post(cls.url, headers=headers, json=payload)
            if response.status_code != 200:
                err = response.json()
                if 'error' in err:
                    print(err['error'])
                    return {}
                
                print(f"Request failed with status code {response.status_code}")
                return {}
            response_data = response.json()
            return response_data
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {}

    @classmethod
    def get_dataframe(cls, name, user=None, token=None, key=None, keys=None, as_of=None, back_to=None, up_to=None, asof_date=None, limit=None, disable_view=False):
        """Get the query result as a pandas DataFrame."""
        
        json_result = cls.query(name, user, token, key, keys, as_of, back_to, up_to, asof_date, limit, disable_view)
        return pd.DataFrame.from_dict(json_result)
