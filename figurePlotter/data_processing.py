import pandas as pd
import numpy as np


def merge_columns(data, configs_groups, configs_groups_names):
    assert len(configs_groups) == len(configs_groups_names)
    column_names = data.keys().values.tolist()
    for i in range(0, len(configs_groups)):
        data_selected_keys = []
        print("configs_groups[i]:", configs_groups[i])
        for keyword in configs_groups[i]:
            for column_name in column_names:
                if keyword in column_name:
                    data_selected_keys.append(column_name)
                    break
        print(data_selected_keys)
        assert len(data_selected_keys) <= len(configs_groups[i])
        data[configs_groups_names[i]] = (
            data[data_selected_keys].where(data[data_selected_keys] > 0).max(axis=1)
        )
    return data


def merge_columns_mean(data, configs_groups, configs_groups_names):
    assert len(configs_groups) == len(configs_groups_names)
    column_names = data.keys().values.tolist()
    for i in range(0, len(configs_groups)):
        data_selected_keys = []
        print("configs_groups[i]:", configs_groups[i])
        for keyword in configs_groups[i]:
            for column_name in column_names:
                if keyword in column_name:
                    data_selected_keys.append(column_name)
                    break
        print(data_selected_keys)
        assert len(data_selected_keys) <= len(configs_groups[i])
        data[configs_groups_names[i]] = (
            data[data_selected_keys].where(data[data_selected_keys] > 0).mean(axis=1)
        )
    return data


def merge_columns_min(data, configs_groups, configs_groups_names):
    assert len(configs_groups) == len(configs_groups_names)
    column_names = data.keys().values.tolist()
    for i in range(0, len(configs_groups)):
        data_selected_keys = []
        print("configs_groups[i]:", configs_groups[i])
        for keyword in configs_groups[i]:
            for column_name in column_names:
                if keyword in column_name:
                    data_selected_keys.append(column_name)
                    break
        print(data_selected_keys)
        assert len(data_selected_keys) <= len(configs_groups[i])
        data[configs_groups_names[i]] = (
            data[data_selected_keys].where(data[data_selected_keys] > 0).min(axis=1)
        )
    return data


def exclude_and_sort_data(data, row_dict, column_dict):
    # sort by column name
    # add order-row
    if column_dict != None:
        order_row = {}
        column_names = data.keys().values.tolist()
        for column_name in column_names:
            order_row_value = -1
            for column_name_keyword in list(column_dict.keys()):
                if column_name_keyword in column_name:
                    order_row_value = column_dict[column_name_keyword][1]
                    break
            order_row[column_name] = order_row_value
        data.loc["order"] = pd.DataFrame(order_row, index=[0]).loc[0]
        # sort by order row
        data = data.sort_values(by="order", axis=1, ascending=True)
        # remove excluded column
        data = data.loc[:, data.loc["order"] >= 0]
        # remove order row
        data = data.drop(labels="order")

    if row_dict != None:
        # sort by row name
        # add order-column
        order_column = []
        row_names = data.index.tolist()
        for row_name in row_names:
            order_column_value = -1
            for row_name_keyword in list(row_dict.keys()):
                if row_name_keyword in row_name:
                    order_column_value = row_dict[row_name_keyword][1]
                    break
            order_column.append(order_column_value)
        data["order"] = order_column
        # sort by order column
        data = data.sort_values(by=["order"], ascending=True)
        # remove excluded row
        data = data[data.order >= 0]
        # remove order column
        data = data.drop(columns=["order"])
    return data


def rename_data(data, row_dict, column_dict):
    # rename column name
    if column_dict != None:
        old_column_names = data.keys().values.tolist()
        new_column_name_dict = {}
        for old_column_name in old_column_names:
            new_column_name = old_column_name
            for column_name_keyword in list(column_dict.keys()):
                if column_name_keyword in old_column_name:
                    new_column_name = column_dict[column_name_keyword][0]
                    break
            new_column_name_dict[old_column_name] = new_column_name
        data = data.rename(columns=new_column_name_dict)
    # rename row name
    if row_dict != None:
        old_row_names = data.index.tolist()
        new_row_name_dict = {}
        for old_row_name in old_row_names:
            new_row_name = old_row_name
            for row_name_keyword in list(row_dict.keys()):
                if row_name_keyword in old_row_name:
                    new_row_name = row_dict[row_name_keyword][0]
                    break
            new_row_name_dict[old_row_name] = new_row_name
        data = data.rename(index=new_row_name_dict)
    return data


def geo_mean(input_list):
    cleaned_input = [x for x in input_list if str(x) != "nan"]
    if len(cleaned_input) < len(input_list):
        print("WARNING: geo_mean: NaN in data")
    assert len(cleaned_input) > 0
    a = np.log(cleaned_input)
    return np.exp(a.mean())
