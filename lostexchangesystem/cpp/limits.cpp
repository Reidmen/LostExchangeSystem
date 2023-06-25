#include <math.h>

#include <memory>

#include "customs.hpp"
#include "utils.cpp"

std::shared_ptr<Limit> createRoot() {
    // Create a Limit structure as root and return ptr
    // using make_shared instead of malloc(sizeof(Limit))
    std::shared_ptr<Limit> ptr_limit = std::make_shared<Limit>();
    initializeLimit(ptr_limit);
    ptr_limit->limitPrice = -INFINITY;
}

int addNewLimit(std::shared_ptr<Limit> root, std::shared_ptr<Limit> limit) {
    // add new Limit structure to a given limit tree
    if (limitExists(root, limit) == 1) {
        return 0;
    }

    limit->leftChild = NULL;
    limit->rightChild = NULL;

    std::shared_ptr<Limit> currentLimit = root;
    std::shared_ptr<Limit> child;

    while (1) {
        if (currentLimit->limitPrice < limit->limitPrice) {
            if (currentLimit->rightChild == NULL) {
                currentLimit->rightChild = limit;
                limit->parent = currentLimit;
                return 1;
            } else {
                currentLimit = currentLimit->rightChild;
            }
        } else if (currentLimit->limitPrice > limit->limitPrice) {
            if (currentLimit->leftChild == NULL) {
                currentLimit->leftChild = limit;
                limit->parent = currentLimit;
                return 1;
            } else {
                currentLimit = currentLimit->leftChild;
            }

        } else {
            // if not bigger nor smaller, then it is equal
            break;
        }
        continue;
    }

    return 0;
}
