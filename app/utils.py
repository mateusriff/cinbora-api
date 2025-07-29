import httpx
import os
import asyncio
from dotenv import load_dotenv

load_dotenv("compose/.env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

async def geocode_address(address: str):

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": GOOGLE_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    data = response.json()
    print(f"GOOGLE_API_KEY: {GOOGLE_API_KEY}")
    print(data)

    if data["results"]:
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    
    return None