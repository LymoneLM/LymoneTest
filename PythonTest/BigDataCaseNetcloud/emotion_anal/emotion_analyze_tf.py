import re
import csv
import jieba
import tensorflow as tf
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


def preprocess_sentence(w):
    w = jieba.lcut(w)
    return w


def create_dataset():
    # 读取csv至字典
    csvFile = open("../output/comments_excel1.csv", "r", encoding='utf-8')
    reader = csv.reader(csvFile)
    # labels = [item[0] for item in reader if item]
    # sentences = [preprocess_sentence(item[1]) for item in reader if item]
    items = [[int(float(item[0])), preprocess_sentence(item[1])] for item in reader if item]
    csvFile.close()
    # print(len(labels))
    # print(len(sentences))
    return zip(*items)


def tokenize(lang):
    lang_tokenizer = tf.keras.preprocessing.text.Tokenizer(
        num_words=5000,
        filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n ，。【】[]()（）')
    lang_tokenizer.fit_on_texts(lang)

    tensor = lang_tokenizer.texts_to_sequences(lang)

    tensor = tf.keras.preprocessing.sequence.pad_sequences(tensor, padding='post')

    return tensor, lang_tokenizer


def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(
            input_dim=5000,
            output_dim=64,
            # Use masking to handle the variable sequence lengths
            mask_zero=True),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    return model


def create_double_lstm_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(5000,
                                64,
                                mask_zero=True),
        tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(64, return_sequences=True)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1)
    ])
    return model


def plot_graphs(history, metric):
    plt.plot(history.history[metric])
    plt.plot(history.history['val_' + metric], '')
    plt.xlabel("Epochs")
    plt.ylabel(metric)
    plt.legend([metric, 'val_' + metric])


if __name__ == '__main__':
    label, data = create_dataset()
    tensor, tokenizer = tokenize(data)

    BUFFER_SIZE = 1000
    BATCH_SIZE = 64
    # Creating training and validation sets using an 80-20 split
    input_train, input_val, target_train, target_val = train_test_split(tensor, label, test_size=0.2)
    dataset = tf.data.Dataset.from_tensor_slices((input_train, target_train)).shuffle(BUFFER_SIZE)
    dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)
    test_dataset = tf.data.Dataset.from_tensor_slices((input_val, target_val)).shuffle(BUFFER_SIZE)
    test_dataset = test_dataset.batch(BATCH_SIZE, drop_remainder=True)

    model = create_double_lstm_model()

    model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  optimizer=tf.keras.optimizers.Adam(1e-4),
                  metrics=['accuracy'])

    history = model.fit(dataset,
                        epochs=20,
                        validation_data=test_dataset,
                        validation_steps=1)

    test_loss, test_acc = model.evaluate(test_dataset)
    print('Test Loss: {}'.format(test_loss))
    print('Test Accuracy: {}'.format(test_acc))
    plt.figure(figsize=(16, 6))
    plt.subplot(1, 2, 1)
    plot_graphs(history, 'accuracy')
    plt.subplot(1, 2, 2)
    plot_graphs(history, 'loss')
    plt.savefig("double_lstm.png")
