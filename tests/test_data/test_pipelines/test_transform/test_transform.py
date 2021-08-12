import copy
import os.path as osp

import numpy as np
import pytest

from mmcv.datasets import PIPELINES
from mmcv.image import imread
from mmcv.utils import build_from_cfg


@pytest.mark.parametrize('to_rgb', [True, False])
def test_normalize(to_rgb):
    img_norm_cfg = dict(
        mean=[123.675, 116.28, 103.53],
        std=[58.395, 57.12, 57.375],
        to_rgb=to_rgb)
    results = dict()
    img = imread(
        osp.join(osp.dirname(__file__), '../../../data/color.jpg'), 'color')
    original_img = copy.deepcopy(img)
    results['img'] = img
    results['img2'] = copy.deepcopy(img)
    results['img_shape'] = img.shape
    results['ori_shape'] = img.shape
    # Set initial values for default meta_keys
    results['pad_shape'] = img.shape
    results['scale_factor'] = 1.0

    transform_cfg = dict(type='Normalize', **img_norm_cfg)
    transform = build_from_cfg(transform_cfg, PIPELINES)

    with pytest.raises(AssertionError):
        # Required key of results is 'img_fields'
        results = transform(results)

    results['img_fields'] = ['img', 'img2']
    results = transform(results)
    assert np.equal(results['img'], results['img2']).all()

    mean = np.array(img_norm_cfg['mean'])
    std = np.array(img_norm_cfg['std'])
    if to_rgb:
        original_img = original_img[..., ::-1]
    converted_img = (original_img - mean) / std
    assert np.allclose(results['img'], converted_img)
