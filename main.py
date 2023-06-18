import socket
import threading


class VPN_Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))

    def start(self):
        self.server_socket.listen(5)
        print(f"VPN-сервер запущен и слушает на {self.host}:{self.port}...")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Получено подключение от {client_address}")

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        try:
            # Отправляем требование ввода логина и пароля
            client_socket.sendall(b"Введите логин: ")
            login = client_socket.recv(1024).decode().strip()

            client_socket.sendall(b"Введите пароль: ")
            password = client_socket.recv(1024).decode().strip()

            # Проверяем логин и пароль
            if login == "Demor22" and password == "Bazar228":
                client_socket.sendall(b"Доступ разрешен. Введите данные для обработки:\n")
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break

                    processed_data = self.process_data(data)
                    client_socket.sendall(processed_data)
            else:
                client_socket.sendall(b"Неверный логин или пароль. Соединение закрыто.\n")
        except Exception as e:
            print(f"Произошла ошибка во время обработки клиента: {e}")
        finally:
            client_socket.close()

    def process_data(self, data):
        # Здесь можно добавить свою логику для обработки и изменения данных
        processed_data = data.upper()  # В примере просто преобразуем данные в верхний регистр
        return processed_data


# Создаем экземпляр VPN-сервера и запускаем его
vpn_server = VPN_Server('angry-swamp-waxflower.glitch.me', 80)
vpn_server.start()
