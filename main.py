from agno.agent import Agent
from agno.models.google import Gemini
from agno.team import Team
from agno.tools.file import FileTools
from Tools.file import get_dir_tree
from textwrap import dedent
from Tools.api import wrapperforrequests
from Documentor import PostProcessingAgent

tester = Agent(
    name="API Tester",
    role="Tests API endpoints",
    model=Gemini(id="gemini-2.0-flash"),
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

documentor = PostProcessingAgent(
    name="API Documentor",
    role="Generates API documentation",
    model=Gemini(id="gemini-2.0-flash"),
    tools=[FileTools(), get_dir_tree],
    description=dedent("""
        You are an API analysis tool. You generate and save their proper documentations in JSON format in the working directory.
    """),
    instructions=dedent("""
        You are given a project directory, you will get the directory tree of the project and then you will analyse the files in the project.
        You will find the API endpoints in the project and you will generate a JSON file which contains all the lists of API endpoints along with their expected response and parameters.
        
        IMPORTANT: After generating the JSON documentation, you MUST save it to a file named "api_documentation.json" using the FileTools' save_file tool.
        
        The JSON file should be structured in a way that each endpoint is a key, and its value is an object containing the expected response and parameters.
        The expected response should be analysed by reviewing the code.
        
        Steps to follow:
        1. Use get_dir_tree tool to get the directory tree of the project
        2. Use FileTools to read the relevant API files in the project
        3. Analyze the code to extract API endpoints, parameters, and responses
        4. Generate full parameter format in JSON for each endpoint
        5. Generate full response format in JSON for each endpoint
        6. Use the FileTools' save_file tool to save the JSON as "api_documentation.json"
    """),
    show_tool_calls=True,
    markdown=True,
)

organizer = Team(
    name="API Testing Team",
    mode="coordinate",
    model=Gemini(id="gemini-2.0-flash"),
    tools=[FileTools(), wrapperforrequests],
    description="You are a testing team coordinator. Your goal is to test a given api and if there is no documentation present or given for an api, document it.",
    instructions=[
        "First determine the tech stack of the API by reading some file in project directory.",
        "Then, check if that tech stack gives standard documentation generation like swagger or openapi.",
        "If yes, then use that documentation to test the API.",
        "If no, then ask the documentor member to create a documentation file.",
        "Then, ask the tester member to test the API endpoint using the documentation file. send the file name to the tester member.",
        "Now, check if all the endpoints are tested and if there is any endpoint left, ask the tester member to test it.",
        "At the end, generate a report of all the endpoints tested and their results."
    ],
    members=[
        documentor,
        tester,
    ],
    add_datetime_to_instructions=True,
    add_member_tools_to_system_message=False,
    enable_agentic_context=True,
    share_member_interactions=True,
    show_members_responses=True,
    show_tool_calls=True,
    markdown=True,
)

organizer.print_response(f"""
                        test if this api is giving valid response: http://localhost:5000. 
                        Read its documentation from doc.json in the current directory. 
                        Valid responses and parameters are provided in that same documentation along with extra info about each endpoint.
                        Read it carefully.

                        Do strict checking, with each field having exact same data type as described by me.  
                        for post request, if you are getting status of 201, its fine too!""", stream=True
                    )