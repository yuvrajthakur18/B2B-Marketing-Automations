import streamlit as st
from pymongo import MongoClient
from groq import Groq
import os
from dotenv import load_dotenv


# Load environment variables from a .env file
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# MongoDB connection setup
MONGO_URI = os.getenv("MONGO_URI")  
DATABASE_NAME = "lead"  
COLLECTION_NAME = "leads"  

def connect_to_mongo():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    return collection


# Streamlit interface
st.title("Cold Email Generator")

# Connect to MongoDB
collection = connect_to_mongo()

import requests

# Define the API URL for fetching all prospects
api_url = "http://your-backend-url/api/prospects"

# Call the API
try:
    response = requests.get(api_url)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    
    # Parse the JSON response
    prospects = response.json()
    print("Fetched Prospects:", prospects)

except requests.exceptions.RequestException as e:
    print("Error fetching prospects:", e)

# Extract prospect names from the nested structure
prospect_names = [prospect["UnifiedLeadDetails"]["Name"] for prospect in prospects if "UnifiedLeadDetails" in prospect and "Name" in prospect["UnifiedLeadDetails"]]

if prospect_names:
    # Dropdown for selecting a prospect
    selected_name = st.selectbox("Select a prospect", prospect_names)

    # if selected_name:
    #     # Fetch the data for the selected prospect
    #     selected_prospect = fetch_prospect_by_name(collection, selected_name)
        
    #     if selected_prospect:
    #         # Display prospect data
    #         st.subheader("Prospect Details")
            
    #         # Show prospect details : 
    #         with st.expander("View Lead's Details"):
    #             st.json(selected_prospect)  # Full prospect data in JSON format

    #         # Add a button to generate the email
    #         if st.button("Generate Cold Email"):
    #             # Generate the cold email
    #             email = generate_cold_email(selected_prospect, sender_details, sender_company_details)
                
    #             # Display the generated email
    #             st.subheader("Generated Email")
    #             st.text_area("Cold Email", email, height=600)

    #             # Input field for feedback
    #             feedback = st.text_area("Provide Feedback on the Email", height=100)

    #             # Button to save feedback
    #             if st.button("Submit Feedback"):
    #                 # Save the feedback, email, and lead's name into MongoDB
    #                 save_feedback_to_mongo(collection, selected_name, email, feedback)
    #                 st.success("Feedback submitted successfully!")
#         else:
#             st.error("Selected prospect not found in the database.")
# else:
#     st.warning("No prospects found in the database.")