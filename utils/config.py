import os
import yaml
from easydict import EasyDict
from utils.utils import mkdir_if_missing

def create_config(config_file_env, config_file_exp, meta_info=None):
    # Config for environment path
    with open(config_file_env, 'r') as stream:
        root_dir = yaml.safe_load(stream)['root_dir']
   
    with open(config_file_exp, 'r') as stream:
        config = yaml.safe_load(stream)
    
    cfg = EasyDict()
   
    # Copy
    for k, v in config.items():
        cfg[k] = v

    # Set paths for pretext task (These directories are needed in every stage)
    base_dir = os.path.join(root_dir, cfg['train_db_name'])
    pretext_dir = os.path.join(base_dir, 'pretext')
    noise_specific = ''
    if cfg['to_noisy_dataset']:
        noise_specific = 'r={}_{}'.format(meta_info['r'], meta_info['noise_mode'])
    mkdir_if_missing(base_dir)
    mkdir_if_missing(pretext_dir)
    cfg['pretext_dir'] = pretext_dir
    cfg['pretext_checkpoint'] = os.path.join(pretext_dir, 'checkpoint.pth.tar')
    cfg['pretext_model'] = os.path.join(pretext_dir, 'model.pth.tar')
    cfg['topk_neighbors_train_path'] = os.path.join(pretext_dir, 'topk-train-neighbors.npy')
    cfg['topk_neighbors_val_path'] = os.path.join(pretext_dir, 'topk-val-neighbors.npy')

    # if cfg['setup'] in ['scanmix']:
    #     cfg['topk_neighbors_train_path'] = os.path.join(base_dir, 'scanmix/topk-train-neighbors.npy')
    #     cfg['topk_neighbors_val_path'] = None

    if cfg['setup'] in ['scan', 'selflabel', 'dividemix', 'scanmix']:
        base_dir = os.path.join(root_dir, cfg['train_db_name'])
        scan_dir = os.path.join(base_dir, 'scan')
        selflabel_dir = os.path.join(base_dir, 'selflabel') 
        dividemix_dir = os.path.join(base_dir, 'dividemix')
        scanmix_dir = os.path.join(base_dir, 'scanmix')
        scanmix_dir = os.path.join(scanmix_dir, noise_specific)
        mkdir_if_missing(base_dir)
        mkdir_if_missing(scan_dir)
        mkdir_if_missing(selflabel_dir)
        cfg['base_dir'] = os.path.join(base_dir)
        cfg['scan_dir'] = scan_dir
        cfg['scan_checkpoint'] = os.path.join(scan_dir, 'checkpoint.pth.tar')
        cfg['scan_model'] = os.path.join(scan_dir, 'model.pth.tar')
        cfg['selflabel_dir'] = selflabel_dir
        cfg['selflabel_checkpoint'] = os.path.join(selflabel_dir, 'checkpoint.pth.tar')
        cfg['selflabel_model'] = os.path.join(selflabel_dir, 'model.pth.tar')
        cfg['scanmix_dir'] = os.path.join(scanmix_dir)
        cfg['scanmix_checkpoint'] = os.path.join(scanmix_dir, 'checkpoint.pth.tar')
        cfg['scanmix_model'] = os.path.join(scanmix_dir, 'model.pth.tar')

    return cfg
