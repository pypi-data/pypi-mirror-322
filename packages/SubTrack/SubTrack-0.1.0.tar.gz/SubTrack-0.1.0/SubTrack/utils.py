# utils.py
import pandas as pd
from datetime import datetime
import os
from bs4 import BeautifulSoup

def load_profiles_from_html(file_path):
    """Parse html and get data about followers"""
    with open(file_path, "r") as w:
        soup = BeautifulSoup(w, "html.parser")
    
    profiles = set()
    profile_links = soup.find_all('a', href=True)
    for link in profile_links:
        href = link['href']
        if href.startswith('/'):
            profile_name = href.strip('/').split('/')[0]
            if profile_name != "":
                profiles.add(profile_name)
    return list(profiles)

def load_existing_data(file_path):
    """Load data from Excel file"""
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path, sheet_name='Subscribers')
        except ValueError:
            df = pd.DataFrame(columns=['Profile Name'])
        
        try:
            unsubscribed_df = pd.read_excel(file_path, sheet_name='Unsubscribed')
            existing_unsubscribed = unsubscribed_df['Unsubscribed Profiles'].tolist()
        except ValueError:
            existing_unsubscribed = []
    else:
        df = pd.DataFrame(columns=['Profile Name'])
        existing_unsubscribed = []
    return df, existing_unsubscribed

def update_subscription_status(df, profiles, current_date):
    """Update status to followers"""
    df[current_date] = df['Profile Name'].apply(lambda x: x in profiles)
    return df

def detect_unsubscribed(df, current_date):
    """Check unfollofers"""
    if len(df.columns) > 2:  
        unsubscribed = df.loc[(~df[current_date]) & (df.iloc[:, -2]), 'Profile Name'].tolist()
    else:
        unsubscribed = []
    return unsubscribed

def save_data_to_excel(df, unsubscribed, file_path, existing_unsubscribed):
    """Save data about followers and unfollowers to Excel."""
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, sheet_name='Subscribers', index=False)
        
        if existing_unsubscribed:
            unsubscribed_df = pd.DataFrame({'Unsubscribed Profiles': existing_unsubscribed})
            unsubscribed_df.to_excel(writer, sheet_name='Unsubscribed', index=False)