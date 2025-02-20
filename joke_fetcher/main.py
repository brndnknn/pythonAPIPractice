import requests
import json

def get_random_joke():
    # Fetch a random Chuck Norris joke from the API.
    api_url = "https://api.chucknorris.io/jokes/random"
    request = requests.get(api_url)
    raw_content = json.loads(request.text)
    joke = raw_content['value']

    print()
    print(joke)

def get_categories():
    """Fetch available joke categories."""
    pass  # TODO: Implement API call to retrieve categories

def get_joke_by_category(category):
    """Fetch a joke from a specific category."""
    pass  # TODO: Implement API call to fetch joke by category

def save_joke(joke):
    """Save a joke to a local file."""
    pass  # TODO: Implement file writing logic

def main():
    """Main function to run the CLI interface."""
    print("Welcome to the Chuck Norris Joke Machine! 🤠")
    while True:
        print("\nChoose an option:")
        print("[1] Get a random joke")
        print("[2] Get a joke from a category")
        print("[3] View available categories")
        print("[4] Exit")
        choice = input(">> ")
        
        if choice == "1":
            get_random_joke()
        elif choice == "2":
            pass  # TODO: Call function to fetch a joke by category
        elif choice == "3":
            pass  # TODO: Call function to display categories
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
