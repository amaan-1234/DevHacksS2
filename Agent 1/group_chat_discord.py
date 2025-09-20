import discord
import json
import asyncio
from collections import defaultdict


# Replace with your bot token and target channel ID
BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
CHANNEL_ID = 1368294173509419123  # Replace with actual channel ID

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    channel = client.get_channel(CHANNEL_ID)

    if not channel:
        print("Channel not found!")
        await client.close()
        return

    grouped_messages = defaultdict(list)

    async for message in channel.history(limit=None):
        grouped_messages[message.author.name].append({
            "content": message.content,
            "timestamp": message.created_at.isoformat()
        })

    # Convert defaultdict to normal dict and save to JSON
    with open("grouped_discord_messages.json", "w", encoding="utf-8") as f:
        json.dump(grouped_messages, f, indent=4)

    print("Grouped messages saved to grouped_discord_messages.json")
    await client.close()

client.run(BOT_TOKEN)
