from sklearn.pipeline import Pipeline

from config import config
import processing.data_preprocessing as pp
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression

classification_pipeline = Pipeline([
    ('Mean Imputation' , pp.MeanImputer(config.NUM_FEATURES)),
    ('Mode Imputation' , pp.ModeImputer(config.CAT_FEATURES)),
    ('Domain Processing' , pp.DomainProcessing(variables_to_modify=config.FEATURES_TO_MODIFY,
                                               variables_to_add=config.FEATURE_TO_ADD)),
    ('Drop Columns' , pp.DropColumns(config.DROP_FEATURES)),
    ('Label Encoder' , pp.CustomLabelEncoder(config.FEATURE_TO_ENCODE)),
    ('Log Transform' , pp.LogTransformation(config.LOG_FEATURES)),
    ('MinMaxScaler' , MinMaxScaler()),
    ('LogisticRegression' , LogisticRegression())                     
])