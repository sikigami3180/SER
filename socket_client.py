import socket
import threading
import socket_server
import random


class SocketClient():
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 50007
        self.number = random.randint(1, 10)


    def socket_client_up(self):
        print('{}さん、こんにちは。チャットを開始します。'.format(self.number))
        # クライアントソケット作成(IPv4, TCP)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # サーバソケットへ接続しに行く(サーバのホスト名, ポート番号)
                sock.connect((self.host, self.port))
                # スレッド作成
                thread = threading.Thread(target=self.handler, args=(sock,), daemon=True)
                # スレッドスタート
                thread.start()
                # クライアントからメッセージを送る
                self.send_message(sock)
            except ConnectionRefusedError:
                # 接続先のソケットサーバが立ち上がっていない場合、
                # 接続拒否になることが多い
                print('ソケットサーバに接続を拒否されました。')
                print('ソケットサーバを立ち上げます。')
                print('Starting....')
                ss = socket_server.SocketServer()
                ss.socket_server_up()

    def send_message(self, sock):
        while True:
            try:
                # ユーザのキーボード入力を受け取る
                msg = "[{}]".format(self.number) + input()
            except KeyboardInterrupt:
                msg = '{} さんが退出しました。'.format(self.number)
                # メッセージ送信
                sock.send(msg.encode('utf-8'))
                break
            if msg == '[{}]exit'.format(self.number):
                msg = '{} さんが退出しました。'.format(self.number)
                # メッセージ送信
                sock.send(msg.encode('utf-8'))
                break
            elif msg:
                try:
                    # メッセージ送信
                    sock.send(msg.encode('utf-8'))
                except ConnectionRefusedError:
                    # 接続先のソケットサーバが立ち上がっていない場合、
                    # 接続拒否になることが多い
                    break
                except ConnectionResetError:
                    break

    def handler(self, sock):
        while True:
            try:
                # クライアントから送信されたメッセージを 1024 バイトずつ受信
                data = sock.recv(1024)
                print("  {}".format(data.decode("utf-8")))
            except ConnectionRefusedError:
                # 接続先のソケットサーバが立ち上がっていない場合、
                # 接続拒否になることが多い
                break
            except ConnectionResetError:
                break


if __name__ == "__main__":
    sc = SocketClient()
    sc.socket_client_up()