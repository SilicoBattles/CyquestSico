import discord
from discord.ext import commands
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
AI_API_URL = os.getenv("AI_API_URL")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True
bot = commands.Bot(command_prefix='~!@#', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    print(f'User ID: {bot.user.id}')

@bot.event
async def on_message(message):
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
            response = requests.post(AI_API_URL, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            ai_response = response.json()
            if ai_response and ai_response.get("choices"):
                bot_reply = ai_response["choices"][0]["message"]["content"]
                if "Relevant" in bot_reply:
                    await message.channel.send("Relevant")
                elif "Irrelevant" in bot_reply:
                    await message.channel.send("Irrelevant")
                else:
                    await message.channel.send("Sorry, I couldn't get a valid response from the AI.")
            else:
                await message.channel.send("Sorry, I couldn't get a valid response from the AI.")
        except requests.exceptions.RequestException as e:
            print(f"Error calling AI API: {e}")
            await message.channel.send("Sorry, I'm having trouble connecting to the AI service right now.")
        except json.JSONDecodeError:
            print("Error decoding JSON response from AI API.")
            await message.channel.send("Sorry, I received an unreadable response from the AI service.")
    await bot.process_commands(message)


def run_bot():
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("Invalid bot token.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    run_bot()
