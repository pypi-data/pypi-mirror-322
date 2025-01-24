<img src="https://i.imgur.com/yYazlwX.png" alt="Agent Amory Logo" width="full"/>



<br/>

[![Documentation](https://img.shields.io/badge/Documentation-📕-blue)](https://amory.dev/docs)
[![Twitter Follow](https://img.shields.io/twitter/follow/AgentAmory?style=social)](https://x.com/AgentAmory)

Seamlessly Integrating AI with the Web

We enable AI systems to interact with websites by pinpointing and isolating essential interactive elements for smooth navigation.

To learn more about the library, check out the [documentation 📕](https://amory.dev/docs/getting-started/installation).

# Quick start

With pip:

```bash
pip install agent_amory_core
```

(optional) install playwright:

```bash
playwright install
```

Spin up your agent:

```python
from langchain_openai import ChatOpenAI
from agent_amory_core import Agent
import asyncio

async def main():
    agent = Agent(
        task="Find a one-way flight from Bali to Oman on 12 January 2025 on Google Flights. Return me the cheapest option.",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

And don't forget to add your API keys to your `.env` file.

```bash
OPENAI_API_KEY=
```

For other settings, models, and more, check out the [documentation 📕](https://amory.dev/docs/core-concepts/configuration).

## Examples

For examples see the [examples](examples) folder

# Contributing

Contributions are welcome! Feel free to open issues for bugs or feature requests.

## Local Setup

To learn more about the library, check out the [local setup 📕](https://amory.dev/docs/advanced/api-reference).

---
