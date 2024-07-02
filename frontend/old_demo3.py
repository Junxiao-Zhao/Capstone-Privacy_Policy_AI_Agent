import streamlit as st
import pandas as pd

# Constants for testing
SKIP_VALIDATION = True

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
        'Data Usage',
        'Data Sharing',
        'Data Protection',
        'User Rights',
        'Child Privacy',
        'International Data Transfer',
        'Summary'
    ]

    # Display current page
    display_page(pages[st.session_state['page']])

    # Page navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.session_state['page'] > 0:
            if st.button('Previous'):
                st.session_state['page'] -= 1
    with col3:
        if st.session_state['page'] < len(pages) - 1:
            if st.button('Next'):
                if validate_page(st.session_state['page']):
                    st.session_state['page'] += 1
        else:
            if st.button('Submit'):
                if validate_page(st.session_state['page']):
                    save_data(st.session_state['form_data'])
                    st.success('Data saved successfully!')
                    st.session_state['page'] = 0
                    st.session_state['form_data'] = {}

def display_page(page):
    st.title(page)
    if page == 'Company Info':
        st.session_state['form_data']['company_name'] = st.text_input('Company Name', st.session_state['form_data'].get('company_name', ''))
        st.session_state['form_data']['address'] = st.text_input('Address', st.session_state['form_data'].get('address', ''))
        st.session_state['form_data']['contact'] = st.text_input('Contact Email', st.session_state['form_data'].get('contact', ''))
    elif page == 'Data Collection':
        st.session_state['form_data']['data_types'] = st.multiselect('Types of Data Collected', ['Personal Information', 'Account Information', 'Content Data', 'Usage Data', 'Device Information', 'Location Data', 'Payment Information'], st.session_state['form_data'].get('data_types', []))
    elif page == 'Data Usage':
        st.session_state['form_data']['usage_purposes'] = st.multiselect('Data Usage Purposes', ['Providing Services', 'Customer Support', 'Improving Services', 'Security and Fraud Prevention', 'Legal Compliance'], st.session_state['form_data'].get('usage_purposes', []))
    elif page == 'Data Sharing':
        st.session_state['form_data']['sharing_partners'] = st.multiselect('Data Sharing Partners', ['Service Providers', 'Advertisers', 'Legal Authorities', 'Other Users'], st.session_state['form_data'].get('sharing_partners', []))
    elif page == 'Data Protection':
        st.session_state['form_data']['protection_measures'] = st.multiselect('Data Protection Measures', ['Encryption', 'Access Control', 'Data Minimization'], st.session_state['form_data'].get('protection_measures', []))
    elif page == 'User Rights':
        st.session_state['form_data']['user_rights'] = st.multiselect('User Rights', ['Access Data', 'Correct Data', 'Delete Data', 'Data Portability', 'Opt-out'], st.session_state['form_data'].get('user_rights', []))
    elif page == 'Child Privacy':
        st.session_state['form_data']['collect_child_data'] = st.checkbox('Collect Data from Children?', st.session_state['form_data'].get('collect_child_data', False))
        if st.session_state['form_data']['collect_child_data']:
            st.session_state['form_data']['child_protection_measures'] = st.multiselect('Child Data Protection Measures', ['Parental Consent', 'Child Data Encryption'], st.session_state['form_data'].get('child_protection_measures', []))
    elif page == 'International Data Transfer':
        st.session_state['form_data']['international_transfer'] = st.checkbox('Transfer Data Internationally?', st.session_state['form_data'].get('international_transfer', False))
        if st.session_state['form_data']['international_transfer']:
            st.session_state['form_data']['transfer_measures'] = st.multiselect('International Transfer Measures', ['Standard Contractual Clauses', 'Privacy Shield'], st.session_state['form_data'].get('transfer_measures', []))
    elif page == 'Summary':
        st.write('## Summary')
        st.json(st.session_state['form_data'])

def validate_page(page_index):
    if SKIP_VALIDATION:
        return True
    required_fields = {
        0: ['company_name', 'address', 'contact'],
        1: ['data_types'],
        2: ['usage_purposes'],
        3: ['sharing_partners'],
        4: ['protection_measures'],
        5: ['user_rights'],
        6: ['collect_child_data'],
        7: ['international_transfer'],
    }
    page = list(required_fields.keys())[page_index]
    for field in required_fields.get(page, []):
        if not st.session_state['form_data'].get(field):
            st.warning(f"Please complete the '{field}' field.")
            return False
    return True

def save_data(data):
    df = pd.DataFrame([data])
    df.to_csv('privacy_policy_data.csv', index=False)

if __name__ == '__main__':
    main()