import streamlit as st
import pandas as pd

# Function to process the uploaded file and calculate what needs to be restocked
def process_file(file):
    # Read the Excel file
    df = pd.read_excel(file)
    
    # Check if the required columns exist
    if 'Product' not in df.columns or 'Quantity (Current)' not in df.columns or 'Required' not in df.columns:
        st.error("The Excel file must contain 'Product', 'Quantity (Current)', and 'Required' columns.")
        return None
    
    # Calculate the difference between required and current quantities
    df['Restock'] = df['Required'] - df['Quantity (Current)']
    
    # Set any negative values to 0 (can't restock negative quantities)
    df['Restock'] = df['Restock'].apply(lambda x: max(x, 0))
    
    # Filter products that need restocking
    restock_df = df[df['Restock'] > 0]
    
    return restock_df

# Streamlit file uploader
st.title("Inventory Restock Suggestion")
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Process the uploaded file
    restock_df = process_file(uploaded_file)
    
    if restock_df is not None:
        # Display the processed data (restock suggestions)
        st.write("Products that need to be restocked:")
        st.dataframe(restock_df)
        
        # Provide option to download the restock list as a new Excel file
        output_file_path = "/mnt/data/restock_list.xlsx"
        restock_df.to_excel(output_file_path, index=False)
        
        st.download_button(
            label="Download Restock List",
            data=open(output_file_path, "rb").read(),
            file_name="restock_list.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Prepare an email message with the restock items
        email_message = "Dear Team,\n\nThe following products need to be restocked:\n_
