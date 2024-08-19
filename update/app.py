import streamlit as st
import pandas as pd
import requests
import json
import os

from constants import (
    VERSION,
    API_URL,
    SKIP_VALIDATION,
    # Development version
    DISPLAY_TEMPLATE,
    DATA_TYPES,
    USAGE_PURPOSES,
    SHARING_PARTNERS,
    PROTECTION_MEASURES,
    USER_RIGHTS,
    TRANSFER_MEASURES,
    LEGAL_BASIS,
    SECTION_NAMES,
    SECTION_REQ,
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
        st.session_state['form_data']['area'] = ''
        st.session_state['form_data']['contact_email'] = ''
        st.session_state['form_data']['data_types'] = []
        st.session_state['form_data']['collection_methods'] = []
        st.session_state['form_data']['use_cookies'] = False
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
        st.session_state['uploaded_files'] = None
        
        st.session_state['from_back'] = {}
        st.session_state['from_back']['reg'] = []
        st.session_state['from_back']['syl'] = {}
        st.session_state['from_back']['SEC1'] = {}
        st.session_state['from_back']['SEC2'] = {}
        st.session_state['from_back']['SEC3'] = {}
        st.session_state['from_back']['SEC4'] = {}
        st.session_state['from_back']['SEC5'] = {}
        st.session_state['from_back']['SEC6'] = {}
        st.session_state['from_back']['SEC7'] = {}
        st.session_state['from_back']['SEC8'] = {}
        st.session_state['from_back']['SEC9'] = {}
        st.session_state['from_back']['SEC10'] = {}
        st.session_state['from_back']['SEC11'] = {}
        st.session_state['from_back']['SEC12'] = {}
        
        st.session_state['from_back']['SEC1_flag'] = True
        st.session_state['from_back']['SEC2_flag'] = True
        st.session_state['from_back']['SEC3_flag'] = True
        st.session_state['from_back']['SEC4_flag'] = True
        st.session_state['from_back']['SEC5_flag'] = True
        st.session_state['from_back']['SEC6_flag'] = True
        st.session_state['from_back']['SEC7_flag'] = True
        st.session_state['from_back']['SEC8_flag'] = True
        st.session_state['from_back']['SEC9_flag'] = True
        st.session_state['from_back']['SEC10_flag'] = True
        st.session_state['from_back']['SEC11_flag'] = True
        st.session_state['from_back']['SEC12_flag'] = True
        st.session_state['from_back']['flag'] = [False]*12
        st.session_state['from_back']['flag'][0] = True
        st.session_state['from_back']['flag'][6] = True
        st.session_state['from_back']['flag'][8] = True
        st.session_state['from_back']['flag'][10] = True
        
        st.session_state['user_input'] = ''

    # Pages
    pages = [
        'Company Information',
        'Data Collection and Usage',
        'Data Subject Rights',
        'Data Sharing and Transfers',
        'Data Retention and Security',
        'Cookies Usage',
        'Laws and Dispute Resolution',
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
            if st.button('Confirm'):
                if validate_page(st.session_state['page']):
                    save_current_page_data(pages[st.session_state['page']])
                    save_data(st.session_state['form_data'])
                    st.success('Data saved successfully!')
                    st.session_state['page'] = 0
                    st.session_state['form_data'] = {}
                    st.rerun()
                    
def suggestions_input():
    col1, col2, col3 = st.columns([1, 4, 1], vertical_alignment='bottom')

    with col1:
        categories = [x.upper() for x in SECTION_NAMES.keys()]
        selected_category = st.selectbox("Select a category:", categories)

    with col2:
        user_input = st.text_input("Enter info:", st.session_state.get('user_input', ''))

    with col3:
        if st.button("Submit"):
            st.success(f"Data for {selected_category} received: {user_input}")
            if st.session_state['from_back'][selected_category]!={} and user_input != 'regenerate':
                print(st.session_state['from_back'][selected_category])
                text = st.session_state['from_back'][selected_category]
                reg = ','.join(st.session_state['from_back']['reg'])
                #syl = json.dumps(st.session_state['from_back']['syl'][f'{value}'], indent=4) 
                syl = json.dumps({SECTION_NAMES[selected_category]: st.session_state['from_back']['syl'][SECTION_NAMES[selected_category]]}, indent=4) 
                try:
                    # Send a request to obtain the regulations of the corresponding region
                    response = requests.post(f"{API_URL}/regenerate", data={"section_name": SECTION_NAMES[selected_category],
                                                                        "section_text": text,
                                                                        "syllabus" : syl,
                                                                        "regulations" : reg,
                                                                        "suggestions" : user_input})
                    
                    if response.status_code == 200:
                        section = response.json()
                        st.session_state['from_back'][f'{selected_category}'] = section['content']
                        print(st.session_state['from_back'][f'{selected_category}'])  
                        if DISPLAY_TEMPLATE:
                            print(f"{SECTION_NAMES[selected_category]}:")
                            print(section)
                    else:
                        print(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                st.session_state['from_back'][f'{selected_category}_flag'] = True
            else:
                infor = json.dumps(st.session_state['form_data'], indent=4)
                reg = ','.join(st.session_state['from_back']['reg'])
                #syl = json.dumps(st.session_state['from_back']['syl'][f'{value}'], indent=4) 
                syl = json.dumps({SECTION_NAMES[selected_category]: st.session_state['from_back']['syl'][SECTION_NAMES[selected_category]]}, indent=4) 
                try:
                    # Send a request to obtain the regulations of the corresponding region
                    response = requests.post(f"{API_URL}/generate", data={"section_name": SECTION_NAMES[selected_category],
                                                                        "information" : infor,
                                                                        "syllabus" : syl,
                                                                        "regulations" : reg})
                    
                    if response.status_code == 200:
                        section = response.json()
                        st.session_state['from_back'][f'{selected_category}'] = section['content']
                        print(st.session_state['from_back'][f'{selected_category}'])  
                        if DISPLAY_TEMPLATE:
                            print(f"{SECTION_NAMES[selected_category]}:")
                            print(section)
                    else:
                        print(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                st.session_state['from_back'][f'{selected_category}_flag'] = True
            st.rerun()
            
            
def renew_flag(num):
    if num == 0:
        for  i in range(len(st.session_state['from_back']['flag'])):
            if st.session_state['from_back']['flag'][i] == True:
                st.session_state['from_back'][f'SEC{i+1}_flag'] = False
    else:
        st.session_state['from_back'][f'SEC{num}_flag'] = False


def save_current_page_data(page):
    # Check which page is active and save data accordingly
    form_data = st.session_state['form_data']
    
    if page == 'Company Information':
        # Save company info
        if form_data['area'] != st.session_state.get('area', ''):
            renew_flag(0)
            try:
                # Send a request to obtain the regulations of the corresponding region
                response = requests.post(f"{API_URL}/regulations", data={"areas": st.session_state.get('area', '')})
                if response.status_code == 200:
                    regulations = response.json()
                    st.session_state['from_back']['reg'] = [reg["regulations"] for reg in regulations]
                    if DISPLAY_TEMPLATE:
                        st.write("Regulations for the selected area:")
                        st.json(regulations)
                    try:
                        # Send a request to generate a course outline for the corresponding regulations
                        response = requests.post(f"{API_URL}/syllabus", data={"regulations": ",".join(st.session_state['from_back']['reg'])})
                        if response.status_code == 200:
                            st.session_state['from_back']['syl'] = response.json()
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                
        if (form_data['company_name'] != st.session_state.get('company_name', '') or 
             form_data['address'] != st.session_state.get('address', '')):
            renew_flag(2)
            
        if (form_data['contact_email'] != st.session_state.get('contact_email', '')):
            renew_flag(12)
            
            
        form_data['company_name'] = st.session_state.get('company_name', '')
        form_data['address'] = st.session_state.get('address', '')
        form_data['area'] = st.session_state.get('area', '')
        form_data['contact_email'] = st.session_state.get('contact_email', '')
        
        st.session_state['from_back']['flag'][1] = True

    elif page == 'Data Collection and Usage':
        # Save data collection and usage info
        if (form_data['data_types'] != st.session_state.get('data_types', []) or 
             form_data['collection_methods'] != st.session_state.get('collection_methods', []) or
             form_data['usage_purposes'] != st.session_state.get('usage_purposes', []) or 
             form_data['legal_basis'] != st.session_state.get('legal_basis', []) ):
            renew_flag(3)
            
        form_data['data_types'] = st.session_state.get('data_types', [])
        form_data['collection_methods'] = st.session_state.get('collection_methods', [])
        form_data['usage_purposes'] = st.session_state.get('usage_purposes', [])
        form_data['legal_basis'] = st.session_state.get('legal_basis', [])
        
        st.session_state['from_back']['flag'][2] = True

    elif page == 'Data Subject Rights':
        # Save data subject rights info
        if (form_data['user_rights'] != st.session_state.get('user_rights', []) or 
             form_data['collect_child_data'] != st.session_state.get('collect_child_data', False) or
             form_data['child_protection_measures'] != st.session_state.get('child_protection_measures', [])):
            renew_flag(4)
        
        form_data['user_rights'] = st.session_state.get('user_rights', [])
        form_data['collect_child_data'] = st.session_state.get('collect_child_data', False)
        form_data['child_protection_measures'] = st.session_state.get('child_protection_measures', [])

        st.session_state['from_back']['flag'][3] = True
    elif page == 'Data Sharing and Transfers':
        # Save data sharing and transfers info
        if (form_data['sharing_partners'] != st.session_state.get('sharing_partners', []) or 
             form_data['international_transfer'] != st.session_state.get('international_transfer', False) or
             form_data['transfer_measures'] != st.session_state.get('transfer_measures', [])):
            renew_flag(5)
        
        form_data['sharing_partners'] = st.session_state.get('sharing_partners', [])
        form_data['international_transfer'] = st.session_state.get('international_transfer', False)
        form_data['transfer_measures'] = st.session_state.get('transfer_measures', [])
        
        st.session_state['from_back']['flag'][4] = True
    elif page == 'Data Retention and Security':
        # Save data retention and security info
        if (form_data['retention_period'] != st.session_state.get('retention_period', '')):
            renew_flag(6)
            
        if (form_data['protection_measures'] != st.session_state.get('protection_measures', [])):
            renew_flag(8)
            
        form_data['retention_period'] = st.session_state.get('retention_period', '')
        form_data['protection_measures'] = st.session_state.get('protection_measures', [])

        st.session_state['from_back']['flag'][5] = True
        st.session_state['from_back']['flag'][7] = True
    elif page == 'Cookies Usage':
        # Save cookies usage info
        if (form_data['use_cookies'] != st.session_state.get('use_cookies', False)):
            renew_flag(10)
        
        form_data['use_cookies'] = st.session_state.get('use_cookies', False)
        
        st.session_state['from_back']['flag'][9] = True
    elif page == 'Laws and Dispute Resolution':
        # Save laws and dispute resolution info
        if (form_data['dispute_resolution'] != st.session_state.get('dispute_resolution', '')):
            renew_flag(12)
        
        if (form_data['uploaded_files'] != st.session_state.get('uploaded_files', None)):
            renew_flag(0)
            try:
                # Send a request to generate a course outline for the corresponding regulations
                response = requests.post(f"{API_URL}/syllabus", data={"regulations": ",".join(st.session_state['from_back']['reg']),
                                                                      "upload_files": st.session_state.get('uploaded_files', None)})
                if response.status_code == 200:
                    st.session_state['from_back']['syl'] = response.json()
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        
        # if (form_data['uploaded_files'] != st.session_state['form_data']['uploaded_files']):
        #     renew_flag(10) 上传文档
            
        form_data['dispute_resolution'] = st.session_state.get('dispute_resolution', '')
        form_data['uploaded_files'] = [file.name for file in st.session_state.get('uploaded_files', []) if file is not None]

        st.session_state['from_back']['flag'][11] = True
    
    # After handling the specific page, save the updated form_data back to the session state   
    if st.session_state['from_back']['syl']!={}:
        infor = json.dumps(st.session_state['form_data'], indent=4)
        reg = ','.join(st.session_state['from_back']['reg'])
        for key, value in SECTION_NAMES.items():
            #syl = json.dumps(st.session_state['from_back']['syl'][f'{value}'], indent=4) 
            syl = json.dumps({value: st.session_state['from_back']['syl'][value]}, indent=4) 
            if st.session_state['from_back'][f'{key}_flag'] == False:
                #st.text_area("Form Data as JSON String:", form_data_json, height=300)
                try:
                    # Send a request to obtain the regulations of the corresponding region
                    response = requests.post(f"{API_URL}/generate", data={"section_name": value,
                                                                          "information" : infor,
                                                                          "syllabus" : syl,
                                                                          "regulations" : reg})
                    
                    if response.status_code == 200:
                        section = response.json()
                        st.session_state['from_back'][f'{key}'] = section['content']
                        print(st.session_state['from_back'][f'{key}'])  
                        if DISPLAY_TEMPLATE:
                            print(f"{value}:")
                            print(section)
                    else:
                        print(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                st.session_state['from_back'][f'{key}_flag'] = True
    st.session_state['form_data'] = form_data

def display_page(page):
    st.title(page)
    if page == 'Company Information':
        st.session_state['company_name'] = st.text_input('Company Name', st.session_state['form_data'].get('company_name', ''))
        st.session_state['address'] = st.text_input('Address', st.session_state['form_data'].get('address', ''))
        st.session_state['area'] = st.text_input('Service Area', st.session_state['form_data'].get('area', ''))
        st.session_state['contact_email'] = st.text_input('Contact Email', st.session_state['form_data'].get('contact_email', ''))

    elif page == 'Data Collection and Usage':
        st.session_state['data_types'] = st.multiselect('Types of Data Collected', DATA_TYPES, st.session_state['form_data'].get('data_types', []))
        st.session_state['collection_methods'] = st.multiselect('Data Collection Methods', ['Directly from you', 'Automatically', 'From third parties'], st.session_state['form_data'].get('collection_methods', []))
        st.session_state['usage_purposes'] = st.multiselect('Data Usage Purposes', USAGE_PURPOSES, st.session_state['form_data'].get('usage_purposes', []))
        st.session_state['legal_basis'] = st.multiselect('Legal Basis for Processing', LEGAL_BASIS, st.session_state['form_data'].get('legal_basis', []))
        
    elif page == 'Data Subject Rights':
        st.session_state['user_rights'] = st.multiselect('User Rights', USER_RIGHTS, st.session_state['form_data'].get('user_rights', []))
        st.session_state['collect_child_data'] = st.checkbox('Collect Data from Children?', st.session_state['form_data'].get('collect_child_data', False))
        if st.session_state['collect_child_data']:
            st.session_state['child_protection_measures'] = st.multiselect('Child Data Protection Measures', ['Parental Consent', 'Child Data Encryption'], st.session_state['form_data'].get('child_protection_measures', []))

    elif page == 'Data Sharing and Transfers':
        st.session_state['sharing_partners'] = st.multiselect('Data Sharing Partners', SHARING_PARTNERS, st.session_state['form_data'].get('sharing_partners', []))
        st.session_state['international_transfer'] = st.checkbox('Transfer Data Internationally?', st.session_state['form_data'].get('international_transfer', False))
        if st.session_state['international_transfer']:
            st.session_state['transfer_measures'] = st.multiselect('International Transfer Measures', TRANSFER_MEASURES, st.session_state['form_data'].get('transfer_measures', []))

    elif page == 'Data Retention and Security':
        st.session_state['retention_period'] = st.text_input('Data Retention Period', st.session_state['form_data'].get('retention_period', ''))
        st.session_state['protection_measures'] = st.multiselect('Data Protection Measures', PROTECTION_MEASURES, st.session_state['form_data'].get('protection_measures', []))

    elif page == 'Cookies Usage':
        st.session_state['use_cookies'] = st.checkbox('Use Cookies and Tracking Technologies?', st.session_state['form_data'].get('use_cookies', False))

    elif page == 'Laws and Dispute Resolution':
        st.session_state['dispute_resolution'] = st.text_input('Dispute Resolution Mechanism', st.session_state['form_data'].get('dispute_resolution', ''))
        uploaded_files = st.file_uploader("Upload relevant documents", accept_multiple_files=True, type=['pdf', 'docx', 'txt'])
        # Store uploaded files in session_state if you need to access them later
        st.session_state['uploaded_files'] = uploaded_files
    elif page == 'Summary':
        #st.json(st.session_state['form_data'])
        for key, value in SECTION_NAMES.items():
            st.subheader(f'{key}:{value}')
            st.write(st.session_state['from_back'][key])
        suggestions_input()
        


    with st.sidebar:
        st.markdown(f"Version {VERSION}")
        
    
    # SECTION1 = "Introduction"
    # SECTION2 = "Data Controller Information"
    # SECTION3 = "Data Collection and Usage"
    # SECTION4 = "Data Subject Rights"
    # SECTION5 = "Data Sharing and Transfers"
    # SECTION6 = "Data Retention"
    # SECTION7 = "Disclosure of Personal Information"
    # SECTION8 = "Security Measures"
    # SECTION9 = "Automated Decision-Making and Profiling"
    # SECTION10 = "Cookies and Tracking Technologies"
    # SECTION11 = "Changes to the Privacy Policy"
    # SECTION12 = "Contact Information"
    
    # if st.session_state['form_data']['company_name'] or st.session_state['form_data']['address'] or st.session_state['form_data']['contact_email']:
    #         with st.sidebar.expander("Company Information"):
    #             st.markdown(pg.generate_company_information(
    #                     st.session_state['form_data'], 
    #                 ), unsafe_allow_html=True)
    #             if not (st.session_state['form_data']['company_name'] and st.session_state['form_data']['address'] and st.session_state['form_data']['contact_email']):
    #                 st.warning(" You haven't finnish Company Info Part" )
    #     else:
    #         with st.sidebar:
    #             st.warning("Company Info Part left to be finish" )


        
    #     if st.session_state['form_data']['company_name'] or st.session_state['form_data']['address'] or st.session_state['form_data']['contact_email']:
    #         with st.sidebar.expander("Contact Us"):
    #             st.markdown(pg.generate_contact_us(
    #                     st.session_state['form_data'], 
    #                 ), unsafe_allow_html=True)
    #             if not (st.session_state['form_data']['company_name'] and st.session_state['form_data']['address'] and st.session_state['form_data']['contact_email']):
    #                 st.warning(" You haven't finnish Company Info Part" )
    #     with st.sidebar:
    #         st.warning("Contact Us Part left to be finish" )
    
    if st.session_state['from_back']['syl'] != {}:
        # SECTION1 = "Introduction"
        
        
        
        # SECTION2 = "Data Controller Information"
        
        
        
        # SECTION3 = "Data Collection and Usage"
        
        
        
        # SECTION4 = "Data Subject Rights"
        
        
        
        # SECTION5 = "Data Sharing and Transfers"
        
        
        # SECTION6 = "Data Retention"
        
        
        # SECTION7 = "Disclosure of Personal Information"
        
        
        # SECTION8 = "Security Measures"
        
        
        # SECTION9 = "Automated Decision-Making and Profiling"
        
        
        # SECTION10 = "Cookies and Tracking Technologies"
        
        
        # SECTION11 = "Changes to the Privacy Policy"
        # SECTION12 = "Contact Information"
        if DISPLAY_TEMPLATE:
            for key, value in SECTION_REQ.items():
                if st.session_state['from_back'][key] != {}:
                    with st.sidebar.expander(f"{SECTION_NAMES[key]}"):
                        st.markdown(f"{st.session_state['from_back'][key]}")
                else:
                    with st.sidebar:
                        if DISPLAY_TEMPLATE:
                            st.warning(f"Need More Info for {key}: {value}" )
                        else:
                            st.warning(f"Need More Info for {key}" )


        
        
        
        
        
        # Template Beta
        if DISPLAY_TEMPLATE:
            # Dynamically generate and display privacy policy template
            with st.sidebar.expander("Preview Privacy Policy Template"):
                if st.session_state['form_data']:
                    st.json(st.session_state['from_back']['syl'])
    else:
        with st.sidebar:
            st.warning("Need Area Info for template" )

def validate_page(page_index):
    if SKIP_VALIDATION:
        return True
    required_fields = {
        0: ['company_name', 'address', 'area',  'contact_email'],
        1: ['data_types', 'collection_methods', 'usage_purposes'],
        2: ['user_rights', 'collect_child_data'],
        3: ['sharing_partners', 'international_transfer'],
        4: ['retention_period', 'protection_measures'],
        5: ['use_cookies'],
        6: ['dispute_resolution']
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