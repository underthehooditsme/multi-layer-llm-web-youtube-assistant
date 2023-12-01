import streamlit as st
from researcher import *

def process_query(query, selected_options):

    print("Article based" in selected_options)
    if ("Article based" in selected_options) and ("Youtube video" in selected_options):
        result = do_both_research(query)
    elif "Youtube video" in selected_options:
        result = do_text_youtube_research(query)
    else :
        result = do_text_web_research(query)

    return result




# Streamlit app
def main():
    st.title("Txt/Video Assistant")

    # Sidebar
    st.sidebar.header("Explore Assistance Options ")
    selected_options = st.sidebar.multiselect("Select Options", ["Article based", "Youtube video"])

    # Main screen
    st.write("## Query")
    query = st.text_input("Enter your query:")

    if st.button("Process Query"):
        if query:
            # Display a loading spinner while processing the query
            with st.spinner("Processing..."):
                result = process_query(query, selected_options)
                # Remove the spinner when the processing is done
                st.success("Query processed!")
                result = process_query(query, selected_options)
                st.write("### Result:")
                st.write(result)
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()


