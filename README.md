# Socket.IO Chat Application with DES Encryption

This Python-based chat application leverages Socket.IO for real-time communication and employs the Data Encryption Standard (DES) algorithm to ensure secure messaging between users.

## Features

- **Socket.IO Real-Time Communication:**
  - Facilitates real-time communication between the server and clients.
  - Utilizes Socket.IO events for seamless messaging.

- **Secure Message Encryption with DES:**
  - Implements the Data Encryption Standard (DES) algorithm for message encryption.
  - Provides a secure communication channel for users.

- **User Management:**
  - Users can set and display their usernames.
  - Maintains a list of connected users.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages: `socketio`, `eventlet`

### Installation

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd DES-Implementation-Internet-Communication-App
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Server:**

    ```bash
    python3 server/server.py
    ```

   The server will start and listen for incoming connections on `http://localhost:8888`.

2. **Run the Client:**

    ```bash
    python3 client/client.py
    ```

   The client will prompt you to enter a username and an encryption key. Follow the on-screen instructions to send and receive encrypted messages.

## Customization

- **DES Encryption Settings:**
  - The DES encryption settings, including key generation and message encryption/decryption, are configured in the `server/des.py` and `server/server.py` files.

- **Socket.IO Event Handling:**
  - Customize Socket.IO event handlers in the `server/server.py` and `client/client.py` files based on your application's requirements.

## Contributing

Feel free to contribute to this project by opening issues or submitting pull requests. Your feedback and contributions are highly appreciated.

## Acknowledgments

- Special thanks to the Socket.IO library for enabling real-time communication.

---

Created by Jabalnur
