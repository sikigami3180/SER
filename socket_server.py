import socket
import threading


class SocketServer():
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 50007
        self.clients = []

    def socket_server_up(self):
        # ソケットサーバ作成(IPv4, TCP)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 接続待ちするサーバのホスト名とポート番号を指定
        sock.bind((self.host, self.port))
        # 5 ユーザまで接続を許可
        sock.listen(5)
        while True:
            try:
                # 接続要求を受信
                conn, addr = sock.accept()
            except KeyboardInterrupt:
                break
            # アドレス確認
            print("[接続]{}".format(addr))
            # クライアントを追加
            self.clients.append((conn, addr))
            # スレッド作成
            thread = threading.Thread(target=self.handler, args=(conn, addr), daemon=True)
            # スレッドスタート
            thread.start()

    def close_connection(self, conn, addr):
        print('[切断]{}'.format(addr))
        # 通信を遮断する
        conn.close()
        # クライアントを除外する
        self.clients.remove((conn, addr))

    def handler(self, conn, addr):
        while True:
            try:
                # クライアントから送信されたメッセージを 1024 バイトずつ受信
                data = conn.recv(1024)
            except ConnectionResetError:
                # クライアント側でソケットを強制終了(Ctrl + c)すると
                # ソケットサーバが処理落ちするので、コネクションを切断する
                self.close_connection(conn, addr)
                break

            if not data:
                # データが無い場合、接続を切る
                self.close_connection(conn, addr)
                break
            else:
                print('data : {}, addr&port: {}'.format(data, addr))
                for client in self.clients:
                    try:
                        client[0].sendto(data, client[1])
                    except ConnectionResetError:
                        break


if __name__ == "__main__":
    ss = SocketServer()
    ss.socket_server_up()