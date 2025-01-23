import os
import joblib
from tensorflow.keras.models import load_model
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

PACKAGE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(PACKAGE_DIR, "Model_F_2,4_Acc97.h5")
TOKENIZER_PATH = os.path.join(PACKAGE_DIR, "Model_T_2,4_Acc97.pkl")

# Load model dan tokenizer
model = load_model(MODEL_PATH)
tokenizer = joblib.load(TOKENIZER_PATH) 
 
from .package import tokenize_and_padding,preprocessing,only_prediction,full_prediction,detokenized

__all__ = ['preprocessing', 'tokenize_and_padding', 'only_prediction','full_prediction','model','tokenizer','stop_words','detokenized']