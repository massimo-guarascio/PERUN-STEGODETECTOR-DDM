import json
import os
import sys
import numpy as np
import torch
from src.dataset.dataset_loader import load_dataset, get_dataloaders
from src.arn.trainer import ARN
import time
from src.support.arguments import parse_arguments
from src.support.utils import set_reproducibility, print_args


def run(params, args):
    attack_type = params['attack_type']

    n_runs = params['n_runs']
    if 'start_runs'  in params:
        start_runs = params['start_runs']
    else:
        start_runs = 0

    seed = params['seed']

    for i in range(start_runs, n_runs):
        print(f'Iteration: {i}')
        params['seed'] = seed*(i+1)
        x_train_unsupervised,x_train_few_shot, y_train_few_shot, x_test, y_test = load_dataset(args)
        train_loader, _, test_loader = get_dataloaders(x_train_unsupervised, x_train_few_shot,y_train_few_shot,
                                                                                        x_test, y_test, args)

        model = ARN(params)

        name_G = f'ARN_Generator_{attack_type}_{i}.ckpt'
        name_D = f'ARN_Discriminator_{attack_type}_{i}.ckpt'

        path_G = os.path.join(params['SAVE_FOLDER'], 'models', name_G)
        path_D = os.path.join(params['SAVE_FOLDER'], 'models', name_D)

        name_G = f'ARN_Generator_{attack_type}_{i}_best.ckpt'
        name_D = f'ARN_Discriminator_{attack_type}_{i}_best.ckpt'

        path_best_G = os.path.join(params['SAVE_FOLDER'], 'models', name_G)
        path_best_D = os.path.join(params['SAVE_FOLDER'], 'models', name_D)

        ### Training ###
        start_time = time.time()
        _ = model.train(train_loader, path_G, path_D, batch_size=params['batch_size'],
                        num_epochs=params['num_epochs'], num_q_steps=5,
                        path_best_G=path_best_G, path_best_D=path_best_D)
        end_time = time.time()
        print((end_time-start_time)/60)
    

def main():
    args = parse_arguments()
    print_args(args)

    params = vars(args)
    seed = params['seed']
    set_reproducibility(seed)

    device = torch.device('cuda' if (torch.cuda.is_available()) else 'cpu')
    print(f'Device: {device}')

    os.makedirs(params['SAVE_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(params['SAVE_FOLDER'], 'models'), exist_ok=True)

    params['device'] = device
    params['seed'] = 42

    x_train_unsupervised, _, _, _, _ = load_dataset(args)

    params['show'] = False
    params['nc'] = x_train_unsupervised.shape[1]
    print(params['nc'])

    run(params, args)

if __name__ == '__main__':
    main()

