import numpy as np
import pandas as pd

import sys
import os
config_root = os.path.dirname(os.path.abspath(__file__))
#print(config_root)
sys.path.append(config_root)

from config import config
from processing.data_handling import load_data,save_pipeline
import processing.data_preprocessing as pp
import pipeline as pipe

def perform_training():
    train_data = load_data(config.TRAIN_FILE)
    train_x = train_data[config.FEATURES]
    train_y = train_data[config.TARGET].map({'Y':1,'N':0})
    pipe.classification_pipeline.fit(train_x,train_y)
    save_pipeline(pipe.classification_pipeline)

if __name__ == '__main__':
    perform_training()