import matplotlib.pyplot as plt

class TreeBinaryNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
class LinkedListNode:
    def __init__(self, data):
        self.data = data  
        self.next = None  
        self.prev = None
class StructLib:
    class LinkedList:
        class Singly:
            def __init__(self):
                self.head = None  
            def insert_at_end(self, data):
                new_node = LinkedListNode(data)
                if self.head is None:  
                    self.head = new_node
                    return
                last_node = self.head
                while last_node.next:  
                    last_node = last_node.next
                last_node.next = new_node  

            def insert_at_beginning(self, data):
                new_node = LinkedListNode(data)
                new_node.next = self.head  
                self.head = new_node  

            def insert_after(self, prev_data, data):
                current = self.head
                while current:
                    if current.data == prev_data:  
                        new_node = LinkedListNode(data)
                        new_node.next = current.next 
                        current.next = new_node 
                        return
                    current = current.next
                print("العنصر السابق غير موجود.")

            def delete_node(self, key):
                current = self.head

                if current is None:
                    print("القائمة فارغة.")
                    return

                if current.data == key:
                    self.head = current.next  
                    current = None
                    return

                prev = None
                while current and current.data != key:
                    prev = current
                    current = current.next

                if current is None:
                    print("العنصر غير موجود.")
                    return

                prev.next = current.next
                current = None

            def display(self):
                current = self.head
                if current is None:
                    print("القائمة فارغة.")
                    return
                while current:
                    print(current.data, end=" -> ")
                    current = current.next
                print("None")
        class Doubly:
            def __init__(self):
                self.head = None  
                self.tail = None  

            def append(self, data):
                new_node = LinkedListNode(data)  
                if not self.head:  # إذا كانت القائمة فارغة
                    self.head = new_node
                    self.tail = new_node
                    return
                # ربط العقدة الجديدة بالنهاية
                self.tail.next = new_node  # ربط العقدة السابقة بالعقدة الجديدة
                new_node.prev = self.tail  # ربط العقدة الجديدة بالعقدة السابقة
                self.tail = new_node  # تحديث الذيل

            def prepend(self, data):
                new_node = LinkedListNode(data)
                if not self.head:  # إذا كانت القائمة فارغة
                    self.head = new_node
                    self.tail = new_node
                    return
                new_node.next = self.head  # ربط العقدة الجديدة بالرأس الحالي
                self.head.prev = new_node  # ربط الرأس بالعقدة الجديدة
                self.head = new_node  # تحديث الرأس

            # حذف عنصر من القائمة
            def delete(self, key):
                current_node = self.head
                while current_node:
                    if current_node.data == key:  # إذا كانت القيمة هي القيمة المستهدفة
                        if current_node.prev:  # إذا لم تكن العقدة هي رأس القائمة
                            current_node.prev.next = current_node.next
                        if current_node.next:  # إذا لم تكن العقدة هي ذيل القائمة
                            current_node.next.prev = current_node.prev
                        if current_node == self.head:  # إذا كانت العقدة هي رأس القائمة
                            self.head = current_node.next
                        if current_node == self.tail:  # إذا كانت العقدة هي ذيل القائمة
                            self.tail = current_node.prev
                        return
                    current_node = current_node.next

            # طباعة عناصر القائمة من البداية إلى النهاية
            def print_list_forward(self):
                current_node = self.head
                while current_node:
                    print(current_node.data, end=" <-> ")
                    current_node = current_node.next
                print("None")

            # طباعة عناصر القائمة من النهاية إلى البداية
            def print_list_backward(self):
                current_node = self.tail
                while current_node:
                    print(current_node.data, end=" <-> ")
                    current_node = current_node.prev
                print("None")
        class Circuly:
            def __init__(self):
                self.first = None
                self.last =None
                self.lengh = 0
            def pushFirst(self,item):
                new_Node = LinkedListNode(item)
                if self.lengh == 0:
                    self.first = new_Node
                    self.last = new_Node
                    new_Node.next = new_Node
                    new_Node.prev = new_Node

                else:
                    new_Node.next = self.first
                    new_Node.prev = self.last
                    self.first.prev = new_Node
                    self.last.next =new_Node
                    self.first = new_Node
                self.lengh +=1
            def deleteItem(self,value):
                cursr = self.first
                if self.lengh == 1:
                    self.last ,self.first = None , None
                    return
                while cursr != None:
                    if cursr.data == value:
                        cursr.prev.next = cursr.next
                        cursr.next.prev = cursr.prev
                        if cursr == self.first:
                            self.first = cursr.next
                        if cursr == self.last:
                            self.last = cursr.prev
                        return f'{value} removed successfully'
                    cursr = cursr.next
                    if cursr == self.first:
                        return 'Node not found'
            def pushLast(self,item):
                new_Node = LinkedListNode(item)
                
                if self.lengh == 0:
                    self.first = new_Node
                    self.last = new_Node
                    new_Node.next = new_Node
                    new_Node.prev = new_Node
                else:
                    new_Node.prev = self.last
                    new_Node.next = self.first
                    self.last.next = new_Node
                    self.first.prev = new_Node
                    self.last = new_Node
                    
                self.lengh +=1
            def deleteFirst(self):
                if self.lengh == 0:
                    print("List is Null !!")
                elif self.lengh == 1:
                    self.last , self.first = None, None
                else:
                    
                    self.first = self.first.next
                    self.last.next = self.first
                    self.first.prev = self.last
                self.lengh -= 1
            def deleteLast(self):
                if self.lengh == 0:
                    print("List is Null !!")
                elif self.lengh == 1:
                    self.last , self.first = None, None
                else:
                    self.last  = self.last.prev
                    self.last.next = self.first
                    self.first.prev = self.last
                self.lengh -= 1
            def ViewItemFtoL(self,num=0):
                frist = self.first
                cont = 0
                looping = False
                if num > 0:
                    looping = True
                while frist != None:
                    print(frist.data)
                    frist = frist.next
                    if looping and frist == self.first:
                        cont +=1
                        print('_'*25)
                        if cont >= num:
                            break
            def ViewItemLtof(self,num=0):
                frist = self.last
                cont = 0
                looping = False
                if num > 0:
                    looping = True
                while frist != None:
                    print(frist.data)
                    frist = frist.prev
                    if looping and frist == self.last :
                        print('_'*25)
                        cont += 1
                        if cont >= num:
                            break
    class Stack:
        def __init__(self, size=100):
            self.stack = [None] * size
            self.size = size
            self.top = -1

        def push(self, value):
            if self.is_full():
                return False
            self.top += 1
            self.stack[self.top] = value
            return True

        def pop(self):
            if self.is_empty():
                return None
            value = self.stack[self.top]
            self.stack[self.top] = None
            self.top -= 1
            return value

        def peek(self):
            if self.is_empty():
                return None
            return self.stack[self.top]

        def is_empty(self):
            return self.top == -1

        def is_full(self):
            return self.top == self.size - 1

        def Size(self):
            return self.top + 1
    class Queue:
        class Circular:
            def __init__(self, size=100):
                self.queue = [None] * size
                self.size = size
                self.front = int(-1)
                self.rear = int(-1)

            def enqueue(self, value):
                if (self.rear+1) % self.size == self.front:
                    return False
                if self.front == -1:
                    self.front = 0
                self.rear = (self.rear + 1) % self.size
                self.queue[self.rear] = value
                return True

            def dequeue(self):
                if self.front == -1:
                    return None
                temp = self.queue[self.front]
                if self.front == self.rear:
                    self.front = -1
                    self.rear = -1
                else:
                    self.front = (self.front + 1) % self.size
                return temp

            def is_empty(self):
                return self.front == -1

            def is_full(self):
                return (self.rear + 1) % self.size == self.front

            def peek(self):
                if self.front == -1:
                    return None
                return self.queue[self.front]

            def size_of_queue(self):
                if self.front == -1:
                    return 0
                if self.rear >= self.front:
                    return self.rear - self.front + 1
                return self.size - self.front + self.rear + 1
        class CircularDeque:
            def __init__(self, size):
                self.queue = [None] * size
                self.size = size
                self.front = -1
                self.rear = -1

            def enqueue_end(self, value):
                if (self.rear + 1) % self.size == self.front:
                    return False
                if self.front == -1:
                    self.front = 0
                self.rear = (self.rear + 1) % self.size
                self.queue[self.rear] = value
                return True
            def enqueue_frist(self, value):
                if (self.rear + 1) % self.size == self.front:
                    return False
                if self.front == -1 :
                    self.front = 0
                    
                self.front = (self.front - 1) % self.rear
                self.queue[self.front] = value
                return True
            def dequeue_frist(self):
                if self.front == -1:
                    return None
                temp = self.queue[self.front]
                if self.front == self.rear:
                    self.front = -1
                    self.rear = -1
                else:
                    self.front = (self.front + 1) % self.size
                return temp
            def dequeue_end(self):
                if self.rear == -1:
                    return None
                temp = self.queue[self.rear]
                if self.front == self.rear:
                    self.front = -1
                    self.rear = -1
                else:
                    self.rear = (self.rear - 1) % self.size
                return temp

            def is_empty(self):
                return self.front == -1

            def is_full(self):
                return (self.rear + 1) % self.size == self.front

            def peek(self):
                if self.front == -1:
                    return None
                return self.queue[self.front]

            def Size(self):
                if self.front == -1:
                    return 0
                if self.rear >= self.front:
                    return self.rear - self.front + 1
                return self.size - self.front + self.rear + 1
        class SimpleDeque:
            def __init__(self, size):
                self.queue = [None] * size
                self.size = size
                self.front = -1
                self.rear = -1

            def enqueue_end(self, value):
                if self.is_full():
                    return False
                if self.front == -1:
                    self.front = 0
                self.rear += 1 
                self.queue[self.rear] = value
                return True
            def enqueue_frist(self, value):
                if self.front <= 0:
                    return False
                if self.rear == -1 :
                    self.rear = 0
                    
                self.front -= 1
                self.queue[self.front] = value
                return True
            def dequeue_frist(self):
                if self.front == -1:
                    return None
                temp = self.queue[self.front]
                if self.front == self.rear:
                    self.front = -1
                    self.rear = -1
                else:
                    self.front += 1
                return temp
            def dequeue_end(self):
                if self.rear == -1:
                    return None
                temp = self.queue[self.rear]
                if self.front == self.rear:
                    self.front = -1
                    self.rear = -1
                else:
                    self.rear -= 1
                return temp

            def is_empty(self):
                return self.rear == -1 and self.front == -1

            def is_full(self):
                return self.rear == self.size

            def peek(self):
                if self.front == -1:
                    return None
                return self.queue[self.front]

            def Size(self):
                return self.rear + 1
        class Simple:
            def __init__(self, size):
                self.queue = [None] * size
                self.size = size
                self.front = -1
                self.rear = -1

            def enqueue(self, value):
                if self.is_full():
                    return False
                if self.front == -1:
                    self.front = 0
                self.rear += 1 
                self.queue[self.rear] = value
                return True
            def dequeue(self):
                if self.front == -1:
                    return None
                temp = self.queue[self.front]
                if self.front == self.rear:
                    self.front = -1
                    self.rear = -1
                else:
                    self.front += 1
                return temp

            def is_empty(self):
                return self.rear == -1 and self.front == -1

            def is_full(self):
                return self.rear == self.size

            def peek(self):
                if self.front == -1:
                    return None
                return self.queue[self.front]

            def Size(self):
                return self.rear +1
        class Priority:
            def __init__(self, size=100):
                self.size = size
                self.queue = [None] * size
                self.front = -1
                self.rear = -1

            def is_empty(self):
                return self.front == -1

            def is_full(self):
                return self.rear == self.size - 1

            def enqueue(self, value, priority):
                if self.is_full():
                    return False
                if self.is_empty():
                    self.front = 0
                    self.rear = 0
                    self.queue[self.rear] = (value, priority)
                else:
                    i = self.rear
                    while i >= self.front and self.queue[i][1] > priority:
                        self.queue[i + 1] = self.queue[i]
                        i -= 1
                    self.queue[i + 1] = (value, priority)
                    self.rear += 1
                return True

            def dequeue(self):
                if self.is_empty():
                    return None
                item = self.queue[self.front]
                if self.front == self.rear:
                    self.front = -1
                    self.rear = -1
                else:
                    self.front += 1
                return item

            def peek(self):
                if self.is_empty():
                    return None
                return self.queue[self.front]

            def display(self):
                if self.is_empty():
                    return []
                return self.queue[self.front:self.rear + 1]
    class Tree:
        class Binary:
            def __init__(self):
                self.root = None

            def add(self, val):
                if not self.root:
                    self.root = TreeBinaryNode(val)
                else:
                    self._add(self.root, val)

            def _add(self, curr, val):
                if val < curr.val:
                    if curr.left:
                        self._add(curr.left, val)
                    else:
                        curr.left = TreeBinaryNode(val)
                else:
                    if curr.right:
                        self._add(curr.right, val)
                    else:
                        curr.right = TreeBinaryNode(val)

            def find(self, val):
                return self._find(self.root, val)

            def _find(self, curr, val):
                if not curr:
                    return False
                if curr.val == val:
                    return True
                if val < curr.val:
                    return self._find(curr.left, val)
                return self._find(curr.right, val)

            def delete(self, val):
                self.root = self._delete(self.root, val)

            def _delete(self, curr, val):
                if not curr:
                    return curr
                if val < curr.val:
                    curr.left = self._delete(curr.left, val)
                elif val > curr.val:
                    curr.right = self._delete(curr.right, val)
                else:
                    if not curr.left:
                        return curr.right
                    if not curr.right:
                        return curr.left
                    temp = self._min(curr.right)
                    curr.val = temp.val
                    curr.right = self._delete(curr.right, temp.val)
                return curr

            def _min(self, curr):
                while curr.left:
                    curr = curr.left
                return curr

            def inorder(self):
                res = []
                self._inorder(self.root, res)
                return res

            def _inorder(self, curr, res):
                if curr:
                    self._inorder(curr.left, res)
                    res.append(curr.val)
                    self._inorder(curr.right, res)

            def preorder(self):
                res = []
                self._preorder(self.root, res)
                return res

            def _preorder(self, curr, res):
                if curr:
                    res.append(curr.val)
                    self._preorder(curr.left, res)
                    self._preorder(curr.right, res)

            def postorder(self):
                res = []
                self._postorder(self.root, res)
                return res

            def _postorder(self, curr, res):
                if curr:
                    self._postorder(curr.left, res)
                    self._postorder(curr.right, res)
                    res.append(curr.val)
            def leftNode(self):
                res = []
                self._leftNode(self.root, res)
                res.pop()
                return res

            def _leftNode(self, curr, res):
                if curr:
                    self._postorder(curr.left, res)
                    res.append(curr.val)
                    
            def rightNode(self):
                res = []
                self._rightNode(self.root, res)
                res.pop()
                return res

            def _rightNode(self, curr, res):
                if curr:
                    self._postorder(curr.right, res)
                    res.append(curr.val)
    class Graph:
        def __init__(self):
            self.graph = {}

        def add_node(self, node):
            if node not in self.graph:
                self.graph[node] = []

        def remove_node(self, node):
            if node in self.graph:
                self.graph.pop(node)
            for edges in self.graph.values():
                if node in edges:
                    edges.remove(node)

        def add_edge_one_way(self, from_node, to_node):
            if from_node in self.graph:
                self.graph[from_node].append(to_node)

        def add_edge_two_way(self, node1, node2):
            self.add_edge_one_way(node1, node2)
            self.add_edge_one_way(node2, node1)

        def remove_edge_one_way(self, from_node, to_node):
            if from_node in self.graph and to_node in self.graph[from_node]:
                self.graph[from_node].remove(to_node)

        def remove_edge_two_way(self, node1, node2):
            self.remove_edge_one_way(node1, node2)
            self.remove_edge_one_way(node2, node1)

        def display_edges(self):
            return [(node, neighbor) for node, neighbors in self.graph.items() for neighbor in neighbors]

        def display_single_edges(self):
            return [(node, neighbor) for node, neighbors in self.graph.items() for neighbor in neighbors if (neighbor, node) not in self.display_edges()]

        def bfs(self, start, end):
            visited = set()
            queue = [start]
            while queue:
                node = queue.pop(0)
                if node == end:
                    return True
                if node not in visited:
                    visited.add(node)
                    queue.extend(neighbor for neighbor in self.graph[node] if neighbor not in visited)
            return False

        def dfs(self, start, end):
            visited = set()
            stack = [start]
            while stack:
                node = stack.pop()
                if node == end:
                    return True
                if node not in visited:
                    visited.add(node)
                    stack.extend(neighbor for neighbor in self.graph[node] if neighbor not in visited)
            return False

        def bfs_all(self, start, direction='right'):
            visited = set()
            queue = [start]
            result = []
            while queue:
                node = queue.pop(0 if direction == 'right' else -1)
                if node not in visited:
                    visited.add(node)
                    result.append(node)
                    queue.extend(neighbor for neighbor in self.graph[node] if neighbor not in visited)
            return result

        def dfs_all(self, start):
            visited = set()
            stack = [start]
            result = []
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    result.append(node)
                    stack.extend(neighbor for neighbor in self.graph[node] if neighbor not in visited)
            return result

        def load_tree(self, tree):
            for val in tree.inorder():
                self.add_node(val)
            for val in tree.inorder():
                left = tree.find(val - 1)
                right = tree.find(val + 1)
                if left:
                    self.add_edge_two_way(val, val - 1)
                if right:
                    self.add_edge_two_way(val, val + 1)

        def plot_graph(self):
            edges = self.display_edges()
            nodes = self.graph.keys()
            pos = {node: (i, len(neighbors)) for i, (node, neighbors) in enumerate(self.graph.items())}
            plt.figure(figsize=(10, 7))
            for edge in edges:
                plt.plot(
                    [pos[edge[0]][0], pos[edge[1]][0]],
                    [pos[edge[0]][1], pos[edge[1]][1]],
                    'bo-', markersize=8
                )
            for node, (x, y) in pos.items():
                plt.text(x, y, str(node), fontsize=12, ha='right', color="red")
            plt.show()
        def plot_tree(self):
            edges = self.display_edges()
            nodes = list(self.graph.keys())

            level = {}  
            pos = {}  
            queue = [(nodes[0], 0)]  

            while queue:
                node, depth = queue.pop(0)
                if node not in level:
                    level[node] = depth
                    if depth not in pos:
                        pos[depth] = []
                    pos[depth].append(node)

                for child in self.graph.get(node,[]):
                    if child not in level:
                        queue.append((child, depth + 1))
                
                for edge in edges:
                    if edge[0] not in level:
                        level[edge[0]]= 0
                        pos.setdefault(0,[]).append(edge[0])
                    if edge[1] not in level:
                        level[edge[1]] = level[edge[0]] +1
                        pos.setdefault(level[edge[1]],[]).append(edge[1])

            coords = {}
            for depth, nodes_at_level in pos.items():
                for i, node in enumerate(nodes_at_level):
                    x = i - len(nodes_at_level) / 2  
                    y = -depth  
                    coords[node] = (x, y)

            plt.figure(figsize=(10, 7))
            for edge in edges:
                x1, y1 = coords[edge[0]]
                x2, y2 = coords[edge[1]]
                plt.plot([x1, x2], [y1, y2], 'bo-', markersize=8)

            for node, (x, y) in coords.items():
                plt.text(x, y, str(node), fontsize=12, ha='center', color="red")

            plt.axis("off")  
            plt.show()
