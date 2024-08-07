import json
import re
import os
from tabulate import tabulate
from colorama import init, Fore

#initialize colorama
init()

class Contact:
    """
    A class to represent a contact.
    """

    def __init__(self, first_name, last_name, phone_number, email):
        """
        Constructs all the necessary attributes for the contact object.
        
        Parameters:
        -----------
        first_name : str
            The first name of the contact.
        last_name : str
            The last name of the contact.
        phone_number : str
            The phone number of the contact.
        email : str
            The email address of the contact.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email

    def __str__(self):
        """
        Returns a string representation of the contact.
        """
        return f"{self.first_name} {self.last_name}, Phone: {self.phone_number}, Email: {self.email}"

class ContactManager:
    """
    A class to manage contacts.
    """

    def __init__(self, filename="contacts.json"):
        """
        Constructs all the necessary attributes for the contact manager.
        
        Parameters:
        -----------
        filename : str, optional
            The name of the file to save and load contacts from (default is "contacts.json").
        """
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        """
        Loads contacts from the file.
        """
        try:
            with open(self.filename, "r") as file:
                contacts_data = json.load(file)
                self.contacts = [Contact(**data) for data in contacts_data]
        except FileNotFoundError:
            self.contacts = []
        except json.JSONDecodeError:
            print_in_color("Error reading the contacts file.", 'red')
            self.contacts = []

    def save_contacts(self):
        """
        Saves contacts to the file.
        """
        with open(self.filename, "w") as file:
            json.dump([contact.__dict__ for contact in self.contacts], file, indent=4)

    def get_valid_input(self, prompt, validation_func, error_message):
        """
        Gets a valid input from the user based on the validation function.
        """
        while True:
            value = input(prompt).strip()
            if validation_func(value):
                return value
            else:
                print_in_color(error_message, 'red')

    def add_contact(self, first_name=None, last_name=None, phone_number=None, email=None):
        """
        Adds a new contact to the contact list.
         
        This method validates the input values for the contact's first name, last name, phone number, and email.
        If any of the values are invalid, the user is prompted to provide correct values. If a contact with the same 
        details already exists, the user is asked for confirmation before adding the new contact.

        Parameters:
        -----------
        first_name : str
            The first name of the contact. It must consist of alphabetic characters only.
        last_name : str
            The last name of the contact. It must consist of alphabetic characters only.
        phone_number : str
            The phone number of the contact. It can include numbers and optionally start with a plus sign (+).
        email : str
            The email address of the contact. It must be in a valid email format.

        Raises:
        -------
        ValueError
            If any of the provided details are invalid, appropriate error messages are displayed and the user is prompted 
            to correct the input.

        Example usage:
        --------------
        >>> manager.add_contact("John", "Doe", "+1234567890", "john.doe@example.com")
        """
        first_name = self.get_valid_input("First name: ", self._is_valid_name, "Invalid first name. Only letters and spaces are allowed.")                                          if first_name is None else first_name
        last_name = self.get_valid_input("Last name: ", self._is_valid_name, "Invalid last name. Only letters and spaces are allowed.") if                                         last_name is None else last_name
        phone_number = self.get_valid_input("Phone number: ", self._is_valid_phone, 
                                           "Invalid phone number. Only numbers and optionally a plus sign are allowed.") if phone_number                                              is None else phone_number
        email = self.get_valid_input("Email: ", self._is_valid_email, "Invalid email. Please enter a valid email address.") if email is                                       None else email

        if self._is_duplicate(first_name, last_name, phone_number, email):
            print_in_color("This contact already exists. Do you want to add it anyway? (y/n): ", 'red')
            overwrite = input().strip().lower()
            if overwrite != 'y':
                print_in_color("Contact not added.", 'red')
                return

        contact = Contact(first_name, last_name, phone_number, email)
        self.contacts.append(contact)
        self.save_contacts()
        print_in_color("Contact added successfully.", 'green')

    def _is_valid_name(self, name):
        """
        Validates the name.
        
        Returns:
        --------
        bool
            True if the name is valid, False otherwise.
        """
        return bool(re.match(r"^[A-Za-z\s]+$", name)) #This regex checks whether the string contained in the variable "name" consists                                                             exclusively of letters of the alphabet (both upper and lower case) and contains no                                                         other characters such as numbers, symbols ( blank spaces between the letters are                                                           allowed)


    def _is_valid_phone(self, phone):
        """
        Validates the phone number.
        
        Returns:
        --------
        bool
            True if the phone number is valid, False otherwise.
        
        """
        return bool(re.match(r"^\+?[0-9]*$", phone)) #This regex checks whether the string contained in the phone variable consists                                                            exclusively of numbers and optionally starts with a plus sign (+)

    def _is_valid_email(self, email):
        """
        Validates the email address.
        
        Returns:
        --------
        bool
            True if the email is valid, False otherwise.
        """
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)) #This regex checks whether the string contained in the email variable                                                                     corresponds to a standard email address format.

    def _is_duplicate(self, first_name, last_name, phone_number, email):
        """
        Checks if a contact is a duplicate.
        
        Returns:
        --------
        bool
            True if the contact is a duplicate, False otherwise.
        """
        return any(contact.first_name == first_name and 
                   contact.last_name == last_name and 
                   contact.phone_number == phone_number and 
                   contact.email == email for contact in self.contacts)

    def display_contacts(self):
        """
        Displays all contacts in a tabular format.
        This method displays all contacts in a sorted tabular format, showing the first name, last name, phone number, and email.
        """
        if not self.contacts:
            print_in_color("No contacts available. Please, enter one.", 'red')
        else:
            sorted_contacts = sorted(self.contacts, key=lambda contact: (contact.first_name, contact.last_name))
            table_data = [[contact.first_name, contact.last_name, contact.phone_number, contact.email] for contact in sorted_contacts]
            headers = ["First Name", "Last Name", "Phone Number", "Email"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def modify_contact(self, query):
        """
        Modifies an existing contact based on a search query.
    
        This method allows the user to search for an existing contact by providing a query string.
        If contacts matching the query are found, the user can select which contact to modify.
        The details of the selected contact are shown, and the user is asked for confirmation
        before proceeding with the modification. The user is then prompted to enter new values
        for the contact's first name, last name, phone number, and email. If a new value is not
        provided, the existing value is retained. Input validation is performed for each field.
        If a duplicate contact is detected, the user is asked for confirmation before proceeding
        with the update. The modified contact information is then saved.

        Parameters:
        -----------
        query : str
            The query string used to search for the contact.

        Raises:
        -------
        ValueError
            If the user selects an invalid contact number.
        

        Example usage:
        --------------
        >>> self.modify_contact("John Doe")
        """
        results = self.search_contact(query, display=False)
        if results:
            contact = self._select_contact_from_results(results)
            if not contact:
                return

            print("\nSelected contact to modify:")
            print(contact)

            print_in_color("Are you sure you want to modify this contact? (y/n): ", 'red')
            confirm = input().strip().lower()
            if confirm != 'y':
                print_in_color("Modification cancelled.", 'red')
                return

            index = self.contacts.index(contact)

            def get_new_value(prompt, validation_func, error_message, current_value):
                """
                Prompts the user for input and validates it based on the provided validation function.

                This function repeatedly prompts the user to enter a value until a valid input is provided
                or the user decides to keep the current value by entering an empty string. The input is 
                validated using the provided validation function. If the input is invalid, an error message 
                is displayed and the user is prompted again.

                Parameters:
                -----------
                prompt : str
                    The message displayed to the user when requesting input.
                validation_func : function
                    A function that takes a single string argument and returns a boolean indicating 
                    whether the input is valid or not.
                error_message : str
                    The message displayed to the user when the input is invalid.
                current_value : str
                    The current value to keep if the user provides an empty input.

                Returns:
                --------
                str
                    The validated input provided by the user, or the current value if the input is empty.
                """
                new_value = input(prompt).strip()
                if new_value == "":
                    return current_value
                elif not validation_func(new_value):
                    print_in_color(error_message, 'red')
                    return get_new_value(prompt, validation_func, error_message, current_value)
                return new_value

            first_name = get_new_value("Enter new first name (leave blank to keep current): ", self._is_valid_name, 
                                      "Invalid first name. Only letters and spaces are allowed.", contact.first_name)

            last_name = get_new_value("Enter new last name (leave blank to keep current): ", self._is_valid_name, 
                                     "Invalid last name. Only letters and spaces are allowed.", contact.last_name)

            phone_number = get_new_value("Enter new phone number (leave blank to keep current): ", self._is_valid_phone, 
                                        "Invalid phone number. Only numbers and optionally a plus sign are allowed.",                                                             contact.phone_number)

            email = get_new_value("Enter new email (leave blank to keep current): ", self._is_valid_email, 
                                 "Invalid email. Please enter a valid email address.", contact.email)

            if self._is_duplicate(first_name, last_name, phone_number, email):
                print_in_color("This contact already exists. Do you want to update it anyway? (y/n): ", 'red')
                overwrite = input().strip().lower()
                if overwrite != 'y':
                    print_in_color("Modification cancelled due to duplicate contact.", 'red')
                    return

            self.contacts[index].first_name = first_name
            self.contacts[index].last_name = last_name
            self.contacts[index].phone_number = phone_number
            self.contacts[index].email = email

            self.save_contacts()
            print_in_color("Contact modified successfully.", 'green')
        else:
            print_in_color("No contacts found.", 'red')

    def _select_contact_from_results(self, results):
        """
        Helper function to select a contact from search results.
        """
        if len(results) > 1:
            for i, contact in enumerate(results):
                print(f"{i + 1}: {contact}")

            while True:
                try:
                    choice = int(input("Enter the index number of the contact you want to modify or delete: ")) - 1
                    if 0 <= choice < len(results):
                        return results[choice]
                    else:
                        print_in_color("Invalid selection. Please enter an index number corresponding to one of the contacts listed.",                                           'red')
                except ValueError:
                    print_in_color("Invalid input. Please enter a valid index number.", 'red')
        else:
            return results[0]

    def delete_contact(self, query):
        """
        Deletes a contact based on a search query.
        
        This method allows the user to search for an existing contact by providing a query string.
        If contacts matching the query are found, the user can select which contact to delete.
        The selected contact is then removed from the contact list and the updated list is saved.

        Parameters:
        -----------
        query : str
            The query string used to search for the contact.

        Raises:
        -------
        ValueError
            If the user selects an invalid contact number.

        Example usage:
        --------------
        >>> self.delete_contact("John Doe")
        """
        results = self.search_contact(query, display=False)
        if results:
            contact = self._select_contact_from_results(results)
            if not contact:
                return

            print("\nSelected contact to delete:")
            print(contact)
            
            print_in_color("Are you sure you want to delete this contact? (y/n): ", 'red')
            confirm = input().strip().lower()
            if confirm == 'y':
                self.contacts.remove(contact)
                self.save_contacts()
                print_in_color("Contact deleted successfully.", 'green')
            else:
                print_in_color("Contact deletion cancelled.", 'red')
        else:
            print_in_color("No contacts found.", 'red')

    def search_contact(self, query, display=True):
        """
        Searches for contacts that match the specified query.
        
        This method searches the contact list for any contact where the specified query is found in the contact's 
        first name, last name, phone number, or email. The search is case-insensitive. 

        Parameters:
        -----------
        query : str
            The string to search for within the contact details. The search will be case-insensitive.
        display : bool, optional
            If True (default), the method will print the search results to the console. If False, the results are 
            not printed but still returned.

        Returns:
        --------
        list
            A list of `Contact` objects that match the search query. If no contacts match the query, an empty list is returned.

        Example usage:
        --------------
        >>> results = manager.search_contact("john")
        >>> results
        [Contact(first_name='John', last_name='Doe', phone_number='+1234567890', email='john.doe@example.com')]
    
        >>> manager.search_contact("Smith", display=False)
        [Contact(first_name='Jane', last_name='Smith', phone_number='+0987654321', email='jane.smith@example.com')]
        """
        query = query.lower()
        results = [contact for contact in self.contacts if query in contact.first_name.lower() or 
                                                       query in contact.last_name.lower() or 
                                                       query in contact.phone_number or 
                                                       query in contact.email.lower()]
        if display:
            if results:
                table_data = [[contact.first_name, contact.last_name, contact.phone_number, contact.email] for contact in results]
                headers = ["First Name", "Last Name", "Phone Number", "Email"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
            else:
                print_in_color("No contacts found.", 'red')
        return results


def print_in_color(text, color):
    """
    Print the given text in the specified colour.
    """
    color_map = {
        'yellow': Fore.YELLOW,
        'red': Fore.RED,
        'green': Fore.GREEN,
        'blue': Fore.BLUE,
    }
    color_code = color_map.get(color, Fore.RESET)  # Set default colour if not found
    print(color_code + text + Fore.RESET)
    
    
def main():
    """
    Runs the Contact Management System application.
    
    This function serves as the entry point for the contact management system. It presents a text-based menu to the user, 
    allowing them to choose various options to manage their contacts. The available options include adding a new contact, 
    viewing all contacts, modifying an existing contact, deleting a contact, and searching for contacts. 

    The function continuously displays the menu and processes user input until the user chooses to exit the program. 

    Actions performed:
    -------------------
    1. Displays a menu with options to add, view, modify, delete, or search for contacts.
    2. Prompts the user to enter the required information based on their choice.
    3. Calls the appropriate methods from the `ContactManager` class based on the user's selection:
       - **Add Contact**: Prompts for contact details and adds a new contact to the system.
       - **View Contacts**: Displays all contacts in the contact list.
       - **Modify Contact**: Searches for and modifies an existing contact based on user input.
       - **Delete Contact**: Searches for and deletes a contact based on user input.
       - **Search Contact**: Searches for contacts that match the specified query and displays the results.
    4. Handles cases where no contacts exist and prevents modifications or deletions if no contacts are available.
    5. Exits the program when the user selects the exit option.

    Notes:
    ------
    - The function relies on the existence of a `ContactManager` class that handles the core functionality of contact management.
    - The program checks if the contact data file (`contacts.json`) exists before allowing modification, deletion, or search operations.
    - User inputs are validated, and appropriate messages are displayed for invalid choices or empty contact lists.

    Example usage:
    --------------
    When the user runs the program, they will interact with a menu system and make choices by entering numbers. 
    Example:
    
    1. The user selects "1" to add a contact and provides the required details.
    2. The user selects "2" to view all contacts.
    3. The user selects "3" to modify a contact by entering a query to search for it.
    4. The user selects "4" to delete a contact by entering a query to search for it.
    5. The user selects "5" to search for contacts and view matching results.
    6. The user selects "6" to exit the program.
    """
    manager = ContactManager()
        
    while True:
        print_in_color("\n" + "="*45, 'yellow')
        print_in_color("   ContactEase - Contact Management System", 'yellow')
        print_in_color("="*45, 'yellow')
        print_in_color("1. Add Contact", 'yellow')
        print_in_color("2. View Contacts", 'yellow')
        print_in_color("3. Modify Contact", 'yellow')
        print_in_color("4. Delete Contact", 'yellow')
        print_in_color("5. Search Contact", 'yellow')
        print_in_color("6. Exit", 'yellow')
        print_in_color("="*45, 'yellow')

        print_in_color("Enter your choice (1-6): ", 'yellow')
        choice = input().strip()

        if choice == '1':
            print("\nEnter new contact details:")
            manager.add_contact()
        elif choice == '2':
            print("\nDisplaying all contacts:")
            manager.display_contacts()
        elif choice == '3':
            if os.path.exists("contacts.json"):
                query = input("Enter the name, phone number, or email of the contact to modify: ").strip()
                manager.modify_contact(query)
            else:
                print_in_color("No contacts found. Please add a contact first.", 'red')
        elif choice == '4':
            if os.path.exists("contacts.json"):
                query = input("Enter the name, phone number, or email of the contact to delete: ").strip()
                manager.delete_contact(query)
            else:
                print_in_color("No contacts found. Please add a contact first.", 'red')
        elif choice == '5':
            if os.path.exists("contacts.json"):
                query = input("Enter the name, phone number, or email of the contact to search: ").strip()
                manager.search_contact(query)
            else:
                print_in_color("No contacts found. Please add a contact first.", 'red')
        elif choice == '6':
            print("\nExiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")

if __name__ == "__main__":  #is a common construct in Python used to check whether a script is executed as the main program or imported as                            a module into another script.
    main()
