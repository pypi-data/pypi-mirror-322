import os
import pandas as pd
import sys
import joblib

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Loanapp.config import config

def load_data(file_name):
    filepath = os.path.join(config.DATAPTH, file_name)
    _data = pd.read_csv(filepath)
    return _data


def save_pipeline(pipeline_to_save):
    save_path = os.path.join(config.SAVE_MODEL_PATH , config.MODEL_NAME)
    joblib.dump(pipeline_to_save,save_path)
    print(f"The model has been saved under the name {config.MODEL_NAME}")


def load_pipeline(pipeline_to_load):
    save_path = os.path.join(config.SAVE_MODEL_PATH , config.MODEL_NAME)
    model_loaded = joblib.load(save_path)
    print("Model has been loaded")
    return model_loaded



