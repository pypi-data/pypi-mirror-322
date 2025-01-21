# FastAPI Agents Examples

You can run most examples with `uvicorn`. 

Run `uvicorn --reload <module>:app` from the example directory, replacing `<module>` with the Python filename without the extension.

For example:

```
cd pydantic-ai
pip install uvicorn fastapi fastapi-agents pydantic-ai
uvicorn --reload pydantic_ai:app
```

## Notebooks
- getting-started.ipynb - A step-by-step walkthrough of configuring FastAPI Agents with PydanticAI including tool definitions to build a demo todo list manager agent and serve as an API. Runs within a Jupyter notebook so you can execute each part in sequence to see what happens.
- using-openai-mode.ipynb - A step-by-step walkthrough of configuring FastAPI Agents in 'OpenAI' mode, to use your agents with any OpenAI-compatible tooling, including the OpenAI SDK.

View on [GitHub](https://github.com/blairhudson/fastapi-agents/tree/main/examples/notebooks).

## PydanticAI
- pydantic_ai.py - A basic example showing how to use a PydanticAI agent with FastAPI Agents
- pydantic_ai_deps.py - Adding depdendency injection to PydanticAI

See full code on [GitHub](https://github.com/blairhudson/fastapi-agents/tree/main/examples/pydantic-ai).

## Llama-Index
- llama_index.py - A basic example showing how to use a Llama-Index agent with FastAPI Agents
  
See full code on [GitHub](https://github.com/blairhudson/fastapi-agents/tree/main/examples/llama-index).
  
## Smolagents
- smolagents.py - A basic example showing how to use a smolagents agent with FastAPI Agents
  
See full code on [GitHub](https://github.com/blairhudson/fastapi-agents/tree/main/examples/smolagents).

## CrewAI
- crewai.py - A basic example showing how to use a CrewAI Crew with FastAPI Agents in openai mode

See full code on [GitHub](https://github.com/blairhudson/fastapi-agents/tree/main/examples/crewai).
  
## Security
- security_apikey.py - Adding FastAPI security dependency with API Key header authentication
- security_cookie.py - Adding FastAPI security dependency with cookie-based authentication
- security_httpbasic.py - Adding FastAPI security dependency with HTTP Basic (username/password) authentication
- security_oauth2.py - Adding FastAPI security dependency with Oauth2 (Bearer) authentication
- security_oidc.py - Adding FastAPI security dependency with OIDC-based authentication

See full code on [GitHub](https://github.com/blairhudson/fastapi-agents/tree/main/examples/security).

## Docker
- PydanticAI with OAuth2 security using fastapi-agents container

See full code on [GitHub](https://github.com/blairhudson/fastapi-agents/tree/main/examples/docker).


## OpenAI Mode
- PydanticAI with OAuth2 security in openai-mode using fastapi-agents container
  
See full code on [GitHub](https://github.com/blairhudson/fastapi-agents/tree/main/examples/openai-mode).
