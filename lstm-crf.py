import pandas as pd
import numpy as np

# data = pd.read_csv("ner_dataset.csv", encoding="latin1")

data = pd.read_csv('train.pos-chunk-name', sep="\t", header=None)
data.columns = ["token", "pos", "chunk", "tag"]

# print(data)
# data['SentenceNum'] = 0

sentenceNum=0
for index, rows in data.iterrows():
    if (data.at[index, 'token']=="."):
        sentenceNum+=1
        data.at[index, 'sentenceNum'] = sentenceNum-1
    else:
        data.at[index, 'sentenceNum'] = sentenceNum
    # print(row['sentenceNum'], row['token'])

print(data)
token = list(set(data["token"].values))
token.append("ENDPAD")
n_token = len(token); n_token

tags = list(set(data["tag"].values))
n_tags = len(tags); n_tags


class SentenceGetter(object):

    def __init__(self, data):
        self.n_sent = 1
        self.data = data
        self.empty = False
        agg_func = lambda s: [(w, p, c, t) for w, p, c, t in zip(s["token"].values.tolist(),
                                                           s["pos"].values.tolist(),
                                                           s["chunk"].values.tolist(),
                                                           s["tag"].values.tolist())]
        self.grouped = self.data.groupby("sentenceNum").apply(agg_func)
        self.sentences = [s for s in self.grouped]

    def get_next(self):
        try:
            s = self.grouped["Sentence: {}".format(self.n_sent)]
            self.n_sent += 1
            return s
        except:
            return None


getter = SentenceGetter(data)
sent = getter.get_next()

print(sent)

sentences = getter.sentences


##############################
# PREPARE THE DATA
##############################
max_len = 75
token2idx = {w: i + 1 for i, w in enumerate(token)}
tag2idx = {t: i for i, t in enumerate(tags)}
# chunk2idx = {c: i for i, c in enumerate(chunks)}


from keras.preprocessing.sequence import pad_sequences
X = [[token2idx[w[0]] for w in s] for s in sentences]
X = pad_sequences(maxlen=max_len, sequences=X, padding="post", value=n_token-1)

# y = [[chunk2idx[w[2]] for w in s] for s in sentences]
# y = pad_sequences(maxlen=max_len, sequences=y, padding="post", value=chunk2idx["O"])


y = [[tag2idx[w[3]] for w in s] for s in sentences]
y = pad_sequences(maxlen=max_len, sequences=y, padding="post", value=tag2idx["O"])

from keras.utils import to_categorical
y = [to_categorical(i, num_classes=n_tags) for i in y]



##############################
# SETUP CRF-LSTM
##############################

from keras.models import Model, Input
from keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional
from keras_contrib.layers import CRF

input = Input(shape=(max_len,))
model = Embedding(input_dim=n_words + 1, output_dim=20,
                  input_length=max_len, mask_zero=True)(input)  # 20-dim embedding
model = Bidirectional(LSTM(units=50, return_sequences=True,
                           recurrent_dropout=0.1))(model)  # variational biLSTM
model = TimeDistributed(Dense(50, activation="relu"))(model)  # a dense layer as suggested by neuralNer
crf = CRF(n_tags)  # CRF layer
out = crf(model)  # output

model = Model(input, out)

model.compile(optimizer="rmsprop", loss=crf.loss_function, metrics=[crf.accuracy])

model.summary()

history = model.fit(X_tr, np.array(y_tr), batch_size=32, epochs=5,
                    validation_split=0.1, verbose=1)

hist = pd.DataFrame(history.history)
