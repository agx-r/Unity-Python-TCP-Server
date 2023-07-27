import socket
import threading
import logging

class PeerToPeerServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {}
        self.lock = threading.Lock()
        self.banned_clients = set()  # Set to store banned client addresses
        self.server_socket = None
        self.is_running = False
        self.handlers = {}  # Dictionary to store registered handler functions

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.is_running = True

        logging.info(f"Server listening on {self.host}:{self.port}")

        while self.is_running:
            try:
                client_socket, client_address = self.server_socket.accept()

                # Check if client is banned before handling the connection
                if client_address in self.banned_clients:
                    logging.info(f"Connection attempt from banned client {client_address}.")
                    client_socket.close()
                    continue

                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
            except Exception as e:
                logging.error(f"Error accepting client connection: {e}")

    def stop(self):
        self.is_running = False
        self.server_socket.close()

    def handle_client(self, client_socket):
        client_address = client_socket.getpeername()
        logging.info(f"New connection from {client_address}")

        # Implement client authentication here (e.g., check credentials or generate a unique client identifier)

        with self.lock:
            self.clients[client_address] = client_socket

        try:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                # Process and synchronize game data here
                self.broadcast(data, client_address)

                # Call registered handler functions for data processing
                for handler in self.handlers.values():
                    handler(data, client_address)

        except Exception as e:
            logging.error(f"Error handling client connection: {e}")

        finally:
            with self.lock:
                del self.clients[client_address]
                client_socket.close()
                logging.info(f"Connection closed with {client_address}")

    def broadcast(self, data, sender_address):
        with self.lock:
            for address, client_socket in self.clients.items():
                if address != sender_address:
                    try:
                        client_socket.sendall(data)
                    except Exception as e:
                        logging.error(f"Error broadcasting data to {address}: {e}")

    def kick_client(self, client_address):
        with self.lock:
            if client_address in self.clients:
                client_socket = self.clients[client_address]
                del self.clients[client_address]
                client_socket.close()
                logging.info(f"Kicked client {client_address}.")

    def ban_client(self, client_address):
        with self.lock:
            if client_address in self.clients:
                self.kick_client(client_address)
            self.banned_clients.add(client_address)
            logging.info(f"Banned client {client_address}.")

    def unban_client(self, client_address):
        with self.lock:
            if client_address in self.banned_clients:
                self.banned_clients.remove(client_address)
                logging.info(f"Unbanned client {client_address}.")

    def add_handler(self, name, handler_func):
        self.handlers[name] = handler_func

    def send_response(self, client_address, data):
        with self.lock:
            client_socket = self.clients.get(client_address)
            if client_socket:
                try:
                    client_socket.sendall(data)
                except Exception as e:
                    logging.error(f"Error sending response to {client_address}: {e}")

    def remove_handler(self, name):
        if name in self.handlers:
            del self.handlers[name]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    server_host = "127.0.0.1"
    server_port = 5000

    server = PeerToPeerServer(server_host, server_port)
    try:
        server.start()
    except KeyboardInterrupt:
        logging.info("Server stopped by user.")
    finally:
        server.stop()
