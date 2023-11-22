import socketio
import time

sio = socketio.Client()

username = input("Enter your username: ")
encryption_key = input("Enter the key to encrypt the message: ")

connected_users = []
received_messages = []

@sio.event
def connect():
    global connected_users
    print("Connected to server")
    sio.emit('set_username', {'username': username})

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.event
def receive_message(data):
    sender_sid = data['sender_sid']
    encrypted_text = data['encrypted_text']
    global received_messages
    received_messages.append({'sender_sid': sender_sid, 'text': encrypted_text})

@sio.event
def open_message(data):
    print(f"Received Message from {data['username']}: {data['text']}")

@sio.event
def user_list(data):
    global connected_users
    for user in data['users']:
        if user not in connected_users:
            connected_users.append(user)

if __name__ == '__main__':
    server_url = 'http://localhost:8888'
    sio.connect(server_url)
    sio.emit('get_user_list')
    
    while True:
        sio.emit('get_user_list')
        print("\nMenu:")
        print("1. Send Message")
        print("2. Receive Message")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            while True:
                sio.emit('get_user_list')
                time.sleep(1)
                print("Choose a user to send a message:")
                for i, user in enumerate(connected_users, start=1):
                    print(f"{i}. {user['username']}")
                
                try:
                    choice = int(input("Enter the number of the user: "))
                    recipient_sid = connected_users[choice - 1]['sid']
                    print("Recepient Username: ", connected_users[choice - 1]['username'])
                except (ValueError, IndexError):
                    print("Invalid choice. Please enter a valid number.")
                    continue

                text_to_send = input("Enter message to send: ")
                
                sio.emit('send_message', {'text': text_to_send, 'key': encryption_key, 'recipient_sid': recipient_sid})
                
                print("Send Again? (y/n)")
                exit_choice = input()
                if exit_choice == 'n':
                    break

        elif choice == '2':
            while True:
                sio.emit('get_user_list')
                time.sleep(1)
                print("Choose a user to open messages:")
                for i, user in enumerate(connected_users, start=1):
                    print(f"{i}. {user['username']}")
                
                try:
                    choice = int(input("Enter the number of the user: "))
                    sender_user = connected_users[choice - 1]
                except (ValueError, IndexError):
                    print("Invalid choice. Please enter a valid number.")
                    continue
                

                print(f"Total Messages Received: {len(received_messages)}")
                
                if len(received_messages) != 0:
                    decryption_key = input("Enter the key to decrypt the message: ")
                    print(f"Messages from {sender_user['username']}:")
                    for message in received_messages:
                        if message['sender_sid'] == sender_user['sid']:
                            sio.emit('get_message', {'text': message['text'], 'key': decryption_key, 'sender_username': sender_user['username']})
                
                time.sleep(1)
                print("Open Again? (y/n)")
                exit_choice = input()
                if exit_choice == 'n':
                    break
        elif choice == '3':
            break
                
    sio.disconnect()
