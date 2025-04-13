"""
    Title: Contacts Book
    Name: Merga Shasho Mekonnen
    Github: MagMc007
    EdX: mega_mag
    From: Addis Ababa, Ethiopia
    Date: 10/7/2024
"""
import sqlite3
from validator_collection import validators, errors
import re
from tabulate import tabulate


# create database to serve as phonebook
global con
global cur
con = sqlite3.connect("phonebook.db")
cur = con.cursor()
# create a table with four columns
cur.execute(
    """CREATE TABLE IF NOT EXISTS contacts(
                    name TEXT ,
                    phone TEXT NOT NULL,
                    email TEXT,
                    address TEXT)"""
)


def main():
    print("HELLO USER\nCHOOSE THE OPTION YOU WANT")
    options()
    while True:
        print("Would you like to access the phonebook again?")
        confirmation = input("yes/no: ").strip()
        if confirmation == "yes":
            options()
        elif confirmation == "no":
            con.close()
            print("GOOD BYE!")
            break


# views the options to choose to the user
def entry():
    table = [
        ["1.", "To create new contact"],
        ["2.", "To update a existing contact"],
        ["3.", "To delete existing contact"],
        ["4.", "To search contact with name"],
        ["5.", "To search contact with phone number"],
        ["6.", "To display all contacts"],
    ]
    print(tabulate(table, tablefmt="pretty"))
    while True:
        user_input = input("You want: ").strip()
        if user_input in ["1", "2", "3", "4", "5", "6"]:
            return user_input
        else:
            print("Please choose from the provided options")
            pass
        


def options():
    user_input = entry()
    # for creating a new contact
    if user_input == "1":
        name = input("Name: ").title().strip()
        # accept and validate phone number
        while True:
            phone = input("Phone: ").strip()
            if validate_phone_number(phone) == True:
                duplicate = search_contact_with_phone_number(phone)
                if duplicate:
                    print("Phone number already taken, try again")
                else:
                    break
            else:
                pass
        # accept and validate email
        while True:
            email = input("Email(optional): ")
            if email:
                if validate_email(email) == True:
                    break
                else:
                    pass
            else:
                break

        address = input("Address(optional): ")
        # check if contact already exists
        if search_contact_with_name(name):
            print("Contact already exists\n")
        else:
            add_new_contact(name, phone, email, address)
    # for updating contacts
    if user_input == "2":
        # check if contact exists
        while True:
            name = input("Name: ").title().strip()
            data = search_contact_with_name(name)
            if data:
                break
            else:
                print("The contact is not in phonebook")

        # accept and validate phone number
        while True:
            phone = input("Phone: ").strip()
            #check if phone number is valid 
            if validate_phone_number(phone) == True:
                #check if phone number is taken by another contact
                duplicate = search_contact_with_phone_number(phone)
                if not duplicate or duplicate == search_contact_with_name(name):
                    break
                else:
                    print("Phone number already taken, try again")
            else:
                pass
            # accept and validate email
        while True:
            email = input("Email(optional): ")
            if email:
                if validate_email(email) == True:
                    break
                else:
                    pass
            else:
                break
        address = input("Address(optional): ")
        # update contact
        update_contacts(name, phone, email, address)
        print("Contact updated")
    # to delete contact
    if user_input == "3":
        # check if contact is in phonebook and delete it
        name = input("Name: ").title().strip()
        data = search_contact_with_name(name)

        if data:
            delete_contact(name)
        else:
            print("Contact is not in phonebook")
    # search contact by name
    if user_input == "4":
        name = input("Name: ").title().strip()
        data = search_contact_with_name(name)
        # display contacts info in a table format if it's in phone book
        if data:
            print(
                tabulate(
                    data,
                    headers=["Name", "Phone", "Email", "Address"],
                    tablefmt="github",
                )
            )
        else:
            print("Contact is not in phonebook")
    # search contact using phone number
    if user_input == "5":
        # accept and validate phone number
        while True:
            phone = input("Phone: ").strip()
            if validate_phone_number(phone) == True:
                break
            else:
                pass
        data = search_contact_with_phone_number(phone)
        # display data in table if it exists
        if data:
            print(
                tabulate(
                    data,
                    headers=["Name", "Phone", "Email", "Address"],
                    tablefmt="github",
                )
            )
        else:
            print("Contact is not in phonebook")
    # to display all contacts in table
    if user_input == "6":
        data = display_all_contact()
        if data:
            print(
                tabulate(
                    data,
                    headers=["Name", "Phone", "Email", "Address"],
                    tablefmt="github",
                )
            )
        else:
            print("No contacts in phonebook")


# add new contact
def add_new_contact(name, phone, email=None, address=None):
    # command the phonebook to insert the new contact
    cur.execute(
        """INSERT INTO contacts(name,phone,email,address)
                 VALUES(?,?,?,?)""",
        (name, phone, email, address.title()),
    )
    # save changes to phonebook
    con.commit()
    print("Contact has been created")


# to delete existing contact
def delete_contact(user_input):
    # command the phonebook to delete the contact
    cur.execute(
        """DELETE FROM contacts
           WHERE name= ?""",
        (user_input,),
    )
    # save changes to phonebook
    con.commit()
    print("Contact deleted successfully")


# to update existiong contact
def update_contacts(name, phone=None, email=None, address=None):
    # use string and lists to give the proper command to the phonebook on what to update

    query = "UPDATE contacts SET"
    updates = [" phone=?"]
    params = [phone]

    if email:
        updates.append(" email=?")
        params.append(email)

    if address:
        updates.append(" address=?")
        params.append(address.title())
    # combine then update with qeury
    query += ",".join(updates)
    # set the condition to update the contact
    query += " WHERE name = ?"

    params.append(name)
    cur.execute(query, params)
    # save changes
    con.commit()


def search_contact_with_name(user_input):
    # command to selct where the name user  wants
    cur.execute(
        """SELECT * 
            FROM contacts
            WHERE name = ?
        """,
        (user_input,),
    )
    # return those names from contact
    return cur.fetchall()


def search_contact_with_phone_number(user_input):
    # command to search with phone number
    cur.execute(
        """SELECT *
                    FROM contacts
                    WHERE phone = ?
                    """,
        (user_input,),
    )
    # return the contact with that phone number
    return cur.fetchall()


def display_all_contact():
    # select all contact and return them
    cur.execute(
        """SELECT * 
                FROM contacts
                ORDER BY name 
                """
    )

    return cur.fetchall()


def validate_phone_number(phone):
    # chick if users input matches the format of a correct phone number
    phone_pattern = r"^\+?\d{1,3}?\s?\(?\d{2,3}\)?\s?\d{3,5}[-.\s]?\d{4}$"

    match = re.match(phone_pattern, phone)
    if not match:
        print("Invalid phone number, please insert again using correctformat")
        return False
        
    return True
    
        


def validate_email(email):
    # check if users input matches a correct email
    try:
        validators.email(email)
        return True
    except errors.InvalidEmailError:
        print("Invalid email , please insert again")
        return False


if __name__ == "__main__":
    main()
