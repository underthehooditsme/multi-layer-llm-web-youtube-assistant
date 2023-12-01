# Advanced Multi Layer LLM Web/Youtube Research Assistant

## Project Overview

The Advanced Multi Layer Txt/Web Assistant is a powerful tool designed to facilitate in-depth research on user-specified topics. It provides comprehensive reports sourced from online articles, YouTube videos, or both. This system enhances the user's ability to gather diverse information and insights from different mediums.

## How it Works

1. **User Query Input:**
   - Users input their queries through a user interface.

2. **Query Expansion:**
   - The system expands the user's query by generating additional similar queries separately for YouTube and net-based articles using the Google Palm 2 Large Language Model (LLM).

3. **Link Generation:**
   - For net-based articles, the system retrieves relevant links using DuckDuckGo search.
   - For YouTube, the system utilizes a Python library to fetch video links.

4. **Data Extraction:**
   - The system extracts data from the fetched links, including article content and YouTube video transcripts.

5. **Summarization:**
   - The system generates separate summaries for YouTube and net-based articles.
   - Users have the option to receive a combined summary if they choose both options.

## Technology Used

- **Langchain:**
  - Langchain is employed for natural language processing and query expansion.

- **LCEL (LangChain Expression Language):**
  - LCEL is used to build such big and complex chains,which makes any part swappable

- **Google Palm 2 LLM:**
  - The Google Palm 2 Language Model is used for query expansion.

- **Python:**
  - The Google Palm 2 Language Model is used for query expansion.

## Creator

This project is created and maintained by Subham Thirani.

## Getting Started

To use this assistant, follow these steps:

1. Clone the repository.
2. Install the required dependencies (`pip install -r requirements.txt`).
3. Add your credentials to access Google Palm or OPENAI in .env file
4. Run the application (`streamlit run main.py`).

## Dependencies

- Langchain
- LCEL
- Google Palm 2 LLM
- Other necessary Python libraries (specified in the requirements.txt file)

## Contact

For any inquiries or feedback, please contact Subham Thirani at [subhamthirani@gmail.com].
