import discord
import json
import asyncio

# Replace with your bot token and target channel ID
BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
CHANNEL_ID = 1368294173509419123

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

    flat_messages = []

    print("📥 Fetching messages...")
    async for message in channel.history(limit=None):
        flat_messages.append({
            "username": message.author.name,
            "content": message.content,
            "timestamp": message.created_at.isoformat()
        })

    # Save to JSON file in flat format
    with open("discord_messages.json", "w", encoding="utf-8") as f:
        json.dump(flat_messages, f, indent=4)

    print("Messages saved to 'discord_messages.json'")
    await client.close()

client.run(BOT_TOKEN)
