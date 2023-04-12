import disnake
from disnake.ext import commands
from disnake.ui import Button, View
import os
import requests
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

API_URL = 'https://chatapi.louiml.net/api/message'

intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='msg', help='Send a message to the API and get a response.')
async def api_message(ctx, *, message: str):
    async with ctx.typing():
        response = requests.post(API_URL, json={"message": message})
        if response.status_code == 200:
            api_response = response.json()
            await ctx.send(api_response['response'])
        else:
            await ctx.send('Error: Unable to reach API.')

@bot.slash_command(name="msg", description="Send a message to the API and get a response.")
async def _api(ctx, *, message: str):
    response = requests.post(API_URL, json={"message": message})
    if response.status_code == 200:
        api_response = response.json()
        await ctx.send(content=api_response['response'])
    else:
        await ctx.send(content='Error: Unable to reach API.')
        
async def fetch_json_data(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

@bot.command(name='api_status', help='Get the current API status.')
async def fetch_data(ctx):
    url = 'https://chatapi.louiml.net/api/message'
    data = await fetch_json_data(url)
    
    message = data['api_status']

    await ctx.send(message)

@bot.slash_command(name="api_status", description="Get the current API status.")
async def fetch_data(ctx):
    url = 'https://chatapi.louiml.net/api/message'
    data = await fetch_json_data(url)
    
    message = data['api_status']

    await ctx.send("`" + message + "`")

bot.run(token)
