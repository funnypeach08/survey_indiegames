import urllib.request
import json
import os
import sys

# Top 5 Indie Games
top_games = [
    "Hollow Knight",
    "Stardew Valley",
    "Undertale",
    "Hades",
    "Terraria",
    "Celeste"
]

import ssl

# Bypass SSL verify for internal script usage
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def search_steam_image(game_name):
    # Steam Store API search
    search_url = f"https://store.steampowered.com/api/storesearch/?term={urllib.parse.quote(game_name)}&l=english&cc=US"
    try:
        req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode())
            if data.get('total') > 0 and data.get('items'):
                # Return the ID of the first match to get its capsule image
                app_id = data['items'][0]['id']
                return f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{app_id}/capsule_231x87.jpg"
    except Exception as e:
        print(f"Error fetching {game_name}: {e}")
    return None

import urllib.parse

os.makedirs('assets', exist_ok=True)

results = {}
for game in top_games:
    img_url = search_steam_image(game)
    if img_url:
        print(f"Found {game}: {img_url}")
        results[game] = img_url
        
        # Download the image
        safe_name = game.lower().replace(' ', '_') + ".jpg"
        filepath = os.path.join('assets', safe_name)
        try:
            req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx) as response, open(filepath, 'wb') as f:
                f.write(response.read())
            print(f"  Downloaded to {filepath}")
            results[game] = filepath
        except Exception as e:
            print(f"  Failed to download: {e}")
    else:
        print(f"Could not find image for {game}")

print("Results:", results)
