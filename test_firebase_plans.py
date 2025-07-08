import os
import json
from Agents.firebase_plans import get_user_plans

if __name__ == "__main__":
    user_id = input("Enter user ID to fetch plans: ")
    plans = get_user_plans(user_id)
    print(f"\nFound {len(plans)} plan(s) for user '{user_id}':\n")
    print(json.dumps(plans, indent=2))
    
