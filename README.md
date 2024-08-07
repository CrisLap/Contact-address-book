# Software of a contact address book

# ContactEase Solutions

ContactEase Solutions aims to simplify contact management for its users by developing an intuitive and interactive software that optimizes the organization and access to personal information. This project is a console-based application written in Python, leveraging Object-Oriented Programming (OOP) principles to provide a structured and scalable contact management system.

## Project Structure

- `contact_manager.py`: Contains the implementation of the `Contact` and `ContactManager` classes and the `main` user interface.
- `contacts.json`: The JSON file where contacts are saved and loaded.

## Requirements

- Python 3.x
- colorama
- tabulate

## Installation

To install the necessary libraries, you can use `pip`. Run the following commands in the terminal:
- pip install colorama
- pip install tabulate

## Features

- **Add Contact**: Allows the user to add new contacts. Validates the first name, last name, phone number, and email address. Checks for duplicates and prompts the user if a duplicate is found.
- **View Contacts**: Displays all contacts present in the JSON file. If the file is empty, it notifies the user.
- **Modify Contact**: Enables modification of existing contact details. Searches for contacts by name and notifies the user if no contacts are available. Validates the modified data similarly to adding a new contact and checks for duplicates.
- **Delete Contact**: Removes contacts from the address book by searching for contacts by name. Notifies the user if the contact is not found.
- **Search Contact**: Searches for contacts by first name or last name and notifies the user if the contact is not found. If no contacts are available, it notifies the user.
- **Save and Load**: Automatically saves the contacts (new additions, modifications, deletions) to the JSON file and loads the contacts from the file when the program starts.

## Getting Started

### Installation

1. Clone the repository:

2. Ensure you have Python 3.x installed on your machine.

### Running the Program

Run the following command to start the program:

```
python contact_manager.py
```


## Project diagram
```
contact_manager.py
│
├── Contact
│   ├── __init__(first_name, last_name, phone_number, email)
│   ├── __str__()
│
├── ContactManager
│   ├── __init__(filename="contacts.json")
│   ├── load_contacts()
│   ├── save_contacts()
│   ├── get_valid_input(prompt, validation_func, error_message)
│   ├── add_contact(first_name=None, last_name=None, phone_number=None, email=None)
│   ├── _is_valid_name(name)
│   ├── _is_valid_phone(phone)
│   ├── _is_valid_email(email)
│   ├── _is_duplicate(first_name, last_name, phone_number, email)
│   ├── display_contacts()
│   ├── modify_contact(query)
│   ├── _select_contact_from_results(results)
│   ├── delete_contact(query)
│   ├── search_contact(query, display=True)
│
├── print_in_color(text, color)
│
├── main()
```
