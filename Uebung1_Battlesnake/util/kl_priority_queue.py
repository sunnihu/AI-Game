from queue import PriorityQueue


class PrioritizedItem:

    def __init__(self, priority: int, item: any):
        self.priority = priority
        self.item = item

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        return self.priority < other.priority


class KLPriorityQueue:

    def __init__(self):
        self.q = PriorityQueue()

    def empty(self):
        return self.q.empty()

    def get(self)-> any:
        p_item = self.q.get()
        return p_item.item

    def put(self, priority: int, item: any):
        p_item = PrioritizedItem(priority, item)
        self.q.put(p_item)

