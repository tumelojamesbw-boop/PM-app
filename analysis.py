import streamlit as st
from data import load_and_merge_data
from streamlit_extras.dataframe_explorer import dataframe_explorer
import pandas as pd
from visuals.summary_cards import show_summary_cards
from visuals.summary_charts import show_summary_charts
from visuals.gantt_chart import show_gantt_chart


def HomePage():
    st.header("📊 Project Tracking Dashboard", divider="rainbow")
    st.markdown(
        "<h3 style='background: inherit; padding:10px; border-radius:8px; text-align:center;'> Centralized Services</h3>", 
        unsafe_allow_html=True
    )
    
    

    # Load merged dataset
    merged_df = load_and_merge_data()

    # Display last update
    last_update = pd.to_datetime(merged_df['Last_Updated'].max())
    st.caption(f"Last Updated: {last_update.strftime('%d %B %Y')}")

    # Clean and normalize date columns
    date_cols = [
        'Est_Start', 'Est_End', 'Act_Start', 'Act_End',
        'Start_Date', 'End_Date', 'Last_Updated'
    ]

    for col in date_cols:
        if col in merged_df.columns:
            merged_df[col] = (
                pd.to_datetime(merged_df[col], errors='coerce', dayfirst=True)
                .dt.normalize()
            )

    # Clean column names and percentage field
    merged_df.columns = (
        merged_df.columns
        .str.strip()
        .str.replace(' ', '_')
        .str.replace('%', 'percent')
    )

    if 'percent_complete' in merged_df.columns:
        merged_df['percent_complete'] = (
            merged_df['percent_complete']
            .astype(str)
            .str.replace('%', '', regex=False)
        )
        merged_df['percent_complete'] = pd.to_numeric(
            merged_df['percent_complete'], errors='coerce'
        )

    # Convert numeric columns
    num_cols = [
        'Delay_Days', 'Planned_Duration', 'Actual_Duration',
        'Budgeted_Cost', 'Actual_Cost', 'Hours_Allocated',
        'Hours_Worked', 'Cost_of_Hours_Worked', 'Variance'
    ]
    for col in num_cols:
        if col in merged_df.columns:
            merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

    # Fill missing numeric values with 0
    numeric_fill_zero = num_cols
    for col in numeric_fill_zero:
        if col in merged_df.columns:
            merged_df[col] = merged_df[col].fillna(0)

    # Fill missing object (string) columns with "Unknown"
    obj_cols = merged_df.select_dtypes(include='object').columns
    for col in obj_cols:
        merged_df[col] = merged_df[col].fillna('Unknown')

    # Drop duplicates and show cleanup summary
    before = len(merged_df)
    merged_df.drop_duplicates(inplace=True)
    after = len(merged_df)

   

    # Render visuals
    show_summary_cards(merged_df)
    show_summary_charts(merged_df)
    show_gantt_chart(merged_df)



    









  



    
 

   




    


   












