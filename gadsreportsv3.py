import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.title("Google Ads Account and Campaign Performance Report")

st.subheader('Instructions')
st.markdown('Login to Windsor AI and download a CSV file with Google Ads data of the clients you want yo analyze.')
st.markdown(
    'Include the following columns in the Windsor AI report: 1) Account Name, 2) Campaign, 3) Campaign Status, 4) Clicks, 5) Conversions, 6) Cost, 7) Date, 8) Impressions, 9) Search Impression Share, 10, 11, 12) the Search Budget metrics, and 13, 14, 15) the Search Rank metrics.')
st.markdown('Upload the exported CSV file in the box below.')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    # Load the CSV file
    df = pd.read_csv(uploaded_file)

    # Renaming columns to standard names used in the script
    df.rename(columns={
        'account_name': 'Account',
        'campaign': 'Campaign',
        'date': 'Date',
        'clicks': 'Clicks',
        'impressions': 'Impressions',
        'ctr': 'CTR',
        'average_cpc': 'Avg CPC',
        'cost': 'Cost',
        'conversions': 'Conversions',
        'conversion_rate': 'Conv. Rate',
        'cost_per_conversion': 'Cost/Conv.',
        'search_impression_share': 'Search Imp. Share',
        'search_budget_lost_absolute_top_impression_share': 'Search Budget Lost Abs Top Imp Share',
        'search_budget_lost_impression_share': 'Search Budget Lost Imp Share',
        'search_budget_lost_top_impression_share': 'Search Budget Lost Top Imp Share',
        'search_rank_lost_absolute_top_impression_share': 'Search Rank Lost Abs Top Imp Share',
        'search_rank_lost_impression_share': 'Search Rank Lost Imp Share',
        'search_rank_lost_top_impression_share': 'Search Rank Lost Top Imp Share'
    }, inplace=True)

    # Convert the date column to datetime with the correct format
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

    # Handle NaN values and convert columns to numeric
    df['Clicks'] = pd.to_numeric(df['Clicks'], errors='coerce').fillna(0)
    df['Impressions'] = pd.to_numeric(df['Impressions'], errors='coerce').fillna(0)
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce').fillna(0)
    df['Conversions'] = pd.to_numeric(df['Conversions'], errors='coerce').fillna(0)
    df['Search Imp. Share'] = pd.to_numeric(df['Search Imp. Share'], errors='coerce').fillna(0)
    df['Search Budget Lost Abs Top Imp Share'] = pd.to_numeric(df['Search Budget Lost Abs Top Imp Share'], errors='coerce').fillna(0)
    df['Search Budget Lost Imp Share'] = pd.to_numeric(df['Search Budget Lost Imp Share'], errors='coerce').fillna(0)
    df['Search Budget Lost Top Imp Share'] = pd.to_numeric(df['Search Budget Lost Top Imp Share'], errors='coerce').fillna(0)
    df['Search Rank Lost Abs Top Imp Share'] = pd.to_numeric(df['Search Rank Lost Abs Top Imp Share'], errors='coerce').fillna(0)
    df['Search Rank Lost Imp Share'] = pd.to_numeric(df['Search Rank Lost Imp Share'], errors='coerce').fillna(0)
    df['Search Rank Lost Top Imp Share'] = pd.to_numeric(df['Search Rank Lost Top Imp Share'], errors='coerce').fillna(0)

    # Extract month and year from the date
    df['YearMonth'] = df['Date'].dt.to_period('M')

    # Aggregate data at the account level
    account_df = df.groupby(['Account', 'YearMonth']).agg({
        'Clicks': 'sum',
        'Impressions': 'sum',
        'Cost': 'sum',
        'Conversions': 'sum',
        'Search Imp. Share': 'mean',
        'Search Budget Lost Abs Top Imp Share': 'mean',
        'Search Budget Lost Imp Share': 'mean',
        'Search Budget Lost Top Imp Share': 'mean',
        'Search Rank Lost Abs Top Imp Share': 'mean',
        'Search Rank Lost Imp Share': 'mean',
        'Search Rank Lost Top Imp Share': 'mean'
    }).reset_index()

    # Calculate metrics for account level
    account_df['CTR'] = account_df['Clicks'] / account_df['Impressions']
    account_df['Avg CPC'] = account_df['Cost'] / account_df['Clicks']
    account_df['Conv. Rate'] = account_df['Conversions'] / account_df['Clicks']
    account_df['Cost/Conv.'] = account_df['Cost'] / account_df['Conversions']

    # Add status columns for account level
    account_df['CTR Status'] = account_df['CTR'].apply(lambda x: 'Needs attention' if x < 0.09 else 'Ok')
    account_df['Conv. Rate Status'] = account_df['Conv. Rate'].apply(lambda x: 'Needs attention' if x < 0.05 else 'Ok')
    account_df['Cost/Conv. Status'] = account_df['Cost/Conv.'].apply(lambda x: 'Needs attention' if x > 150 else 'Ok')

    # Order columns for account level
    account_columns = [
        'Account', 'YearMonth', 'Clicks', 'Impressions', 'CTR', 'CTR Status', 'Avg CPC',
        'Cost', 'Conversions', 'Conv. Rate', 'Conv. Rate Status', 'Cost/Conv.', 'Cost/Conv. Status',
        'Search Imp. Share', 'Search Budget Lost Imp Share', 'Search Budget Lost Top Imp Share',
        'Search Budget Lost Abs Top Imp Share', 'Search Rank Lost Imp Share', 'Search Rank Lost Top Imp Share',
        'Search Rank Lost Abs Top Imp Share'
    ]
    account_df = account_df[account_columns]

    # Save account level data to CSV
    account_csv = account_df.to_csv(index=False).encode('utf-8')

    # Aggregate data at the campaign level
    campaign_df = df.groupby(['Account', 'Campaign', 'YearMonth']).agg({
        'Clicks': 'sum',
        'Impressions': 'sum',
        'Cost': 'sum',
        'Conversions': 'sum',
        'Search Imp. Share': 'mean',
        'Search Budget Lost Abs Top Imp Share': 'mean',
        'Search Budget Lost Imp Share': 'mean',
        'Search Budget Lost Top Imp Share': 'mean',
        'Search Rank Lost Abs Top Imp Share': 'mean',
        'Search Rank Lost Imp Share': 'mean',
        'Search Rank Lost Top Imp Share': 'mean'
    }).reset_index()

    # Calculate metrics for campaign level
    campaign_df['CTR'] = campaign_df['Clicks'] / campaign_df['Impressions']
    campaign_df['Avg CPC'] = campaign_df['Cost'] / campaign_df['Clicks']
    campaign_df['Conv. Rate'] = campaign_df['Conversions'] / campaign_df['Clicks']
    campaign_df['Cost/Conv.'] = campaign_df['Cost'] / campaign_df['Conversions']

    # Add status columns for campaign level
    campaign_df['CTR Status'] = campaign_df['CTR'].apply(lambda x: 'Needs attention' if x < 0.09 else 'Ok')
    campaign_df['Conv. Rate Status'] = campaign_df['Conv. Rate'].apply(lambda x: 'Needs attention' if x < 0.05 else 'Ok')
    campaign_df['Cost/Conv. Status'] = campaign_df['Cost/Conv.'].apply(lambda x: 'Needs attention' if x > 150 else 'Ok')

    # Order columns for campaign level
    campaign_columns = [
        'Account', 'Campaign', 'YearMonth', 'Clicks', 'Impressions', 'CTR', 'CTR Status', 'Avg CPC',
        'Cost', 'Conversions', 'Conv. Rate', 'Conv. Rate Status', 'Cost/Conv.', 'Cost/Conv. Status',
        'Search Imp. Share', 'Search Budget Lost Imp Share', 'Search Budget Lost Top Imp Share',
        'Search Budget Lost Abs Top Imp Share', 'Search Rank Lost Imp Share', 'Search Rank Lost Top Imp Share',
        'Search Rank Lost Abs Top Imp Share'
    ]
    campaign_df = campaign_df[campaign_columns]

    # Save campaign level data to CSV
    campaign_csv = campaign_df.to_csv(index=False).encode('utf-8')

    # Create a directory for charts
    charts_dir = "charts"
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)

    # Display tables and download buttons with account level data and campaign level data
    st.subheader('Account Level Table')
    st.dataframe(account_df)
    st.download_button(
        label="Download Account Level Data as CSV",
        data=account_csv,
        file_name='account_level_data.csv',
        mime='text/csv'
    )

    st.subheader('Campaign Level Table')
    st.dataframe(campaign_df)
    st.download_button(
        label="Download Campaign Level Data as CSV",
        data=campaign_csv,
        file_name='campaign_level_data.csv',
        mime='text/csv'
    )

    # Display plots and save images for account level performance
    st.subheader('Account Level Performance Charts')
    for account in account_df['Account'].unique():
        account_data = account_df[account_df['Account'] == account]
        st.text(f"Account: {account}")
        plt.figure(figsize=(10, 6))
        plt.plot(account_data['YearMonth'].astype(str), account_data['Clicks'], marker='o', linestyle='-', label='Clicks')
        for i, txt in enumerate(account_data['Clicks']):
            plt.annotate(f"{txt:.2f}", (account_data['YearMonth'].astype(str).iloc[i], account_data['Clicks'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')
        plt.plot(account_data['YearMonth'].astype(str), account_data['Conversions'], marker='o', linestyle='-', label='Conversions')
        for i, txt in enumerate(account_data['Conversions']):
            plt.annotate(f"{txt:.2f}", (account_data['YearMonth'].astype(str).iloc[i], account_data['Conversions'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')
        plt.title(f'Clicks and Conversions Over Time for {account}')
        plt.xlabel('YearMonth')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        chart_path = os.path.join(charts_dir, f'{account}_account_performance.png')
        plt.savefig(chart_path)
        st.pyplot(plt)

    # Display plots and save images for campaign level performance
    st.subheader('Campaign Level Performance Charts')
    for account in campaign_df['Account'].unique():
        account_data = campaign_df[campaign_df['Account'] == account]
        st.text(f"Account: {account}")
        for campaign in account_data['Campaign'].unique():
            campaign_data = account_data[account_data['Campaign'] == campaign]
            st.text(f"Campaign: {campaign}")
            plt.figure(figsize=(10, 6))
            plt.plot(campaign_data['YearMonth'].astype(str), campaign_data['Clicks'], marker='o', linestyle='-', label='Clicks')
            for i, txt in enumerate(campaign_data['Clicks']):
                plt.annotate(f"{txt:.2f}", (campaign_data['YearMonth'].astype(str).iloc[i], campaign_data['Clicks'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')
            plt.plot(campaign_data['YearMonth'].astype(str), campaign_data['Conversions'], marker='o', linestyle='-', label='Conversions')
            for i, txt in enumerate(campaign_data['Conversions']):
                plt.annotate(f"{txt:.2f}", (campaign_data['YearMonth'].astype(str).iloc[i], campaign_data['Conversions'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')
            plt.title(f'Clicks and Conversions Over Time for {account} - {campaign}')
            plt.xlabel('YearMonth')
            plt.ylabel('Count')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.legend()
            chart_path = os.path.join(charts_dir, f'{account}_{campaign}_campaign_performance.png')
            plt.savefig(chart_path)
            st.pyplot(plt)