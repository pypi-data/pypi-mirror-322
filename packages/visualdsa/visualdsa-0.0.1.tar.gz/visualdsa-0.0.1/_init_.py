import matplotlib.pyplot as plt

def showStack(arr):
    if not len(arr):
      print('showStack : This is an empty list.')
      return
      
    fig, node = plt.subplots(figsize=(2, len(arr)/2))
    node.text(0.5, len(arr)/2, 'Top', ha='center')
    for i, item in enumerate(arr._data):
        node.text(0.5, i/2, str(item), ha='center', bbox=dict(facecolor="white", boxstyle="round"))
    node.text(0.5, -0.5, 'Bottom', ha='center')
    node.set_ylim(-0.5, len(arr)/2)
    plt.axis('off')
    plt.show()

def showQueue(arr):
    fig, node = plt.subplots(figsize=(len(arr._data),2))

    for i, item in enumerate(arr._data):
        varColor = 'black' # box color

        # front label
        if i == arr._front:
          varColor = 'royalblue'
          node.text(i, 0.25, 'Front', ha='center', color=varColor)

        # rear label
        if i == arr._rear and i == arr._front:
          varColor = 'indianred'
          node.text(i, 0.15, 'Rear', ha='center', color=varColor)
          varColor = 'black'
        elif i == arr._rear:
          varColor = 'indianred'
          node.text(i, 0.25, 'Rear', ha='center', color=varColor)

        # none
        if arr._data[i] == None:
          varColor = 'lightgray'

        # box element
        node.text(i, 0.5, str(item), ha='center', color=varColor, bbox=dict(facecolor="white", edgecolor=varColor, boxstyle="round"))

    node.set_xlim(0, len(arr._data))
    plt.axis('off')
    plt.show()

def showLinkedList(arr):
    def tableNode(color, name, next):
      table = node.table(cellText=[[name, next]] , 
                          cellLoc='center', 
                          colWidths=[3, 1], 
                          cellColours=[['white', color]],
                          bbox=[index/arr._count, 0.2, 0.75/arr._count, 0.4])

    if arr._head is None:
      print("showLinkedList : This is an empty list.")
      return
    else:  
      #setup
      fig, node = plt.subplots(figsize=(arr._count*1.25, 1))
      current = None
      index = 0

      #root node
      tableNode('lightblue', arr._count, '')
      node.annotate('', xytext=(index+0.65, 0.4) , xy=(index+1, 0.4),va='center', arrowprops=dict(arrowstyle='->'))
      current = arr._head
      index += 1

    #data node
    while current != None:
      if current._next != None:
        tableNode('pink', current._name, '')
        node.annotate('', xytext=(index+0.65, 0.4) , xy=(index+1, 0.4),va='center', arrowprops=dict(arrowstyle='->'))
      else:
        tableNode('pink', current._name, 'X')

      current = current._next
      index += 1

    node.set_xlim(0, arr._count)
    plt.axis('off')
    plt.show()

S = ArrayStack()
showStack(S)
S.push(1)
S.push(2)
S.push(3)
showStack(S)