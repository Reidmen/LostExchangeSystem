#include "customs.hpp"
#include "test.cpp"
#include <iostream>

int main(int argc, char* argv[]) {
    std::cout << "Running dummy order pushing test" << std::endl;
    TestOrderPushing();
    std::cout << "Running dummy order popping test" << std::endl;
    TestOrderPopping();
    std::cout << "Running dummy tree test" << std::endl;
    TestCreateDummyTree();
    return 0;
};
