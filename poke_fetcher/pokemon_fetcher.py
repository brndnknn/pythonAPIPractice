import requests
import os
from rich.console import Console
from rich.text import Text

def poke_parser(api_results):
    """
    Parse data from api results
    :param api_results: dict - the raw json data returned by the api request
    : return: dict - cleaned up data form api response
    """
    # handle simpler data
    keys = ['name', 'abilities', 'types']
    poke_data = {}
    for k in keys:
        poke_data[k] = api_results[k]

    # simplify stats
    poke_data['stats'] = {}
    stats = api_results['stats']
    for stat in stats:
        name = stat['stat']['name']
        poke_data['stats'][name] = stat['base_stat']

    # only keep main sprites
    poke_data['sprites'] = {}
    sprites = api_results['sprites']
    for s in sprites:
        #if type(sprites[s]) != dict:
        poke_data['sprites'][s] = sprites[s]
    
    return poke_data


def get_pokemon_data(pokemon_name_or_id):
    """
    Fetch Pokémon details from the PokéAPI.
    :param pokemon_name_or_id: str or int - Name or ID of the Pokémon
    :return: dict - Pokémon data (to be implemented)
    """
    api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id}"
    results = requests.get(api_url).json()

    return poke_parser(results)

def display_pokemon_info(pokemon_data):
    """
    Format and display Pokémon details.
    :param pokemon_data: dict - Pokémon API response
    """
    print("\n=== Pokémon Info ===\n")
    
    # Name
    print(f"Name: {pokemon_data['name'].capitalize()}\n")
    
    # Types
    types = [t['type']['name'].capitalize() for t in pokemon_data['types']]
    print(f"Type(s): {', '.join(types)}\n")
    
    # Abilities
    print("Abilities:")
    for ability in pokemon_data['abilities']:
        ability_name = ability['ability']['name'].capitalize()
        is_hidden = " (Hidden)" if ability['is_hidden'] else ""
        print(f"  - {ability_name}{is_hidden}")
    print()
    
    # Stats
    print("Base Stats:")
    for stat_name, stat_value in pokemon_data['stats'].items():
        formatted_stat = stat_name.replace('-', ' ').title()
        print(f"  {formatted_stat:<15} {stat_value}")
    print()
    
    # Sprite (ASCII Art)
    sprite_url = pokemon_data['sprites'].get('other', {}).get('official-artwork', {}).get('front_default', '')
    if sprite_url and sprite_url.startswith("http"):
        response = requests.get(sprite_url)
        if response.status_code == 200:
            with open("sprite.png", "wb") as f:
                f.write(response.content)
            os.system("img2txt sprite.png")  # Convert image to ASCII
        else:
            print("Failed to load sprite.")
    else:
        print("No valid sprite available.")


def main():
    """
    Main function to run the Pokémon fetcher.
    """
    pokemon = input("Enter a Pokémon name or ID: ").strip()
    pokemon_data = get_pokemon_data(pokemon)
    if pokemon_data:
        display_pokemon_info(pokemon_data)
    else:
        print("Error: Could not retrieve Pokémon data.")

if __name__ == "__main__":
    main()
