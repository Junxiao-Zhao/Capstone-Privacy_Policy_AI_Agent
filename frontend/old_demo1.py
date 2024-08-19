import streamlit as st
import pandas as pd
import os

def check_login(username, password):
    return username == "user" and password == "password"

def save_data(data, filename='data.csv'):
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df = df.append(data, ignore_index=True)
    else:
        df = pd.DataFrame(data, index=[0])
    df.to_csv(filename, index=False)

countries = [
    "United States", "Canada", "Australia", "United Kingdom", "Germany", "France",
    "China", "India", "Japan", "South Korea", "Brazil", "Mexico"
    # 可以继续添加更多国家
]

def main():
    """
    st.title("User Information App")

    # Login section
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            if check_login(username, password):
                st.session_state['logged_in'] = True
                st.success("Login successful")
            else:
                st.error("Invalid username or password")
    else:
    """
    st.title("Information Collection Form")

    # Section 1: Basic Company and Website Information
    st.header("1. Basic Company and Website Information")
    company_name = st.text_input("Company Name *")
    company_location = st.selectbox("Company Location *", countries)
    website_name = st.text_input("Website Name *")
    domain_name = st.text_input("Domain Name (URL) *")
    contact_address = st.text_input("Contact Address *")
    contact_phone = st.text_input("Contact Phone *")
    contact_email = st.text_input("Contact Email *")

    # Section 2: Main Features and Services of the Website
    st.header("2. Main Features and Services of the Website")
    website_type = st.selectbox("Website Type *", ["E-commerce", "Social Media", "Content Publishing Platform", "Online Service Platform", "Others"])
    main_features = st.text_area("Main Features (e.g., user registration, payment, content upload, social interaction, health monitoring)", help="Please describe the main features of your website.")
    user_group = st.text_area("User Group (e.g., age, location, usage purpose)", help="Please describe the main user group of your website.")
    user_location = st.selectbox("User Location", countries, help="Select the primary location of your users.")

    # Section 3: Data Collection and Usage
    st.header("3. Data Collection and Usage")
    data_types = st.multiselect("Collected Data Types", ["Name", "Email", "Address", "Payment Information", "Browsing History", "Others"])
    data_sources = st.text_area("Data Sources (e.g., directly from users, automated tools like cookies)")
    data_uses = st.text_area("Data Uses (e.g., account management, payment processing, personalized recommendations, marketing)")
    data_sharing = st.radio("Data Sharing", ["Yes", "No"])
    if data_sharing == "Yes":
        st.text_area("Please specify the third parties and their purposes")

    # Section 4: Data Storage and Security Measures
    st.header("4. Data Storage and Security Measures")
    storage_location = st.selectbox("Storage Location", ["Local Servers", "Cloud Service Providers"])
    security_measures = st.multiselect("Security Measures", ["Encryption", "Access Control", "Data Backup", "Others"])
    data_retention_period = st.text_input("Data Retention Period (e.g., how long the data is kept, how it is deleted or anonymized after the period)")

    # Section 5: User Rights
    st.header("5. User Rights")
    access_correction = st.radio("Access and Correction", ["Yes", "No"])
    if access_correction == "Yes":
        st.text_area("Please describe how users can access and correct their personal data")
    deletion_restriction = st.radio("Deletion and Restriction", ["Yes", "No"])
    if deletion_restriction == "Yes":
        st.text_area("Please describe how users can request deletion or restriction of their data")
    data_portability = st.radio("Data Portability", ["Yes", "No"])
    if data_portability == "Yes":
        st.text_area("Please describe how users can request to transfer their data to other service providers")

    # Section 6: Cookies and Tracking Technologies
    st.header("6. Cookies and Tracking Technologies")
    usage_situation = st.radio("Usage Situation", ["Yes", "No"])
    if usage_situation == "Yes":
        purposes = st.text_area("Purposes (e.g., user authentication, preference storage, traffic analysis)")
        opt_out = st.text_area("Opt-out (e.g., how users can opt-out of the use of cookies and tracking technologies)")

    # Section 7: Legal Compliance
    st.header("7. Legal Compliance")
    legal_basis = st.multiselect("Legal Basis", ["User Consent", "Contract Fulfillment", "Legitimate Interests", "Others"])
    minor_protection = st.radio("Minor Protection", ["Yes", "No"])
    if minor_protection == "Yes":
        st.text_area("Please describe the special provisions and protection measures for processing data of minors")
    privacy_policy_changes = st.radio("Privacy Policy Changes", ["Yes", "No"])
    if privacy_policy_changes == "Yes":
        st.text_area("Please describe the process for changing the privacy policy and notifying users")

    # Section 8: International Data Transfer
    st.header("8. International Data Transfer")
    cross_border_transfer = st.radio("Cross-border Transfer", ["Yes", "No"])
    if cross_border_transfer == "Yes":
        st.text_area("Please describe how to ensure data security and legal compliance during cross-border transfer")

    # Section 9: Additional Information
    st.header("9. Additional Information")
    third_party_services = st.radio("Third-party Services", ["Yes", "No"])
    if third_party_services == "Yes":
        st.text_area("Please describe the third-party services or plugins, such as payment processors, advertising networks, analytics tools")
    privacy_policy_template = st.radio("Privacy Policy Template", ["Yes", "No"])
    if privacy_policy_template == "Yes":
        st.text_area("Please describe the existing privacy policy template or specific requirements")

    # Section 10: Other Special Requirements
    st.header("10. Other Special Requirements")
    industry_regulations = st.radio("Industry Regulations", ["Yes", "No"])
    if industry_regulations == "Yes":
        st.text_area("Please describe the specific industry regulations, such as privacy protection requirements in the medical or financial sectors")
    customer_specific_needs = st.radio("Customer-specific Needs", ["Yes", "No"])
    if customer_specific_needs == "Yes":
        st.text_area("Please describe any other special needs or requirements, such as specific user consent processes, data processing agreements, etc.")

    # Submit Button
    if st.button("Submit"):
        # Check if all required fields are filled
        required_fields = [company_name, company_location, website_name, domain_name, contact_address, contact_phone, contact_email, website_type]
        if all(required_fields):
            data = {
                'Company Name': company_name,
                'Company Location':company_location,
                'Website Name': website_name,
                'Domain Name': domain_name,
                'Contact Address': contact_address,
                'Contact Phone': contact_phone,
                'Contact Email': contact_email,
                'Website Type': website_type,
                'Main Features': main_features,
                'User Group': user_group,
                'User Location': user_location,
                'Collected Data Types': data_types,
                'Data Sources': data_sources,
                'Data Uses': data_uses,
                'Data Sharing': data_sharing,
                'Storage Location': storage_location,
                'Security Measures': security_measures,
                'Data Retention Period': data_retention_period,
                'Access and Correction': access_correction,
                'Deletion and Restriction': deletion_restriction,
                'Data Portability': data_portability,
                'Usage Situation': usage_situation,
                'Purposes': purposes,
                'Opt-out': opt_out,
                'Legal Basis': legal_basis,
                'Minor Protection': minor_protection,
                'Privacy Policy Changes': privacy_policy_changes,
                'Cross-border Transfer': cross_border_transfer,
                'Third-party Services': third_party_services,
                'Privacy Policy Template': privacy_policy_template,
                'Industry Regulations': industry_regulations,
                'Customer-specific Needs': customer_specific_needs
            }
            save_data(data)
            st.success("Data saved successfully")
        else:
            st.error("Please fill in all required fields.")
    
    # Logout button
    #if st.button("Logout"):
        #st.session_state['logged_in'] = False

if __name__ == "__main__":
    main()