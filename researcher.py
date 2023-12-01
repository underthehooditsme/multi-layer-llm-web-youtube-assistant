from langchain.llms import GooglePalm
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain.prompts import HumanMessagePromptTemplate
from langchain.schema.runnable import ConfigurableField
from langchain.document_loaders import YoutubeLoader
from youtube_transcript_api import YouTubeTranscriptApi
from youtubesearchpython import VideosSearch
from pytube import YouTube
from prompts_templates import *
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re
import json
import requests


MAX_CHARACTERS_EXTRACTED_FROM_PAGE = 10000
RESULTS_PER_QUESTION = 3

load_dotenv()

model = GooglePalm( temperature = 0)

def scrape_text(url: str) -> str:
    """
    Retrieve text content from a webpage.

    Parameters:
    - url (str): The URL of the webpage to scrape.

    Returns:
    - str: The text content of the webpage.

    If the retrieval is successful (status code 200), the function parses the HTML content
    using BeautifulSoup and returns the text content, stripping leading and trailing whitespaces.

    If the retrieval fails, an error message is returned, including the HTTP status code.
    """
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            page_text = soup.get_text(separator=" ", strip=True)
            return page_text
        else:
            return f"Failed to retrieve the webpage: Status code {response.status_code}"

    except Exception as e:
        print(e)
        return f"Failed to retrieve the webpage: {e}"
    
def web_search(query: str, num_results: int = RESULTS_PER_QUESTION) -> list[str]:
    """
    Perform a web search using DuckDuckGo Search API and retrieve a specified number of results.

    Parameters:
    - query (str): The search query to be performed.
    - num_results (int, optional): The number of results to retrieve. Defaults to RESULTS_PER_QUESTION.

    Returns:
    - List[str]: A list of URLs representing the search results.

    This function uses the DuckDuckGo Search API to perform a web search based on the given query.
    It retrieves a specified number of results (default is RESULTS_PER_QUESTION) and returns a list
    of URLs extracted from the search results.

    Parameters:
    - query (str): The search query to be performed.
    - num_results (int, optional): The number of results to retrieve. Defaults to RESULTS_PER_QUESTION.

    Returns:
    - List[str]: A list of URLs representing the search results.
    """
    results = ddg_search.results(query, num_results)
    return [r['link'] for r in results]




#   Prompt to summarize a text from a yrl
SUMMARY_PROMPT = ChatPromptTemplate.from_template(SUMMARY_TEMPLATE)


# scrape_and_summarize_chain = RunnablePassthrough.assign(text=lambda x: scrape_text(x["url"])[:min(MAX_CHARACTERS_EXTRACTED_FROM_PAGE, len(x["url"]))]
# )|SUMMARY_PROMPT | model | StrOutputParser()

scrape_and_summarize_chain = RunnablePassthrough.assign(summary = RunnablePassthrough.assign(text=lambda x: scrape_text(x["url"])[:min(10000, len(x["url"]))]
)|SUMMARY_PROMPT | model | StrOutputParser()) | (lambda x:f"url : {x['url']}\n\nsummary : {x['summary']}")

ddg_search = DuckDuckGoSearchAPIWrapper()

# get list of dictionary of question and link from a question
link_extraction_chain = RunnablePassthrough.assign(
    urls = lambda x: web_search(x["question"])
)| (lambda x : [{"question":x["question"],"url": u} for u in x["urls"]])


text_single_question_multilink_web_search_chain = link_extraction_chain | scrape_and_summarize_chain.map()

SEARCH_PROMPT = ChatPromptTemplate.from_messages(
    [
        HumanMessagePromptTemplate.from_template(SEARCH_TEMPLATE)
    ]
)

create_question_chain = SEARCH_PROMPT | model | StrOutputParser() | json.loads


#given a question it creates question then for each question finds multiple urls then for each such url data is fetched,creates a list of list
full_text_web_search_chain =create_question_chain |(lambda x : [ {"question": q} for q in x]) |text_single_question_multilink_web_search_chain.map()

full_web_text_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", WRITER_SYSTEM_PROMPT),
        ("user", RESEARCH_REPORT_TEMPLATE),
    ]
).configurable_alternatives(
    ConfigurableField("report_type"),
    default_key="research_report",
    resource_report=ChatPromptTemplate.from_messages(
        [
            ("system", WRITER_SYSTEM_PROMPT),
            ("user", RESOURCE_REPORT_TEMPLATE),
        ]
    ),
    outline_report=ChatPromptTemplate.from_messages(
        [
            ("system", WRITER_SYSTEM_PROMPT),
            ("user", OUTLINE_REPORT_TEMPLATE),
        ]
    ),
)


full_text_chain = RunnablePassthrough.assign(
    research_summary= full_text_web_search_chain | (lambda x: "\n\n".join(["\n\n".join(l) for l in x]))

) | full_web_text_prompt | model | StrOutputParser()


##################################################

def get_youTubeTranscript_text(url):
    try:
        loader = YoutubeLoader.from_youtube_url(
    url, add_video_info=True,language=["en","hi"],translation="en",
)

        data = loader.load()
        data= (data[0].page_content[:10000]).strip()
        clean_text = re.sub(r'[^A-Za-z0-9\s]', '', data)
        clean_text = re.sub(' +', ' ', clean_text)  # Remove extra spaces
        return clean_text

    except Exception as e:
        print(e)
        return f"Failed to retrieve the transcript or the language is not available:"


def has_english_captions(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        return len(transcript) > 0
    except Exception as e:
        return False

def get_youtube_links(search_query, RESULTS_PER_QUESTION=3, MAX_DURATION=1800):
    videos_search = VideosSearch(search_query, limit=30)
    results = videos_search.result()

    video_links = []
    for video in results["result"]:
        video_url = video["link"]
        try:
            yt = YouTube(video_url)
            duration_seconds = yt.length
            title = yt.title
            video_id = yt.video_id

            # Check if the video has English title and descriptions
            if duration_seconds <= MAX_DURATION  and has_english_captions(video_id):
                video_links.append(video_url)
                if len(video_links) >= RESULTS_PER_QUESTION:
                    break
        except Exception as e:
            print(f"Error processing video {video_url}: {e}")

    return video_links


YOUTUBE_SUMMARY_PROMPT = ChatPromptTemplate.from_template(YOUTUBE_SUMMARY_TEMPLATE)
model = GooglePalm( temperature = 0)

get_youTubeTranscript_and_summarize_chain = RunnablePassthrough.assign(summary = RunnablePassthrough.assign(text=lambda x: get_youTubeTranscript_text(x["url"])
)|YOUTUBE_SUMMARY_PROMPT | model | StrOutputParser()) | (lambda x:f"url : {x['url']}\n\nsummary : {x['summary']}")

# get list of dictionary of question and youTube link from a question
youTubelink_extraction_chain = RunnablePassthrough.assign(
    urls = lambda x: get_youtube_links(x["question"])
)| (lambda x : [{"question":x["question"],"url": u} for u in x["urls"]])

youTube_single_question_multilink_web_search_chain = youTubelink_extraction_chain | get_youTubeTranscript_and_summarize_chain.map()


YOUTUBE_SEARCH_PROMPT = ChatPromptTemplate.from_messages(
    [
        HumanMessagePromptTemplate.from_template(SEARCH_TEMPLATE)
    ]
)

create_youtube_question_chain = YOUTUBE_SEARCH_PROMPT | model | StrOutputParser() | json.loads

#given a question it creates question then for each question finds multiple urls then for each such url data is fetched,creates a list of list
full_youTube_web_search_chain =create_youtube_question_chain |(lambda x : [ {"question": q} for q in x]) |youTube_single_question_multilink_web_search_chain.map()

full_youTube_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", WRITER_SYSTEM_PROMPT),
        ("user", YOUTUBE_RESEARCH_REPORT_TEMPLATE),
    ]
)

full_youTube_chain = RunnablePassthrough.assign(
    research_summary= full_youTube_web_search_chain | (lambda x: "\n\n".join(["\n\n".join(l) for l in x]))

) | full_youTube_prompt | model | StrOutputParser()




########################################



full_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", WRITER_SYSTEM_PROMPT),
        ("user", BOTH_TEMPLATE),
    ]
)


full_chain = full_prompt | model | StrOutputParser()




#######################################


def do_text_web_research(question):
    print(question)
    # result = full_text_chain.invoke({"question":question,})
    result = full_text_chain.invoke({"question":question.strip(),})
    print(result)
    print("######text_web_research_done######")
    return result

def do_text_youtube_research(question):
    result = full_youTube_chain.invoke({"question":question,})
    print(result)
    print("#########text_youtube_research_done###########")
    return result

def do_both_research(question):

    text_based_web_research_summary = do_text_web_research(question)

    youtube_based_web_research_summary = do_text_youtube_research(question)

    result = full_text_chain.invoke({"text_based_web_research_summary":text_based_web_research_summary,"youtube_based_web_research_summary":youtube_based_web_research_summary,"question":question})
    print(result)
    return result

##########################

# print(full_youTube_chain.invoke(
#        {
#         "question":"Deep Learning",
#     }
# )
# )


# full_text_chain.invoke(
#        {
#         "question":"dollar vs INR",
#     }
# )

# do_text_youtube_research("Deep Learning")

# do_both_research("Deep Learning")

# print(full_text_chain.invoke(
#        {
#         "question":"dollar vs INR",
#     }
# ))