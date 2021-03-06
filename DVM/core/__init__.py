# __init__.py
# Mathijs Saey
# DVM

# The MIT License (MIT)
#
# Copyright (c) 2013, 2014 Mathijs Saey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

##
# \package core
# \brief Dataflow Virtual Machine
# 
# This is the core of DVM. It contains the code that is necessary
# to execute the program in instruction memory.
#
# This top level namespace also declares some convenience functions
# to control the instruction memory and runtime.
##

import instruction
import runtime
import memory

##
# Create an instruction and add it to memory.
# 
# \param constructor
#		The instruction constructor
# \param argLst
#		The arguments to pass to the constructor.
#		The exact sructure of this list depends on the
#		instruction type.
#
# \return 
#		The key of the newly added instruction.
##
def _addInstruction(constructor, argLst = []):
	inst = constructor(*argLst)
	return memory.add(inst)

## 
# Add an operation instruction.
#
# \param op
#		The operation of this instruction.
# \param inputs
#		The amount of inputs this instruction
#		will accept.
#
# \return
#		The key of the operation instruction.
##
def addOperationInstruction(op, inputs):
	return _addInstruction(
		instruction.OperationInstruction,
		[op, inputs])

##
# Add a constant instruction.
#
# \param value
#		The value the constant should return.
#
# \return 
#		The key of the constant instruction.
## 
def addConstant(value):
	return _addInstruction(instruction.Constant, [value])

##
# Add a sink instruction.
#
# \return
#		The key of the sink instruction.
##
def addSink():
	return _addInstruction(instruction.Sink)

##
# Create a switch instruction.
# 
# \param dstList
#		The list of the possible destinations.
#
# \return 
#		The key of the switch instruction.
##
def addSwitch(dstList):
	return _addInstruction(instruction.Switch, [dstList])

##
# Add a context change instruction.
#
# \param binds
#		The amount of tokens to bind to a new
#		context.
# \param restores
#		The amount of tokens the context will
#		produce before being deleted.
# \param destSink
#		The destination of the token after
#		the context change.
# \param retSink
#		The destination of the token
#		after the context restore.
#
# \return 
#		The key of the context change instruction.
##
def addContextChange(binds, restores, destSink, retSink):
	return _addInstruction(
		instruction.ContextChange,
		[binds, restores, destSink, retSink])

##
# Add a split instruction.
#
# \param binds
#		The amount of inputs that the split will take.
#		A split should always take at least one argument,
#		which is the array that will be split.
# \param dest
#		The destination of the tokens after
#		the context change.
# \param merge
#		The instruction that will recreate
#		the array after the contextrestore.
# \return
#		The key of the context map instruction.
##
def addSplit(binds, dest, merge):
	return _addInstruction(
		instruction.Split,
		[binds, dest, merge])

##
# Add a context restore instruction.
#
# \return 
#		The key of the context restore instruction.
##
def addContextRestore():
	return _addInstruction(instruction.ContextRestore)

##
# Add a stop instruction.
#
# \return
#		The key of the stop instruction.
##
def addStopInstruction():
	return _addInstruction(instruction.StopInstruction)

##
# Add a destination to a given instruction.
#
# This only works on instruction::OperationInstruction 
# and on instruction::Sink
#
# \param srcKey
#		The key of the from instruction.
# \param srcPort
#		The index of the from port.
# \param dstKey
#		The key of the destination instruction.
# \param dstPort
#		The index of the destination port.
##
def addDestination(srcKey, srcPort, dstKey, dstPort):
	inst = memory.get(srcKey)
	inst.addDestination(srcPort, dstKey, dstPort)

##
# Add a literal to a given instruction.
#
# This only works on instruction::OperationInstruction
# and on instruction:ContextChangeInstruction
##
def addLiteral(key, port, val):
	inst = memory.get(key)
	inst.addLiteral(port, val)

##
# Start the execution cores.
#
# \see runtime::init()
##
def start(cores): runtime.start(cores)

##
# Add an external token containing data.
#
# \see runtime::addData()
##
def addData(data): runtime.addData(data)

##
# Add data to the core, that immediately 
# adds a stop token containing data.
#
# This can be used if the program does not require
# any user input. 
#
# \see runtime::addTrivial()
##
def addTrivial(data): runtime.addTrivial(data)

##
# Check the current port of the runtime.
##
def getPort():
	return runtime.__port__

##
# Return the amount of input the
# runtime requires.
##
def getIn():
	return runtime.__in__

##
# Set the amount of inputs that the 
# runtime expects.
##
def setIn(i):
	runtime.__in__ = i

##
# See if the runtime expects additional input.
#
# \return
# 		True if the runtime has received all the
#		required data.
##
def hasIn(): 
	return getPort() >= getIn()
