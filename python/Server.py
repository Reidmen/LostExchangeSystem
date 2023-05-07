import asyncio
import logging
import pathlib
import datetime
import os
import sys

class Server:
    def __init__(self, ip: str, port: int, loop: asyncio.AbstractEventLoop):
        self.__ip = ip
        self.__port = port
        self.__loop = loop
        self.__logger: logging.Logger = self.initialize_logger()

        print(f"Server initialized at {self.ip}:{self.port}")

    @property
    def logger(self):
        return self.__logger

    @property
    def ip(self):
        return self.__ip

    @property
    def port(self):
        return self.__port

    @property
    def loop(self):
        return self.__loop

    def initialize_logger(self) -> logging.Logger:
        path = pathlib.Path(os.path.join(os.getcwd(), "logs"))
        path.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger("Server")
        logger.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        fh = logging.FileHandler(filename=f"logs/server.log")
        sh.setLevel(logging.INFO)
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter("[%(asctime)s] :: %(levelname)s :: %(message)s")
        sh.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(sh)
        logger.addHandler(fh)

        return logger

    def start_server(self):
        try:
            self.server = asyncio.start_server(
                    self.accept_client, self.ip, self.port
                    )
            self.loop.run_until_complete(self.server)
            self.loop.run_forever()

        except Exception as exc:
            self.logger.error(exc)
        except KeyboardInterrupt:
            self.logger.warning("Keyboard Interruption. Shutting down!")

    def accept_client(
        self, client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter
    ):
        task = asyncio.Task(self.handle_client(client_reader, client_writer))
        client_ip = client_writer.get_extra_info('peername')[0]
        client_port = client_writer.get_extra_info('peername')[1]

        self.logger.info(f"New connection: {client_ip}:{client_port}")

    async  def handle_client(self, client_reader: asyncio.StreamReader,
                             client_writer: asyncio.StreamWriter):
        while True:
            client_message = str(
                    (await client_reader.read(255)).decode('utf-8')
                    )

            if client_message.startswith("quit"):
                break

            self.logger.info(f"{client_message}")

            await client_writer.drain()

        self.logger.info("Client Disconnected")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(f"Usage: {sys.argv[0]} HOST_IP PORT")

    loop = asyncio.get_event_loop()
    server = Server(sys.argv[1], int(sys.argv[2]), loop)
    server.start_server()
