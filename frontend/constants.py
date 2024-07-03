# constants.py

# Constants for testing
VERSION = '1.0.0.Beta'

SKIP_VALIDATION = False
DISPLAY_TEMPLATE = False

if VERSION[-1] == 'a':
    SKIP_VALIDATION = True
    DISPLAY_TEMPLATE = True

LETTER_COLOR = 'red'

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
