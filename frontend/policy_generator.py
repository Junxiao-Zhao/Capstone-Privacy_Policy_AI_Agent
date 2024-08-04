global LETTER_COLOR
LETTER_COLOR = 'red'

def get_description(key, desc_dict):
    return desc_dict.get(key, 'Description not available')

def generate_privacy_policy(user_data, data_type_desc, collection_method_desc, usage_purpose_desc, sharing_partner_desc, protection_measure_desc, user_right_desc, transfer_measure_desc, legal_basis_desc):

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

    color = LETTER_COLOR
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


def generate_company_information(user_data):

    # Initialize all variables
    color = LETTER_COLOR
    

    template = f"""
    <h2>Privacy Policy</h2>

    <h3>Introduction</h3>
    <p>Welcome to <span style="color:{color};">{user_data.get('company_name', 'Your Company')}</span>'s Privacy Policy. Your privacy is critically important to us. This policy explains the types of information we collect, how we use it, and the measures we take to protect it.</p>

    <h3>Company Information</h3>
    <p><strong>Company Name</strong>: <span style="color:{color};">{user_data.get('company_name', 'Your Company')}</span></p>
    <p><strong>Address</strong>: <span style="color:{color};">{user_data.get('address', 'Your Address')}</span></p>
    <p><strong>Contact Email</strong>: <span style="color:{color};">{user_data.get('contact_email', 'your.email@example.com')}</span></p>
    """

    return template

def generate_contact_us(user_data):

    # Initialize all variables
    color = LETTER_COLOR
    

    template = f"""
    <h3>Dispute Resolution</h3>
    <p>If you have any complaints or concerns about our Privacy Policy or practices, please contact us at <span style="color:{color};">{user_data.get('contact_email', 'your.email@example.com')}</span>. We will work with you to resolve any issues.</p>

    <h3>Changes to This Privacy Policy</h3>
    <p>We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page. You are advised to review this Privacy Policy periodically for any changes.</p>

    <h3>Contact Us</h3>
    <p>If you have any questions about this Privacy Policy, please contact us at <span style="color:{color};">{user_data.get('contact_email', 'your.email@example.com')}</span>.</p>
    """

    return template