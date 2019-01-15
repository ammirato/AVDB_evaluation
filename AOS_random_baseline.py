import numpy as np
import os
import gym
import gym_AVD
import json


AVD_ROOT_DIR = '/net/bvisionserver3/playpen1/ammirato/Data/TDID_datasets/ActiveVisionDataset/'
#TARGET_IMAGE_DIR = '/net/bvisionserver3/playpen1/ammirato/Data/TDID_datasets/target_images/'
TARGET_IMAGE_DIR = '/net/bvisionserver3/playpen1/ammirato/Data/TDID_datasets/timgs/'

#if you are not using target images, just omit the target_path input
env = gym.make('AVD-v0')
env.setup(AVD_path=AVD_ROOT_DIR, 
          target_path=TARGET_IMAGE_DIR, 
          instance_ids=[], #choose all possible instances
          scene_names=['Home_001_1', 'Home_005_2'], #choose 2 scenes
          choose_sequentially=True, #go sequentially through every 
          max_steps=10000) #max steps env will allow.
#note: while decreasing max_steps could also decrease you average number of
#steps per episode, it will only do so if it also reduces your success rate.  


action_space = env.action_space
first_obs = env.reset()
env_info = env.get_current_env_info()


done = False
num_steps = 0
all_paths = {}
num_episodes = 0
while(first_obs != -1):
    scene_name = env_info[0]
    instance_id = env_info[1]
    starting_img_name = env_info[2]

    #a silly way to populate the dictionary for AVDB AOS evaluation
    try:
        all_paths[scene_name][instance_id][starting_img_name] = []
    except:
        try:
            all_paths[scene_name][instance_id] = {}
            all_paths[scene_name][instance_id][starting_img_name] = []
        except:
            all_paths[scene_name] = {}
            all_paths[scene_name][instance_id] = {}
            all_paths[scene_name][instance_id][starting_img_name] = []

    num_episodes+=1
    while not(done):
        action = action_space.sample()
        all_paths[scene_name][instance_id][starting_img_name].append(action)
        obs, reward, done,info = env.step(action) 
        num_steps +=1 
        cur_img_name = env.current_scene_info[1][1]
    print(scene_name, instance_id,starting_img_name, 
          len(all_paths[scene_name][instance_id][starting_img_name]))
    done=False
    first_obs = env.reset()
    if first_obs != -1:
        env_info = env.get_current_env_info()


with open(os.path.join('./random_output_paths.json'),'w') as outfile:
    json.dump(all_paths,outfile)

