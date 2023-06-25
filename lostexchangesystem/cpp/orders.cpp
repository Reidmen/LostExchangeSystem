#include <memory>

#include "customs.hpp"

int pushOrder(std::shared_ptr<Limit> limit, std::shared_ptr<Order> newOrder) {
    // Add newOrder to the limit structure head
    if (limit->limitPrice != newOrder->limit) {
        return 0;
    }
    newOrder->parentLimit = limit;
    newOrder->nextOrder = limit->headOrder;
    newOrder->prevOrder = NULL;

    if (limit->headOrder != NULL) {
        limit->headOrder->prevOrder = newOrder;
    } else {
        limit->tailOrder = newOrder;
    };

    limit->headOrder = newOrder;
    limit->orderCount++;
    limit->size += newOrder->shares;
    limit->totalVolume += (newOrder->shares * limit->limitPrice);

    return 1;
};

std::shared_ptr<Order> popOrder(std::shared_ptr<Limit> limit) {
    // Pop the order at the tail of the Limit structure
    if (limit->tailOrder == NULL) {
        return NULL;
    };
    std::shared_ptr<Order> ptr_poppedOrder = limit->tailOrder;

    if (limit->tailOrder->prevOrder != NULL) {
        limit->tailOrder = limit->tailOrder->prevOrder;
        limit->tailOrder->nextOrder = NULL;
        limit->orderCount--;
        limit->size -= ptr_poppedOrder->shares;
        limit->totalVolume -= ptr_poppedOrder->shares * limit->limitPrice;
    } else {
        limit->headOrder = NULL;
        limit->tailOrder = NULL;
        limit->orderCount = 0;
        limit->size = 0;
        limit->totalVolume = 0;
    };

    return ptr_poppedOrder;
};

int removeOrder(std::shared_ptr<Order> order) {
    // remove there where it is at (head, tail, or in between)
    if (order->parentLimit->headOrder == order && order->parentLimit->tailOrder == order) {
        // head and tail are identicall, set them NULL
        order->parentLimit->headOrder = NULL;
        order->parentLimit->tailOrder = NULL;
    }
    else if (order->prevOrder != NULL && order->nextOrder != NULL) {
        // order is in between
        order->prevOrder->nextOrder = order->nextOrder;
        order->nextOrder->prevOrder = order->prevOrder;
    }
    else if (order->nextOrder == NULL && order->parentLimit->tailOrder == order) {
        // order is at tail, replace tail order with previous order
        order->prevOrder->nextOrder = NULL;
        order->parentLimit->tailOrder = order->prevOrder;
    }
    else if (order->prevOrder == NULL && order->parentLimit->headOrder == order) {
        // order is at head, replace head with next order
        order->nextOrder->prevOrder = NULL;
        order->parentLimit->headOrder = order->nextOrder;
    } else {
        // if none of the cases above, there is a problem 
        return -1;
    }

    return 1;
};
