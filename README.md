# LostExchangeSystem
A practical Stock Exchange System

## Ideas

* Introduce the Account, Member and Order classes that define a brokage system.
* Use python for high-level implementation of them. 
* Expand them into cpp for low-latency cases.


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



