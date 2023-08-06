import asyncio
import logging
import pathlib
import hashlib

# import datetime
from typing import Tuple
import os
import sys
from Client import Client
from Utils import Order

OrderType = Order


class Server:
    def __init__(self, ip: str, port: int, loop: asyncio.AbstractEventLoop):
        self.__ip = ip
        self.__port = port
        self.__loop = loop
        self.__logger: logging.Logger = self.initialize_logger()
        self.__clients: dict[asyncio.Task, Client] = {}
        self.__orders_with_hash: dict[str, Order] = {}
        self.orders_to_send = asyncio.Queue(maxsize=100)

        self.logger.info(f"Server initialized at {self.ip}:{self.port}")

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

    @property
    def clients(self):
        return self.__clients

    @property
    def orders_with_hash(self):
        return self.__orders_with_hash

    def initialize_logger(self) -> logging.Logger:
        path = pathlib.Path(os.path.join(os.getcwd(), "logs"))
        path.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger("Server")
        logger.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        fh = logging.FileHandler(filename="logs/server.log")
        sh.setLevel(logging.INFO)
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "[%(asctime)s] :: %(levelname)s :: %(message)s"
        )
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

        self.shutdown_server()

    def shutdown_server(self):
        self.logger.info("Shutting down server")
        for client in self.clients.values():
            client.writer.write("quit".encode("utf-8"))

        self.loop.stop()

    def accept_client(
        self,
        client_reader: asyncio.StreamReader,
        client_writer: asyncio.StreamWriter,
    ):
        client = Client(client_reader, client_writer)
        task = asyncio.Task(self.handle_client(client))
        self.clients[task] = client

        client_ip = client_writer.get_extra_info("peername")[0]
        client_port = client_writer.get_extra_info("peername")[1]

        self.logger.info(f"New connection: {client_ip}:{client_port}")
        task.add_done_callback(self.disconnect_client)

    async def handle_client(self, client: Client):
        while True:
            client_message = str(
                (await client.reader.read(255)).decode("utf-8")
            )

            if client_message.startswith("quit"):
                break

            elif client_message.startswith("/"):
                await self.handle_client_command(client, client_message)

            else:
                self.broadcast_message(
                    f"{client.nickname}: {client_message}".encode("utf-8")
                )

            self.logger.info(f"raw message - {client_message}")

            await client.writer.drain()

        self.logger.info("Client Disconnected")

    async def handle_client_command(self, client: Client, client_message: str):
        client_message = client_message.replace("\n", "").replace("\r", "")

        if client_message.startswith("/NICKNAME"):
            split_client_message = client_message.split(" ")
            if len(split_client_message) >= 2:
                client.nickname = split_client_message[1]
                client.writer.write(
                    f"Client name changed to: {client.nickname}\n".encode(
                        "utf-8"
                    )
                )
                return

        elif client_message.startswith("/ADD"):
            # Expect ADD Order(symbol, LONG/SHORT, quantity, price)
            order, is_valid = Server.process_message_with_order(client_message)

            if is_valid:
                hexa_digest = hashlib.md5(
                    order.representation.encode("utf-8")
                ).hexdigest()
                client.writer.write(
                    f"Adding Order\n {order.representation}".encode("utf-8")
                )
                client.writer.write(
                    f"hex digest: {hexa_digest}\n".encode("utf-8")
                )
                self._add_order_with_hash(order, hexa_digest)
                await self._add_order_to_queue(order, hexa_digest)

            # TODO: create Orders object O(1) operations
        elif client_message.startswith("/CANCEL"):
            # Expect CANCEL Order(hash)
            order_hash = Server.process_message_with_hash(client_message)
            order, is_valid = self._remove_order_with_hash(order_hash)

            if is_valid:
                # hexa_digest = hashlib.md5(order.encode("utf-8")).hexdigest()
                client.writer.write(
                    f"Removing Order\n {order.representation}".encode("utf-8")
                )
                await self._remove_order_from_queue(order, order_hash)

    async def _add_order_to_queue(
        self, order: OrderType, hexa_digest: str
    ) -> None:
        await self.orders_to_send.put(order)
        self.logger.info("Added order to queue")

    async def _remove_order_from_queue(
        self, order: OrderType, hexa_digest: str
    ) -> None:
        await self.orders_to_send.get()
        self.logger.info("Order removed from the queue")

    @staticmethod
    def process_message_with_hash(message: str) -> str:
        # Assumes format CANCEL Order(hash)
        split_client_message = message.split("(")
        hash_raw_message = split_client_message[1].split(")")[0]

        order_hash = ""

        if len(hash_raw_message) == 1:
            order_hash = hash_raw_message

        return order_hash

    @staticmethod
    def process_message_with_order(
        message: str,
    ) -> Tuple[OrderType, bool]:
        # Enforces format ADD Order(symbol, LONG/SHORT, quantity, price)
        split_client_message = message.split("(")
        order_raw_message = split_client_message[1].split(")")[0]
        order_raw_data = order_raw_message.split(",")

        is_valid = False
        order = Order()

        if len(order_raw_data) == 4:
            is_valid = True

            symbol = str(order_raw_data[0])
            position_type = str(order_raw_data[1])
            quantity = float(order_raw_data[2])
            price = float(order_raw_data[3])

            order = Order(
                symbol=symbol,
                position=position_type,
                quantity=quantity,
                price=price,
            )

        return order, is_valid

    def _add_order_with_hash(self, order: OrderType, order_hash: str) -> None:
        self.orders_with_hash[order_hash] = order

    def _remove_order_with_hash(
        self, order_hash: str
    ) -> Tuple[OrderType, bool]:
        is_valid = True
        order = Order()
        if order_hash in self.orders_with_hash.keys():
            is_valid = True
            order = self.orders_with_hash[order_hash]

        return order, is_valid

    def broadcast_message(self, message: bytes, exclusion_list: list = []):
        for client in self.clients.values():
            if client not in exclusion_list:
                client.writer.write(message)

    def disconnect_client(self, task: asyncio.Task):
        client = self.clients[task]

        self.broadcast_message(
            f"{client.nickname} left!".encode("utf-8"), [client]
        )

        del self.clients[task]

        client.writer.write("quit".encode("utf-8"))
        client.writer.close()
        self.logger.info("End connection")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(f"Usage: {sys.argv[0]} HOST_IP PORT")

    loop = asyncio.get_event_loop()
    server = Server(sys.argv[1], int(sys.argv[2]), loop)
    server.start_server()
