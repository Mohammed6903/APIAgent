from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from Tools.api import wrapperforrequests

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[FileTools(), wrapperforrequests],
    description="You are an API testing tool. You test the APIs and return the results.",
    instructions="""
                    You are given an API endpoint, you will test the API and return the results.
                    You will use the wrapperforrequests tool to test the API.
                    You will read the API documentation provided by the user using FileTools.
                    """,
    show_tool_calls=True,
    markdown=True,
)

agent.print_response(f"""test if this api is giving valid response: http://localhost:5000. 
                     Read its documentation from doc.json in the current directory. 
                     Valid responses and parameters are provided in that same documentation along with extra info about each endpoint.
                     Read it carefully.

                     Do strict checking, with each field having exact same data type as described by me.  
                    for post request, if you are getting status of 201, its fine too!""", stream=True
                    )