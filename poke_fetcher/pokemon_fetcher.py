import requests
import json

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
        if type(sprites[s]) != dict:
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
    for i in pokemon_data:
        print(f"{i}: {pokemon_data[i]}")

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
