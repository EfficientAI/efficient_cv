import os
import numpy as np

def parse_comet_config(configs):
    """
    retrives vizier compatible configuration(only descrete values are supported)
    used for creating a comet.ml configuration dictionary
    """
    params = {}
    for k in configs.keys():
        if type(configs[k]) == list:
            params[k] = {'type': 'discrete', 'values': configs[k]}
    vizier_config = {'algorithm': configs['algorithm'],
                     'parameters': params,
                     'spec': {'metric': configs['metric'],
                     'maxCombo':configs['maxCombo'] ,
                     'objective': configs['objective']}
                     }
    return vizier_config

def get_parameters(comet_experiment, configs):
    """
    Get parameters from comet_experiment
    these parameters are corresponds to hp mentioned in configs
    """
    cf = {}
    for k in configs.keys():
        if type(configs[k]) == list:
            cf[k] = comet_experiment.get_parameter(k)
        else:
            cf[k] = configs[k]
    return cf

def get_configurations(configs):
    """
    Builds a list of all possible configuration dictionary
    from one configuration dictionary that contains all values for a key
    """
    all_configs = []
    config_keys = list(configs.keys())
    def recursive_config_list_builder(param_type_index, current_param_dict,
                                                                    param_list):
        if param_type_index == len(param_list):
            all_configs.append(current_param_dict)
        else:
            if type(configs[config_keys[param_type_index]]) == list:
                for val in configs[param_list[param_type_index]]:
                    temp = current_param_dict.copy()
                    temp[param_list[param_type_index]] = val
                    recursive_config_list_builder(param_type_index+1, temp, 
                                                                     param_list)
            else:
                temp = current_param_dict.copy()
                temp[param_list[param_type_index]] = \
                                          configs[config_keys[param_type_index]]
                recursive_config_list_builder(param_type_index+1, temp,
                                                                     param_list)

    recursive_config_list_builder(0, dict(), config_keys)
    return all_configs

def hit_refresh():
    e = os.path.isfile("refresh")
    if e:
        os.remove("refresh")
        return True
    else:
        return False

def stringify(vals):
    """
    return a string version of vals (a list of object implementing __str__)
    return type: 'val1_val2_val3_ ... _valn'
    """
    return '_'.join([str(e) for e in vals])

def valuefy(strings, type_cast = None):
    """
    return a list of value, type casted by type_cast list
    return type: list if values
    By default, type cast is int
    """
    vals_string = strings.split('_')
    if type_cast == None:
        type_cast = [int]*len(vals_string)
    return [t(e) for e,t in zip(vals_string, type_cast)]

def folder_exists(path):
    """
    Makes folder iteratively, if it already does not exists
    There is no output.
    """
    try:
        os.makedirs(path)    
    except FileExistsError:
        pass

def generate_permulations(param_list):
    """
    param_list is a list(types of parameter) of list(possible parameter values).
    returns a list(all permulation) of list(parameter value) in same order
    as in param_list
    """
    permu = []
    def recurse(param_type_index, current_param_value, param_list):
        if param_type_index == len(param_list):
            permu.append(current_param_value)
        else:
            for val in param_list[param_type_index]:
                temp = current_param_value.copy()
                temp.append(val)
                recurse(param_type_index+1, temp, param_list)
    recurse(0, [], param_list)
    return permu

################################### Test #######################################
def test_generate_permulations():
    a = [[1,2], ['a', 'b'], ["String1", "String2", "String3"]]
    b = generate_permulations(a)
    print(b)

def test_folder_exists():
    path = '/home/vishal/test_folder/test'
    folder_exists(path)

def test_stringify():
    a = ['abc', 34, 1.89, 'c']
    b = stringify(a)
    print(b)

def test_valuefy():
    a = '34_1.28_500_str'
    b = valuefy(a, [int, float, int, str])
    print(b)

def test_parse_comet_config():
    config={
        'project_name': 'project',
        'workspace': 'workspace',
        ############## USE LISTS FOR HP ##############
        'learning_rate': [0.0001, 0.00001],
        'nr_epochs': [100, 200],
        'batch_size': [8, 16],
        ##############################################
        'metric': 'loss',
        'objective': 'maximize',
        'algorithm': 'bayes'
    }
    vizier_config = parse_comet_config(config)
    print(vizier_config)

def test_get_parameters():
    # No test
    pass

def test_get_configurations():
    configs={
        'project_name': 'wesad',
        'workspace': 'vishal-keshav',
        ############## USE LISTS FOR HP ##############
        'learning_rate': [0.0001, 0.00001],
        'nr_epochs': [100, 200,500],
        'batch_size': [8, 16],
        ##############################################
        'metric': 'loss',
        'objective': 'maximize',
        'algorithm': 'bayes'
    }
    all_configs = get_configurations(configs)
    for config in all_configs:
        print(config)
        print()

if __name__ == "__main__":
    pass