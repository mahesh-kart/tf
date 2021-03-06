import tensorflow_datasets as tfds

imdb, info = tfds.load("imdb_reviews", with_info=True, as_supervised=True)

train_data, test_data = imdb["train"], imdb["test"]

training_sentences  = []
testing_sentences   = []

training_labels     = []
testing_labels      = []

import numpy as np

for s,l in train_data:
  training_sentences.append(str( s.numpy() ))
  training_labels.append(l.numpy())

for s,l in test_data:
  testing_sentences.append(str( s.numpy() ))
  testing_labels.append(l.numpy())

training_labels_final = np.array(training_labels)
testing_labels_final  = np.array(testing_labels)


import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

vocab_size  = 10000
oov_tok     = "<OOV>"
max_len     = 120
trunc_type  = "post"
embedding_dim= 16

tokenizer   = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(training_sentences)
word_index  = tokenizer.word_index

sequences   = tokenizer.texts_to_sequences(training_sentences)
padded      = pad_sequences(sequences, maxlen=max_len)


testing_seq     = tokenizer.texts_to_sequences(testing_sentences)
testing_padded  = pad_sequences(testing_seq, maxlen=max_len)

model = tf.keras.Sequential([
                             tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_len ),
                             tf.keras.layers.Flatten(),
                             tf.keras.layers.Dense(6, activation="relu"),
                             tf.keras.layers.Dense(1, activation="sigmoid")
])
model.summary()

print(training_sentences[0])

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

num_epochs = 10
#model.fit(padded, training_labels_final, epochs=num_epochs, validation_data=(testing_padded, testing_labels_final))









