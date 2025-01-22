# main.py
from datetime import datetime
from SubTrack.utils import load_profiles_from_html, load_existing_data, update_subscription_status, detect_unsubscribed, save_data_to_excel
import pandas as pd

def GetSubscribers(html_file, file_path):
    # Load data from Instagram
    profiles = load_profiles_from_html(html_file)
    
    # Get current data about followers
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Load data about subscribers
    df, existing_unsubscribed = load_existing_data(file_path)
    
    # Update status
    df = update_subscription_status(df, profiles, current_date)
    
    # Find unsubscribers
    unsubscribed = detect_unsubscribed(df, current_date)
    
    # Delete unsubscribers
    if unsubscribed:
        df = df[~df['Profile Name'].isin(unsubscribed)]
    
    # Get new followers
    existing_profiles = set(df['Profile Name'])
    new_subscribers = [p for p in profiles if p not in existing_profiles]
    
    if new_subscribers:
        new_rows = pd.DataFrame({'Profile Name': new_subscribers, current_date: [True] * len(new_subscribers)})
        df = pd.concat([df, new_rows], ignore_index=True)
    
    # Update status
    if unsubscribed:
        unsubscribed = list(set(unsubscribed) - set(existing_unsubscribed))
        existing_unsubscribed.extend(unsubscribed)
    
    # Save data to excel
    save_data_to_excel(df, unsubscribed, file_path, existing_unsubscribed)
    
    print(f"Followers list saved")
    if new_subscribers:
        print("New followers:")
        print(new_subscribers)
    else:
        print("No subscribed.")
    
    if unsubscribed:
        print("The user who unsubscribed:")
        print(unsubscribed)
    else:
        print("No unsubscribed.")

if __name__ == "__main__":
    GetSubscribers("subs.html", 'profiles.xlsx')