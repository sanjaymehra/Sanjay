from spy_details import spy, Spy, ChatMessage, friends
from steganography.steganography import Steganography
from termcolor import colored
from datetime import datetime

# LIST....

STATUS_MESSAGES = [
                   'Hey there! Im using spyChat!',
                   'My name sanjay, sanjay mehra',
                   'love is easy but I am very busy.',
                   'Typing.... Sir',
                   'Pyar Mohabbat Dhokha Hai, Padh Le Beta Moka Hai.',
                   '36 Aayengi 36 Jayengi Meri Wali To Mummy Layengi'
                   ]

SPECIAL_MESSAGES = [
                    'SPM',
                    'SAVE ME'
    ]

#SELECT A FRIENDS........

def select_a_friend():
    if len(friends) != 0:
        print_friends()
        friend_choice = raw_input("Choose from your friends")
        friend_choice_position = int(friend_choice) - 1
    else:
        print "No friend found! Add a friend first"
        return -1

    return friend_choice_position

#GETTING STARTED.........


print colored("Hello! Welcome to SpyChat","blue")

question = "Do you want to continue as " + spy.salutation + " " + spy.name + " (Y/N)? "
existing = raw_input(question).upper()

#UPDATE STATUS.......


def add_status():

    updated_status_message = None


    if spy.current_status_message != None:

        print colored('Your current status message is %s \n','red') % colored((spy.current_status_message),'blue')
    else:
        print 'You don\'t have any status message currently \n'

    default = raw_input("Do you want to select from the older status (y/n)? ")

    if default.upper() == "N":
        new_status_message = raw_input("What status message do you want to set? ")


        if len(new_status_message) > 0:
            if new_status_message.decode('utf-8').isspace():
                updated_status_message = None
            else:
                STATUS_MESSAGES.append(new_status_message)
                updated_status_message = new_status_message

    elif default.upper() == 'Y':

        item_position = 1

        for message in STATUS_MESSAGES:
            print colored('%d. %s' % (item_position, message),'blue')
            item_position = item_position + 1

        message_selection = int(raw_input("\nChoose from the above messages "))


        if len(STATUS_MESSAGES) >= message_selection:
            updated_status_message = STATUS_MESSAGES[message_selection - 1]

    else:
        print 'The option you chose is not valid! Press either y or n.'

    if updated_status_message:
        print colored('Your updated status message is: %s','red') % colored((updated_status_message),'blue')
    else:
        print 'You current don\'t have a status update'

    return updated_status_message

# PRINT FRIEND LIST ....

def print_friends():
    if len(friends) != 0:
        item_number = 0
        print '\nYour friends are:\n'
        for friend in friends:
            print colored(
                '%d. %s %s aged %d with rating %.2f is online' % (item_number + 1, friend.salutation, friend.name,
                                                                  friend.age,
                                                                  friend.rating), 'blue')
            item_number = item_number + 1
    else:
        return
    return


#  ADD A FRIEND ....



def add_friend():

    new_friend = Spy('','',0,0.0)

    new_friend.name = raw_input("Please add your friend's name: ")
    new_friend.salutation = raw_input("Are they Mr. or Ms.?: ")


    new_friend.age = raw_input("Age?")
    new_friend.age = int(new_friend.age)

    new_friend.rating = raw_input("Spy rating?")
    new_friend.rating = float(new_friend.rating)

    if len(new_friend.name) > 0 and new_friend.age > 12 and new_friend.rating >= spy.rating:
        friends.append(new_friend)
        print 'Friend Added!'
        print_friends()
    else:
        print 'Sorry! Invalid entry. We can\'t add spy with the details you provided'

    return len(friends)

# REMOVE A FRIEND.....


def remove_friend():
    friend_choice = select_a_friend()
    if friend_choice == -1:
        return 0
    friend_choice_position = int(friend_choice)

    del friends[friend_choice_position]
    print_friends()
    return len(friends)

#REMOVE A FRIEND....

def send_message():

    friend_choice = select_a_friend()
    original_image = raw_input("\nWhat is the name of the image?")
    output_path = "output.jpg"

    default = raw_input("Do you want to select from the special messages (y/n)? ")
    if default.upper() == "N":
        text = raw_input("What do you want to say? ")
    elif default.upper() == "Y":
        item_position = 1

        for message in SPECIAL_MESSAGES:
            print '%d. %s' % (item_position, message)
            item_position = item_position + 1

        message_selection = int(raw_input("\nChoose from the above messages "))-1


        if len(SPECIAL_MESSAGES) >= message_selection:
            if message_selection == 0:
                text = "This is an SOS"
            elif message_selection == 1:
                text = "Please Help Me!"

    Steganography.encode(original_image, output_path, text)

    new_chat = ChatMessage(text, True)

    friends[friend_choice].chats.append(new_chat)

    print "Your secret message image is ready!\n"

# READ A MESSAGE,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,


def read_message():

    sender = select_a_friend()

    output_path = raw_input("What is the name of the file?")

    secret_text = Steganography.decode(output_path)

    if 0 < len(secret_text.split(" ")) < 100:
        new_chat = ChatMessage(secret_text, False)

        print secret_text

    elif len(secret_text.split(" ")) > 100:
        del friends[sender]
        print "Friend deleted because he/she was speaking too much!"
    else:
        print "Image doesn't have any messages"

#CHAT HISTORY,,,,,,,,,,,,,,,,,,,,,,,,,,,,,


def read_chat_history():

    read_for = select_a_friend()

    print '\n'

    for chat in friends[read_for].chats:
        if chat.sent_by_me:
            print colored('[%s] %s: %s' % (colored(chat.time.strftime("%d %B %Y %H:%M"),"blue"), colored('Me','red'), chat.message))
        else:
            print '[%s] %s: %s' % (chat.time.strftime("%d %B %Y %H:%M"), friends[read_for].name, chat.message)


 #START CHAT,,,,,,,,,,,,,,,,,,,,,,,,,,


def start_chat(spy):

    spy.name = spy.salutation + " " + spy.name


    if spy.age > 12 and spy.age < 50:


        print "\nAuthentication complete. Welcome " + spy.name + " age: " \
              + str(spy.age) + " and rating of: " + str(spy.rating) + " Proud to have you onboard\n"

        show_menu = True

        while show_menu:
            print "What do you want to do? \n"
            menu_choices = ["Add a status update",
                            "View friends",
                            "Add a friend",
                            "Remove a friend",
                            "Send a secret message",
                            "Read a secret message",
                            "Read Chats from a user",
                            "Close Application \n"
                            ]
            for i in range(0,len(menu_choices)):
                print colored((i+1),'red'),colored(menu_choices[i],'grey')

            menu_choice = int(raw_input("Enter choice:"))
            if menu_choice == 1:
                spy.current_status_message = add_status()
            elif menu_choice == 2:
                print_friends()
            elif menu_choice == 3:
                number_of_friends = add_friend()
                print 'You have %d friends' % (number_of_friends)
            elif menu_choice == 4:
                remove_friend()
            elif menu_choice == 5:
                send_message()
            elif menu_choice == 6:
                read_message()
            elif menu_choice == 7:
                read_chat_history()
            else:
                show_menu = False
                print 'application closed'

    else:
        print 'Sorry you are not of the correct age to be a spy'

if existing == "Y":
    start_chat(spy)
else:

    spy = Spy('','',0,0.0)


    spy.name = raw_input("Welcome to spy chat, you must tell me your spy name first: ")

    if len(spy.name) > 0:
        spy.salutation = raw_input("Should I call you Mr. or Ms.?: ")

        spy.age = raw_input("What is your age?")
        spy.age = int(spy.age)

        spy.rating = raw_input("What is your spy rating?")
        spy.rating = float(spy.rating)

        start_chat(spy)
    else:
        print 'Please add a valid spy name'

#APPLICATION CLOSED,,,,,,,,,,,,,,,,