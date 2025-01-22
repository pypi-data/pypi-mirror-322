# HeadlessAgents Python

A Python library for interacting with headless agents through various AI providers.

## Installation

```bash
pip install headlessagents
```

## Usage

```python
from headlessagents import HeadlessAgent

# Initialize the agent
agent = HeadlessAgent(
    agent_id="20250119021511fa6df4c248b0",  # Your agent ID
    user_id="3aYTwTRJCb8P4Jtf3e0v",         # Your user ID
    client_provider="openai"                 # or "anthropic", "o1", "xai"
)

# Get agent tools
tools = agent.get_tools()
print(f"Available tools: {tools}")

# Query the agent
response = agent.query("Your query here")
print(f"Agent response: {response}")
```

## Features

- Support for multiple AI providers (OpenAI, Anthropic, O1, XAI)
- Easy-to-use API for interacting with headless agents
- Tool retrieval and formatting
- Configurable base URL for API endpoints

## Configuration

The default base URL is `https://agents-api-434678060995.us-central1.run.app`. You can override it by passing a custom `base_url` parameter to the HeadlessAgent constructor:

```python
agent = HeadlessAgent(
    agent_id="your_agent_id",
    user_id="your_user_id",
    client_provider="openai",
    base_url="https://your-custom-url.com"
)
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.