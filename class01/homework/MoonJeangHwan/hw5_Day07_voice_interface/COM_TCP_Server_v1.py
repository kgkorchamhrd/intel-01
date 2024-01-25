import socket

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"서버가 {host}:{port}에서 연결을 기다리고 있습니다.")

        connection, address = server_socket.accept()
        with connection:
            print(f"{address}로부터 연결됨")
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                print(f"받은 데이터: {data.decode()}")
        
                response_message = f"'{data.decode()}' 수신"
                connection.sendall(response_message.encode())

if __name__ == "__main__":
    start_server('10.10.59.56', 2112)
    
