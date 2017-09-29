import random

from binary_tree import *


# defining the slices in the dataset
def no_of_parts(total_data, column_name):
    list_node = {column_name: []}  # DE
    tree_node = Node(column_name)
    grouped_data = total_data.groupby(column_name)
    for parts in grouped_data:
        part_dict = {str(parts[0]): []}  # de
        new_sliced_data = parts[1].drop(column_name, 1)
        part_dict[str(parts[0])], sub_node = column_at_level(new_sliced_data)  # first ard
        list_node[column_name].append(part_dict)  # de

        if isinstance(sub_node, str):
            tree_node.setPrediction(sub_node)
        elif parts[0] == 0:
            sub_node.parent = tree_node
            tree_node.insert_left(sub_node)
        else:
            sub_node.parent = tree_node
            tree_node.insert_right(sub_node)

    return list_node, tree_node


# defining at calculation of the entropy and appending it to the list
def column_at_level(sliced_data):
    col_list = sliced_data.columns.values
    if len(col_list) == 1:
        return str(sliced_data.iloc[0, len(col_list) - 1]), str(sliced_data.iloc[0, len(col_list) - 1])
    selected_column_no = random.randrange(0, len(col_list) - 1)
    selected_column = col_list[selected_column_no]
    sliced_data.drop(selected_column, axis=1)
    return no_of_parts(sliced_data, selected_column)


# checking if the given dataframe has pure set
def all_same(given_list):
    for i in range(len(given_list) - 1):
        if given_list[i] is not given_list[i + 1]:
            return False
    return True
