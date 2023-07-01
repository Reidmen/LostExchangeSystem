#include "test.hpp"

#include <cassert>
#include <memory>

#include "customs.hpp"
#include "limits.hpp"
#include "orders.cpp"
#include "utils.cpp"

// convenient functions for testing
// TODO remove utils depedency with an adequate header

// creates limit struct pointer
std::shared_ptr<Limit> createDummyLimit(float price) {
    auto ptr_limit = std::make_shared<Limit>();
    initializeLimit(ptr_limit);
    ptr_limit->limitPrice = price;

    return (ptr_limit);
}

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
}

// asserting on equality on the Limit structures
void AssertPtrLimit(std::shared_ptr<Limit> ptr_firstLimit,
                    std::shared_ptr<Limit> ptr_secondLimit) {
    assert(ptr_firstLimit->limitPrice == ptr_secondLimit->limitPrice);
    assert(ptr_firstLimit->size == ptr_secondLimit->size);
    assert(ptr_firstLimit->totalVolume == ptr_secondLimit->totalVolume);
    assert(ptr_firstLimit->orderCount == ptr_secondLimit->orderCount);
    AssertPtrOrder(ptr_firstLimit->headOrder, ptr_secondLimit->headOrder);
    AssertPtrOrder(ptr_firstLimit->tailOrder, ptr_secondLimit->tailOrder);
}

void AssertPtrOrder(std::shared_ptr<Order> ptr_firstOrder,
                    std::shared_ptr<Order> ptr_secondOrder) {
    assert(ptr_firstOrder->shares == ptr_secondOrder->shares);
    assert(ptr_firstOrder->price == ptr_secondOrder->price);
    assert(ptr_firstOrder->limit == ptr_secondOrder->limit);
}

// test dummy tree
void TestCreateDummyTree() {
    std::shared_ptr<Limit> ptr_limitA = createDummyLimit(100.0);
    std::shared_ptr<Limit> ptr_limitB = createDummyLimit(200.0);
    std::shared_ptr<Limit> ptr_limitC = createDummyLimit(20.0);
    std::shared_ptr<Limit> ptr_limitD = createDummyLimit(50.0);

    std::shared_ptr<Limit> ptr_root =
        createDummyTree(ptr_limitA, ptr_limitB, ptr_limitC, ptr_limitD);

    // TODO assert equality of pointers information between tree and limits
    AssertPtrLimit(ptr_limitA, ptr_root->rightChild);
    AssertPtrLimit(ptr_limitC, ptr_limitA->leftChild);
}

// test on pushing
void TestOrderPushing() {
    // pushes an order to an empty limit
    // checks that head and tail point to it
    std::shared_ptr<Limit> ptr_limit = createDummyLimit(100.0);

    auto ptr_newOrderA = std::make_shared<Order>();

    initializeOrder(ptr_newOrderA);
    ptr_newOrderA->limit = 1000.0;
    ptr_newOrderA->shares = 10;
    ptr_newOrderA->buyOrSell = 0;
    ptr_newOrderA->id = "1234";

    float expectedVolume = 0.0;
    float expectedSize = 0;
    int expectedOrderCount = 0;
    int returnCode = 0;

    returnCode = pushOrder(ptr_limit, ptr_newOrderA);
    assert(returnCode == 1);

    // assert references are correctly updated
    AssertPtrOrder(ptr_limit->headOrder, ptr_limit->tailOrder);
    AssertPtrOrder(ptr_limit->headOrder, ptr_newOrderA);
    AssertPtrOrder(ptr_limit->tailOrder, ptr_newOrderA);
    AssertPtrLimit(ptr_limit, ptr_limit->tailOrder->parentLimit);

    // assert attributes of limits are correctly updated
    assert(ptr_limit->totalVolume == 1000.0);
    assert(ptr_limit->size == 10.0);
    assert(ptr_limit->orderCount == 1);
    // update counters on scope
    expectedVolume = ptr_limit->totalVolume;
    expectedSize = ptr_limit->size;
    expectedOrderCount++;

    // Push another order and assert correct update of head/tail
    auto ptr_newOrderB = std::make_shared<Order>();

    initializeOrder(ptr_newOrderB);
    ptr_newOrderA->limit = 1000.0;
    ptr_newOrderA->shares = 20;
    ptr_newOrderA->buyOrSell = 0;
    ptr_newOrderA->id = "1235";

    returnCode = pushOrder(ptr_limit, ptr_newOrderB);

    // assert references are correctly updated
    AssertPtrOrder(ptr_newOrderB, ptr_limit->headOrder);
    AssertPtrOrder(ptr_newOrderA, ptr_limit->tailOrder);
    AssertPtrLimit(ptr_limit, ptr_limit->tailOrder->parentLimit);
    AssertPtrLimit(ptr_limit, ptr_limit->tailOrder->parentLimit);
    AssertPtrOrder(ptr_newOrderA, ptr_limit->headOrder->nextOrder);
    assert(ptr_limit->headOrder->prevOrder == NULL);
    assert(ptr_limit->tailOrder->nextOrder == NULL);
    // assert ptr equality
    assert(ptr_newOrderB == ptr_limit->tailOrder->prevOrder);
    // assert attributes of limits are correctly updated
    assert(ptr_limit->totalVolume == 3000.0);
    assert(ptr_limit->size == 30.0);
    assert(ptr_limit->orderCount == 2);
}
