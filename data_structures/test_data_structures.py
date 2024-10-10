from binary_search_tree import BSTree


def test_data_structure(DataStructure):
    data_structure = DataStructure()

    # TODO: add delete tests to this.

    # Test Empty Tree
    assert(data_structure.get(0) is None)
    assert(not data_structure.contains_key(0))
    assert(data_structure.minimum() is None)
    assert(data_structure.maximum() is None)
    assert(data_structure.len() == 0)
    # assert(tree.delete is None or however this is implimented)
    # assert(also the transplant one shouldn't work)

    data_structure.insert(0, "a")

    assert(data_structure.get(0) == "a")
    assert(data_structure.contains_key(0))
    assert(data_structure.minimum() == "a")
    assert(data_structure.maximum() == "a")
    assert(data_structure.len() == 1)

    data_structure.insert(1, "b")
    data_structure.insert(2, "c")
    data_structure.insert(-1, "d")

    assert(data_structure.contains_key(-1))
    assert(data_structure.get(2) == "c")
    assert(data_structure.minimum() == "d")
    assert(data_structure.maximum() == "c")
    assert(data_structure.len() == 4)

    print("Data Structure `"+data_structure.__class__.__name__+"` passed all tests!")

    

test_data_structure(BSTree)
