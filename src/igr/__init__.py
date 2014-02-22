# __init__.py
# Mathijs Saey
# dvm

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
# \file igr/__init__.py
# \package IGR
# \author Mathijs Saey
# 
# \brief DVM Intermediate Graph Representation
#
# This python module contains the DVM intermediate form, called 
# Intermediate Graph Representation (IGR).
#
# This form is produced by the parser and is the target of some
# optimizations. 
# 
# This module should be considerd a stable frontend of the module,
# external modules (such as parsers) should only use these functions
# to create and modify the IGR.
#
# \todo 
#		General structure should remain the same
#		Operation lifting will be different with own
#		instructions.
#		Various new node types to make compounds work on a low level
##

import node
import graph
import literal
import subgraph

# ----- #
# Graph #
# ----- #
## \name Graph
## \{

##
# Get a list of all the non-compound subgraphs
# in the program.
#
# \return 
#	 	All the non compound subgraphs in the program.
## 
def getSubGraphs(): 
	return graph.getSubGraphs()

##
# Get a subgraph by name.
#
# \param name
#		The name of the subgraph 
# 		we want to retrieve.
# \return
#		The subgraph
##

def getSubGraph(name):
	return graph.getSubGraph(name)

##\}

# --------- #
# SubGraphs #
# --------- #
## \name Subgraphs
## \{

##
# Create a new subgraph
#
# \param inputs
#		The amount of inputs the subgraph accepts
# \param outputs
# 		The amount of data the subgraph returns
# \return
# 		The subgraph. It's entry and exit fields
#		should be used to access parameters and
#		return values of this subgraph.
#
def createGeneralSubGraph(name , inputs, outputs):
	subGraph = subgraph.SubGraph(None, None, name)
	entry = node.SubGraphEntryNode(subGraph, inputs)
	exit  = node.SubGraphExitNode(subGraph, outputs)
	subGraph.entry = entry
	subGraph.exit = exit
	subGraph.addNode(entry)
	subGraph.addNode(exit)
	return subGraph

##
# Create a subgraph and add it to the program graph.
##
def createSubGraph(name, inputs, outputs):
	subGraph = createGeneralSubGraph(name, inputs, outputs)
	graph.addSubGraph(subGraph)
	graph.bindName(subGraph)
	return subGraph
 
##
# Create a subgraph for a compound node.
##
def createCompoundSubGraph():
	return createGeneralSubGraph(None, 0, 0)

##\}

# ----- #
# Nodes #
# ----- #
## \name Nodes
## \{

##
# Create a node, add it to it's subgraph
# and return it.
#
# \param constructor
#		The constructor to create the node.
# \param subGraph
#		The subgraph that contains this node.
# \param arguments
#		The arguments to pass to the constructor
#		(not including the subgraph)
##
def createNode(constructor, subGraph, arguments = []):
	args = [subGraph] + arguments
	node = constructor(*args)
	subGraph.addNode(node)
	return node

##
# Create an operation node
#
# \param subGraph
#		The subGraph that this node is part of
#
# \param operation
#		The operation that this node performs
##
def createOperationNode(subGraph, operation):
	return createNode(node.OperationNode, subGraph, [operation])

##
# Create a Compound node
#
# \param constructor
#		The constructor of the compound node to use
# \param subGraph
#		The subgraph this node belongs too
# \param subGraphss
#		The subgraphs that are part of this compound node
##
def createCompoundNode(constructor, subGraph, subGraphs):
	return createNode(constructor, subGraph, [subGraphs])

##
# Create a call node.
#
# \param subGraph
# 		the subgraph this node belongs to
# \param inputs
#		the amount of inputs this 
##
def createCallNode(subGraph):
	return createNode(node.CallNode, subGraph)

##\}

# ---------------- #
# Edges & Literals #
# ---------------- #
## \name Edges and Literals
## \{

##
# Add a literal to a port.
#
# \param value
#		The value of the literal
# \param dstNode
#		The node that the literal targets
# \param dstPort
#		The idx of the port on this node
##
def addLiteral(value, dstNode, dstPort):
	dest = dstNode.getInputPort(dstPort)
	lit = literal.Literal(value, dest)
	dest.attach(lit)

##
# Connect 2 ports with an implicit edge.
#
# \param srcNode
#		The node that provides data
# \param srcPort
#		The idx of the output port on src
# \param dstNode
#		The node that accepts the data
# \param dstPort
#		The idx of the port on dst that accepts the data.
##
def connect(srcNode, srcPort, dstNode, dstPort):
	srcP = srcNode.getOutputPort(srcPort)
	dstP = dstNode.getInputPort(dstPort)
	srcP.addTarget(dstP)
	dstP.attach(srcP)

## \}