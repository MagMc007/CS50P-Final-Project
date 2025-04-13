from project import *


def test_validate_email():
    assert validate_email("mergas.mokonnnen@gmail.com") == True
    assert validate_email("mergas%gmail.com") == False

def test_validate_phone_number():
    assert validate_phone_number("+251910349460") == True
    assert validate_phone_number("091345") == False

def test_search_contact_with_name():
    add_new_contact("Joe", "0987654321", "jav@yahoo.com", "Addis Ababa")

    assert search_contact_with_name("Joe") == [("Joe", "0987654321",
                                                 "jav@yahoo.com", 
                                                 "Addis Ababa")]
    
    update_contacts("Joe", "0987654321", "jav@gmail.com", "Addis Ababa")

    assert search_contact_with_name("Joe") == [("Joe", "0987654321",
                                                 "jav@gmail.com", 
                                                 "Addis Ababa")]
                                                
    delete_contact("Joe")
    assert search_contact_with_name("Joe") == []
    

def test_search_contact_with_phone_number():
    add_new_contact("Joe Clinton", "0987654321", "jav@yahoo.com", "Addis Ababa")

    assert search_contact_with_phone_number("0987654321") == [("Joe Clinton", "0987654321",
                                                        "jav@yahoo.com", "Addis Ababa")]
                                                
    delete_contact("Joe Clinton")
