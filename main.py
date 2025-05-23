from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from Tools.api import get, post

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[DuckDuckGoTools(), get, post],
    show_tool_calls=True,
    markdown=True,
)

valid_response = {
    "get_request": """
        {
            "page": number,
            "per_page": number,
            "total": number,
            "total_pages": number,
            "data": [
                {
                    "id": string,
                    "email": string,
                    "first_name": string,
                    "last_name": string,
                    "avatar": string
                },
                {
                    "id": string,
                    "email": string,
                    "first_name": string,
                    "last_name": string,
                    "avatar": string
                }
            ],
            "support": {
                "url": string,
                "text": string
            }
        }
        """,
    "post_request": """
        {
            "name": string,
            "job": string,
            "id": string,
            "createdAt": string
        }
        """
}

valid_params = {
    "get_request": {
        "page": 2
    },
    "post_request": {
        "name": "morpheus",
        "job": "leader"
    }
}

agent.print_response(f"""test if this api is giving valid response: https://reqres.in. 
                     test if post and get requests are working correctly for this endpoint on that api: /api/users
                     valid params looks like this: {valid_params}

                     Do strict checking, with each field having exact same data type as described by me.  
                     valid response looks like this: {valid_response}
                    for post request, if I am getting status of 201, its fine too!""", stream=True
                    )