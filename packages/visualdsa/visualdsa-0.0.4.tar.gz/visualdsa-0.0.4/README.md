This Python library provides functions for visualizing various data structures, including linked lists, queue, stack, and more. It utilizes Matplotlib for creating interactive and informative visualizations.

This library was developed for the Data Structures and Algorithms course at King Mongkut's Institute of Technology Ladkrabang (KMITL) to enhance student understanding of these fundamental concepts.
## Installation

Install using pip

```bash
pip install visualdsa
```
    
## Usage

### Stack
#### Context
- A stack is a linear data structure that follows the Last-In, First-Out (LIFO) principle.
- Imagine a stack of plates – you can only add or remove plates from the top of the stack.


#### Sample stack class
```python
class ArrayStack:
  def __init__(self):
    self._data = []

  def __len__(self):
    return len(self._data)
  
  # ... (class methods)
```

#### Visualization
```python
import visualdsa as vd

# Sample stack data
my_stack = ArrayStack()
my_stack._data = [3, 2, 1]

# Visualize the stack
vd.showStack(my_stack)
```
![](https://media.discordapp.net/attachments/1120016379588907049/1331492507510509690/Unknown-8.png?ex=6791d087&is=67907f07&hm=e97dd3e76e078206c9adc5a00dad81f93ec9b4a95c7926d251070af9f998848e&=&format=webp&quality=lossless&width=350&height=298)

### Queue
#### Context
- A circular queue is a linear data structure that follows the First-In, First-Out (FIFO) principle, like a regular queue, but with a circular arrangement.
- The last element of the queue is logically connected to the first element, creating a circular structure. This efficient use of space by avoiding wasted memory at the beginning of the array.
- There are 2 pointers, front and rear, track the positions of the first and last elements in the queue, respectively.
#### Sample circular queue class
```python
class ArrayQueue:
  def __init__(self):
    self._data = [None] * 5   # A list to store the queue elements with capacity of 5
    self._front = 0           # The index of the front of the queue
    self._rear = 0            # he index of the rear of the queue

  def __len__(self):
    return len(self._data)
  
  # ... (class methods)

```

#### Visualization
```python
import visualdsa as vd

# Sample queue data
my_queue = ArrayQueue()
my_queue._data = [3, 2, 1, None, None]
my_queue._front = 0
my_queue._rear = 2

# Visualize the queue
vd.showCircularQueue(my_queue)
```
![](https://media.discordapp.net/attachments/1120016379588907049/1331492887371841668/Unknown-9.png?ex=6791d0e2&is=67907f62&hm=c37f6599f83624890c056d1aa454aca1c2835097c1612a2de53d5da7de982cad&=&format=webp&quality=lossless&width=850&height=348)

### Singly Linked List
#### Context
- A singly linked list is a linear data structure where each element (node) points to the next element in the sequence.

#### Sample singly linked list class
```python
class SinglyLinkedListBase:
  def __init__(self):
    self._count = 0       # The number of nodes in the list
    self._head = None     # A reference to the first node of the list 

class DataNode:
  def __init__(self, name, next):
    self._name = name     # The value stored within the node
    self._next = next     # A reference to the next node in the list (None if it's the last node)

class SinglyLinkedList(SinglyLinkedListBase):
  # self._count = 0        Inherited from SinglyLinkedListBase class
  # self._head = None      Inherited from SinglyLinkedListBase class
  
  # ... (class methods)
  pass # can delete after add class methods

```

#### Visualization
```python
import visualdsa as vd

# Sample linked list data
my_list = SinglyLinkedList()
my_node1 = DataNode("John", None)
my_node2 = DataNode("Adam", my_node1)
my_list._head = my_node2
my_list._count += 2

# Visualize the linked list
vd.showSinglyLinkedList(my_list)
```
![](https://media.discordapp.net/attachments/1120016379588907049/1331493954293731409/Unknown-10.png?ex=6791d1e0&is=67908060&hm=df5aad6e50ff11ebd39b578568e3364ae896159812a981e8d0b6f05650bd825e&=&format=webp&quality=lossless&width=572&height=194)
