#include <memory>

#include "customs.hpp"

void initializeOrder(std::shared_ptr<Order> order) {
    order->id = NULL;
    order->buyOrSell = -1;
    order->shares = 0;
    order->limit = 0;
    order->nextOrder = NULL;
    order->prevOrder = NULL;
    order->parentLimit = NULL;
};

void initializeLimit(std::shared_ptr<Limit> limit) {
    limit->limitPrice = 0;
    limit->size = 0;
    limit->totalVolume = 0;
    limit->orderCount = 0;
    limit->parent = NULL;
    limit->leftChild = NULL;
    limit->rightChild = NULL;
    limit->headOrder = NULL;
    limit->tailOrder = NULL;
};

int limitExists(std::shared_ptr<Limit> root, std::shared_ptr<Limit> limit) {
    // check if the given price level exists in the given limit tree (root)
    if (root->parent == NULL && root->rightChild == NULL) {
        return 0;
    }

    std::shared_ptr<Limit> currentLimit = root;

    while (currentLimit->limitPrice != limit->limitPrice) {
        if (currentLimit->leftChild == NULL &&
            currentLimit->rightChild == NULL) {
            return 0;
        } else {
            if (currentLimit->rightChild != NULL &&
                currentLimit->limitPrice < limit->limitPrice) {
                currentLimit = currentLimit->rightChild;
            } else if (currentLimit->leftChild != NULL &&
                       currentLimit->limitPrice > limit->limitPrice) {
                currentLimit = currentLimit->leftChild;
            } else {
                return -1;
            }
            continue;
        }
    }
    return 1;
};
