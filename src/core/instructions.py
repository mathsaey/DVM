# instructions.py
# Mathijs Saey
# dvm prototype

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

"""
This file allows the user to create and retrieve instructions
"""

import copy
import tokens
import runtime
import context

# ---------------- #
# Public functions #
# ---------------- #

""" Creates an instruction and returns it's key """
def addOperationInstruction(operation, inputs): pass
def addFunctionInstruction(inputs, outputs): pass
def addCallInstruction(inputs, outputs): pass

""" Retrieve an instruction with a given key """
def getInstruction(key): pass

# ------------- #
# Key Generator #
# ------------- #

__KEY__ = 1

def getKey():
	global __KEY__
	__KEY__ += 1
	return __KEY__ - 1

# ------------------ #
# Instruction Memory #
# ------------------ #

__INSTRUCTION_MEMORY__ 	= {}

def getInstruction(key):
	return __INSTRUCTION_MEMORY__[key]

def createInstruction(constructor, args):
	key 	= getKey()
	args	= [key] + args
	inst	= constructor(*args)
	__INSTRUCTION_MEMORY__.update({key:inst})
	return key

def addOperationInstruction(operation, inputs):
	return createInstruction(OperationInstruction, [operation, inputs])
def addFunctionInstruction(inputs, outputs):
	return createInstruction(FunctionInstruction, [inputs, outputs])
def addCallInstruction(inputs, outputs):
	return createInstruction(CallInstruction, [inputs, outputs])

# ----------- #
# Instruction #
# ----------- #

class Instruction(object):
	def __init__(self, key, inputs):
		super(Instruction, self).__init__()
		self.key 			= key
		self.tokens			= {}
		self.inputs 		= inputs
		self.outputs 		= []
		self.literals		= [None] * self.inputs

	def __str__(self):
		name = self.__class__.__name__
		return name + " " + "'" + str(self.key) + "'"

	def addDestination(self, port, toKey, toPort):
		self.outputs += [(toKey, toPort)]

	def sendDatum(self, datum):
		for o in self.outputs:
			key 	= o[0]
			port 	= o[1]
			token 	= tokens.Token(key, port, datum, 0)
			runtime.addToken(token)

	def acceptToken(self, token):
		print self, "accepting", token
		cont = token.context

		if token.isLiteral():
			self.acceptLiteral(token)
			return

		try:
			arr = self.tokens[cont]
			arr[token.port] = token
		except KeyError:
			arr = copy.copy(self.literals)
			arr[token.port] = token
			self.tokens.update({cont : arr})

	def isContextComplete(self, context):
		try:
			arr = self.tokens[context]
		except KeyError:
			return False
		else:
			return arr.count(None) == 0

	def acceptLiteral(self, literal):
		self.literals[literal.port] = literal


# --------------------- #
# Operation Instruction #
# --------------------- #

class OperationInstruction(Instruction):
	def __init__(self, key, operation, inputs):
		super(OperationInstruction, self).__init__(key, inputs)
		self.operation = operation

	def acceptToken(self, token):
		super(OperationInstruction, self).acceptToken(token)
		cont = token.context
		if self.isContextComplete(cont):
			self.executeContext(cont)

	def acceptLiteral(self, literal):
		super(OperationInstruction, self).acceptLiteral(literal)
		if self.literals.count(None) == 0:
			self.executeLiterals()

	def execute(self, lst):
		print self, "executing"
		args = map(lambda x : x.datum, lst)
		res = self.operation(*args)
		self.sendDatum(res)		

	def executeContext(self, context):
		lst = self.tokens[context]
		self.execute(lst)

	def executeLiterals(self):
		self.execute(self.literals)

# -------------------- #
# Function Instruction #
# -------------------- #

class FunctionInstruction(Instruction):
	def __init__(self, key, inputs, outputs):
		super(FunctionInstruction, self).__init__(key, inputs)
	
# ---------------- #
# Call Instruction #
# ---------------- #

class CallInstruction(Instruction):
	def __init__(self, key, inputs, outputs):
		super(CallInstruction, self).__init__(key, inputs)
		self.inputKey = None
		self.outputKey = None

	def setTarget(self, key):
		self.key = key	