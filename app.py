import streamlit as st
from pymongo import MongoClient
from groq import Groq
import os
from dotenv import load_dotenv



# Load environment variables from a .env file
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

sender_details = {
    "UnifiedLeadDetails": {
        "Name": "Neeraj Kumar",
        "Title": "Founder and CEO, Valuebound",
        "Email": "null",
        "ProfessionalRole": "Founder and CEO",
        "Location": "Bengaluru, Karnataka, India",
        "Industry": "IT Services and IT Consulting",
        "RelevantSkills": [
            "Drupal Development",
            "Digital Experience Platforms",
            "Cloud-Native Application Development",
            "AWS Services",
            "Project Management",
            "Content Management",
            "Customer Experience",
            "System Integration",
            "AI",
            "Sales",
            "Business Growth",
            "Leadership"
        ],
        "OtherInformation": [
            "8K followers on LinkedIn",
            "500+ connections on LinkedIn",
            "AWS Certified Cloud Practitioner (Aug 2020)",
            "Project Management Professional (PMP) (Jun 2013 - Jun 2016)",
            "Author of \"Drupal 8 Development: Beginner's Guide - Second Edition\"",
            "16+ years of experience leading Valuebound"
        ]
    },
    "LeadRecentPosts": [
        {
            "Title": "Struggling to bring all your customer data together across channels?",
            "URL": "null",
            "Date": "2w ago",
            "Summary": "Highlights the challenges of managing customer data across different channels, leading to wasted time and energy on repetitive tasks. Promotes Valuebound's automation services to address this issue, freeing up team time for high-impact work.",
            "Tone": "Problem/Solution, Professional",
            "Metrics": "10 Likes"
        },
        {
            "Title": "Learning from an Unexpected Quarter: A Different Approach to Growth Through Strategic Partnerships",
            "URL": "null",
            "Date": "1mo ago",
            "Summary": "Shares an experience from a job interview where a candidate suggested a different approach to business development: focusing on a specific core strength and building strategic partnerships around it.",
            "Tone": "Reflective, Inspirational",
            "Metrics": "131 Comments"
        },
        {
            "Title": "We were loyal to one bookstore for years - until a single experience changed everything.",
            "URL": "null",
            "Date": "1mo ago",
            "Summary": "Describes a personal experience where a change in preference for a bookstore highlights the importance of customer experience (CX), focusing on efficiency and empowerment. Connects this to a recent project focusing on improving CX for mid-sized companies.",
            "Tone": "Anecdotal, Reflective",
            "Metrics": "691 Comments"
        },
        {
            "Title": "I have been trying to find answers on how to grow Valuebound.",
            "URL": "null",
            "Date": "6mo ago",
            "Summary": "Discusses the author's 15+ year journey of finding ways to grow Valuebound, highlighting the challenges of the hit-and-trial method and the value of mentorship and coaching. Concludes that creating a personalized growth blueprint is crucial for organizational growth.",
            "Tone": "Reflective, Honest",
            "Metrics": "443 Comments"
        },
        {
            "Title": "Frustrated with Inconsistent Customer Journeys?",
            "URL": "null",
            "Date": "2w ago",
            "Summary": "Addresses the common problem of inconsistent customer journeys, outlining the negative impact on brand loyalty. Promotes Valuebound's services to unify customer touchpoints, resulting in cohesive, data-driven, and trustworthy interactions.",
            "Tone": "Problem/Solution, Professional",
            "Metrics": "4 Likes"
        },
        {
            "Title": "The Future of Content Management: Simplified, Smart, and Personal",
            "URL": "null",
            "Date": "Feb 9, 2024",
            "Summary": "Discusses the future of content management, emphasizing the role of technology in simplifying, personalizing, and making content smarter.",
            "Tone": "Professional, Forward-looking",
            "Metrics": "12 likes, 2 comments"
        },
        {
            "Title": "Embracing 4AM club: A Journey of Self-Discovery and Innovation",
            "URL": "null",
            "Date": "Dec 22, 2023",
            "Summary": "Shares the author's experience with waking up before 4 AM, describing it as a transformative journey leading to self-discovery and innovation.",
            "Tone": "Personal, Inspirational",
            "Metrics": "59 likes, 13 comments"
        },
        {
            "Title": "The Strategic Advantage of Tool Integration for Startup Growth",
            "URL": "null",
            "Date": "Jul 31, 2023",
            "Summary": "Discusses the importance of tool integration for startup growth in today's evolving business landscape.",
            "Tone": "Professional, Informative",
            "Metrics": "19 likes, 1 comment"
        }
    ],
    "Keywords": {
        "Lead": [
            "Neeraj Kumar",
            "Valuebound",
            "CEO",
            "Drupal",
            "Cloud",
            "AWS",
            "Customer Experience",
            "Digital Transformation",
            "AI",
            "Leadership",
            "Open Source",
            "Content Management",
            "Sales",
            "Business Growth"
        ]
    }
    }

sender_company_details = {
    "UnifiedCompanyDetails": {
        "CompanyName": "Valuebound",
        "Industry": "IT Services and IT Consulting",
        "KeyActivities": [
            "Digital Experience Platforms",
            "Drupal Development",
            "Cloud-Native Software Engineering",
            "AWS Services",
            "Integration Services",
            "Customer Experience Management",
            "Product Consulting"
        ],
        "CompanySize": "51-200 employees",
        "Location": [
            "Bengaluru, Karnataka, India",
            "New York, USA",
            "Indore, India"
        ],
        "NotableAchievements": [
            "AWS Advanced Consulting Partner Status (Mar 2023)",
            "Great Place to Work® Certification (Dec 2021)",
            "Added 3 unicorn clients in a year (2022), 3X headcount increase in 2022",
            "$800k ARR in 3 months with a 1-person sales team"
        ],
        "HiringNews": [
            "Hiring a Senior Data Manager (mentioned in a LinkedIn post)"
        ],
        "GrowthNews": [
            "Added 3 Indian unicorn start-ups as clients in 2022",
            "Increased headcount by 3X in 2022",
            "$800k ARR in 3 months with a 1-person sales team (2022)"
        ],
        "RecentEvents": [
            "Fun Fridays with Tambola (recent LinkedIn post)",
            "Visit from Peethasheesh of Kudali Mattha (recent LinkedIn post)"
        ],
        "CampusVisitors": [
            "Peethasheesh of Kudali Mattha (recent LinkedIn post)"
        ]
    },
    "CompanyRecentPosts": [
        {
            "Title": "Upcoming Webinar Alert! Join us for \"Log Smart: Transformative Practices for Centralized System Log Management\"",
            "URL": "https://lnkd.in/g3g7NYTg",
            "Date": "3w ago",
            "Summary": "Announces an upcoming webinar on centralized system log management, outlining the topics covered: demystifying system logs, tool selection guide, centralization benefits, and practical setup tips.",
            "Tone": "Promotional, Informative",
            "Metrics": "20 Likes"
        },
        {
            "Title": "Valuebound Attains AWS Advanced Consulting Partner Status, Offering Expert Cloud Migration Services",
            "URL": "https://www.prnewswire.com/in/news-releases/valuebound-attains-aws-advanced-con…",
            "Date": "Mar 29, 2023",
            "Summary": "Announces Valuebound's achievement of AWS Advanced Consulting Partner status, highlighting its commitment to delivering exceptional AWS cloud solutions and the benefits it offers clients.",
            "Tone": "Promotional, Accomplishment",
            "Metrics": "null"
        },
        {
            "Title": "Valuebound bags 3 unicorn clients in a year, increases headcount by 3X",
            "URL": "https://www.prnewswire.com/in/news-releases/valuebound-bags-3-unicorn-clients-i…",
            "Date": "Feb 15, 2022",
            "Summary": "Announces Valuebound's significant growth in 2022, including adding three Indian unicorn start-ups as clients and a 3X increase in headcount.",
            "Tone": "Promotional, Accomplishment",
            "Metrics": "null"
        },
        {
            "Title": "Fun Fridays just got a whole lot more exciting!",
            "URL": "null",
            "Date": "2d ago",
            "Summary": "Shares a post about a recent 'Fun Friday' team-building activity, playing Tambola.",
            "Tone": "Informal, Positive",
            "Metrics": "19 Likes"
        }
    ],
    "Keywords": {
        "Company": [
            "Valuebound",
            "IT Services",
            "Digital Transformation",
            "Drupal Development",
            "Cloud-Native Development",
            "AWS",
            "Customer Experience",
            "System Integration",
            "AI",
            "Growth",
            "Hiring",
            "Open Source",
            "Agile",
            "Employee Experience"
        ]
    }
    }


# Your email generation function
def generate_cold_email(data, sender, sender_company):
    """
    Generates a cold email using structured JSON data.

    Args:
        data (dict): A JSON object containing lead information.
        sender (dict): A dictionary containing sender information.
        sender_company (dict): A dictionary containing sender's company information.

    Returns:
        str: A generated cold email or an error message.
    """
    try:
        # Extract Unified Lead Details
        lead_details = data.get("UnifiedLeadDetails", {})
        company_details = data.get("UnifiedCompanyDetails", {})
        lead_posts = data.get("LeadRecentPosts", [])
        company_posts = data.get("CompanyRecentPosts", [])
        recent_projects = data.get("RecentProjectsAndWork", [])
        keywords = data.get("Keywords", {})

        # Extract lead details
        lead_name = lead_details.get("Name", "N/A")
        lead_title = lead_details.get("Title", "N/A")
        lead_email = lead_details.get("Email", "N/A")
        lead_location = lead_details.get("Location", "N/A")
        lead_industry = lead_details.get("Industry", "N/A")
        lead_skills = ', '.join(str(skill) for skill in lead_details.get("RelevantSkills", []))
        lead_other_info = '. '.join(str(info) for info in lead_details.get("OtherInformation", []))

        # Extract company details
        company_name = company_details.get("CompanyName", "N/A")
        company_industry = company_details.get("Industry", "N/A")
        company_size = company_details.get("CompanySize", "N/A")
        company_location = company_details.get("Location", "N/A")
        company_achievements = '. '.join(str(achievement) for achievement in company_details.get("NotableAchievements", []))
        company_activities = ', '.join(str(activity) for activity in company_details.get("KeyActivities", []))
        company_hiring_news = ', '.join(str(news) for news in company_details.get("HiringNews", []))
        company_growth_news = ', '.join(str(news) for news in company_details.get("GrowthNews", []))
        company_recent_events = ', '.join(str(event) for event in company_details.get("RecentEvents", []))

        # Use the first post or project as fallback if lists are not empty
        lead_recent_post = lead_posts[0].get("Summary", "No recent posts") if lead_posts else "No recent posts"
        company_recent_post = company_posts[0].get("Summary", "No recent posts") if company_posts else "No recent posts"
        recent_project = recent_projects[0] if recent_projects else "No recent projects"

        # Keywords formatting
        lead_keywords = ', '.join(str(keyword) for keyword in keywords.get("Lead", []))
        company_keywords = ', '.join(str(keyword) for keyword in keywords.get("Company", []))


        # Create a structured prompt
        prompt = f"""
        You are an expert B2B marketing assistant focused on creating engaging, natural-sounding outreach emails. Your primary goal is to open conversations through shared insights while maintaining a friendly and personalized tone.

        ### Input Data:
        **Lead Information:**
        - Name: {lead_name}
        - Title: {lead_title}
        - Email: {lead_email}
        - Location: {lead_location}
        - Industry: {lead_industry}
        - Skills: {lead_skills if lead_skills else 'None'}
        - Other Info: {lead_other_info if lead_other_info else 'None'}
        - Keywords: {lead_keywords if lead_keywords else 'None'}

        **Company Information:**
        - Company Name: {company_name}
        - Industry: {company_industry}
        - Company Size: {company_size}
        - Location: {company_location}
        - Notable Achievements: {company_achievements if company_achievements else 'None'}
        - Key Activities: {company_activities if company_activities else 'None'}
        - Hiring News: {company_hiring_news if company_hiring_news else 'None'}
        - Growth News: {company_growth_news if company_growth_news else 'None'}
        - Recent Events: {company_recent_events if company_recent_events else 'None'}
        - Keywords: {company_keywords if company_keywords else 'None'}


        **Recent Content:**
        - Lead's Most Recent Post: {lead_recent_post if lead_recent_post else 'None'}
        - Company’s Most Recent Post: {company_recent_post if company_recent_post else 'None'}

        **Recent Projects:**
        - Most Recent Project: {recent_project if recent_project else 'None'}

        **Sender (Email Author):**
        - Name: {sender.get('name', 'N/A')}
        - Title: {sender.get('title', 'N/A')}
        - Company: {sender.get('company', 'N/A')}
        - LinkedIn URL: {sender.get('linkedin_url', 'N/A')}

        **Sender’s Company:**
        - Name: {sender_company.get('name', 'N/A')}
        - Industry: {sender_company.get('industry', 'N/A')}
        - Website: {sender_company.get('website_url', 'N/A')}

        ### Selection Logic:

        1. **Identify 1-2 key topics**:
            - Focus on **shared interests or mutual benefits** such as a specific achievement, recent project, or post that resonates with both the lead and the sender.
            - Avoid covering too many topics. Select the **most relevant data points** from the provided input.

        2. **Prioritize depth over breadth**:
            - Instead of touching on multiple points, expand on the chosen topics with personalized insights or meaningful context.

        3. Create **relevance**:
            - Use data like lead's or company's recent post, achievements, or projects to establish context for collaboration.
            - Ensure there’s a logical flow in how the topics are connected to the sender’s goals.

        4. End with a **specific, open-ended call to action** to initiate a meaningful conversation.


        ### Objective:
        - Craft a tailored email that captures the recipient's attention by focusing on one or two compelling topics.
        - Highlight how the sender's expertise or offerings align with the recipient’s work.
        - Maintain a warm, professional tone.
        - Please generate the email content only, without any additional commentary or explanation.

        ### Example Email Flow:
        - **Opening**: Start by referencing a shared or relevant insight from the prioritized data.
        - **Body**: Highlight mutual benefits or unique contributions from either the sender or receiver. Avoid introducing unrelated topics.
        - **Conclusion**: Conclude with a relevant and specific call to action (e.g., suggesting a meeting to explore potential synergies).

        """

        print("Generated Prompt : " ,prompt)
        
        # Generate email using AI
        chat_completions = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a highly skilled B2B marketing assistant who specializes in writing personalized cold outreach emails."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-70b-versatile"
        )

        return chat_completions.choices[0].message.content

    except Exception as e:
        return f"Error generating email: {str(e)}"

# MongoDB connection setup
MONGO_URI = "mongodb+srv://valuebound:E2gfdCBGyPrGy9C@cluster0.d3y7p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Replace with your MongoDB URI
DATABASE_NAME = "lead"  # Replace with your database name
COLLECTION_NAME = "leads"  # Replace with your collection name

def connect_to_mongo():
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    return collection

def fetch_all_prospects(collection):
    # Fetch all documents and ensure the _id is converted to string
    prospects = list(collection.find({}))
    for prospect in prospects:
        prospect["_id"] = str(prospect["_id"])
    return prospects

def fetch_prospect_by_name(collection, person_name):
    # Search for a specific prospect by name in the nested field
    return collection.find_one({"UnifiedLeadDetails.Name": person_name})

# Streamlit interface
st.title("Cold Email Generator")

# Connect to MongoDB
collection = connect_to_mongo()
prospects = fetch_all_prospects(collection)

# Extract prospect names from the nested structure
prospect_names = [prospect["UnifiedLeadDetails"]["Name"] for prospect in prospects if "UnifiedLeadDetails" in prospect and "Name" in prospect["UnifiedLeadDetails"]]

if prospect_names:
    # Dropdown for selecting a prospect
    selected_name = st.selectbox("Select a prospect", prospect_names)

    if selected_name:
        # Fetch the data for the selected prospect
        selected_prospect = fetch_prospect_by_name(collection, selected_name)
        
        if selected_prospect:
            # Generate the cold email
            email = generate_cold_email(selected_prospect, sender_details, sender_company_details)
            
            # Display the generated email
            st.subheader("Generated Email")
            st.text_area("Cold Email", email, height=200, disabled=True)
        else:
            st.error("Selected prospect not found in the database.")
else:
    st.warning("No prospects found in the database.")