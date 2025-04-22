import requests
import config
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class UserFetcher:
    def __init__(self, base_url=config.BASE_URL, identity=config.Username, secret=config.Password):
        """
        Initializes the UserFetcher with a base URL and credentials.
        """
        if not base_url:
            raise ValueError("Base URL cannot be empty.")
        if not isinstance(base_url, str):
            raise TypeError("Base URL must be a string.")
        if not base_url.startswith("http"):
            raise ValueError("Base URL must start with 'http' or 'https'.")

        self.base_url = base_url
        self.identity = identity
        self.secret = secret

        logging.info(f"UserFetcher initialized with base_url: {self.base_url}")

    def fetch_auth_token(self):
        """
        Fetches the authentication token from the API.
        :return: A dict with 'access_token' and 'refresh_token' if successful, None otherwise.
        """
        url = f"{self.base_url}/users/token/issue"
        try:
            response = requests.post(url, json={
                "identity": self.identity,
                "secret": self.secret
            })

            response.raise_for_status()
            token_data = response.json()

            access_token = token_data.get("access_token")
            refresh_token = token_data.get("refresh_token")

            if access_token and refresh_token:
                logging.info("Authentication tokens fetched successfully.")
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            else:
                logging.error("Missing access or refresh token in the response.")
                return None

        except requests.RequestException as e:
            logging.error(f"Error fetching auth token: {e}")
            return None
        except ValueError as e:
            logging.error(f"Error parsing token response: {e}")
            return None

    def fetch_all_users(self):
        """
        Fetches all users from the API.
        :return: A list of users if the request is successful, None otherwise.
        """
        tokens = self.fetch_auth_token()
        if not tokens or not tokens.get("access_token"):
            logging.error("Failed to fetch users: no valid auth token.")
            return None

        url = f"{self.base_url}/users"
        try:
            response = requests.get(
                url,
                params={"status": "enabled"},
                headers={"Authorization": f"Bearer {tokens['access_token']}"}
            )
            response.raise_for_status()
            logging.info("Fetched user list successfully.")
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error fetching users: {e}")
            return None
        except ValueError as e:
            logging.error(f"Error parsing user list response: {e}")
            return None
