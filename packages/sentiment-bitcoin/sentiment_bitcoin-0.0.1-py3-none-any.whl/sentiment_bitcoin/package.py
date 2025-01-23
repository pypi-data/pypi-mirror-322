import pandas as pd
import numpy as np
import re
from tensorflow.keras.preprocessing.sequence import pad_sequences
from statistics import mean, mode


from sentiment_bitcoin import model, tokenizer,stop_words

def preprocessing(text):
    try:
        if isinstance(text, pd.Series):
            # Handle NaN values
            text = text.fillna('').astype(str)  
            # symbol handle
            text = text.apply(lambda x: re.sub(r'[^a-zA-Z0-9]', ' ', x)) 
            text = text.apply(lambda x: " ".join(
                [word.lower() for word in x.split() if word.lower() not in stop_words]
            ))
            return text
        
        elif isinstance(text, list):
            # Proses setiap elemen dalam list
            processed_list = [
                re.sub(r'[^a-zA-Z0-9]', ' ', t) for t in text
            ]
            processed_list = [
                " ".join([word.lower() for word in t.split() if word.lower() not in stop_words]) 
                for t in processed_list
            ]
            return pd.Series(processed_list)

        elif isinstance(text, str):
            # symbol handle
            text = re.sub(r'[^a-zA-Z0-9]', ' ', text)  
            text = " ".join(
                [word.lower() for word in text.split() if word.lower() not in stop_words]
            )
            return pd.Series(text)

        else:
            raise ValueError("Input harus berupa pandas Series atau string!")

    except Exception as e:
        raise ValueError(f"Error saat preprocessing: {e}")


def tokenize_and_padding(text, max_len=0):
    try:
        if isinstance(text, pd.Series):
            text = text.tolist()

        if isinstance(text, str):
            text = [text]

        if not isinstance(text, list):
            raise ValueError("Input text harus berupa list, string, atau pandas Series")

        # Tokenisasi teks
        sequences = tokenizer.texts_to_sequences(text)

        if max_len == 0:
            if len(sequences) == 1:  # 1 teks 
                max_len = len(sequences[0])  
            else:  # Untuk banyak teks
                sequence_lengths = [len(seq) for seq in sequences]
                average = round(mean(sequence_lengths))
                try:
                    modus = mode(sequence_lengths)
                except:
                    modus = 0
                max_len = average + modus

        # padding
        padded_sequences = pad_sequences(sequences, maxlen=max_len)
        return padded_sequences

    except Exception as e:
        raise ValueError(f"Error saat tokenisasi dan padding: {e}")



def only_prediction(tokenized):
    try:
        if isinstance(tokenized, list):
            tokenized = np.array(tokenized)

        if not isinstance(tokenized, np.ndarray):
            raise ValueError("Input tokenized harus berupa numpy array atau list")

        prediction = model.predict(tokenized)
        sentiment = (prediction >= 0.5).astype(int)

        df = pd.DataFrame({
            'prediction': prediction.flatten(), 
            'sentiment': sentiment.flatten() 
        })
        return df

    except Exception as e:
        raise ValueError(f"Error saat membuat prediksi: {e}")


def full_prediction(text,pad=0):
    try:
        if not isinstance(text, (str, pd.Series)):
            raise ValueError("Input harus berupa string atau pandas Series")

        text_processed = preprocessing(text)
        sequences = tokenize_and_padding(text_processed, pad)
        results = only_prediction(sequences)

        result_df = pd.DataFrame({
            'text': text_processed,
            'padded': list(sequences),
        })

        result_df = pd.concat([result_df, results], axis=1)
        return result_df

    except Exception as e:
        raise ValueError(f"Error saat melakukan prediksi penuh: {e}")
    

def detokenized(sequences):
    # testing list
    if not all(isinstance(seq, list) for seq in sequences):
        raise ValueError("Input harus berupa list dua dimensi.")
    
    # zero hendling
    cleaned_sequences = [[token for token in sequence if token != 0] for sequence in sequences]

    # detokenized
    index_word = tokenizer.index_word  
    
    # mergering
    try:
        detokenized_texts = [
            " ".join(index_word.get(token, "[UNK]") for token in sequence) for sequence in cleaned_sequences
        ]
    except Exception as e:
        raise ValueError(f"Terjadi kesalahan saat detokenisasi: {str(e)}")
    
    return detokenized_texts
