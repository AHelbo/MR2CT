from functools import partial
import numpy as np

from torch.utils.data.distributed import DistributedSampler
from torch import Generator, randperm
from torch.utils.data import DataLoader, Subset

import core.util as Util
from core.praser import init_obj

def define_dataloader(logger, opt, nc = -1, is_val = False):
    """ create train/test dataloader and validation dataloader,  validation dataloader is None when phase is test or not GPU 0 """
    '''create dataset and set random seed'''
    dataloader_args = opt['datasets'][opt['phase']]['dataloader']['args']
    worker_init_fn = partial(Util.set_seed, gl_seed=opt['seed'])

    phase_dataset = define_dataset(logger, opt, nc)

    '''create datasampler'''
    data_sampler = None
    if opt['distributed'] and not is_val:
        data_sampler = DistributedSampler(phase_dataset, shuffle=dataloader_args.get('shuffle', False), num_replicas=opt['world_size'], rank=opt['global_rank'])
        dataloader_args.update({'shuffle':False}) # sampler option is mutually exclusive with shuffle 
    
    ''' create dataloader'''
    dataloader = DataLoader(phase_dataset, sampler=data_sampler, worker_init_fn=worker_init_fn, **dataloader_args)

    return dataloader


def define_dataset(logger, opt, nc = -1):
    ''' loading Dataset() class from given file's name '''
    dataset_opt = opt['datasets'][opt['phase']]['which_dataset']

    phase_dataset = init_obj(dataset_opt, logger, default_file_name='data.dataset', init_type='Dataset')

    phase_dataset.set_in_channel

    if (nc != -1):
        phase_dataset.set_in_channel(nc)
         
    data_len = len(phase_dataset)
    
    logger.info('Dataset for {} have {} samples.'.format(opt['phase'], data_len))
    
    return phase_dataset
