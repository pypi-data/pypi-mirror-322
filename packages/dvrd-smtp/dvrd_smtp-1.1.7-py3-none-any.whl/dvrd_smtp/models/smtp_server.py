from smtplib import SMTP, SMTP_SSL, SMTPException

from dvrd_smtp.models.smtp_message import SMTPMessage


class SMTPServer:
    def __init__(self, *, host: str, port: int, username: str, password: str, use_ssl: bool = True,
                 use_tls: bool = True, auto_connect: bool = True):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._use_ssl = use_ssl
        self._use_tls = use_tls
        self._connection: SMTP | SMTP_SSL | None = None
        if auto_connect:
            self.connect()

    def send_message(self, *, message: SMTPMessage) -> dict[str, tuple[int, bytes]]:
        if not message.from_addr:
            message.from_addr = self._username
        return self._get_connection().send_message(message.build(), from_addr=message.envelope,
                                                   to_addrs=message.all_recipients)

    def connect(self):
        if self._use_ssl:
            server = SMTP_SSL(host=self._host, port=self._port)
        else:
            server = SMTP(host=self._host, port=self._port)
            if self._use_tls:
                server.starttls()
        server.login(user=self._username, password=self._password)
        self._connection = server

    def close(self):
        if self._connection:
            self._connection.quit()

    def _get_connection(self) -> SMTP | SMTP_SSL:
        if not (connection := self._connection):
            raise SMTPException('Not connected to the SMTP server yet, use `connect()` first.')
        return connection

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
