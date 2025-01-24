import os
import sys


#print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(BASE_DIR)

DATAPTH = os.path.join(BASE_DIR,"datasets")
#print(DATAPTH)

TRAIN_FILE = os.path.join(DATAPTH,"loanTrain.csv")
TEST_FILE = os.path.join(DATAPTH,"test_loan.csv")
#print(TRAIN_FILE)
#print(TEST_FILE)

MODEL_NAME = 'classification.pkl'
SAVE_MODEL_PATH = os.path.join(BASE_DIR,"trained_models")

print(SAVE_MODEL_PATH)

TARGET = "Loan_Status"
FEATURES = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
            'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
            'Loan_Amount_Term', 'Credit_History', 'Property_Area']

NUM_FEATURES = ['ApplicantIncome', 'LoanAmount','Loan_Amount_Term']
CAT_FEATURES = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
                'Credit_History', 'Property_Area']

FEATURE_TO_ENCODE = CAT_FEATURES
FEATURES_TO_MODIFY = ['ApplicantIncome']
FEATURE_TO_ADD = 'CoapplicantIncome'
DROP_FEATURES = 'CoapplicantIncome'
LOG_FEATURES = ['ApplicantIncome', 'LoanAmount','Loan_Amount_Term']


