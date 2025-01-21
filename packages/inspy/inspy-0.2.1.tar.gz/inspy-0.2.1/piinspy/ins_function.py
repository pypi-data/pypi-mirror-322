# -*- encoding: utf-8 -*-
"""
    @File : ins_function.py \n
    @Contact : yafei.wang@pisemi.com \n
    @License: (C)Copyright {} \n
    @Modify Time: 2023/11/20 10:04 \n
    @Author : Pisemi Yafei Wang \n
    @Version: 1.0 \n
    @Description : None \n
    @Create Time: 2023/11/20 10:04 \n
"""

import json
import os
import importlib.resources


def register_function(pInsType, pInsName):
    """
    register the instrument function
    :param pInsType: instrument type
    :param pInsName: instrument name
    :return: command
    """

    # # Get the path of the current file
    # current_file = os.path.realpath(__file__)
    #
    # # Get the directory containing the current file
    # current_dir = os.path.dirname(current_file)
    #
    # # Construct the path to the JSON file
    # json_file = os.path.join(current_dir, 'ins.json')
    #
    # # Read and parse the JSON file
    # with open(json_file, 'r') as f:
    #     command1 = json.load(f)

    try:
        with importlib.resources.open_text(__package__, 'ins.json') as f:
            command = json.load(f)
    except FileNotFoundError:
        print("JSON file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
        return None

    # print(command1)
    # print(command)

    for i in command.keys():
        if pInsType == i:
            for j in command[i].keys():
                if pInsName[:3] in j:
                    print(command[i][j])
                    return command[i][j]

    print("No matching instrument found.")
    return None