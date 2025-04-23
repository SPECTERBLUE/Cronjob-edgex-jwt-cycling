import logging
from User_fetcher import UserFetcher
import json
import os

#  Set this to True to remove users not in current API response
REMOVE_OLD_USERS = True

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":

    list_of_users = UserFetcher().fetch_all_users()

    users = list_of_users.get("users")
    if users and isinstance(users, list):
        logging.info(f"Number of users fetched: {len(users)}")

        credentials_list = [user.get("credentials") for user in users if "credentials" in user]
        logging.info(f"Credentials extracted: {credentials_list}")
    else:
        logging.error("No users found or invalid response format.")
        credentials_list = []

    usernames_list = [cred["identity"] for cred in credentials_list if "identity" in cred]
    logging.info(f"Usernames_list extracted: {usernames_list}")

    # Extract actual usernames from email
    current_usernames = {email.split("@", 1)[0] for email in usernames_list if "@" in email}
    current_usernames.add("admin")  # Always include admin

    # Load existing data
    existing_data = {}
    if os.path.exists("edgex_users.json"):
        try:
            with open("edgex_users.json", "r") as f:
                existing_users = json.load(f)
                existing_data = {entry["username"]: entry["token"] for entry in existing_users}
                logging.info("Existing edgex_users.json loaded.")
        except Exception as e:
            logging.error(f"Error reading existing JSON: {e}")

    # Merge or preserve data
    edgex_user_data = []
    for username in current_usernames:
        token = existing_data.get(username, "")
        edgex_user_data.append({
            "username": username,
            "token": token
        })

    # If REMOVE_OLD_USERS is False, keep old ones not in API
    if not REMOVE_OLD_USERS:
        for username, token in existing_data.items():
            if username not in current_usernames:
                edgex_user_data.append({
                    "username": username,
                    "token": token
                })
        logging.info("Old users retained.")

    # Write back
    try:
        with open("edgex_users.json", "w") as f:
            json.dump(edgex_user_data, f, indent=4)
        logging.info("edgex_users.json updated successfully.")
    except Exception as e:
        logging.error(f"Error writing to JSON file: {e}")
