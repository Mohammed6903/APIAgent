from agno.agent import Agent
from Tools.file import save_file
import re


class PostProcessingAgent(Agent):
    def run(self, *args, **kwargs):
        response = super().run(*args, **kwargs)

        if hasattr(response, "content"):
            content = response.content
        else:
            content_chunks = []
            try:
                for chunk in response:
                    if hasattr(chunk, "content"):
                        content_chunks.append(chunk.content)
                    elif isinstance(chunk, str):
                        content_chunks.append(chunk)
                content = "".join(content_chunks)
            except Exception as e:
                print(f"Error processing streaming response: {e}")
                return response

        matches = re.findall(r"```json\s*(.*?)\s*```", content, re.DOTALL)
        if matches:
            try:
                save_file(matches[0], "api_documentation.json", overwrite=True)
                print("Successfully saved API documentation to api_documentation.json")
            except Exception as e:
                print(f"Error saving documentation file: {e}")
        else:
            print("No JSON code blocks found in response")

        return response

