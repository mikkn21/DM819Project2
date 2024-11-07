
from tree import *

def test_leaf_neighbours():
    """
    Also test replace child
    """
    # Arrange

    root = Node(None, None, None, [], None)
    node_left = Node(None, None, root, [], None)
    root.left = node_left
    leaf1 = Leaf(Point(1,1), node_left, None)
    node_left.left = leaf1
    leaf2 = Leaf(Point(2,2), node_left, None)
    node_left.right = leaf2
    leaf3 = Leaf(Point(3,3), root, None)
    root.right = leaf3

    # Act
    next_leaf = leaf1.next_leaf()
    next_next_leaf = next_leaf.next_leaf()
    prev_leaf = leaf3.prev_leaf()
    prev_prev_leaf = prev_leaf.prev_leaf()

    # Assert
    assert id(next_leaf) == id(leaf2)
    assert id(next_next_leaf) == id(leaf3)
    assert id(prev_leaf) == id(leaf2)
    assert id(prev_prev_leaf) == id(leaf1)

    new_child = Node(None, None, None, [], None)
    new_child.left = Leaf(Point(4,4), new_child, None)
    new_child.right = Leaf(Point(5,5), new_child, None)
    
    node_left.replace_child(leaf2, new_child)
    assert id(node_left.right) == id(new_child)
    assert id(node_left.right) != id(leaf2)