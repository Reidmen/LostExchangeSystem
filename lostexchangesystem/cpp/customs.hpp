#ifndef CUSTOMS_H
#define CUSTOMS_H

struct OrderNode {
    struct OrderNode *prev;
    struct OrderNode *next;
    char32_t *id;
};

struct LimitNode {
    struct LimitNode *parent;
    struct LimitNode *leftChild;
    struct LimitNode *rightChild;
};

typedef OrderNode OrderNode;
typedef LimitNode LimitNode;

struct Order {
    char32_t *id;
    unsigned buyOrSell;
    double shares;
    OrderNode *orderNode;
    LimitNode *parentLimit;
};

struct Limit {
    double limitPrice;
    double price;
    double totalVolume;
    int orderCount;
    LimitNode *limitNode;
    Order *headOrder;
    Order *tailOrder;
};

typedef Limit Limit;

struct QueueItem {
    Limit *limit;
    struct QueueItem *previous;
};

typedef QueueItem QueueItem;

struct Queue {
    int size;
    QueueItem *head;
    QueueItem *tail;
};

#endif
