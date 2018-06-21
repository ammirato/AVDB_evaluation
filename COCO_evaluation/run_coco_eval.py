#!/usr/bin/python 

from cocoapi.PythonAPI.pycocotools.coco import COCO
from cocoapi.PythonAPI.pycocotools.cocoeval import COCOeval
import numpy as np
import os
import json

#SET THESE PATHS
gt_path = './GT/AVD_split1_test.json'
results_path = './my_results.json'
#gather the object instance ids
all_catIds = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
known_catIds = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
novel_catIds = [18,19,20,21,22,23,24,25,26,27]



iouThrs = .5
maxDets = [1,10,100]
#initialize COCO ground truth api
cocoGt=COCO(gt_path)
#initialize COCO detections api
cocoDt=cocoGt.loadRes(my_results.json)

annType = 'bbox' 
cocoEval = COCOeval(cocoGt,cocoDt,annType)
cocoEval.params.iouThrs = np.array([iouThrs])
cocoEval.params.maxDets = maxDets 
#cocoEval.params.areaRng = [[0, 10000000000.0], [416, 10000000000.0 ], [0, 416], [416, 1250], [1250, 3750], [3750, 7500], [7500,10000000000.0]]
#cocoEval.params.areaRngLbl = ['all', 'valid', 'l0', 'l1', 'l2', 'l3', 'l4']
cocoEval.params.areaRng = [[0, 10000000000.0]]
cocoEval.params.areaRngLbl = ['all']
cocoEval.params.useSegs = [0]



catIds_types = [all_catIds, known_catIds, novel_catIds]
results = []

for catIds in catIds_types:
    cocoEval.params.catIds = catIds 
    cocoEval.evaluate()
    cocoEval.accumulate()
    cocoEval.summarize()
    results.append(cocoEval.stats[1])

results = {'main':results[0], 'known': results[1], 'novel': results[2]}

print(results)

