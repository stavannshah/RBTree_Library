class MinHeapNode:
    def __init__(var_self, priority, value):
        var_self.priority = priority
        var_self.value = value

class MinHeap:
    def __init__(var_self):
        var_self.heap = []

    def insert(var_self, priority, value):
        node = MinHeapNode(priority, value)
        var_self.heap.append(node)
        var_self._heapify_up(len(var_self.heap) - 1)

    def extract_min(var_self):
        if not var_self.heap:
            return None

        if len(var_self.heap) == 1:
            return var_self.heap.pop()

        root = var_self.heap[0]
        var_self.heap[0] = var_self.heap.pop()
        var_self._heapify_down(0)
        return root

    def is_empty(var_self):
        return len(var_self.heap) == 0

    def _heapify_up(var_self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if var_self.heap[index].priority < var_self.heap[parent_index].priority:
                var_self.heap[index], var_self.heap[parent_index] = var_self.heap[parent_index], var_self.heap[index]
                index = parent_index
            else:
                break

    def _heapify_down(var_self, index):
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        smallest = index

        if left_child_index < len(var_self.heap) and var_self.heap[left_child_index].priority < var_self.heap[smallest].priority:
            smallest = left_child_index

        if right_child_index < len(var_self.heap) and var_self.heap[right_child_index].priority < var_self.heap[smallest].priority:
            smallest = right_child_index

        if smallest != index:
            var_self.heap[index], var_self.heap[smallest] = var_self.heap[smallest], var_self.heap[index]
            var_self._heapify_down(smallest)
    
    def get_heap_elements(var_self):
        return [node.value for node in var_self.heap]

