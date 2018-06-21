# AVDB evaluation
Here we provide instructions and code for running evaluations for the tasks in [AVDB](http://cs.unc.edu/~ammirato/active_vision_dataset_website/avdb.html)




## Active Object Search (AOS) Evalution
See `AOS_eval.py`

See `AOS_random_baseline` for an example of using the [gym-AVD](https://github.com/ammirato/gym_AVD) environment to produce outputs for evaluation. The evaluation expects a single file that holds a models chosen paths from each starting image to a destination image for the object of interest. The format of the file is as follows:

- `A json file holding a single Dict with Keys=scene-names Values=`
-     `a Dict with Keys=object ids Values=`
-         `a Dict with Keys=inital-image-name Values=PATH`

Where PATH is a list of integers, where each integer represent an action taken. The mapping from integers to actions is:

- 0:forward
- 1:backward
- 2:rotate-cw
- 3:rotate-ccw

(we do not allow right and left movement)
 
The evaluation first checks to make sure the path is valid from starting image to destination, so it is fine to output noisy paths.  

`AOS_eval` computes 3 evaluation metrics:
1. Success rate: how often a destination image is reached
2. Average path length of successful episodes
3. Average (shortest path length)/(model path length) of successful episodes. This has a max of 1, higher is better, and is useful for comparing across different 
cenes of different sizes. 



## Object Detection
We use the MSCOCO evaluation code to compute the mAP metric for object detection.

1. Build the coco evaluation cython code 
```
cd COCO_evaluation/cocoapi/PythonAPI/
make all
cd ../../
```

2. Convert AVD annotations to COCO format yourself, or download the converted files

**To Download the files:**
```
mkdir Data
cd Data
``` 

Download the tar [here](https://drive.google.com/file/d/1VgDBR5K1I-Tb6QVqyqVfGEXxcwKGHjQx/view?usp=sharing) 

`tar -xf tdid_gt_boxes.tar`

**Or to convert yourself:**
```python
cd  evaluation/
#Update paths in `convert_AVDgt_to_COCOgt.py` with:
#your AVD_ROOT_DIR
#a path to save the annotations, we will call it VAL_GROUND_TRUTH_BOXES
python convert_AVDgt_to_COCOgt.py

#now update the scene_list in convert_AVDgt_to_COCOgt.py 
#to make the test set
#change the path to save the annotations, we will call it TEST_GROUND_TRUTH_BOXES
python convert_AVDgt_to_COCOgt.py

```


#### Example
See `COCO_evaluation/run_coco_eval.py` for an example of runnning the evaluation code for the full object detection and few-shot detection tasks. 

Alternatively, see the project [`target_driven_instance_detection`](https://github.com/ammirato/target_driven_instance_detection) for an example of an instance detector trained/tested on AVD.
