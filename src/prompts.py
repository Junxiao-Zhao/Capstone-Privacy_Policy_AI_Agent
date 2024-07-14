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

GENERATE_PROMPT = """\
Please generate a {section_name} section of a privacy policy \
based on these information provided below:

{information}

NOTE THAT: The generated section should comply with the following key points:

{key_points}
"""

REGENERATE_PROMPT = """\
This {section_name} is a section of a privacy policy:

{section_text}

Now, please revise the section based on the following suggestions:

{suggestions}

NOTE THAT: The revised section should comply with the following key points:

{key_points}
"""

JUDGE_SECTION_TEMPLATE = """\
This {section_name} is a section of a privacy policy:

{section_text}

Please judge whether this section is compliant with the {regulations} \
regulations. If not, please provide suggestions on how to improve it.
NOTE THAT this is just one section, not the whole privacy policy. \
Only judge this section in isolation.
"""

FORMAT_JUDGE_TEMPLATE = """\
Given the comments from a legal expert:

{query_str}

Please extract the legal expert's suggestions on how to improve \
the sections in a privacy policy.
"""
