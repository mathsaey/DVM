# callnode.py
# Mathijs Saey
# dvm prototype

# The MIT License (MIT)
#
# Copyright (c) 2013 Mathijs Saey
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
This module contains the nodes used to call functions
"""

from executablenode import ExecutableNode
import runtime
import edge
import port

class CallNode(ExecutableNode):

	def __init__(self, inputs, outputs):
		super(CallNode, self).__init__(inputs, outputs)
		self.fillList(self.inputs, port.OutputPort)
		self.fillList(self.outputs, port.OutputPort)
		self.inputs[0] = port.InputPort(self, 0)

	def __str__(self):
		id = super(CallNode, self).__str__()
		return "CallNode: (" + id + ")"

	def getInput(self, idx):
		return self.getFromList(self.inputs, port.OutputPort, idx)
	def getOutput(self, idx):
		return self.getFromList(self.outputs, port.OutputPort, idx)

	def receiveInput(self, idx):
		if idx is 0:
			self.addToScheduler()

	def execute(self):
		super(CallNode, self).execute()
		key = self.inputs[0].value()
		func = runtime.pool.getFunction(key)
		for idx in xrange(0,len(func.outputs)):
			src = func.getOutput(idx)
			dst = self.getOutput(idx)
			edge.Edge(src, dst)
		for idx in xrange(0,len(func.inputs)):
			src = self.getInput(idx + 1)
			dst = func.getInput(idx)
			edge.Edge(src, dst)
