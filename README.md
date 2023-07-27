# Unity-Python-TCP-Server

![License](https://img.shields.io/badge/License-GNUv3-blue.svg)

## Project Overview

This project includes a server and a client script for a decentralized peer-to-peer network game. The server, implemented in Python as `unityserver.py`, facilitates communication between multiple clients, allowing them to interact with each other in the game. The C# client script `TCPClient.cs` is designed for Unity and connects to the server via TCP for data exchange.

The server is responsible for handling incoming client connections, client authentication, peer-to-peer communication setup, data synchronization, error handling, and security measures.

The client is a Unity TCP client that can connect to the server and receive data. It is designed to be efficient, robust, and easily integrated into Unity projects.

## Table of Contents

- [Server Features](#server-features)
- [Client Features](#client-features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Server Features

The `unityserver.py` script includes the following features:

- **Server Setup:** Sets up a Python server socket to listen for incoming client connections. The server can run continuously, accepting connections from multiple clients without interrupting the gameplay experience.

- **Client Authentication:** Implements a secure client authentication mechanism to ensure only legitimate clients can connect to the server. You can customize the authentication logic to suit your game's requirements.

- **Peer-to-Peer Communication:** Handles communication between clients in a peer-to-peer manner. The server facilitates the initial connection and communication setup, but the actual communication between clients is direct and decentralized.

- **Data Synchronization:** Manages synchronization of game data between connected clients. This includes handling player actions, positions, game state, and other relevant gameplay information that must be consistent across all players.

- **Error Handling and Logging:** Implements robust error handling mechanisms to handle potential issues such as client disconnections or network errors. Logging functionality records server activities and errors for debugging purposes.

- **Security Measures:** Includes necessary security measures to protect the server and clients from potential security threats, such as unauthorized access, data tampering, or denial-of-service attacks.

## Client Features

The `TCPClient.cs` script includes the following features:

- **TCP Communication:** Implements a TCP client for Unity that can establish and maintain a reliable connection to the server. The client can send and receive data in a structured format.

- **Data Serialization:** Provides a basic data serialization mechanism for converting complex data structures (e.g., JSON, binary) into a format suitable for transmission over TCP. You can customize this serialization based on your specific data requirements.

- **Error Handling:** Implements proper error handling to address various scenarios, such as connection failures, data corruption, and server unavailability.

- **Threading:** Uses appropriate threading mechanisms to handle TCP communication without blocking the main Unity thread. This ensures a smooth user experience and prevents application freezes.

- **Callbacks/Events:** Designed to use callbacks or events to notify other parts of the Unity application when new data is received or the connection status changes.

## Installation

1. Clone this repository to your local machine using Git:

```
git clone https://github.com/agx-r/Unity-Python-TCP-Server.git
```

2. For the Python server script, ensure you have Python 3.x installed. No additional dependencies are required.

3. For the Unity client script, open your Unity project and place the `TCPClient.cs` script in the appropriate Unity project folder.

## Usage

1. Start the Python server:

```bash
python unityserver.py
```

2. In Unity, attach the `TCPClient.cs` script to an empty GameObject.

3. Customize the `unityserver.py` and `TCPClient.cs` scripts according to your game's specific needs.

## License

This project is licensed under the GNU General Public License v3.0 (GNUv3) - see the [LICENSE](LICENSE) file for details.
