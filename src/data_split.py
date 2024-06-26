import pandas as pd 
from sklearn.model_selection import train_test_split 
import argparse
import os
import yaml
import numpy as np
import dvc.api

def data_split():

    param_yaml = dvc.api.params_show()
    print("Loaded parameters:", param_yaml)
    local_data = param_yaml["data_source"]["local_path"]
    
    data_df = pd.read_csv(local_data)
    data_df['quality'] = np.where(data_df['quality']>6.5, 1,0)
    random_state = param_yaml["base"]["random_state"]
    split_ratio = param_yaml["split"]["split_ratio"]
    
    train, test = train_test_split(
        data_df, 
        test_size=split_ratio, 
        random_state=random_state
        )
    os.makedirs(param_yaml["split"]["dir"], exist_ok=True)
    train_data_path = os.path.join(param_yaml["split"]["dir"], param_yaml["split"]["train_file"])
    
    train.to_csv(train_data_path, index=False)

    test_data_path = os.path.join(param_yaml["split"]["dir"], param_yaml["split"]["test_file"])
    test.to_csv(test_data_path, index=False)


if __name__=="__main__":
    data_split()