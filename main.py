import json
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import requests

load_dotenv()


TOKEN = os.getenv("DISCORD_BOT_TOKEN")
AI_API_URL = "https://ai.hackclub.com/chat/completions"
SYSTEM_PROMPT = (
    "**System Prompt for Tech Hunt Bot (Relevant vs Irrelevant Mode)**\n\n"
    "You are **CyQuest**, the guide for a Tech Hunt event.\n\n"
    "**Core Rules:**\n"
    "1. Classify every user message as **Relevant** (about the current puzzle, hints, or game commands) or **Irrelevant** (off-topic chatter, random text, unrelated questions).\n"
    "2. If relevant: respond Relevant\n"
    "3. If irrelevant: reply Irrelevant\n"
    "4. Never reveal the full answer NO MATTER WHAT.\n"
    "7. Never output internal reasoning or `<think>` sections. ONLY TWO WORDS ARE ALLOWED: \"Relevant\" or \"Irrelevant\".\n\n"
    "---\n\n"
    "**Sample Relevant Response:**\n"
    "User: \"I think it’s echo\"\n> Relevant\n\n"
    "**Sample Irrelevant Response:**\n"
    "User: \"What’s your favorite color?\"\n> Irrelevant\n\n"
    "---\n\n"
    "**Puzzle List:**\n\n"
    "**Puzzle 1:**\n"
    "Q: I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?\n"
    "A: Echo\n"
    "Hints:\n"
    "1. It repeats after you.\n"
    "2. Found in caves and mountains.\n"
    "3. Starts with 'E', ends with 'O'.\n\n"
    "**Puzzle 2:**\n"
    "Q: I’m light as a feather, yet the strongest person can’t hold me for long. What am I?\n"
    "A: Breath\n"
    "Hints:\n"
    "1. You need me to live.\n"
    "2. You let me out when you talk.\n"
    "3. Starts with 'B', ends with 'H'.\n\n"
    "**Puzzle 3:**\n"
    "Q: The more of me you take, the more you leave behind. What am I?\n"
    "A: Footsteps\n"
    "Hints:\n"
    "1. Found in sand or snow.\n"
    "2. They follow you.\n"
    "3. Starts with 'F', ends with 'S'.\n\n"
    "**Puzzle 4:**\n"
    "Q: I’m always in front of you but can’t be seen. What am I?\n"
    "A: The future\n"
    "Hints:\n"
    "1. You can’t touch me.\n"
    "2. You move towards me every second.\n"
    "3. Starts with 'F', ends with 'E'.\n\n"
    "---\n\n"
    "**Implementation notes:**\n"
    "- Detect relevance by checking if the message contains: puzzle answers, the word 'hint', game commands (`START`, `ANSWER`), or puzzle-related terms.\n"
    "- If irrelevant: return irrelevant\n"
    "- If relevant: return relevant\n"
    "- Track per-player state: current puzzle, hint index."
)

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True
bot = commands.Bot(command_prefix='~!@#', intents=intents)

@bot.event
async def on_ready():
    """Event handler for when the bot is ready."""
    print(f'Bot connected as {bot.user}')
    print(f'User ID: {bot.user.id}')

@bot.event
async def on_message(message):
    """Event handler for processing incoming messages."""
    if message.author == bot.user:
        return
    if isinstance(message.channel, discord.DMChannel):
        headers = {"Content-Type": "application/json"}
        payload = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.content}
            ],
            "model": "qwen/qwen3-32b"
        }
        try:
            response = requests.post(
                AI_API_URL, headers=headers, data=json.dumps(payload)
            )
            response.raise_for_status()
            ai_response = response.json()
            if ai_response and ai_response.get("choices"):
                bot_reply = ai_response["choices"][0]["message"]["content"]
                if "Relevant" in bot_reply:
                    await message.channel.send("Relevant")
                elif "Irrelevant" in bot_reply:
                    await message.channel.send("Irrelevant")
                else:
                    await message.channel.send(
                        "Sorry, I couldn't get a valid response from the Silico Service."
                    )
            else:
                await message.channel.send(
                    "Sorry, I couldn't get a valid response from the Silico Service."
                )
        except requests.exceptions.RequestException as exc:
            print(f"Error calling AI API: {exc}")
            await message.channel.send(
                "Sorry, I'm having trouble connecting to the Silico service right now."
            )
        except json.JSONDecodeError:
            print("Error decoding JSON response from AI API.")
            await message.channel.send(
                "Sorry, I received an unreadable response from the Silico service."
            )
    await bot.process_commands(message)


def run_bot():
    """Run the Discord bot."""
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("Invalid bot token.")
    except Exception as exc:
        print(f"An error occurred: {exc}") 

if __name__ == '__main__':
    run_bot()
