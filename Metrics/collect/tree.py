\
#! /usr/bin/env python

'''
General purpose tree object, which allows only one parent per child.
Tree class has to be inherited and parse method implemented.

'''

#####################################################
class Node:
    '''
    '''
    #################################################
    def __init__(self, label, myObject = None):
        '''
        '''
        self.label = label     # Mandatory label
        self.dict = {}         # Child nodes
        self.object = myObject # Optional object
        self.level = 0         # Used in printing


#####################################################
class Tree:
    '''
    '''
    #################################################
    def __init__(self, label = "root", myObject = None):
        '''
        '''
        self.name = label
        self.root = Node(label, myObject)
        self.cnt = 0           # Key for dictionaries


    #################################################
    def parse(self, filename):
        '''
        '''
        print "Tree::parse: not implemented."
        sys.exit()


    #################################################
    def addChild(self, parent, label, myObject = None):
        '''
        '''
        parent.dict[self.cnt] = Node(label, myObject)
        parent.dict[self.cnt].level = parent.level + 1
        self.cnt += 1
        return parent.dict[self.cnt - 1]


    #################################################
    def rmNodes(self, labels):
        ''' Root cannot be removed (it would not make sense anyway)
        '''
        dLabels = {}
        for label in labels:
            dLabels[label] = True
        stack = []
        stack.append(self.root)
        while len(stack) > 0:
            node = stack.pop()
            for key in sorted(node.dict.iterkeys()):
                try:
                    dLabels[node.dict[key].label]
                    del node.dict[key]
                except KeyError:
                    stack.append(node.dict[key])


    #################################################
    def rmNode(self, node, label):
        '''
        '''
        for key in sorted(node.dict.iterkeys()):
            if node.dict[key].label == label:
                del node.dict[key]
                break


    #################################################
    def preserveNodes(self, labels):
        ''' Remove all others but the given labels
            PKo: This is under construction. Currently works for genes only!
        '''
        dLabels = {}
        for label in labels:
            dLabels[label] = True
        stack = []
        stack.append(self.root)
        while len(stack) > 0:
            node = stack.pop()
            nodes = sorted(node.dict.iterkeys())
            for i in xrange(len(nodes)):
                key = nodes[i]
                try:
                    dLabels[node.dict[key].label]
                    #stack.append(node.dict[key])
                    #i += 1
                except KeyError:
                    del node.dict[key]


    #################################################
    def depthFirst(self):
        ''' Iterator
        '''
        stack = []
        stack.append(self.root)
        while len(stack) > 0:
            node = stack.pop()
            yield node
            for key in sorted(node.dict.iterkeys()):
                stack.append(node.dict[key])
        

    #################################################
    def branchFirst(self, node):
        ''' Iterator
        '''
        stack = []
        stack.append(node)
        while len(stack) > 0:
            node = stack.pop()
            yield node
            for key in sorted(node.dict.iterkeys()):
                stack.append(node.dict[key])
        

    #################################################
    def breadthFirst(self):
        ''' Iterator
        '''
        stack = []
        stack.append(self.root)
        while len(stack) > 0:
            node = stack.pop(0)
            yield node
            for key in sorted(node.dict.iterkeys()):
                stack.append(node.dict[key])
        

    #################################################
    def __repr__(self):
        '''
        '''
        myStr = ""
        for node in self.depthFirst():
            myStr += node.level * '\t' + node.label + '\n'
        return myStr

