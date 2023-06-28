#include <cassert>
#include <memory>

#include "customs.hpp"
#include "limits.cpp"
#include "utils.cpp"

// convenient functions for testing
// TODO remove utils depedency with an adequate header
//

// creates limit struct pointer
std::shared_ptr<Limit> createDummyLimit(float price) {
    auto ptr_limit = std::make_shared<Limit>();
    initializeLimit(ptr_limit);
    ptr_limit->limitPrice = price;

    return (ptr_limit);
};

// creates tree structure
std::shared_ptr<Limit> createDummyTree(std::shared_ptr<Limit> dummyA,
                                       std::shared_ptr<Limit> dummyB,
                                       std::shared_ptr<Limit> dummyC,
                                       std::shared_ptr<Limit> dummyD) {
    int statusCode = 0;
    auto ptr_root = createRoot();
    statusCode = addLimit(ptr_root, dummyA);
    assert(statusCode == 1);
    statusCode = addLimit(ptr_root, dummyB);
    assert(statusCode == 1);
    statusCode = addLimit(ptr_root, dummyC);
    assert(statusCode == 1);
    statusCode = addLimit(ptr_root, dummyD);
    assert(statusCode == 1);
};

// asserting on equality of Limit structures
void AssertPtrEquals(std::shared_ptr<Limit> ptr_firstLimit,
                     std::shared_ptr<Limit> ptr_secondLimit){};

// test dummy tree
void TestCreateDummyTree() {
    std::shared_ptr<Limit> ptr_limitA = createDummyLimit(100.0);
    std::shared_ptr<Limit> ptr_limitB = createDummyLimit(200.0);
    std::shared_ptr<Limit> ptr_limitC = createDummyLimit(20.0);
    std::shared_ptr<Limit> ptr_limitD = createDummyLimit(50.0);

    std::shared_ptr<Limit> ptr_root =
        createDummyTree(ptr_limitA, ptr_limitB, ptr_limitC, ptr_limitD);

    // TODO assert equality of pointers information between tree and limits
    AssertPtrEquals(ptr_limitA, ptr_root->rightChild);
    AssertPtrEquals(ptr_limitC, ptr_limitA->leftChild);
};

// test on pushing
void TestOrderPushing(){};
