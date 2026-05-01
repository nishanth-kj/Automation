import asyncio
import json
import threading
from PySide6.QtWebSockets import QWebSocketServer
from PySide6.QtNetwork import QHostAddress
from PySide6.QtCore import QObject, Signal

class WebSocketService(QObject):
    new_connection = Signal(object)
    message_received = Signal(str, str) # client_id, message

    def __init__(self, port=8765):
        super().__init__()
        self.port = port
        self.server = QWebSocketServer("MemeServer", QWebSocketServer.NonSecureMode)
        self.clients = []

    def start(self):
        if self.server.listen(QHostAddress.Any, self.port):
            print(f"WebSocket Server started on port {self.port}")
            self.server.newConnection.connect(self.on_new_connection)
            return True
        return False

    def on_new_connection(self):
        client = self.server.nextPendingConnection()
        client.textMessageReceived.connect(lambda msg: self.on_message(client, msg))
        client.disconnected.connect(lambda: self.on_disconnected(client))
        self.clients.append(client)
        print("New client connected")

    def on_message(self, client, message):
        print(f"Message received: {message}")
        # Echo back or handle specific requests (like 'fetch_news')
        try:
            data = json.loads(message)
            if data.get("action") == "ping":
                client.sendTextMessage(json.dumps({"action": "pong"}))
        except:
            pass

    def on_disconnected(self, client):
        if client in self.clients:
            self.clients.remove(client)
            print("Client disconnected")

    def broadcast(self, message_dict):
        msg = json.dumps(message_dict)
        for client in self.clients:
            client.sendTextMessage(msg)
