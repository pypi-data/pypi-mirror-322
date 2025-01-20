class Stack:
    def __init__(self):
        self.stack = []  # Initialize an empty stack.

    def push(self, item):
        self.stack.append(item)  # Add an item to the stack.

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()  # Remove and return the top item.
        else:
            return None

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]  # Return the top item without removing it.
        else:
            return None

    def is_empty(self):
        return len(self.stack) == 0  # Check if the stack is empty.

    def display(self):
        return self.stack  # Return the current stack contents.

    def search(self, item):
        if item in self.stack:
            return self.stack.index(item)
        else:
            return -1
