import logging
from User_fetcher import UserFetcher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

__name__ = "__main__"

list_of_users = UserFetcher().fetch_all_users()
logging.info(f"List of users: {list_of_users}")
