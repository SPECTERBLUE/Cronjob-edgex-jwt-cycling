import logging
from User_fetcher import UserFetcher

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

__name__ = "__main__"

list_of_users = UserFetcher().fetch_all_users()

users = list_of_users.get("users")
if users and isinstance(users, list):
    logging.info(f"Number of users fetched: {len(users)}")

    # Extract credentials from each user
    credentials_list = [user.get("credentials") for user in users if "credentials" in user]

    logging.info(f"Credentials extracted: {credentials_list}")
else:
    logging.error("No users found or invalid response format.")
    
usernames_list = [credentials_list.get("identity") for credentials_list in credentials_list if "identity" in credentials_list]
logging.info(f"Usernames_list extracted: {usernames_list}")

edgexname_list = [usernames_list.split("@",1) for usernames_list in usernames_list if "@" in usernames_list]
edgexname_list = [edgexname[0] for edgexname in edgexname_list if len(edgexname) > 0]
edgexname_list.append("admin")
logging.info(f"edgexname_list extracted: {edgexname_list}")



