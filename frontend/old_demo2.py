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
        st.session_state['form_data']['contact'] = st.session_state.get('contact', '')
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
        st.text_input('Company Name', st.session_state['form_data'].get('company_name', ''), key='company_name', on_change=save_current_page_data, args=(page,))
        st.text_input('Address', st.session_state['form_data'].get('address', ''), key='address', on_change=save_current_page_data, args=(page,))
        st.text_input('Contact Email', st.session_state['form_data'].get('contact', ''), key='contact', on_change=save_current_page_data, args=(page,))
    elif page == 'Data Collection':
        st.multiselect('Types of Data Collected', DATA_TYPES, st.session_state['form_data'].get('data_types', []), key='data_types', on_change=save_current_page_data, args=(page,))
        st.multiselect('Data Collection Methods', ['Directly from you', 'Automatically', 'From third parties'], st.session_state['form_data'].get('collection_methods', []), key='collection_methods', on_change=save_current_page_data, args=(page,))
    elif page == 'Cookies and Tracking':
        st.checkbox('Use Cookies and Tracking Technologies?', st.session_state['form_data'].get('use_cookies', False), key='use_cookies', on_change=save_current_page_data, args=(page,))
    elif page == 'Data Usage':
        st.multiselect('Data Usage Purposes', USAGE_PURPOSES, st.session_state['form_data'].get('usage_purposes', []), key='usage_purposes', on_change=save_current_page_data, args=(page,))
    elif page == 'Data Sharing':
        st.multiselect('Data Sharing Partners', SHARING_PARTNERS, st.session_state['form_data'].get('sharing_partners', []), key='sharing_partners', on_change=save_current_page_data, args=(page,))
    elif page == 'Data Protection':
        st.multiselect('Data Protection Measures', PROTECTION_MEASURES, st.session_state['form_data'].get('protection_measures', []), key='protection_measures', on_change=save_current_page_data, args=(page,))
    elif page == 'Data Retention':
        st.text_input('Data Retention Period', st.session_state['form_data'].get('retention_period', ''), key='retention_period', on_change=save_current_page_data, args=(page,))
    elif page == 'User Rights':
        st.multiselect('User Rights', USER_RIGHTS, st.session_state['form_data'].get('user_rights', []), key='user_rights', on_change=save_current_page_data, args=(page,))
    elif page == 'Child Privacy':
        st.checkbox('Collect Data from Children?', st.session_state['form_data'].get('collect_child_data', False), key='collect_child_data', on_change=save_current_page_data, args=(page,))
        if st.session_state['form_data'].get('collect_child_data', False):
            st.multiselect('Child Data Protection Measures', ['Parental Consent', 'Child Data Encryption'], st.session_state['form_data'].get('child_protection_measures', []), key='child_protection_measures', on_change=save_current_page_data, args=(page,))
    elif page == 'International Data Transfer':
        st.checkbox('Transfer Data Internationally?', st.session_state['form_data'].get('international_transfer', False), key='international_transfer', on_change=save_current_page_data, args=(page,))
        if st.session_state['form_data'].get('international_transfer', False):
            st.multiselect('International Transfer Measures', TRANSFER_MEASURES, st.session_state['form_data'].get('transfer_measures', []), key='transfer_measures', on_change=save_current_page_data, args=(page,))
    elif page == 'Dispute Resolution':
        st.text_input('Dispute Resolution Mechanism', st.session_state['form_data'].get('dispute_resolution', ''), key='dispute_resolution', on_change=save_current_page_data, args=(page,))
    elif page == 'User Additions':
        st.text_area('Additional Requirements or Comments', st.session_state['form_data'].get('user_additions', ''), key='user_additions', on_change=save_current_page_data, args=(page,))
    elif page == 'Summary':
        st.write('## Summary')
        st.json(st.session_state['form_data'])

def validate_page(page_index):
    if SKIP_VALIDATION:
        return True
    required_fields = {
        0: ['company_name', 'address', 'contact'],
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