#ifndef UTILS_H
#define UTILS_H

#include "customs.hpp"
#include <memory>

void initializeOrder();

void initializeLimit();

int limitExists();

int hasGrandparent();

bool limitIsRoot();

std::shared_ptr<Limit> getMinimumLimit();

#endif
