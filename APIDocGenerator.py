from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.ollama import Ollama
from Tools.file import get_dir_tree, save_file
from agno.tools.file import FileTools
from textwrap import dedent

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[FileTools(), save_file ,get_dir_tree],
    description=dedent("""
                        You are an API analysis tool. You generate and save their proper documentations in JSON format in the working directory.
                        """),
    instructions=dedent("""
                        You are given a project directory, you will get the directory tree of the project and then you will analyse the files in the project.
                        You will find the API endpoints in the project and you will generate a JSON file which contains all the lists of API endpoints along with their expected response and parameters.
                        
                        IMPORTANT: After generating the JSON documentation, you MUST save it to a file named "api_documentation" using the save_file tool.
                        
                        The JSON file should be structured in a way that each endpoint is a key, and its value is an object containing the expected response and parameters.
                        The expected response should be analysed by reviewing the code.
                        
                        Steps to follow:
                        1. Use get_dir_tree tool to get the directory tree of the project
                        2. Use FileTools to read the relevant API files in the project
                        3. Analyze the code to extract API endpoints, parameters, and responses
                        4. Generate full parameter format in JSON for each endpoint
                        5. Generate full response format in JSON for each endpoint
                        6. Use the save_file tool to save the JSON as "api_documentation"
                        """),
    show_tool_calls=True,
    markdown=True,
)

agent.print_response("""
                        Analyse the api at this directory: /home/mohammed/dev/COHERENCE-25_CodeWizard_AIML/fastapi
                        
                        Make sure to save the final JSON documentation as "api_documentation" file.
                    """, stream=True)

# from agno.agent import Agent
# # from agno.models.google import Gemini
# from agno.models.ollama import Ollama
# from Tools.file import get_dir_tree, save_file
# from agno.tools.file import FileTools
# from textwrap import dedent

# agent = Agent(
#     model=Ollama("qwen3:8b"),
#     tools=[FileTools(save_files=True, read_files=True), save_file ,get_dir_tree],
#     description=dedent("""
#                         You are an API analysis tool. You generate and save their proper documentations in JSON format in the working directory.
#                         """),
#     instructions=dedent("""
#                         You are given a project directory, you will get the directory tree of the project and then you will analyse the files in the project.
#                         You will find the API endpoints in the project and you will generate a JSON file which contains all the lists of API endpoints along with their expected response and parameters.
                        
#                         IMPORTANT: After generating the JSON documentation, you MUST save it to a file named "api_documentation" using the save_file tool.
                        
#                         The JSON file should be structured in a way that each endpoint is a key, and its value is an object containing the expected response and parameters.
#                         The expected response should be analysed by reviewing the code.
                        
#                         Steps to follow:
#                         1. Use get_dir_tree tool to get the directory tree of the project
#                         2. Use FileTools to read the relevant API files in the project
#                         3. Analyze the code to extract API endpoints, parameters, and responses
#                         4. Generate a comprehensive JSON documentation
#                         5. Use the save_file tool to save the JSON as "api_documentation"
#                         """),
#     show_tool_calls=True,
#     markdown=True,
# )

# agent.print_response("""
#                         Analyse the api at this directory: /home/mohammed/dev/COHERENCE-25_CodeWizard_AIML/fastapi
                        
#                         Make sure to save the final JSON documentation as "api_documentation" file.
#                     """, stream=True)