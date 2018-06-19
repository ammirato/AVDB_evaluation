import numpy as np
import os
import gym
import gym_AVD
import json

AVD_ROOT_DIR = '/playpen/ammirato/Data/RohitData/'
TARGET_IMAGE_DIR = '/playpen/ammirato/Data/Target_Images/AVD_BB_exact_few'


env = gym.make('AVD-v0')
env.setup(AVD_path=AVD_ROOT_DIR, 
          target_path=TARGET_IMAGE_DIR, 
          instance_ids=[],
          scene_names='Home_001_1',
          choose_sequentially=True,
          max_steps=10000)


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

    print(scene_name)
    print(instance_id)
    print(starting_img_name)
    print(num_episodes)
    num_episodes+=1
    while not(done):
        action = action_space.sample()
        all_paths[scene_name][instance_id][starting_img_name].append(action)
        obs, reward, done,info = env.step(action) 
        num_steps +=1 
        #print(num_steps)
        cur_img_name = env.current_scene_info[1][1]
    done=False
    first_obs = env.reset()
    if first_obs != -1:
        env_info = env.get_current_env_info()


with open(os.path.join('./random_output_paths.json'),'w') as outfile:
    json.dump(all_paths,outfile)
