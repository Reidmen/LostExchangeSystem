![CodeBase](https://progress-bar.dev/21/?title=Codebase)
![MIT](https://img.shields.io/badge/License-MIT-green)
![Black](https://img.shields.io/badge/Style-Black-black)
# LostExchangeSystem
A Lost Stock Exchange System trying to find its way back!
Implements a Server/Client protocol for creating orders and storing them in an efficient way.
As a toy example, its purpose is for learning the mechanism of book keeping.

## Run Server 
To run a server, you must specify the host ip address and the port. To execute it
on the localhost `127.0.0.1` with port `10001`, use:
```shell
cd lostexchangesystem/
python3 Server.py 127.0.0.1 10001 
```

## Interaction
We assume the server is running in the local host `127.0.0.1` and port `10001`.
In order to interact with the server, use:
```shell
nc 127.0.0.1 10001
```

### Add Orders
Orders can be added to the queue by using the add method.
To add an order, e.g. 10 long on APPL at strike price $130, use:
```shell
/ADD Order(APPL, LONG, 10, 130.0) 
```

The server will prompt a digested hash of the order information, useful to cancel it.

### Cancel Orders 
Order can be removed from the queue by using the cancel method.
To cancel an order its enough to specify the hash, use (example hash):
```shell
/CANCEL Order(0ecbb9115ef1380b2f7194f84d38a776)
```

## Ideas

* Introduce the Account, Member and Order classes that define a brokage system.
* Use python for high-level implementation of them. 
* Overview of the Exchange system is provided in the `lostexchangesystem/` folder.
* Use c++ for implementation of the order book, and pybind11 for python usage.
* Other attempts will be given in `ideas/` folder.


## How to build a Fast Limit Order Book 

> The Nasdaq TotalView ITCH feed, which is every event in every instrument traded
 in the Nasdaq, can have data rates of 20+ GB/day with spikes of 3 MB/sec or more.
 Each message averages about 20 bytes each so this means handling
 100,000 - 200,000 messsages per second during high volume
 periods [ref](https://web.archive.org/web/20110219155647/http://howtohft.wordpress.com/author/howtohft/).

A (fast) limit order book must implement three primary functions.

1. Add: Places order at the end of a list or orders to be 
    executed a limit price.

2. Cancel: Remove an arbitrary order.

3. Execute: Remove an order from the inside of the book, *inside* meaning
    the oldest buy at highest price and oldest sell and lowest price.

> These operations should be implemented in $O(1)$ time while making it
 possible for the trading model to efficiently ask questions lie
 *what are the best bid and offer?* or *what is order x's current position?*.


# Python style
- [Black](https://github.com/psf/black)
- [PEP8](https://peps.python.org/pep-0008/)
- [Google Python Style](https://google.github.io/styleguide/pyguide.html)

Under MIT License
