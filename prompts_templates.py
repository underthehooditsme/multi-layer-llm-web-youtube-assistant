SUMMARY_TEMPLATE = """{text}

-----------------
Using the above text, answer in short the following questions:

> {question}

------------------
if the question cannot be answered using the text,imply summarize the text. Include all factual information,numbers,stats etc
"""


SEARCH_TEMPLATE ="""
Write 3 google search queries to search online to form an objective opinion of from the following: 
{question} 
-----------------

You must respond with a list of strings in the following format:
-----------------
["query 1","query 2","query 3"]
"""


RESEARCH_REPORT_TEMPLATE = """Information: 
--------
{research_summary}
--------

Using the above information, answer the following question or topic: "{question}" in a detailed report -- \
The report should focus on the answer to the question, should be well structured, informative, \
in depth, with facts and numbers if available and a minimum of 1,200 words.

You should strive to write the report as long as you can using all relevant and necessary information provided.
You must write the report with markdown syntax.
You MUST determine your own concrete and valid opinion based on the given information. Do NOT deter to general and meaningless conclusions.
Write all used source urls at the end of the report, and make sure to not add duplicated sources, but only one reference for each.
You must write the report in apa format.
Please do your best, this is very important to my career.""" 

RESOURCE_REPORT_TEMPLATE = """Information: 
--------
{research_summary}
--------

Based on the above information, generate a bibliography recommendation report for the following question or topic: "{question}". \
The report should provide a detailed analysis of each recommended resource, explaining how each source can contribute to finding answers to the research question. \
Focus on the relevance, reliability, and significance of each source. \
Ensure that the report is well-structured, informative, in-depth, and follows Markdown syntax. \
Include relevant facts, figures, and numbers whenever available. \
The report should have a minimum length of 1,200 words.

Please do your best, this is very important to my career."""  


OUTLINE_REPORT_TEMPLATE = """Information: 
--------
{research_summary}
--------

Using the above information, generate an outline for a research report in Markdown syntax for the following question or topic: "{question}". \
The outline should provide a well-structured framework for the research report, including the main sections, subsections, and key points to be covered. \
The research report should be detailed, informative, in-depth, and a minimum of 1,200 words. \
Use appropriate Markdown syntax to format the outline and ensure readability.

Please do your best, this is very important to my career."""  


WRITER_SYSTEM_PROMPT = "You are an AI critical thinker research assistant. Your sole purpose is to write well written, critically acclaimed, objective and structured reports on given text."


YOUTUBE_SUMMARY_TEMPLATE = """{text}

-----------------
Using the above youtube transcript text, answer in short the following questions:

> {question}

------------------
if the question cannot be answered using the text,imply summarize the text. Include all factual information,numbers,stats etc
"""

YOUTUBE_SEARCH_TEMPLATE ="""
Write 3 youtube search queries to search youtube to form an objective opinion of from the following: 
{question} 
-----------------

You must respond with a list of strings in the following format:
-----------------
["query 1","query 2","query 3"]
"""


YOUTUBE_RESEARCH_REPORT_TEMPLATE = """Information: 
--------
{research_summary}
--------

Using the above information, answer the following question or topic: "{question}" in a detailed report -- \
The report should focus on the answer to the question, should be well structured, informative, \
in depth, with facts and numbers if available and a minimum of 1,200 words.

You should strive to write the report as long as you can using all relevant and necessary information provided.
You must write the report with markdown syntax.
You MUST determine your own concrete and valid opinion based on the given information. Do NOT deter to general and meaningless conclusions.
Write all used youtube source urls  at the end of the report, and make sure to not add duplicated sources, but only one reference for each.
You must write the report in apa format.
The data above comes from youtube transcripts so make the reference accordingly
Please do your best, this is very important to my career.""" 


BOTH_TEMPLATE ="""Text based web search Report Information: 
--------
{text_based_web_research_summary}
--------

Youtube based web search Report Information: 

--------
{youtube_based_web_research_summary}
--------

Using the above both information from both text based and youtube based , answer the following question or topic: "{question}" in a detailed report -- \
The report should focus on the answer to the question, should be well structured, informative, \
in depth, with facts and numbers if available and a minimum of 1,200 words.

You should strive to write the report as long as you can using all relevant and necessary information provided.
You must write the report with markdown syntax.
You MUST determine your own concrete and valid opinion based on the given information. Do NOT deter to general and meaningless conclusions.
Write all used source urls at the end of the report,Also mention at the end from where  you got the information from youtube and web based.
Also make sure to not add duplicated sources, but only one reference for each.
You must write the report in apa format.
Please do your best, this is very important to my career.
"""