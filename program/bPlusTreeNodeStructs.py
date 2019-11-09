'''
Author : Advait Trivedi
MUN # : 201892202
Description : This file contains B+ Tree Data Structures to help with building an actual B+ Tree. They are used further in buildTree.py
'''

import copy, random

class SingleNode:
    prev = ""
    prevPtr = None
    val = ""
    nextPtr = None
    next = ""
    dataFilePtr = []

    def __init__(self, value):
        self.dataFilePtr = []
        self.val = value

    def changeValue(self, value):
        self.val = value

    def assignPrevNextPtrs(self, prevNode, nextNode):
        self.prevPtr = prevNode
        self.nextPtr = nextNode

    def __gt__(self, other):
        if(self.val > other.val): 
            return True
        else: 
            return False

    def __lt__(self, other):
        if(self.val < other.val): 
            return True
        else: 
            return False

    def __eq__(self, other):
        if(self.val == other.val): 
            return True
        else: 
            return False

    def __repr__(self):
        return "< prev : "+ ("nil" if self.prevPtr == None else hex(id(self.prevPtr))) + " | val : " + str(self.val) + " | data file pointers : " + str(self.dataFilePtr) +" | next : " + ("nil" if self.nextPtr == None else hex(id(self.nextPtr))) + ">\n"


class TreeNode:
    name = ""
    order = 0
    parentLabel = ""
    parentPtr = None
    isLeaf = True
    valueStruct = []
    left = ""
    right = ""
    leftPtr = None
    rightPtr = None
    ptrToSelf = None

    def __init__(self, parentLabel, parentPtr, order, name):
        self.name = name
        self.parentLabel = parentLabel
        self.parentPtr = parentPtr
        self.order = order
        self.valueStruct = []
        self.ptrToSelf = hex(id(self))

    def __repr__(self):
        a = "<\nSelf-Addr : " + self.name + " - " + self.ptrToSelf +" ;\nParent : "+ ('nil' if self.parentPtr is None else self.parentLabel + "-" + hex(id(self.parentPtr)))+ (" ;\nLeaf : "+str(self.isLeaf)+" ;\nLeft : "+ hex(id(self.leftPtr)) +" ;\nRight : "+ hex(id(self.rightPtr)) +" ;\n" if self.isLeaf else "") +";\nValues : \n\t" + "\t".join(map(str, self.valueStruct)) + ">"
        return a

    def insertValueAtIndex(self, index, value):
        if not self.isFull():
            self.valueStruct.insert(index, value)
            return True
        else:
            return False

    def insertValueAtEnd(self, value):
        if not self.isFull():    
            node = SingleNode(value)
            self.valueStruct.append(node)
        else:
            return False

    def insertNodeAtEnd(self, node):
        if not self.isFull():
            self.valueStruct.append(node)
        else:
            return False

    def attachNodesAtIndex(self, index, prevTreeNodePtr, nextTreeNodePtr):
        self.valueStruct[index].assignPrevNextPtrs(
            prevTreeNodePtr, nextTreeNodePtr)

    def isFull(self):
        if len(self.valueStruct) == 2 * self.order:
            return True
        return False

    def setParent(self, parentPtr):
        self.parentPtr = parentPtr

    def checkAgainstValuesWithNode(self, node):
        for index, each in enumerate(self.valueStruct):
            if node < each:
                return index - 1
        return 2 * self.order

    def doesNodeFitInThisTreeNode(self, node):
        ret = self.checkAgainstValuesWithNode(node)
        if self.isFull() and (ret < 0):
            return "left"
        elif self.isFull() and not ret<2*self.order:
            return "right"
        else:
            return "this"

# builder functions

def traverseRightUntilLeaf(treeNode):
    if treeNode.isLeaf:
        return treeNode
    elif treeNode.valueStruct[-1].nextPtr is None:
        return treeNode
    else:
        return traverseRightUntilLeaf(treeNode.valueStruct[-1].nextPtr)


def splitInHalfAndInsert(treeNode, node, tree_node_list):
    # create new nodes with NO parent
    leftTreeNode = TreeNode("", None, treeNode.order, "")
    rightTreeNode = TreeNode("", None, treeNode.order, "")

    # assign node values down to the left and right stuff
    leftTreeNode.valueStruct[:leftTreeNode.order] = copy.copy(treeNode.valueStruct[:treeNode.order])
    rightTreeNode.valueStruct[:rightTreeNode.order] = copy.copy(treeNode.valueStruct[treeNode.order:])

    # insert new value into the right child
    # this will essentially also be the value copied to the parent
    rightTreeNode.insertNodeAtEnd(node)

    if treeNode.isLeaf:
        # set the leaf status of all the concerned nodes in this loop and function
        treeNode.isLeaf = False
        leftTreeNode.isLeaf = True
        rightTreeNode.isLeaf = True

        # Set left and right for the leaf
        if treeNode.leftPtr is not None:
            treeNode.leftPtr.rightPtr = leftTreeNode # only the left because we are inserting a sorted list?

        leftTreeNode.rightPtr = rightTreeNode
        leftTreeNode.leftPtr = treeNode.leftPtr

        rightTreeNode.leftPtr = leftTreeNode
        rightTreeNode.rightPtr = treeNode.rightPtr

        # check if there is a parent
        parentOfPassedNode = treeNode.parentPtr
        if parentOfPassedNode is not None:
            keptNode = copy.copy(treeNode.valueStruct[treeNode.order])
            if parentOfPassedNode.isFull():
                # split the parent node too 
                # mostly increases the height recursively
                # check for dangling values in pointers
                if parentOfPassedNode.parentPtr is None:
                    # this means we have hit a full leaf node whose Parent is a ROOT
                   
                    # # change parent for the left and right newly created nodes 
                    leftTreeNode.setParent(parentOfPassedNode)
                    rightTreeNode.setParent(parentOfPassedNode)

                    # # clean the parent
                    # keptNode = treeNode.valueStruct[treeNode.order]
                    keptNode.assignPrevNextPtrs(leftTreeNode, rightTreeNode)

                    # fix the pointers for the parent's last value so that it is reflected correctly...
                    parentOfPassedNode.valueStruct[-1].nextPtr = leftTreeNode

                    # treeNode.valueStruct.clear()
                    # treeNode.insertNodeAtEnd(keptNode)
                    tree_node_list.extend([leftTreeNode, rightTreeNode])
                    tree_node_list.remove(treeNode)

                    # Split this shit
                    splitInHalfAndInsert(parentOfPassedNode, keptNode, tree_node_list)
                else:
                    # this is an intermediate node, somewhere between the leaves and the ROOT
                    # split and push to parent
                    # change parent for the left and right newly created nodes 
                    leftTreeNode.setParent(parentOfPassedNode)
                    rightTreeNode.setParent(parentOfPassedNode)

                    # keptNode = treeNode.valueStruct[treeNode.order]
                    keptNode.assignPrevNextPtrs(leftTreeNode, rightTreeNode)

                    # fix the pointers for the parent's last value so that it is reflected correctly...
                    parentOfPassedNode.valueStruct[-1].nextPtr = leftTreeNode

                    tree_node_list.extend([leftTreeNode, rightTreeNode])
                    tree_node_list.remove(treeNode)

                    # Split this shit
                    splitInHalfAndInsert(parentOfPassedNode, keptNode, tree_node_list)
                    None
            else:
                # set the parent for the leaves.
                leftTreeNode.setParent(parentOfPassedNode)
                rightTreeNode.setParent(parentOfPassedNode)
                # compare values to insert in a proper place (always in the end due to ascending sorting)??
                # Copy to parent
                parentOfPassedNode.valueStruct[-1].nextPtr = leftTreeNode
                keptNode.prevPtr = leftTreeNode
                keptNode.nextPtr = rightTreeNode
                parentOfPassedNode.insertNodeAtEnd(keptNode)

                # remove the broken node
                tree_node_list.remove(treeNode)

                # add more nodes to the tree
                tree_node_list.extend([leftTreeNode, rightTreeNode])
                # insert
        else:
            # this corresponds only to the ROOT NODE
            # set parents of new nodes
            leftTreeNode.setParent(treeNode)
            rightTreeNode.setParent(treeNode)

            # clean the parent
            keptNode = treeNode.valueStruct[treeNode.order]
            keptNode.assignPrevNextPtrs(leftTreeNode, rightTreeNode)
            treeNode.valueStruct.clear()
            treeNode.insertNodeAtEnd(keptNode)
            # treeNode.attachNodesAtIndex(0, leftTreeNode, rightTreeNode)
            tree_node_list.extend([leftTreeNode, rightTreeNode])
    else:
        # cases for intermediate node or the ROOT when height is 2

         # save the split node to shove into some more parent later
        keptNode = copy.copy(treeNode.valueStruct[treeNode.order])

        parentOfPassedNode = treeNode.parentPtr
        if parentOfPassedNode is None:
            # parent is an intermedite ROOT
            # create a new parent
            newRoot = TreeNode("", None,treeNode.order, "")
            newRoot.isLeaf = False
            
            # set parents for newly create interme3diate nodes 
            leftTreeNode.setParent(newRoot)
            rightTreeNode.setParent(newRoot)

            leftTreeNode.isLeaf = False
            rightTreeNode.isLeaf = False
            
            # remove one of the dangliing pointer that remains
            del rightTreeNode.valueStruct[0]

            # one might need to recursively drill down and fetch the parent pointers and set them appropriately to the new parents
            for each in leftTreeNode.valueStruct:
                each.prevPtr.setParent(leftTreeNode)
                each.nextPtr.setParent(leftTreeNode)
            for each in rightTreeNode.valueStruct:
                each.prevPtr.setParent(rightTreeNode)
                each.nextPtr.setParent(rightTreeNode)
            
            # need logic to probably remove the pushed node from the rest of the tree? MAYBE?

            # keptNode = treeNode.valueStruct[treeNode.order]
            keptNode.assignPrevNextPtrs(leftTreeNode, rightTreeNode)
            # treeNode.valueStruct.clear()
            newRoot.insertNodeAtEnd(keptNode)
            # treeNode.attachNodesAtIndex(0, leftTreeNode, rightTreeNode)
            # insert new root and new intermediate nodes 
            tree_node_list.extend([newRoot, leftTreeNode, rightTreeNode])
            tree_node_list.remove(treeNode)
        else:
            # handle the split of an intermediate node and alignment of individual pointers
            # set parents for newly create interme3diate nodes 
            leftTreeNode.setParent(parentOfPassedNode)
            rightTreeNode.setParent(parentOfPassedNode)

            keptNode.assignPrevNextPtrs(leftTreeNode, rightTreeNode)

            leftTreeNode.isLeaf = False
            rightTreeNode.isLeaf = False

            # remove one of the dangliing pointer that remains
            del rightTreeNode.valueStruct[0]

            # one might need to recursively drill down and fetch the parent pointers and set them appropriately to the new parents
            for each in leftTreeNode.valueStruct:
                each.prevPtr.setParent(leftTreeNode)
                each.nextPtr.setParent(leftTreeNode)
            for each in rightTreeNode.valueStruct:
                each.prevPtr.setParent(rightTreeNode)
                each.nextPtr.setParent(rightTreeNode)

            # fix the pointers for the parent's last value so that it is reflected correctly...
            parentOfPassedNode.valueStruct[-1].nextPtr = leftTreeNode

            tree_node_list.extend([leftTreeNode, rightTreeNode])

            tree_node_list.remove(treeNode)

            if parentOfPassedNode.isFull():
                # splitting intermediate node
                # take the children and make them intermediate too

                # Split this shit
                splitInHalfAndInsert(parentOfPassedNode, keptNode, tree_node_list)

                None
            else:
                #copy to parent and handle extended split with alignment of pointers in both the intermediate ROOT and the children
                parentOfPassedNode.insertNodeAtEnd(keptNode)

def recursivelyAssignPagesFromRoot(node : TreeNode) -> None:
    # assign page to a node
    # page = random.choice(pageArray)
    # node.name = page
    
    # remove page from list
    # pageArray.remove(page)

    if not (node.parentPtr == None):
        node.parentLabel = node.parentPtr.name

    # node.name = random.choice(pageArray)
    if node.isLeaf:
        return
    else:
        if len(node.valueStruct) > 0:
            for each in node.valueStruct:
                if not (each.prevPtr == None):
                    each.prev = each.prevPtr.name
                    recursivelyAssignPagesFromRoot(each.prevPtr)
                if not (each.nextPtr == None):
                    each.next = each.nextPtr.name
                    recursivelyAssignPagesFromRoot(each.nextPtr)
    return
