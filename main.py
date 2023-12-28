class Node:
    def __init__(self, data):
        self.data = data
        self.children = []


class TreeStore:
    def __init__(self, items):
        self.nodes = {}
        self.root = None

        for item in items:
            node = Node(item)
            self.nodes[item["id"]] = node
            if item["parent"] == "root":
                self.root = node
            else:
                parent_node = self.nodes.get(item["parent"])
                if parent_node:
                    parent_node.children.append(node)

    def getAll(self):
        return [node.data for node in self.nodes.values()]

    def getItem(self, item_id: int):
        node = self.nodes.get(item_id)
        return node.data if node else None

    def getChildren(self, item_id: int):
        node = self.nodes.get(item_id)
        return [child.data for child in (node.children if node else [])]

    def getAllParents(self, item_id: int):
        parents = []
        node = self.nodes.get(item_id)
        while node and node.data["parent"] != "root":
            parent_id = node.data["parent"]
            parent_node = self.nodes.get(parent_id)
            if parent_node:
                parents.append(parent_node.data)
                node = parent_node
            else:
                break
        return parents


def main():
    items = [
        {"id": 1, "parent": "root"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 3, "parent": 1, "type": "test"},
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 5, "parent": 2, "type": "test"},
        {"id": 6, "parent": 2, "type": "test"},
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None},
    ]

    ts = TreeStore(items)

    assert ts.getAll() == items

    assert ts.getItem(7) == {"id": 7, "parent": 4, "type": None}

    assert ts.getChildren(4) == [
        {"id": 7, "parent": 4, "type": None}, {"id": 8, "parent": 4, "type": None}]

    assert ts.getChildren(5) == []

    assert ts.getAllParents(7) == [
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 1, "parent": "root"}]


if __name__ == '__main__':
    main()
