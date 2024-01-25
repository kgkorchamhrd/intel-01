import socket

def connect_to_server(host, port, message, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"서버에 연결됨: {host}:{port}")

        # 서버에 메세지 보내기
        client_socket.sendall(message.encode())
        print(f"서버에 메세지 전송: {message}")

        if isinstance(data, str) or isinstance(data, int):
            client_socket.sendall(str(data).encode())
        else:
            client_socket.sendall(message.encode())
            print(f"서버에 메세지 전송: 잘못된 형식입니다. string인지 확인해보세요.")

        # 서버로부터의 메세지 받기
        response = client_socket.recv(1024)
        print(f"서버로부터의 응답: {response.decode()}")

if __name__ == '__main__':    
    data_int = 1
    data_str = '안녕하세요'
    data_file = './temp/test'
    server_port = 2112
    server_ip = '10.10.59.56'
    connect_to_server(server_ip, server_port, '문자를 보내겠습니다.', data_str)



