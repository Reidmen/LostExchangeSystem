#ifndef CUSTOMS_H
#define CUSTOMS_H

#include <memory>
typedef struct Order {
    std::shared_ptr<char32_t> id;
    unsigned buyOrSell;
    double shares;
    double price;
    double limit;
    std::shared_ptr<struct Order> nextOrder;
    std::shared_ptr<struct Order> prevOrder;
    std::shared_ptr<struct Limit> parentLimit;
} Order;

typedef struct Limit {
    double limitPrice;
    double size;
    double totalVolume;
    int orderCount;
    std::shared_ptr<Limit> parent;
    std::shared_ptr<Limit> leftChild;
    std::shared_ptr<Limit> rightChild;
    std::shared_ptr<Order> headOrder;
    std::shared_ptr<Order> tailOrder;
} Limit;

typedef struct QueueItem {
    std::shared_ptr<Limit> limit;
    struct QueueItem *prevItem;
} QueueItem;

typedef struct Queue {
    int size;
    std::shared_ptr<QueueItem> head;
    std::shared_ptr<QueueItem> tail;
} Queue;

#endif
