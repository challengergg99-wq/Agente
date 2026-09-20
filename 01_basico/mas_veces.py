def most_frequent_item_count(collection):
    if not collection:
        return 0
    return max(collection.count(item) for item in collection)

print(most_frequent_item_count([3, -1, -1, 2, 3, 3, 3, -1, 4, 3, 2, 4, 9, 3]))