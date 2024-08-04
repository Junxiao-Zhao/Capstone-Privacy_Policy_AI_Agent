import streamlit as st
import pandas as pd

from constants import (
    VERSION,
    SKIP_VALIDATION,
    DISPLAY_TEMPLATE,
    DATA_TYPES,
    USAGE_PURPOSES,
    SHARING_PARTNERS,
    PROTECTION_MEASURES,
    USER_RIGHTS,
    TRANSFER_MEASURES,
    LEGAL_BASIS,
    DATA_TYPE_DESCRIPTIONS,
    USAGE_PURPOSE_DESCRIPTIONS,
    SHARING_PARTNER_DESCRIPTIONS,
    PROTECTION_MEASURE_DESCRIPTIONS,
    USER_RIGHT_DESCRIPTIONS,
    TRANSFER_MEASURE_DESCRIPTIONS,
    LEGAL_BASIS_DESCRIPTIONS,
    COLLECTION_METHODS_DESCRIPTIONS
)

import policy_generator as pg

def add_logo(version, number):
    st.markdown(
        f"{version+number}"
    )

def main():
    # Initialize session state
    st.markdown('test')

    if 'page' not in st.session_state:
        st.session_state['page'] = 0
    if 'form_data' not in st.session_state:
        st.session_state['form_data'] = {}
        st.session_state['form_data']['company_name'] = ''
        st.session_state['form_data']['address'] = ''
        st.session_state['form_data']['contact_email'] = ''
        st.session_state['form_data']['data_types'] = []
        st.session_state['form_data']['collection_methods'] = []
        st.session_state['form_data']['use_cookies'] = []
        st.session_state['form_data']['usage_purposes'] = []
        st.session_state['form_data']['sharing_partners'] = []
        st.session_state['form_data']['protection_measures'] = []
        st.session_state['form_data']['retention_period'] = ''
        st.session_state['form_data']['user_rights'] = []
        st.session_state['form_data']['legal_basis'] = []
        st.session_state['form_data']['collect_child_data'] = False
        st.session_state['form_data']['child_protection_measures'] = []
        st.session_state['form_data']['international_transfer'] = False
        st.session_state['form_data']['transfer_measures'] = []
        st.session_state['form_data']['dispute_resolution'] = ''
        st.session_state['form_data']['user_additions'] = ''

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
                st.rerun()
    with col3:
        if st.session_state['page'] < len(pages) - 1:
            if st.button('Next'):
                if validate_page(st.session_state['page']):
                    save_current_page_data(pages[st.session_state['page']])
                    st.session_state['page'] += 1
                    st.rerun()
        else:
            if st.button('Submit'):
                if validate_page(st.session_state['page']):
                    save_current_page_data(pages[st.session_state['page']])
                    save_data(st.session_state['form_data'])
                    st.success('Data saved successfully!')
                    st.session_state['page'] = 0
                    st.session_state['form_data'] = {}
                    st.rerun()

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
        st.session_state['form_data']['legal_basis'] = st.session_state.get('legal_basis', [])
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
        st.session_state['legal_basis'] = st.multiselect('Legal Basis for Processing', LEGAL_BASIS, st.session_state['form_data'].get('legal_basis', []))
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

    with st.sidebar:
        st.markdown(f"Version {VERSION}")
    
    if st.session_state['form_data']['company_name'] or st.session_state['form_data']['address'] or st.session_state['form_data']['contact_email']:
        with st.sidebar.expander("Company Information"):
            st.markdown(pg.generate_company_information(
                    st.session_state['form_data'], 
                ), unsafe_allow_html=True)
            if not (st.session_state['form_data']['company_name'] and st.session_state['form_data']['address'] and st.session_state['form_data']['contact_email']):
                st.warning(" You haven't finnish Company Info Part" )
    else:
        with st.sidebar:
            st.warning("Company Info Part left to be finish" )


    
    if st.session_state['form_data']['company_name'] or st.session_state['form_data']['address'] or st.session_state['form_data']['contact_email']:
        with st.sidebar.expander("Contact Us"):
            st.markdown(pg.generate_contact_us(
                    st.session_state['form_data'], 
                ), unsafe_allow_html=True)
            if not (st.session_state['form_data']['company_name'] and st.session_state['form_data']['address'] and st.session_state['form_data']['contact_email']):
                st.warning(" You haven't finnish Company Info Part" )
    with st.sidebar:
        st.warning("Contact Us Part left to be finish" )





    if DISPLAY_TEMPLATE:
        # Dynamically generate and display privacy policy template
        with st.sidebar.expander("Preview Privacy Policy Template"):
            if st.session_state['form_data']:
                st.markdown(pg.generate_privacy_policy(
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