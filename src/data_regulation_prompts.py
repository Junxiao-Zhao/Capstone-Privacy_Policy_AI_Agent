REGION_TEMPLATE = """
    Assistant: I can help determine which region a user input belongs to. The options are: {regions}, Other. Make sure to include all options.
    Examples:
    User: los angeles
    Assistant: California
    User: hong kong
    Assistant: Other
    User: London
    Assistant: European Union, United Kingdom
    User: toronto
    Assistant: Canada
    Now, let's try with your input.
    User: {user_input}
    Assistant: The regions that the user input belongs to are:
    """

INDUSTRY_TEMPLATE = """
    Assistant: I can help determine which industry a user input belongs to. The options are: {industries}, Other. Make sure to include all options.
    Example:
    User: children
    Assistant: Children
    User: consume
    Assistant: Consumption
    User: school
    Assistant: Education
    User: media
    Assistant: Digital Media
    Now, let's try with your input.
    User: {user_input}
    Assistant: The industry that the user input belongs to is (are):
    """