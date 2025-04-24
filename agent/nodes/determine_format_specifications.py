from agent.state import State
from agent.format_specifications import FORMAT_SPECIFICATIONS, DEFAULT_FORMAT_SPECIFICATIONS
# from agent.prompts import QUERY_ANALYSIS_TEMPLATE

import os
from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage

# load_dotenv()
# query_analysis_model = ChatOpenAI(model = "gpt-4.1-nano", temperature = 0, api_key = os.getenv("OPENAI_API_KEY")) # TODO: Move it to models dir

def determine_format_specifications(state: State):
    target_format = state["target_format"]
    user_prompt = state["messages"][-1].content

    format_specifications = state.get("format_specifications", None)
    if not format_specifications:
        format_specifications = FORMAT_SPECIFICATIONS.get(target_format, DEFAULT_FORMAT_SPECIFICATIONS)

    # print(f"Format determination complete for {target_format}")
    # print(format_specifications)

    # prompt = ChatPromptTemplate.from_template(QUERY_ANALYSIS_TEMPLATE)

    # chain = prompt | query_analysis_model | StrOutputParser()
    # query_analysis = chain.invoke({
    #     "target_format": target_format,
    #     "format_specifications": format_specifications,
    #     "user_prompt": user_prompt
    # })

    # TODO: Do we need history?
    # state["format_specifications"] = state.get("format_specifications", []) + [format_specifications]
    # state["format_specifications"] = query_analysis
    state["format_specifications"] = format_specifications

    return state 