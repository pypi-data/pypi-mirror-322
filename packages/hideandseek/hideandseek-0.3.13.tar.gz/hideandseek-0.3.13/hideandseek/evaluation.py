from copy import deepcopy as dcopy
import logging
import multiprocessing

import numpy as np
import sklearn.metrics as metrics
import torch

import tools as T
import tools.torch
import tools.numpy
import torch.utils.data as D

# %%
log = logging.getLogger(__name__)

# %%
'''
Testing functions

give x and produce y_hat, y_score, y_pred, etc...
'''
def transfer_misc(model, dataset, verbose=False):
    misc_temp = T.TDict()
    transfer_log = []

    if 'get_f' in model.misc:
        transfer_log.append('get_f')
        misc_temp.get_f, dataset.get_f = dataset.get_f, model.misc.get_f

    if len(transfer_log)!=0:
        log.info(f'Transferring misc from model ({model.name}) -> dataset: {transfer_log}')

    return dataset, misc_temp

def inverse_transfer_misc(misc_temp, dataset):
    transfer_log = []
    if 'get_f' in misc_temp:
        transfer_log.append('get_f')
        dataset.get_f = misc_temp.get_f

    if len(transfer_log)!=0:
        log.info(f'Inverse transferring misc -> dataset: {transfer_log}')

    return dataset

def reproducible_worker_dict():
    '''Generate separate random number generators for workers,
    so that the global random state is not consumed,
    thereby ensuring reproducibility'''
    import random
    def seed_worker(worker_id):
        worker_seed = torch.initial_seed() % 2**32
        np.random.seed(worker_seed)
        random.seed(worker_seed)

    g = torch.Generator()
    g.manual_seed(0)
    return {'worker_init_fn': seed_worker, 'generator': g}

# DEPRECATED: use get_forward_f instead
def _test_assertion(dataset, targets_type, forward_f, result_dict, keep_x):
    # Safety check
    if forward_f is not None and result_dict is not None:
        assert callable(forward_f) and issubclass(type(result_dict), dict), f'forward_f must be callable and result_dict must be dict-like'
    elif forward_f is None and result_dict is None:
        # Infer targets_type and create corresponding forward_f and result_dict
        if targets_type is None:
            if hasattr(dataset, 'targets_type'):
                targets_type = dataset.targets_type
            else:
                raise Exception('When forward_f and result_dict is not given, targets_type must be given or the dataset must have the attribute "targets_type"')
        forward_f, result_dict = get_forward_f(targets_type, keep_x=keep_x)
    else:
        raise Exception(f'forward_f and result_dict must either both be provided or None, received [forward_f: {forward_f}][result_dict: {result_dict}]')
    return forward_f, result_dict

# def forward_network(network, dataset, forward_f=None, batch_size=64, targets_type=None, result_dict=None, keep_x=False, num_workers=0, amp=False):
def forward_network(network, dataset, forward_f=None, batch_size=64, targets_type=None, num_workers=0, amp=False):
    """
    Forward pass of the network on the dataset.
    Takes care of device, dataloader, and mixed precision.
    
    Parameters
    ----------
    network: torch.nn.Module
        Network to be tested.
    dataset : torch.utils.data.Dataset
        Dataset to be tested.
    forward_f : callable, default=None
        Function to be tested.
        If None, it will be inferred from dataset.targets_type
        (Arguments: data, network, device)
        (Returns: dictionary of tensors or tuple of tensors)

    Returns
    -------
    result : ndarrays corresponding to the outputs from the forward_f 
        returns tuple or dict, based on forward_f return
    """

    # forward_f check
    # forward_f, result_dict = _test_assertion(dataset=dataset, targets_type=targets_type, forward_f=forward_f, result_dict=result_dict, keep_x=keep_x)
    if forward_f is None:
        if targets_type is None:
            if hasattr(dataset, 'targets_type'):
                targets_type = dataset.targets_type
            else:
                raise Exception('When forward_f and result_dict is not given, targets_type must be given or the dataset must have the attribute "targets_type"') 
        forward_f = get_forward_f(targets_type)

    device = T.torch.get_device(network) # Test on the network's device
    network.eval()

    # dataset, misc_temp = transfer_misc(node, dataset) # Assume the dataset is consistent
    kwargs_dataloader = reproducible_worker_dict()
    test_loader = D.DataLoader(dataset, batch_size=batch_size, shuffle=False, drop_last=False, num_workers=num_workers, **kwargs_dataloader)

    l_results = []
    with torch.no_grad():
        # Mixed precision for acceleration
        if amp:
            with torch.autocast(device_type=device.type):
                for data in test_loader:
                    data = T.torch.to(data, device)
                    result = forward_f(network=network, data=data)
                    result = T.torch.to(result, device='cpu')
                    l_results.append(result)
        else:
            for data in test_loader:
                data = T.torch.to(data, device)
                result = forward_f(network=network, data=data)
                result = T.torch.to(result, device='cpu')
                l_results.append(result)

    # Formatting: Concatenate, (optional amp), numpy
    if isinstance(result, dict): 
        result = T.merge_dict(l_results)
        result = {k: torch.cat(v, dim=0) if len(v)>0 else v for k, v in result.items()}
        if amp: result = {k: v.to(torch.float16) for k, v in result}
        result = {k: v.numpy() for k, v in result.items()}
    elif isinstance(result, (list, tuple)):
        result = T.merge_tuple(l_results)
        result = tuple(torch.cat(v, dim=0) if len(v)>0 else v for v in result)
        if amp: result = tuple(v.to(torch.float16) for v in result)
        result = tuple(v.numpy() for v in result)
    elif isinstance(result, torch.Tensor): # Single tensor return
        result = torch.cat(l_results, dim=0)
        if amp: result = result.to(torch.float16)
        result = result.numpy()
    else:
        raise Exception(f'Unknown data type from forward_f return: {type(result)}')

    return result

def forward_model(model, dataset, forward_f=None, batch_size=64, targets_type=None, num_workers=0, amp=False):
    '''
    wrapper around model.
    transfers get_f (preprocessing modules) of model to dataset, and returns them to original dataset after inference.
    '''
    network = model.network
    dataset, misc_temp = transfer_misc(model, dataset)
    result = forward_network(network=network, dataset=dataset, forward_f=forward_f, batch_size=batch_size, targets_type=targets_type, num_workers=num_workers, amp=amp)
    dataset = inverse_transfer_misc(misc_temp, dataset)

    return result

def evaluate(result, metrics):
    if isinstance(metrics, dict):
        scores = {}
        for metric_name, metric in metrics.items():
            if isinstance(result, dict):
                scores[metric_name] = metric(**result)
            elif isinstance(result, (list, tuple)):
                scores[metric_name] = metric(*result)
            else:
                scores[metric_name] = metric(result)
    elif isinstance(metrics, (list, tuple)):
        if isinstance(result, dict):
            scores = [metric(**result) for metric in metrics]
        elif isinstance(result, (list, tuple)):
            scores = [metric(*result) for metric in metrics]
        else:
            scores = [metric(result) for metric in metrics]
    else:
        if isinstance(result, dict):
            scores = metrics(**result)
        elif isinstance(result, (list, tuple)):
            scores = metrics(*result)
        else:
            scores = metrics(result)
    return scores

targets_type_list = [None, 'categorical', 'multihead_classification', 'autoencode', 'regression'] # move this to utils?
def get_forward_f(targets_type):
    assert targets_type in targets_type_list, f'targets_type must be one of {targets_type_list}, received: {targets_type}'
    if targets_type is None or targets_type == 'regression':
        forward_f = _forward_base
        result_keys = ['y_true', 'y_pred']
    elif targets_type == 'categorical':
        forward_f = _forward_categorical
        result_keys = ['y_true', 'y_hat', 'y_score', 'y_pred'] # y_hat vs y_logit?
    elif targets_type == 'multihead_classification':
        forward_f = _forward_multihead_categorical
        result_keys = ['y_true', 'y_hat', 'y_score', 'y_pred']
    elif targets_type == 'autoencode':
        forward_f = _forward_autoencode
        result_keys = ['x', 'z', 'x_hat']
    else:
        raise Exception(f'unknown targets_type: {targets_type}')
    
    log.info(f'get_forward_f: targets_type: {targets_type}, keys in result (dict): {result_keys}')

    return forward_f

def _forward_base(network, data):
    # device = device if device is not None else T.torch.get_device(network)
    x = data['x']
    y = data['y']
    y_pred = network(x)

    result_dict = {
        'y_true': y,
        'y_pred': y_pred
    }
    # if keep_x: result_dict['x'] = x
    return result_dict

def _forward_categorical(network, data):
    # Is y_hat necessary? for torch_crossentropyloss? any other methods?
    x = data['x']
    y = data['y']
    y_hat = network(x)
    y_score = torch.softmax(y_hat, dim=1) # (N, n_classes)

    result_dict = {
        'y_true': y,
        'y_hat': y_hat,
        'y_score': y_score,
        'y_pred': y_score.argmax(axis=1)
    }
    # if keep_x: result_dict['x'] = x
    return result_dict

def _forward_multihead_categorical(network, data):
    x = data['x']
    y = data['y']
    y_hat = network(x)
    y_score = torch.softmax(y_hat, dim=-1) # (N, subtype, n_classes)

    result_dict = {
        'y_true': y,
        'y_hat': y_hat,
        'y_score': y_score,
        'y_pred': y_score.argmax(axis=-1)
    }
    # if keep_x: result_dict['x'] = x
    return result_dict

def _forward_autoencode(network, data):
    x = data['x']
    z = network.encoder(x)
    x_hat = torch.sigmoid(network.decoder(z))

    result_dict = {
        'x': x,
        'z': z,
        'x_hat': x_hat
    }
    return result_dict

# %%
'''
Scorers

They all receive dict of numpy arrays.
Predefined keys are:
'y_true', 'y_hat', 'y_pred'

Example
-------
result = {'y_true': y_true, 'y_pred': y_pred}
classification_score(result)

scores = {'scorer type': score, ...}


# order of arguments follow sklearn convention: y_true, y_hat/pred

Note
----
pytorch metrics receive (y_hat/pred, y_true), whereas sklearn receive (y_true, y_hat/pred)
'''

# Regresison scorers
def l1_score(result): # alias
    return metrics.mean_absolute_error(result['y_true'], result['y_hat'])

def l2_score(result): # alias
    return metrics.mean_squared_error(result['y_true'], result['y_hat'])

def mse_score(result): # alias
    return metrics.mean_squared_error(result['y_true'], result['y_hat'])

def r2_score(result):
    return metrics.r2_score(result['y_true'], result['y_hat'])

def p_norm_score(result, p=2): # When using this with Validation object, use functools.partial() to fix ``p``
    score = ((np.abs(result['y_hat']-result['y_true'])**p).sum())**(1/p)
    return score

# Classification score
def accuracy_score(result):
    return metrics.accuracy_score(result['y_true'], result['y_pred'])

# def accuracy_score_y_hat(result): # Use this for Validation object, which feeds y_hat to all of its scorers.
#     return metrics.accuracy_score(result['y_true'], result['y_hat'].argmax(axis=1))

# Binary classification
def sensitivity_score(result): # alias
    '''sensitivity == recall == tpr'''
    return metrics.recall_score(result['y_true'], result['y_pred'])

def specificity_score(result):
    (tn, fp), (fn, tp) = metrics.confusion_matrix(result['y_true'], result['y_pred'])
    if (tn+fp)==0:
        warnings.warn('invalid value in specificity_score, setting to 0.0')
        return 0
    return tn / (tn+fp)

# Multiclass classification
def classification_report_full(result, ovr=True):
    '''
    Adds additional metrics to sklearn.classification_report
    '''
    y_score = result['y_score'] if 'y_score' in result else None
    y_true, y_pred = result['y_true'], result['y_pred']
    
    scores = metrics.classification_report(y_true, y_pred, output_dict=True)
    scores['mcc'] = metrics.matthews_corrcoef(y_true, y_pred)

    if ovr:
        scores_ovr = {k:dcopy(v) for k, v in scores.items() if k.isnumeric()}
        scores_all = {k:dcopy(v) for k, v in scores.items() if not k.isnumeric()}

        more_scorers_y_pred = {'sensitivity': sensitivity_score, 'specificity': specificity_score, 'accuracy': accuracy_score} # Optimize to reduce redundant computations?
        more_scorers_y_score = {}

        # Additional metrics
        for c in scores_ovr.keys():
            c_int = int(c)
            y_true__c, y_pred_c = y_true==c_int, y_pred==c_int
            for scorer_name, scorer in more_scorers_y_pred.items():
                scores_ovr[c][scorer_name] = scorer({'y_true': y_true__c, 'y_pred': y_pred_c})

        if y_score is not None:
            more_scorers_y_score['auroc'] = metrics.roc_auc_score
            for c in scores_ovr.keys():
                c_int = int(c)
                y_true_ = y_true==c_int
                y_score_ = y_score[:, c_int]
                for scorer_name, scorer in more_scorers_y_score.items():
                    scores_ovr[c][scorer_name] = scorer(y_true_, y_score_)

        # summary
        more_scorers = list(more_scorers_y_pred.keys()) + list(more_scorers_y_score.keys())
        for scorer_name in more_scorers:
            scores_all['macro avg'][scorer_name] = np.mean([scores_ovr_[scorer_name] for scores_ovr_ in scores_ovr.values()])
            scores_all['weighted avg'][scorer_name] = np.sum([scores_ovr_[scorer_name]*scores_ovr_['support'] for scores_ovr_ in scores_ovr.values()]) / scores_all['weighted avg']['support']

        scores.update(scores_ovr)
        scores.update(scores_all)

    return scores

# Multihead classification score
def multihead_accuracy_score(y_pred, y):
    '''
    :param y_pred: array of shape (N, subtype)
    :param y: array of shape (N, subtype)
    '''
    assert y_pred.ndim==2 and y.ndim==2
    score = [accuracy_score(y_pred_, y_) for y_pred_, y_ in zip(y_pred.T, y.T)]
    score = np.mean(score)
    return score

def multihead_accuracy_score_score(y_score, y):
    '''
    :param y_pred: array of shape (N, subtype, n_classes)
    :param y: array of shape (N, subtype)
    '''
    assert y_score.ndim==3 and y.ndim==2
    y_pred = y_score.argmax(axis=-1)
    return multihead_accuracy_score(y_pred, y)

# %%
# All scores for each task type
def regression_score(result):
    '''
    :param result: dict with the following keys: [y_hat, y]
    '''
    y_hat, y = result['y_hat'], result['y']
    l1 = l1_score(y_hat, y)
    mse = mse_score(y_hat, y)
    r2 = r2_score(y_hat, y)

    scores = {
    'l1': l1,
    'mse': mse,
    'r2': r2
    }

    return scores

def classification_score(result, multi_class='ovr', discard_ovr=False):
    '''
    :param result: dict with the following keys: [y_pred, y_score, y]


    y_score: array of shape (N, n_classes)
    y: array of shape (N,)
    '''
    y_pred, y_score, y_true = result['y_pred'], result['y_score'], result['y']

    # classification_result = classification_report_full(y_true, y_pred, discard_ovr=discard_ovr)
    classification_result = classification_report_full(result, discard_ovr=discard_ovr)
    auroc = metrics.roc_auc_score(y_true, y_score, multi_class=multi_class)
    kappa = metrics.cohen_kappa_score(y_true, y_pred)
    m_cc = metrics.matthews_corrcoef(y_true, y_pred)
    c_matrix = metrics.confusion_matrix(y_true, y_pred)

    scores = {
    'auroc': auroc,
    'kappa': kappa,
    'm_cc': m_cc,
    'c_matrix': c_matrix,
    }
    classification_result.update(scores)
    return scores

def multihead_classification_score(result):
    '''
    :param result: dict with the following keys: [y_pred, y_score, y]


    y_score: array of shape (N, subtype, n_classes)
    y: array of shape (N, subtype)
    '''
    y_pred, y_score, y = result['y_pred'], result['y_score'], result['y']
    multihead_accuracy = multihead_accuracy_score(y_pred, y)

    scores = {
    'multihead_accuracy_score': multihead_accuracy
    }
    return scores


# Wrapper function for hydra.utils.instantiate
class Score_wrapper:
    '''
    wraps around scorers to:
    1. instantiate an object using hydra.utils.instantiate()
    2. adjust scorer functions such that raw input can be delivered to scorer functions (y_pred or y_score can be delivered to any type of scorers)
    '''
    f_dict = {
    # regression
    'l1_score': l1_score,
    'mse_score': mse_score,
    'r2_score': r2_score,

    # multihead classification
    'multihead_accuracy_score': multihead_accuracy_score_score,
    }
    def __init__(self, func):
        self.func = self.f_dict[func]

    def __call__(self, y_hat, y):
        return self.func(y_hat, y)
# %%
'''
May be deprecated
'''
def save_score():
    f

def _pr_score(y_true, y_score, threshold):
    y_pred = T.numpy.binarize(y_score, threshold)
    pr = metrics.precision_score(y_true, y_pred)
    rec = metrics.recall_score(y_true, y_pred)
    return pr, rec

def precision_recall_curve_all(y_true, y_score, num_workers=None):
    '''
    compute precision-recall curve for all threshold.
    Because sklearn.metrics.precision_recall_curve does not return full set of thresholds
    sklearn drops the results after when recall hits 1.

    -> is this function really necessary?
    -> may be deprecated
    '''
    thresholds = np.sort(np.unique(y_score)) # increasing threshold
    thresholds = np.append(thresholds,1) # Since tnp.binarize binarizes with y_pred[y_score>=threshold] == 1
    if num_workers==0:
        prs, recs = [], []
        for t in thresholds:
            y_pred = T.numpy.binarize(y_score, threshold)
            prs.append(metrics.precision_score(y_true, y_pred))
            recs.append(metrics.recall_score(y_true, y_pred))
    elif num_workers is None or T.isint(num_workers):
        with multiprocessing.Pool() as p:
            l_pr = p.starmap(_pr_score, zip(it.repeat(y_true, len(thresholds)), it.repeat(y_score, len(thresholds)), thresholds))

    return prs, recs, thresholds
