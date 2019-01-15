import os
import json


action_id_to_action_str = {0:'forward', 
                           1:'backward',
                           2:'rotate_cw',
                           3:'rotate_ccw'
                          }

def check_path_is_valid(actions,annotations, starting_img_name,dest_imgs):
    '''
    Checks if path specificed by 'actions' is a valid path in the
    'annotations' for the scene, from 'starting_img_name' to any
    one of the 'dest_imgs'
    '''
    cur_ann = annotations[starting_img_name]
    cur_img_name = starting_img_name
    for ind,action_id in enumerate(actions):
       prev_img_name = cur_img_name
       cur_img_name = cur_ann[action_id_to_action_str[action_id]]
       if len(cur_img_name) < 1:
            cur_img_name = prev_img_name
       #     return False
       cur_ann = annotations[cur_img_name]

    if cur_img_name in dest_imgs: 
        return True
    else:
        return False




def aos_evaluate(AVD_path,model_results, scene_names, closest_dests=False):
    '''
    compute 3 evaluation metrics
    1. Success rate
    2. Average path length of successful episodes
    3. Average (shortest path length)/(model path length) of successes 
    '''
    num_success = 0
    num_total = 0
    total_pl = 0
    total_sppl = 0
    for scene in scene_names:
        try:
            dest_imgs = json.load(open(os.path.join(AVD_path,scene,
                                        'AVDB/destination_images.json')))
            annotations = json.load(open(os.path.join(AVD_path,scene,
                                          'annotations.json')))
            shortest_path_lengths = json.load(open(os.path.join(AVD_path,scene,
                                       'AVDB/shortest_path_lengths.json')))
        except:
            print('FAIL LOADING  {}'.format(scene))
            continue

        model_scene_results = model_results[scene]
        for obj_id in model_scene_results.keys():
            obj_results = model_scene_results[obj_id]
            for init_img_name in shortest_path_lengths[obj_id]:
                num_total+=1
                model_path = obj_results[init_img_name]
                #check to see if path is valid
                success = check_path_is_valid(model_path,annotations,
                                            init_img_name,dest_imgs[obj_id])
                if success:
                    num_success +=1
                    total_pl += len(model_path)
                    if closest_dests:
                        total_sppl += (shortest_path_lengths[obj_id][init_img_name][1]
                                        / float(len(model_path)))
                    else:
                        total_sppl +=(shortest_path_lengths[obj_id][init_img_name][0]
                                      / float(len(model_path)))

     
    num_total = float(num_total)
    num_success = float(num_success)
    success_rate = num_success/num_total
    average_length = total_pl/num_success
    average_sppl = total_sppl/num_success

    return success_rate, average_length, average_sppl




if __name__ == '__main__':
   
    #load the paths output by your model  
    model_results_file = '/net/bvisionserver3/playpen1/ammirato/projects/supervised_active_object_search/code/random_baseline/random_output_paths.json'
    model_results = json.load(open(model_results_file))
    #pick which scenes to evaluate on
    scene_names = [ 
                   'Home_001_1',
                  ]
    AVD_path = '/net/bvisionserver3/playpen1/ammirato/Data/TDID_datasets/ActiveVisionDataset/'
    #get the results
    success_rate, average_length, average_sppl =aos_evaluate(AVD_path,
                model_results, scene_names, closest_dests=False)

    print('{} {} {}'.format(success_rate,average_length,average_sppl))



