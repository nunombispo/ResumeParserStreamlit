import streamlit as st
import requests
from decouple import config


# Function to process the resume using the Unstract API
def process_resume(file):
    # Get the API key from the environment variables
    api_key = config('UNSTRACT_API_KEY')
    # API endpoint
    api_url = 'https://us-central.unstract.com/deployment/api/org_LkRzaCm4cg2eV2GJ/resume_api/'
    # Headers and payload
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    payload = {'timeout': 300, 'include_metadata': False}
    # Files
    files = [('files', ('file', open(file, 'rb'), 'application/octet-stream'))]
    # Send the request
    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    # Print (for debugging) and return the response
    print('Response:', response.json())
    return response.json()['message']['result'][0]['result']['output']


# Streamlit app setup
st.set_page_config(page_title='Resume Parser', page_icon=':page_with_curl:', layout='centered')
st.header('Resume Parser')
st.subheader('Upload your resume and receive a JSON output')
st.divider()

# File uploader
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file:
    # Show a status message
    with st.status('Processing your resume...'):
        # Save the uploaded file to a temporary location
        with open('temp.pdf', 'wb') as f:
            f.write(uploaded_file.getbuffer())
        # Process the resume
        json_response = process_resume('temp.pdf')
        st.write('Resume processed successfully!')
    # Show the name and role extracted from the resume
    st.divider()
    st.title('Name and Role')
    st.write(f'Name: {json_response['name_role']['name']}')
    st.write(f'Role: {json_response['name_role']['job_role']}')
    # Show the profile summary extracted from the resume
    st.divider()
    st.title('Profile Summary')
    st.write(json_response['profile'])
    # Show the contact information extracted from the resume
    st.divider()
    st.title('Contact Information')
    st.write(f'Email: {json_response['contact_info']['e-mail']}')
    st.write(f'Phone: {json_response['contact_info']['phone number']}')
    st.write(f'Address: {json_response['contact_info']['address']}')
    # Show the education information extracted from the resume
    st.divider()
    st.title('Education')
    for education in json_response['education']['education']:
        st.write(f'{education["degree"]} from {education["institution"]} between {education["start_year"]} and '
                 f'{education["end_year"]}')
    # Show the skills extracted from the resume
    st.divider()
    st.title('Skills')
    st.write(', '.join(json_response['skills']))
    # Show the work experience extracted from the resume
    st.divider()
    st.title('Work Experience')
    for experience in json_response['work_experience']:
        st.write(f'{experience["role"]} at {experience["company_name"]} between {experience["dates"]}')
        st.write(', '.join(experience['work_responsibilities']))
