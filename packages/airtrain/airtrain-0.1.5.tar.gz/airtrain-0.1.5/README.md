# Airtrain

A powerful platform for building and deploying AI agents with structured skills and capabilities.

## Features

- **Structured Skills**: Build modular AI skills with defined input/output schemas
- **OpenAI Integration**: Built-in support for OpenAI's GPT models with structured outputs
- **Credential Management**: Secure handling of API keys and credentials
- **Type Safety**: Full type hints and Pydantic model support
- **Async Support**: Both synchronous and asynchronous API implementations

## Installation

```bash
pip install airtrain
```

## Quick Start

### Creating a Structured OpenAI Skill

```python
from airtrain.core.skills import Skill
from airtrain.core.schemas import InputSchema, OutputSchema
from pydantic import BaseModel
from typing import List

# Define your response model
class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str
    skills: List[str]

# Create a skill
class OpenAIParserSkill(Skill):
    def process(self, input_data):
        # Implementation
        return parsed_response

# Use the skill
skill = OpenAIParserSkill()
result = skill.process(input_data)
```

### Managing Credentials

```python
from airtrain.core.credentials import OpenAICredentials
from pathlib import Path

# Load credentials
creds = OpenAICredentials(
    api_key="your-api-key",
    organization_id="optional-org-id"
)

# Save to environment
creds.load_to_env()
```

## Documentation

For detailed documentation, visit [our documentation site](https://docs.airtrain.dev/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 