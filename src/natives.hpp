// natives.hpp
// DVM
// Mathijs Saey

/*
 * The MIT License (MIT)
 * 
 * Copyright (c) 2014 Mathijs Saey
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

/**
 * \file natives.hpp
 * \author Mathijs Saey
 *
 * \brief DVM Natives
 * 
 * This module defines all of the native
 * DVM operations and types.
 */

#ifndef __DVM_NATIVES_HPP__
#define __DVM_NATIVES_HPP__

#include <string>
#include <vector>
#include <boost/variant.hpp>

typedef int dvm_int;

typedef bool dvm_bool;

typedef float dvm_float;

typedef std::string dvm_string;

typedef boost::variant<dvm_int, dvm_bool, dvm_float, dvm_string> Datum;

#endif