ASK_SYLLABUS_TEMPLATE = """\
I want to write a privacy policy, which should be {regulations} compliant.
What sections should it include? And for each section, what key \
points should be covered?
List them as bullet points."""

FORMAT_SYLLABUS_TEMPLATE = """\
Given the privacy policy sections and key points:

{query_str}

DO NOT modify the key points!!!
Please rearrange the sections and key points and output with the \
following JSON format:"""
