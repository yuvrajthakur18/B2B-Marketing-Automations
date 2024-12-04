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
get_all_prospects = "http://172.190.96.197:5000/api/leads/"

# Call the API
try:
    response = requests.get(get_all_prospects)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    
    # Parse the JSON response
    prospects = response.json()
    # Get list of prospects names

    # Extract prospect names and map them to their corresponding object IDs
    prospect_map = {
        prospect["UnifiedLeadDetails"]["Name"]: prospect["_id"]
        for prospect in prospects
        if "UnifiedLeadDetails" in prospect and "Name" in prospect["UnifiedLeadDetails"]
    }

    if prospect_map:
        # Dropdown for selecting a prospect
        selected_name = st.selectbox("Select a prospect", list(prospect_map.keys()))
        selected_obj_id = prospect_map[selected_name]

        if selected_name:
            # Fetch the data for the selected prospect
            # Filter the selected object
            selected_prospect = next(
                (prospect for prospect in prospects if prospect["_id"] == selected_obj_id), None
            )
            
            if selected_prospect:
                # Display prospect data
                st.subheader("Prospect Details")
                
                # Show prospect details : 
                with st.expander("View Lead's Details"):
                    st.json(selected_prospect)  # Full prospect data in JSON format

                # # Add a button to show all emails for the selected prospect
                # if st.button("Show All Emails"):
                #     # Fetch emails for the selected lead
                #     try:
                #         emails_url = f"http://172.190.96.197:5000/api/emails/lead/{selected_obj_id}"
                #         email_response = requests.get(emails_url)
                #         email_response.raise_for_status()  # Raise error for bad responses

                #         # Parse the email response
                #         emails = email_response.json()

                #         if emails:
                #             st.subheader("Emails for this Prospect")
                #             st.write(emails)  # Show all emails (you can format it as needed)
                #         else:
                #             st.write("No emails found for this prospect.")
                #     except requests.exceptions.RequestException as e:
                #         st.error(f"Error fetching emails: {e}")

                # Add a session state variable for email_id
                if "email_id" not in st.session_state:
                    st.session_state["email_id"] = None

                # Add a button to generate the email
                if st.button("Generate Cold Email"):
                    # Email generation API call
                    generate_email_api_url = "http://172.190.96.197:5000/api/emails/generate"
                    
                    try:
                        # Send the request to the email generation API
                        email_response = requests.post(
                            generate_email_api_url,
                            json={"lead_id": selected_obj_id}  # Pass prospect data as payload
                        )
                        email_response.raise_for_status()  # Raise error for bad responses

                        # Parse the response to get the email content and ID
                        response_data = email_response.json()
                        st.session_state["email_id"] = response_data.get("email_id")  # Store in session state
                        generated_email = response_data.get("email_content")

                        if not st.session_state["email_id"]:
                            st.error("No email_id returned in the response.")
                        else:
                            st.success("Email generated successfully!")
                                            
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error generating email: {e}")

                    # Display the generated email
                    st.subheader("Generated Email")
                    st.text_area("Cold Email", generated_email, height=600)

                # Input field for feedback and form submission
                with st.form("feedback_form"):
                    # Input field for reviewer name
                    reviewer_name = st.text_input("Reviewer Name", value="")  # New field for reviewer name

                    feedback = st.text_area("Provide Feedback on the Email", height=100)

                    # Button to submit feedback
                    submitted = st.form_submit_button("Submit Feedback")

                    if submitted:
                        if not st.session_state["email_id"]:
                            st.error("First generate an email")
                        elif not reviewer_name.strip():
                            st.error("Reviewer name is required.")
                        else:
                            # Prepare the data for the feedback API
                            feedback_data = {
                                "email_id": st.session_state["email_id"],
                                "comment": feedback,
                                "person_name": reviewer_name.strip()
                            }
                        
                            try:
                                # Call the feedback API
                                feedback_api_url = "http://172.190.96.197:5000/api/feedbacks/create"
                                feedback_response = requests.post(
                                    feedback_api_url, 
                                    json=feedback_data
                                )
                                feedback_response.raise_for_status()
                                st.success("Feedback submitted successfully!")
                            except requests.exceptions.RequestException as e:
                                st.error(f"Error submitting feedback: {e}")
        
            else:
                st.error("Selected prospect not found in the database.")
    else:
        st.warning("No prospects found in the database.")
    
except requests.exceptions.RequestException as e:
    print("Error fetching prospects:", e)
