#include "limits.hpp"

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

    return ptr_limit;
}

int addLimit(std::shared_ptr<Limit> root, std::shared_ptr<Limit> limit) {
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

void replaceLimitInParent(std::shared_ptr<Limit> limit,
                          std::shared_ptr<Limit> newLimit) {
    // pop the given limit and replace all pointers to it from limit->parent
    // to the newLimit
    if (!limitIsRoot(limit)) {
        if (limit == limit->parent->leftChild && !limitIsRoot(limit->parent)) {
            limit->parent->leftChild = newLimit;
        } else {
            limit->parent->rightChild = newLimit;
        }
    }
    if (newLimit != NULL) {
        newLimit->parent = limit->parent;
    }
};

int removeLimit(std::shared_ptr<Limit> limit) {
    // remove the given limit from the tree it belongs to
    // It assumes it is part of the tree
    if (!hasGrandparent(limit) && limitIsRoot(limit)) {
        return 0;
    }

    std::shared_ptr<Limit> ptr_successor = limit;
    if (limit->leftChild != NULL && limit->rightChild != NULL) {
        // limit with two children
        ptr_successor = getMinimumLimit(limit->rightChild);
        std::shared_ptr<Limit> parent = ptr_successor->parent;
        std::shared_ptr<Limit> leftChild = ptr_successor->leftChild;
        std::shared_ptr<Limit> rightChild = ptr_successor->rightChild;

        if (limit->leftChild != ptr_successor) {
            ptr_successor->leftChild = limit->leftChild;
        } else {
            ptr_successor->leftChild = NULL;
        }

        if (limit->rightChild != ptr_successor) {
            ptr_successor->rightChild = limit->rightChild;
        } else {
            ptr_successor->rightChild = NULL;
        }

        limit->leftChild = leftChild;
        limit->rightChild = rightChild;
        ptr_successor->parent = limit->parent;

        if (ptr_successor->parent->rightChild == limit) {
            ptr_successor->parent->rightChild = ptr_successor;
        } else if (ptr_successor->parent->leftChild == limit) {
            ptr_successor->parent->leftChild = ptr_successor;
        }
        limit->parent = parent;

        removeLimit(parent);

    } else if (limit->leftChild != NULL && limit->rightChild == NULL) {
        // limit has only left child
        replaceLimitInParent(limit, limit->leftChild);
    } else if (limit->rightChild != NULL && limit->leftChild == NULL) {
        // limit has only right child
        replaceLimitInParent(limit, limit->rightChild);
    } else {
        // limit has no children
        replaceLimitInParent(limit, NULL);
    }
    return 1;
};
