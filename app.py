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

# Function to transform prospect data into the required JSON structure
def transform_prospect_data(prospect):
    def format_section(title, data, color, keys_to_remove=None):
        """Filters the data by removing specified keys and then formats it."""
        # Remove unwanted keys
        if keys_to_remove:
            data = {k: v for k, v in data.items() if k not in keys_to_remove}

        # Format the filtered data into a string    
        section_lines = [f"<h3 style='color:{color}'>{title}:</h3>"]  # Use <h3> for title styling
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    # Convert list items to strings, join with a comma
                    value = ", ".join([str(item) for item in value])
                elif isinstance(value, dict):
                    # Flatten dictionary to string
                    value = str(value)
                section_lines.append(f"<p><strong>{key}:</strong> {value}</p>")  # Use <p> and <strong> for styling
        elif isinstance(data, list):
            # Handle case where data is a list
            for item in data:
                section_lines.append(f"<p>{item}</p>")  # Each list item is in a <p> with line breaks
        else:
            # Handle other data types (e.g., string or None)
            section_lines.append(f"<p>{str(data)}</p>")

        return "".join(section_lines)

    # Define the keys to remove from UnifiedLeadDetails and UnifiedCompanyDetails
    lead_keys_to_remove = ["other information", "past experience"]
    company_keys_to_remove = ["key activities"]

    # Format the data for Lead and Company details
    unified_lead_details = format_section(
        "Unified Lead Details", 
        prospect.get("UnifiedLeadDetails", {}),
        color="green",
        keys_to_remove=lead_keys_to_remove
    )
    unified_company_details = format_section(
        "Unified Company Details", 
        prospect.get("UnifiedCompanyDetails", {}),
        color="green",
        keys_to_remove=company_keys_to_remove
    )
    lead_recent_posts = format_section(
        "Lead Recent Posts",
        prospect.get("LeadRecentPosts", {}),
        color="green"
    )
    company_recent_posts = format_section(
        "Company Recent Posts",
        prospect.get("CompanyRecentPosts", {}),
        color="green"
    )
    recent_projects_and_work = format_section(
        "Recent Projects and works",
        prospect.get("RecentProjectsAndWork", {}),
        color="green"
    )
    keywords = format_section(
        "Keywords",
        prospect.get("Keywords", {}),
        color="green"
    )
    references = f"<h4 style='color:red;'><b>References</b></h4><p>{', '.join(prospect.get('References', [])) if prospect.get('References') else 'N/A'}</p>"

    # # Display the formatted sections with applied styles using st.markdown
    # return f"""
    #     <div>{unified_lead_details}</div>
    #     <div>{unified_company_details}</div>
    #     <div>{lead_recent_posts}</div>
    #     <div>{company_recent_posts}</div>
    #     <div>{recent_projects_and_work}</div>
    #     <div>{keywords}</div>
    #     <div>{references}</div>
    # """

    return {
        "Unified Lead Details": unified_lead_details,
        "Unified Company Details": unified_company_details,
        "Lead Recent Posts": lead_recent_posts,
        "Company Recent Posts": company_recent_posts,
        "Recent Projects and Works": recent_projects_and_work,
        "Keywords": keywords,
        "References": references
    }


    
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
                transformed_data = transform_prospect_data(selected_prospect)
                st.subheader("Prospect Details")
                
                # Create a main expander for viewing data (optional)
                for section_title, section_content in transformed_data.items():
                    with st.expander(section_title):
                        st.markdown(section_content, unsafe_allow_html=True)

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
                feedback_container = st.empty()  # This container will be used to reset the input field

                with feedback_container.form("feedback_form"):
                    # Text area for feedback, no session state required
                    feedback = st.text_area("Provide Feedback on the Email", height=100)

                    # Button to submit feedback
                    submitted = st.form_submit_button("Submit Feedback")

                    if submitted:
                        if not st.session_state.get("email_id"):
                            st.error("First generate an email")
                        else:
                            # Prepare the data for the feedback API
                            feedback_data = {
                                "email_id": st.session_state["email_id"],
                                "comment": feedback,  # Directly use the value from the input
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

                                # Manually clear the form by resetting the container
                                feedback_container.empty()  # This will clear the feedback input

                            except requests.exceptions.RequestException as e:
                                st.error(f"Error submitting feedback: {e}")
                        
            else:
                st.error("Selected prospect not found in the database.")
    else:
        st.warning("No prospects found in the database.")
    
except requests.exceptions.RequestException as e:
    print("Error fetching prospects:", e)
