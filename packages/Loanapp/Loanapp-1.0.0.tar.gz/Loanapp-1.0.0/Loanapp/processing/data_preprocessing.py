import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Loanapp.config import config

import numpy as np

#numerical - mean
class MeanImputer:
    def __init__(self,variables=None):
        self.variables = variables

    def fit(self,X,y=None):
        self.mean_dict = {}
        for var in self.variables:
            self.mean_dict[var] = X[var].mean()
        return self

    def transform(self,X):
        for var in self.variables:
            X[var] = X[var].fillna(self.mean_dict[var])
        return X
    
#categorical - mode
class ModeImputer:
    def __init__(self,variables=None):
        self.variables = variables

    def fit(self,X,y=None):
        self.mode_dict = {}
        for var in self.variables:
            self.mode_dict[var] = X[var].mode()[0]
        return self

    def transform(self,X):
        for var in self.variables:
            X[var] = X[var].fillna(self.mode_dict[var])
        return X
        

#drop columns
class DropColumns:
    def __init__(self,variables_to_drop=None):
        self.variables_to_drop = variables_to_drop

    def fit(self,X,y=None):
        return self

    def transform(self,X):
        X = X.drop(columns = self.variables_to_drop)
        return X
    
#Domain Specific processing
class DomainProcessing:
    def __init__(self,variables_to_modify=None,variables_to_add=None):
        self.variables_to_modify = variables_to_modify
        self.variables_to_add  = variables_to_add 

    def fit(self,X,y=None):
        return self

    def transform(self,X):
        for feature in self.variables_to_modify:
            X[feature] = X[feature] + X[self.variables_to_add]
        return X

#Custom Label encoder
class CustomLabelEncoder:
    def __init__(self,variables=None):
        self.variables = variables

    def fit(self,X,y=None):
        self.label_dict = {}
        for val in self.variables:
            categories = X[val].unique()
            self.label_dict[val] = {cat : i for i,cat in enumerate(categories)}
        return self

    def transform(self,X):
        for val in self.variables:
            X[val] = X[val].map(self.label_dict[val])
        return X


#Log Transformation
class LogTransformation:
    def __init__(self,variables=None):
        self.variables = variables

    def fit(self,X,y=None):
        return self

    def transform(self,X):
        for val in self.variables:
            X[val] = np.log(X[val])
        return X