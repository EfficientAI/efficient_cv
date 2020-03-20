# The main run file
# command: python3 run.py --configs default --trainer default --dataset default --model default --experiment 1

from comet_ml import Experiment
from comet_ml import Optimizer
import argparse
import importlib

from utils.utils import parse_comet_config
from utils.utils import get_parameters
from utils.utils import get_configurations

def argument_parser():
    parser = argparse.ArgumentParser(description="sample")
    parser.add_argument('--config', default='default', type=str, help='config')
    parser.add_argument('--trainer', default='default', type=str,help='trainer')
    parser.add_argument('--dataset', default='default', type=str,help='dataset')
    parser.add_argument('--model', default='default', type=str, help='model')
    parser.add_argument('--experiment', default=0, type=int, help='comet.ml')
    args = parser.parse_args()
    return args

def main():
    global model_def
    global dataset
    global train
    args = argument_parser()
    config_module = importlib.import_module("configs."+args.config)
    configs = config_module.config
    model_def = importlib.import_module("model."+args.model).model
    dataset = importlib.import_module("dataset."+args.dataset).dataset
    train = importlib.import_module("trainer."+args.trainer).train

    if 'algorithm' in configs.keys():
        comet_config = parse_comet_config(configs)
        opt = Optimizer(comet_config, api_key=configs['API_KEY'], 
                                      project_name=configs['project_name'])
        for exp in opt.get_experiments():
            experiment = exp
            config = get_parameters(experiment, configs)
            train(**{'config':config, 'model_def':model_def, 'dataset':dataset, 
                                                      'experiment': experiment})
    else:
        if args.experiment:
            experiment = Experiment(api_key=configs['API_KEY'],
                                    project_name=configs['project_name'], 
                                    workspace=configs['workspace'])
        else:
            experiment = None
        tried_configs = []
        end = False
        while True:
            importlib.reload(config_module)
            configs = config_module.config
            possible_configs = get_configurations(configs)
            for config_idx, config in enumerate(possible_configs):
                if config_idx == len(possible_configs)-1:
                    end = True
                if config in tried_configs:
                    continue
                else:
                    tried_configs.append(config)
                    train(**{'config':config, 'model_def':model_def, 
                                    'dataset':dataset, 'experiment':experiment})
                    break
            if end:
                break
        print("*******************End of the training session*****************")

main()