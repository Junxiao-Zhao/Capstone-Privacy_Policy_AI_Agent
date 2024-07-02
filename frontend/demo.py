import streamlit as st
import pandas as pd

# Constants for testing
SKIP_VALIDATION = True

# Options for selection
DATA_TYPES = [
    'Personal Information', 
    'Account Information', 
    'Content Data',
    'Usage Data', 
    'Device Information', 
    'Location Data', 
    'Payment Information',
    'Transaction Data', 
    'Financial Information',
    'Biometric Data',
    'Health Information',
    'Communication Data',
    'Behavioral Data',
    'Preference Data',
    'Employment Information',
    'Educational Information'
]

USAGE_PURPOSES = [
    'Providing Services', 
    'Customer Support', 
    'Improving Services',
    'Security and Fraud Prevention', 
    'Legal Compliance', 
    'Marketing',
    'Personalization',
    'Analytics and Research',
    'Product Development',
    'Communications',
    'Advertising'
]

SHARING_PARTNERS = [
    'Service Providers', 
    'Business Partners', 
    'Legal Authorities', 
    'Advertising Partners',
    'Other Users',
    'Affiliates and Subsidiaries',
    'Data Brokers',
    'Government Agencies',
    'Social Media Platforms'
]

PROTECTION_MEASURES = [
    'Encryption', 
    'Access Control', 
    'Data Minimization', 
    'Security Audits',
    'Firewalls',
    'Intrusion Detection Systems',
    'Multi-factor Authentication',
    'Regular Security Training',
    'Data Anonymization',
    'Secure Data Storage'
]

USER_RIGHTS = [
    'Access Data', 
    'Correct Data', 
    'Delete Data', 
    'Data Portability', 
    'Opt-out',
    'Restrict Processing', 
    'Object to Processing',
    'Withdraw Consent',
    'Complain to Supervisory Authority'
]

TRANSFER_MEASURES = [
    'Standard Contractual Clauses', 
    'Privacy Shield',
    'Binding Corporate Rules',
    'Adequacy Decisions',
    'Data Protection Agreements'
]

LEGAL_BASIS = [
    'Consent', 
    'Contract', 
    'Legal Obligation', 
    'Legitimate Interests',
    'Vital Interests',
    'Public Task'
]

DATA_TYPE_DESCRIPTIONS = {
    'Personal Information': 'Information such as your name, email address, phone number, and other contact details.',
    'Account Information': 'Information related to your account, such as username and password.',
    'Content Data': 'Information you provide when you upload or share content, such as photos, videos, and comments.',
    'Usage Data': 'Information about how you use our services, including your interactions with the platform.',
    'Device Information': 'Information about the devices you use to access our services, such as device type and operating system.',
    'Location Data': 'Information about your location, either provided by you or derived from your IP address or GPS.',
    'Payment Information': 'Information related to your payments and transactions.',
    'Transaction Data': 'Details about the transactions you make using our services.',
    'Financial Information': 'Information related to your financial status and activities.',
    'Biometric Data': 'Information related to your biometric characteristics, such as fingerprints or facial recognition data.',
    'Health Information': 'Information related to your health status or medical history.',
    'Communication Data': 'Information from your communications with us, such as emails and chat messages.',
    'Behavioral Data': 'Information about your behavior and preferences, such as browsing history and interactions.',
    'Preference Data': 'Information about your preferences and interests.',
    'Employment Information': 'Information about your employment history and status.',
    'Educational Information': 'Information about your educational background.'
}

USAGE_PURPOSE_DESCRIPTIONS = {
    'Providing Services': 'To provide, maintain, and improve our services.',
    'Customer Support': 'To provide customer support and respond to your inquiries.',
    'Improving Services': 'To improve our services and develop new features.',
    'Security and Fraud Prevention': 'To ensure the security of our services and prevent fraud.',
    'Legal Compliance': 'To comply with legal obligations and protect our legal rights.',
    'Marketing': 'To send you promotional materials and updates about our services.',
    'Personalization': 'To personalize your experience and provide tailored content.',
    'Analytics and Research': 'To analyze how our services are used and conduct research.',
    'Product Development': 'To develop new products and improve existing ones.',
    'Communications': 'To communicate with you about our services.',
    'Advertising': 'To show you relevant advertisements.'
}

SHARING_PARTNER_DESCRIPTIONS = {
    'Service Providers': 'Third-party service providers who assist us in providing our services.',
    'Business Partners': 'Partners with whom we collaborate to offer integrated services.',
    'Legal Authorities': 'When required by law or to protect our legal rights.',
    'Advertising Partners': 'For advertising purposes, with your consent.',
    'Other Users': 'Information that you choose to make public or share with other users.',
    'Affiliates and Subsidiaries': 'Our affiliated companies and subsidiaries.',
    'Data Brokers': 'Companies that collect and sell data.',
    'Government Agencies': 'Government agencies when required by law.',
    'Social Media Platforms': 'Social media platforms when you link your account with them.'
}

PROTECTION_MEASURE_DESCRIPTIONS = {
    'Encryption': 'We use encryption to protect your data in transit and at rest.',
    'Access Control': 'We restrict access to personal data to authorized personnel only.',
    'Data Minimization': 'We collect only the data necessary for the purposes outlined in this policy.',
    'Security Audits': 'We conduct regular security audits to ensure the safety of your data.',
    'Firewalls': 'We use firewalls to protect our systems from unauthorized access.',
    'Intrusion Detection Systems': 'We use intrusion detection systems to monitor for suspicious activity.',
    'Multi-factor Authentication': 'We require multi-factor authentication for access to sensitive data.',
    'Regular Security Training': 'We provide regular security training to our staff.',
    'Data Anonymization': 'We anonymize data where possible to protect your privacy.',
    'Secure Data Storage': 'We store data securely using advanced security measures.'
}

USER_RIGHT_DESCRIPTIONS = {
    'Access Data': 'You can request access to the data we hold about you.',
    'Correct Data': 'You can request the correction of inaccurate personal data.',
    'Delete Data': 'You can request the deletion of your personal data.',
    'Data Portability': 'You can request to receive your personal data in a structured, commonly used, and machine-readable format.',
    'Opt-out': 'You can opt-out of certain uses of your data, such as marketing communications.',
    'Restrict Processing': 'You can request that we restrict the processing of your personal data under certain circumstances.',
    'Object to Processing': 'You can object to the processing of your personal data under certain circumstances.',
    'Withdraw Consent': 'You can withdraw your consent at any time where we are relying on consent to process your personal data.',
    'Complain to Supervisory Authority': 'You can complain to a supervisory authority if you believe your rights have been violated.'
}

TRANSFER_MEASURE_DESCRIPTIONS = {
    'Standard Contractual Clauses': 'We use standard contractual clauses to protect your data during international transfers.',
    'Privacy Shield': 'We comply with the EU-U.S. and Swiss-U.S. Privacy Shield Frameworks.',
    'Binding Corporate Rules': 'We use binding corporate rules for international data transfers within our corporate group.',
    'Adequacy Decisions': 'We rely on adequacy decisions from the European Commission for transfers to certain countries.',
    'Data Protection Agreements': 'We have data protection agreements in place to safeguard your data.'
}

LEGAL_BASIS_DESCRIPTIONS = {
    'Consent': 'When you have given your explicit consent.',
    'Contract': 'When processing is necessary for the performance of a contract with you.',
    'Legal Obligation': 'When we need to comply with a legal obligation.',
    'Legitimate Interests': 'When processing is necessary for our legitimate interests and your interests and fundamental rights do not override those interests.',
    'Vital Interests': 'When processing is necessary to protect someone’s life.',
    'Public Task': 'When processing is necessary to perform a task in the public interest or for official functions.'
}

COLLECTION_METHODS_DESCRIPTIONS = {
    'Directly from you': 'When you provide it to us directly through forms, account creation, or communications.',
    'Automatically': 'When you use our services, through cookies, log files, and similar technologies.',
    'From Third Parties': 'When you link your account with third-party services or access our services through third-party platforms.'
}

def generate_privacy_policy(user_data, data_type_desc, collection_method_desc, usage_purpose_desc, sharing_partner_desc, protection_measure_desc, user_right_desc, transfer_measure_desc, legal_basis_desc):

    def get_description(key, desc_dict):
        return desc_dict.get(key, 'Description not available')

    # Initialize all variables
    data_types = user_data.get('data_types', [])
    collection_methods = user_data.get('collection_methods', [])
    usage_purposes = user_data.get('usage_purposes', [])
    sharing_partners = user_data.get('sharing_partners', [])
    protection_measures = user_data.get('protection_measures', [])
    user_rights = user_data.get('user_rights', [])
    transfer_measures = user_data.get('transfer_measures', [])
    legal_basis = user_data.get('legal_basis', [])
    use_cookies = user_data.get('use_cookies', False)
    retention_period = user_data.get('retention_period', '')

    color = 'red'
    # Generate sections with descriptions and apply color
    data_types_desc = '<br>'.join([f'- <span style="color:{color};">{data}</span>: {get_description(data, data_type_desc)}' for data in data_types])
    collection_methods_desc = '<br>'.join([f'- <span style="color:{color};">{method}</span>: {get_description(method, collection_method_desc)}' for method in collection_methods])
    usage_purposes_desc = '<br>'.join([f'- <span style="color:{color};">{purpose}</span>: {get_description(purpose, usage_purpose_desc)}' for purpose in usage_purposes])
    sharing_partners_desc = '<br>'.join([f'- <span style="color:{color};">{partner}</span>: {get_description(partner, sharing_partner_desc)}' for partner in sharing_partners])
    protection_measures_desc = '<br>'.join([f'- <span style="color:{color};">{measure}</span>: {get_description(measure, protection_measure_desc)}' for measure in protection_measures])
    legal_basis_desc = '<br>'.join([f'- <span style="color:{color};">{basis}</span>: {get_description(basis, legal_basis_desc)}' for basis in legal_basis])
    user_rights_desc = '<br>'.join([f'- <span style="color:{color};">{right}</span>: {get_description(right, user_right_desc)}' for right in user_rights])
    transfer_measures_desc = '<br>'.join([f'- <span style="color:{color};">{measure}</span>: {get_description(measure, transfer_measure_desc)}' for measure in transfer_measures])
    
    data = ''
    if data_types:
        data = f'\
        <h3>Information We Collect</h3>\
        <p>We collect various types of information in connection with the services we provide, including:</p>\
        <p>{data_types_desc}</p>\
        '

    collection = ''
    if collection_methods:
        collection = f'\
        <h3>How We Collect Information</h3>\
        <p>We collect information in the following ways:</p>\
        <p>{collection_methods_desc}</p>\
        '

    usage = ''
    if usage_purposes:
        usage = f'\
        <h3>How We Use Information</h3>\
        <p>We use the collected information for various purposes, including:</p>\
        <p>{usage_purposes_desc}</p>\
        '

    sharing = ''
    if sharing_partners:
        sharing = f'\
        <h3>Sharing Information</h3>\
        <p>We may share your information with the following parties:</p>\
        <p>{sharing_partners_desc}</p>\
        '

    protection = ''
    if protection_measures:
        protection = f'\
        <h3>Data Protection Measures</h3>\
        <p>We implement a variety of security measures to maintain the safety of your personal information:</p>\
        <p>{protection_measures_desc}</p>\
        '
    
    legal = ''
    if legal_basis:
        legal = f'\
        <h3>Legal Basis for Processing</h3>\
        <p>We process your personal data based on the following legal grounds:</p>\
        <p>{legal_basis_desc}</p>\
        '

    user = ''
    if user_rights:
        user = f'\
        <h3>Your Rights</h3>\
        <p>You have the following rights regarding your personal data:</p>\
        <p>{user_rights_desc}</p>\
        '

    transfer = ''
    if transfer_measures:
        transfer = f'\
        <h3>International Data Transfer</h3>\
        <p>We may transfer your data internationally and ensure it is protected:</p>\
        <p>{transfer_measures_desc}</p>\
        '

    cookie = ''
    if use_cookies:
        cookie = f'\
        <h3>Cookies and Tracking Technologies</h3>\
        <p>We use cookies and similar tracking technologies to track the activity on our service and hold certain information.</p>\
        <p>You can instruct your browser to refuse all cookies or to indicate when a cookie is being sent.</p>\
        '
    
    retention = ''
    if retention_period:
        retention = f'\
        <h3>Data Retention</h3>\
        <p>We will retain your personal data only for as long as is necessary for the purposes set out in this Privacy Policy. </p>\
        <p>We will retain and use your data to the extent necessary to comply with our legal obligations, resolve disputes, and enforce our policies.</p>\
        '

    template = f"""
    <h2>Privacy Policy</h2>

    <h3>Introduction</h3>
    <p>Welcome to <span style="color:{color};">{user_data.get('company_name', 'Your Company')}</span>'s Privacy Policy. Your privacy is critically important to us. This policy explains the types of information we collect, how we use it, and the measures we take to protect it.</p>

    <h3>Company Information</h3>
    <p><strong>Company Name</strong>: <span style="color:{color};">{user_data.get('company_name', 'Your Company')}</span></p>
    <p><strong>Address</strong>: <span style="color:{color};">{user_data.get('address', 'Your Address')}</span></p>
    <p><strong>Contact Email</strong>: <span style="color:{color};">{user_data.get('contact_email', 'your.email@example.com')}</span></p>
    {data+collection+usage+sharing+cookie+protection+retention+legal+user+transfer}
    <h3>Dispute Resolution</h3>
    <p>If you have any complaints or concerns about our Privacy Policy or practices, please contact us at <span style="color:{color};">{user_data.get('contact_email', 'your.email@example.com')}</span>. We will work with you to resolve any issues.</p>

    <h3>Changes to This Privacy Policy</h3>
    <p>We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page. You are advised to review this Privacy Policy periodically for any changes.</p>

    <h3>Contact Us</h3>
    <p>If you have any questions about this Privacy Policy, please contact us at <span style="color:{color};">{user_data.get('contact_email', 'your.email@example.com')}</span>.</p>
    """

    return template



def main():
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state['page'] = 0
    if 'form_data' not in st.session_state:
        st.session_state['form_data'] = {}

    # Pages
    pages = [
        'Company Info',
        'Data Collection',
        'Cookies and Tracking',
        'Data Usage',
        'Data Sharing',
        'Data Protection',
        'Data Retention',
        'User Rights',
        'Child Privacy',
        'International Data Transfer',
        'Dispute Resolution',
        'User Additions',
        'Summary'
    ]

    # Display current page
    display_page(pages[st.session_state['page']])

    # Page navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.session_state['page'] > 0:
            if st.button('Previous'):
                save_current_page_data(pages[st.session_state['page']])
                st.session_state['page'] -= 1
                st.experimental_rerun()
    with col3:
        if st.session_state['page'] < len(pages) - 1:
            if st.button('Next'):
                if validate_page(st.session_state['page']):
                    save_current_page_data(pages[st.session_state['page']])
                    st.session_state['page'] += 1
                    st.experimental_rerun()
        else:
            if st.button('Submit'):
                if validate_page(st.session_state['page']):
                    save_current_page_data(pages[st.session_state['page']])
                    save_data(st.session_state['form_data'])
                    st.success('Data saved successfully!')
                    st.session_state['page'] = 0
                    st.session_state['form_data'] = {}
                    st.experimental_rerun()

def save_current_page_data(page):
    if page == 'Company Info':
        st.session_state['form_data']['company_name'] = st.session_state.get('company_name', '')
        st.session_state['form_data']['address'] = st.session_state.get('address', '')
        st.session_state['form_data']['contact_email'] = st.session_state.get('contact_email', '')
    elif page == 'Data Collection':
        st.session_state['form_data']['data_types'] = st.session_state.get('data_types', [])
        st.session_state['form_data']['collection_methods'] = st.session_state.get('collection_methods', [])
    elif page == 'Cookies and Tracking':
        st.session_state['form_data']['use_cookies'] = st.session_state.get('use_cookies', False)
    elif page == 'Data Usage':
        st.session_state['form_data']['usage_purposes'] = st.session_state.get('usage_purposes', [])
    elif page == 'Data Sharing':
        st.session_state['form_data']['sharing_partners'] = st.session_state.get('sharing_partners', [])
    elif page == 'Data Protection':
        st.session_state['form_data']['protection_measures'] = st.session_state.get('protection_measures', [])
    elif page == 'Data Retention':
        st.session_state['form_data']['retention_period'] = st.session_state.get('retention_period', '')
    elif page == 'User Rights':
        st.session_state['form_data']['user_rights'] = st.session_state.get('user_rights', [])
    elif page == 'Child Privacy':
        st.session_state['form_data']['collect_child_data'] = st.session_state.get('collect_child_data', False)
        if st.session_state['form_data']['collect_child_data']:
            st.session_state['form_data']['child_protection_measures'] = st.session_state.get('child_protection_measures', [])
    elif page == 'International Data Transfer':
        st.session_state['form_data']['international_transfer'] = st.session_state.get('international_transfer', False)
        if st.session_state['form_data']['international_transfer']:
            st.session_state['form_data']['transfer_measures'] = st.session_state.get('transfer_measures', [])
    elif page == 'Dispute Resolution':
        st.session_state['form_data']['dispute_resolution'] = st.session_state.get('dispute_resolution', '')
    elif page == 'User Additions':
        st.session_state['form_data']['user_additions'] = st.session_state.get('user_additions', '')

def display_page(page):
    st.title(page)
    if page == 'Company Info':
        st.session_state['company_name'] = st.text_input('Company Name', st.session_state['form_data'].get('company_name', ''))
        st.session_state['address'] = st.text_input('Address', st.session_state['form_data'].get('address', ''))
        st.session_state['contact_email'] = st.text_input('Contact Email', st.session_state['form_data'].get('contact_email', ''))
    elif page == 'Data Collection':
        st.session_state['data_types'] = st.multiselect('Types of Data Collected', DATA_TYPES, st.session_state['form_data'].get('data_types', []))
        st.session_state['collection_methods'] = st.multiselect('Data Collection Methods', ['Directly from you', 'Automatically', 'From third parties'], st.session_state['form_data'].get('collection_methods', []))
    elif page == 'Cookies and Tracking':
        st.session_state['use_cookies'] = st.checkbox('Use Cookies and Tracking Technologies?', st.session_state['form_data'].get('use_cookies', False))
    elif page == 'Data Usage':
        st.session_state['usage_purposes'] = st.multiselect('Data Usage Purposes', USAGE_PURPOSES, st.session_state['form_data'].get('usage_purposes', []))
    elif page == 'Data Sharing':
        st.session_state['sharing_partners'] = st.multiselect('Data Sharing Partners', SHARING_PARTNERS, st.session_state['form_data'].get('sharing_partners', []))
    elif page == 'Data Protection':
        st.session_state['protection_measures'] = st.multiselect('Data Protection Measures', PROTECTION_MEASURES, st.session_state['form_data'].get('protection_measures', []))
    elif page == 'Data Retention':
        st.session_state['retention_period'] = st.text_input('Data Retention Period', st.session_state['form_data'].get('retention_period', ''))
    elif page == 'User Rights':
        st.session_state['user_rights'] = st.multiselect('User Rights', USER_RIGHTS, st.session_state['form_data'].get('user_rights', []))
    elif page == 'Child Privacy':
        st.session_state['collect_child_data'] = st.checkbox('Collect Data from Children?', st.session_state['form_data'].get('collect_child_data', False))
        if st.session_state['collect_child_data']:
            st.session_state['child_protection_measures'] = st.multiselect('Child Data Protection Measures', ['Parental Consent', 'Child Data Encryption'], st.session_state['form_data'].get('child_protection_measures', []))
    elif page == 'International Data Transfer':
        st.session_state['international_transfer'] = st.checkbox('Transfer Data Internationally?', st.session_state['form_data'].get('international_transfer', False))
        if st.session_state['international_transfer']:
            st.session_state['transfer_measures'] = st.multiselect('International Transfer Measures', TRANSFER_MEASURES, st.session_state['form_data'].get('transfer_measures', []))
    elif page == 'Dispute Resolution':
        st.session_state['dispute_resolution'] = st.text_input('Dispute Resolution Mechanism', st.session_state['form_data'].get('dispute_resolution', ''))
    elif page == 'User Additions':
        st.session_state['user_additions'] = st.text_area('Additional Requirements or Comments', st.session_state['form_data'].get('user_additions', ''))
    elif page == 'Summary':
        st.write('## Summary')
        st.json(st.session_state['form_data'])

    # Dynamically generate and display privacy policy template
    with st.sidebar.expander("Preview Privacy Policy Template"):
        if st.session_state['form_data']:
            st.markdown(generate_privacy_policy(
                st.session_state['form_data'], 
                DATA_TYPE_DESCRIPTIONS, 
                COLLECTION_METHODS_DESCRIPTIONS,
                USAGE_PURPOSE_DESCRIPTIONS, 
                SHARING_PARTNER_DESCRIPTIONS, 
                PROTECTION_MEASURE_DESCRIPTIONS, 
                USER_RIGHT_DESCRIPTIONS, 
                TRANSFER_MEASURE_DESCRIPTIONS, 
                LEGAL_BASIS_DESCRIPTIONS
            ), unsafe_allow_html=True)

def validate_page(page_index):
    if SKIP_VALIDATION:
        return True
    required_fields = {
        0: ['company_name', 'address', 'contact_email'],
        1: ['data_types', 'collection_methods'],
        2: ['use_cookies'],
        3: ['usage_purposes'],
        4: ['sharing_partners'],
        5: ['protection_measures'],
        6: ['retention_period'],
        7: ['user_rights'],
        8: ['collect_child_data'],
        9: ['international_transfer'],
        10: ['dispute_resolution']
    }
    if page_index in required_fields:
        for field in required_fields[page_index]:
            if not st.session_state['form_data'].get(field):
                st.warning(f"Please complete the '{field}' field.")
                return False
    return True

def save_data(data):
    df = pd.DataFrame([data])
    df.to_csv('privacy_policy_data.csv', index=False)

if __name__ == '__main__':
    main()