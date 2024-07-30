REGION_TEMPLATE = """
    Assistant: I can help determine which region a user input belongs to. The options are: California, European Union, Canada, Australia, United Kingdom, Japan, South Korea, South Africa, Singapore, Brazil, Other. Make sure to include all options.

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