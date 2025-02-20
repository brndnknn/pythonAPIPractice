import requests

def get_pokemon_data(pokemon_name_or_id):
    """
    Fetch Pokémon details from the PokéAPI.
    :param pokemon_name_or_id: str or int - Name or ID of the Pokémon
    :return: dict - Pokémon data (to be implemented)
    """
    pass  # TODO: Implement API call and data extraction

def display_pokemon_info(pokemon_data):
    """
    Format and display Pokémon details.
    :param pokemon_data: dict - Pokémon API response
    """
    pass  # TODO: Implement display logic

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
