# Data structures and logic for decision trees based on an array
import math
from Queue import Queue as fifo

test_array_index = ["Alt", "Bar", "Fri", "Hun", "Pat", "Price", "Rain", "Res", "Type", "Est", "WillWait"]

test_array = [["T", "F", "F", "T", "Some", "$$$", "F", "T", "French", "0-10", True],
                ["T", "F", "F", "T", "Full", "$", "F", "F", "Thai", "30-60", False],
                ["F", "T", "F", "F", "Some", "$", "F", "F", "Burger", "0-10", True],
                ["T", "F", "T", "T", "Full", "$", "F", "F", "Thai", "10-30", True],
                ["T", "F", "T", "F", "Full", "$$$", "F", "T", "French", ">60", False],
                ["F", "T", "F", "T", "Some", "$$", "T", "T", "Italian", "0-10", True],
                ["F", "T", "F", "F", "None", "$", "T", "F", "Burger", "0-10", False],
                ["F", "F", "F", "T", "Some", "$$", "T", "T", "Thai", "0-10", True],
                ["F", "T", "T", "F", "Full", "$", "T", "F", "Burger", ">60", False],
                ["T", "T", "T", "T", "Full", "$$$", "F", "T", "Italian", "10-30", False],
                ["F", "F", "F", "F", "None", "$", "F", "F", "Thai", "0-10", False],
                ["T", "T", "T", "T", "Full", "$", "F", "F", "Burger", "30-60", True]]

def remove_attribute_value(table, attribute_column, attribute_value):
    new_table = []
    for row in table:
        if row[attribute_column] != attribute_value:
            new_table.append(row)
    return new_table

def remove_attribute_except_value(table, attribute_column, attribute_value):
    new_table = []
    for row in table:
        if row[attribute_column] == attribute_value:
            new_table.append(row)
    return new_table

def get_unique_values(table, attribute_column):
    attributes = []
    for row in table:
        attribute = row[attribute_column]
        if attribute not in attributes:
            attributes.append(attribute)
    return attributes

def get_values_for_attribute(table, attribute_column, attribute_value, result_column):
    num_true = 0
    num_false = 0
    for row in table:
        if row[attribute_column] == attribute_value:
            if row[result_column]:
                num_true += 1
            else:
                num_false += 1
    return num_true,num_false



class Node:
    name = None
    result = None
    pointers = None
    def __init__(self, name, result):
        self.name = name
        self.result = result
        self.pointers = {}

    def add_pointer(self, other_node):
        self.pointers[other_node.name] = other_node


class DecisionTree:
    def __init__(self):
        return

def calc_entropy(num_true, num_false, total_values):
    total_values = float(total_values)
    num_true = float(num_true)
    weight = (num_true+num_false)/total_values
    fraction = num_true / (num_true+num_false)
    if fraction == 1 or fraction == 0:
        return 0
    entropy = -1 * (fraction*math.log(fraction, 2) + (1-fraction)*math.log((1-fraction), 2))

    return entropy * weight

# calculate the entropy for a certain attribute
def get_entropy(table, attribute_column, result_column):
    total_values = len(table)
    unique_values = get_unique_values(table, attribute_column)
    entropy_sum = 0

    for value in unique_values:
        num_true, num_false = get_values_for_attribute(table, attribute_column, value, result_column)
        entropy_sum += calc_entropy(num_true, num_false, total_values)

    return entropy_sum

def get_initial_entropy(table, result_column):
    num_true = 0
    num_false = 0
    for row in table:
        if row[result_column]:
            num_true += 1
        else:
            num_false += 1
    entropy = calc_entropy(num_true, num_false, num_true+num_false)
    return entropy

def choose_attribute(table, result_column):
    max_entropy_gain = 0
    max_entropy_attribute = None

    initial_entropy = get_initial_entropy(table, result_column)

    for attribute in range(len(table[0])):
        if attribute == result_column:
            continue
        entropy_gain = initial_entropy - get_entropy(table, attribute, result_column)
        if entropy_gain > max_entropy_gain:
            max_entropy_gain = entropy_gain
            max_entropy_attribute = attribute
    # print("Best attribute is {}, with an entropy gain of {}".format(max_entropy_attribute, max_entropy_gain))    
    return max_entropy_attribute

def create_decision_tree(table, result_column):
    attribute = choose_attribute(table, result_column)
    # print("Choosing {} as starting attribute".format(attribute))
    root_node = Node(attribute, None)
    for attribute_value in get_unique_values(table, attribute):
        num_true, num_false = get_values_for_attribute(table, attribute, attribute_value, result_column)
        if num_true == 0:
            child = Node(attribute_value, False)
            # print("Value {} is all false".format(attribute_value))
            root_node.add_pointer(child)
        elif num_false == 0:
            child = Node(attribute_value, True)
            # print("Value {} is all true".format(attribute_value))
            root_node.add_pointer(child)
        else:
            new_table = remove_attribute_except_value(table, attribute, attribute_value)
            # print("Creating sub-tree for value {}".format(attribute_value))
            sub_tree = create_decision_tree(new_table, result_column)
            root_node.add_pointer(sub_tree)
    return root_node

def print_tree(node):
    queue = fifo()
    queue.put(node)
    while(queue.empty() == False):
        node = queue.get()
        for child in node.pointers.values():
            root_name = test_array_index[node.name]
            if child.result == None:
                name = test_array_index[child.name]
            else:
                name = child.name
            print("Node {} points to {} with result {}".format(root_name, name, child.result))
            queue.put(child)



tree = create_decision_tree(test_array, 10)
print_tree(tree)
