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
3. Average (shortest path length)/(model path length) of successful episodes. This has a max of 1, and is useful for comparing across different 
cenes of different sizes. 



