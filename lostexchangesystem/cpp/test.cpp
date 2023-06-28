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
