import json
import math

import yaml

from binary_tree import *


# find the entropy of the given data_frame based on a column name
def find_entropy(data_frame, col_name):
    total_record = len(data_frame)
    grouped = data_frame.groupby(col_name)
    whole_sum = 0.0
    for series in grouped:
        column_size = len(series[1])
        sum = 0.0
        y_n_group = series[1].groupby("Class")
        for y_or_n in y_n_group:
            group_size = len(y_or_n[1])
            div_value = float(group_size) / float(column_size)
            sum -= (div_value * math.log(div_value, 2))
        sum *= float(column_size) / float(total_record)
        whole_sum += sum
    return whole_sum


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

        # sub_node = column_at_level(new_sliced_data)

        if isinstance(sub_node, str):
            tree_node.setPrediction(sub_node)
        elif parts[0] == 0:
            sub_node.parent = tree_node
            tree_node.insert_left(sub_node)
        else:
            sub_node.parent = tree_node
            tree_node.insert_right(sub_node)

    return list_node, tree_node  # first arg


# defining at calculation of the entropy and appending it to the list
def column_at_level(sliced_data):
    col_list = sliced_data.columns.values
    entropy = []
    for x in col_list:
        entropy.append(find_entropy(sliced_data, x))

    if all_zero(entropy):
        return str(sliced_data.iloc[0, len(col_list) - 1]), str(sliced_data.iloc[0, len(col_list) - 1])  # de 2nd param
    else:
        entropy.pop(len(entropy) - 1)
        selected_column_no = entropy.index(min(entropy))
        selected_column = col_list[selected_column_no]
        return no_of_parts(sliced_data, selected_column)


# checking if the given dataframe has pure set
def all_zero(given_list):
    new_list = []
    for x in given_list:
        if x != 0.0:
            new_list.append(x)
    if len(new_list) == 0:
        return True
    else:
        return False


# printing the tree
def print_tree(tree_dict):
    json.dumps(tree_dict, indent=1)
    json_tree = json.loads(json.dumps(tree_dict, indent=1))
    print(yaml.safe_dump(json_tree, allow_unicode=True, default_flow_style=False))


def predict(row, tree_dict):
    key = list(tree_dict.keys())[0]
    val = row[key]

    if list(tree_dict[key][0].keys())[0] == str(val):
        next_node = tree_dict[key][0][str(val)]
    else:
        next_node = tree_dict[key][1][str(val)]
    if isinstance(next_node, str):
        return int(next_node)
    return predict(row, next_node)


def predict_tree(row, tree):
    key = tree.getData()
    val = row[key]

    if val == 0:
        if tree.getLeftChild() is None:
            return tree.getPrediction()
        return predict_tree(row, tree.getLeftChild())
    else:
        if tree.getRightChild() is None:
            return tree.getPrediction()
        return predict_tree(row, tree.getRightChild())


def find_accuracy(df, tree_dict, tree, data_type):
    predicted_output = df.apply(lambda row: predict(row, tree_dict), axis=1)  # rename to predicted_output
    #predicted_output_tree = df.apply(lambda row: predict_tree(row, tree), axis=1)
    count = 0
    given_output = df["Class"]
    for i in range(len(predicted_output)):
        if predicted_output[i] == given_output[i]:
            count += 1

    print("Number of ", data_type, " instances = %d" % len(df))
    print("Number of ", data_type, " attributes = %d" % (len(df.columns.values) - 1))
    print("Accuracy: %f" % (count / len(predicted_output) * 100))
