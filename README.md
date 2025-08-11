# CyquestSico
CyQuestSico
===========

CyQuestSico is a Discord bot designed for Tech Hunt events. It classifies user messages as either relevant or irrelevant to the current puzzle, using an AI backend. The bot is intended for direct messages and does not reveal puzzle answers or internal reasoning.

Features
--------
- Classifies messages as "Relevant" or "Irrelevant" based on puzzle context
- Responds only with the words "Relevant" or "Irrelevant"
- Loads configuration and prompts from a `.env` file
- Uses an external AI API for message classification

Requirements
------------
- Python 3.13+
- Discord bot token
- API endpoint for AI classification

Installation
------------
1. Clone the repository:
   ```sh
   git clone https://github.com/SilicoBattles/CyquestSico.git
   cd CyquestSico
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   Or, if using PEP 621/pyproject.toml:
   ```sh
   pip install .
   ```
3. Copy `.env.example` to `.env` and fill in your values:
   ```sh
   cp .env.example .env
   ```
   Edit `.env` to set your Discord bot token and other configuration.

Usage
-----
Run the bot with:
```sh
python main.py
```

The bot will listen for direct messages and respond with either "Relevant" or "Irrelevant" based on the AI's classification.

Environment Variables
---------------------
- `DISCORD_BOT_TOKEN`: Your Discord bot token
- `AI_API_URL`: The AI API endpoint
- `SYSTEM_PROMPT`: The system prompt for the AI (multi-line string)

License
-------
See the `LICENSE` file for license information.
