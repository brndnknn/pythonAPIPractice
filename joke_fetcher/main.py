import requests
import json

def get_random_joke():
    # Fetch a random Chuck Norris joke from the API.
    api_url = "https://api.chucknorris.io/jokes/random"
    response = requests.get(api_url)
    if not (check_response_code(response)):
        print("Fetching failed, try again later")
        return

    raw_content = json.loads(response.text)
    joke = raw_content['value']

    print()
    print(joke)

def get_categories():
    # Fetch available joke categories.
    api_url = "https://api.chucknorris.io/jokes/categories"
    response = requests.get(api_url)
    if not (check_response_code(response)):
        print("Fetching failed, try again later")
        return
    
    categories = json.loads(response.text)

    # Set column width as two characters longer than the longest word
    col_width = max(len(word) for word in categories) + 2

    for i in range(0, len(categories), 2):
        left = categories[i].ljust(col_width)
        right = categories[i + 1] if i + 1 < len(categories) else ""
        print(left, right)

def get_joke_by_category(category):
    api_url = f"https://api.chucknorris.io/jokes/random?category={category}"
    response = requests.get(api_url)
    if not (check_response_code(response)):
        print("Invalid category, try again")
        return
    
    raw_content = json.loads(response.text)
    joke = raw_content["value"]

    print()
    print(joke)


def check_response_code(response):
    if response.status_code == 200:
        return True
    return False

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
            category = input("Enter a category: ")
            get_joke_by_category(category)
        elif choice == "3":
            get_categories()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
