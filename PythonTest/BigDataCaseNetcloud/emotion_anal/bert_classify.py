import os
import csv
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.model_selection import train_test_split
from official.nlp import optimization
from official.nlp.bert import bert_models
from official.nlp.bert import configs
from official.nlp.bert import tokenization

bert_folder = "../chinese_L-12_H-768_A-12/"
vocab_file = os.path.join(bert_folder, "vocab.txt")
vocab = []
with open(vocab_file, mode='r', encoding='utf-8') as f:
    vocab = [line.strip() for line in f]

# tokenizer
tokenizer = tokenization.FullTokenizer(
    vocab_file=vocab_file
)
print("Vocab size:", len(tokenizer.vocab))
tokens = tokenizer.tokenize("今天是个好日子!")
print(tokens)
ids = tokenizer.convert_tokens_to_ids(tokens)
print(ids)


# preprocess the data
def create_dataset():
    # 读取csv至字典
    csvFile = open("labeled_data.csv", "r", encoding='utf-8')
    reader = csv.reader(csvFile)
    # labels = [item[0] for item in reader if item]
    # sentences = [preprocess_sentence(item[1]) for item in reader if item]
    items = [[int(float(item[0])),
              preprocess_sentence([i for i in item[1] if i in vocab])] for item in reader if item]
    csvFile.close()
    # print(len(labels))
    # print(len(sentences))
    return zip(*items)


def preprocess_sentence(s):
    s = tokenizer.convert_tokens_to_ids(s)
    return s


def bert_encode(data):
    input_word_ids = tf.ragged.constant(data)
    input_mask = tf.ones_like(input_word_ids)
    input_type_ids = tf.ones_like(input_word_ids)
    inputs = {
        'input_word_ids': input_word_ids.to_tensor(),
        'input_mask': input_mask.to_tensor(),
        'input_type_ids': input_type_ids.to_tensor()
    }
    return inputs


label, data = create_dataset()
print(type(label))
print(type(data))
input_train, input_val, target_train, target_val = train_test_split(data, label, test_size=0.2)
input_train = bert_encode(input_train)
input_val = bert_encode(input_val)
target_train = tf.convert_to_tensor(target_train)
target_val = tf.convert_to_tensor(target_val)
for item in input_train:
    print(input_train[item].numpy())


# model_config
bert_config_file = os.path.join(bert_folder, "bert_config.json")
bert_config = configs.BertConfig.from_json_file(bert_config_file)
print(bert_config)
# model
bert_model_path = "../chinese_L-12_H-768_A-12/bert_zh_L-12_H-768_A-12_2"
bert_classifier, bert_encoder = bert_models.classifier_model(bert_config=bert_config, hub_module_url=bert_model_path, num_labels=2)
# pydotprint有问题
tf.keras.utils.plot_model(bert_classifier, show_shapes=True, dpi=48)
# tf.keras.utils.plot_model(bert_encoder, show_shapes=True, dpi=64)
# checkpoint = tf.train.Checkpoint(model=bert_encoder)
# checkpoint.restore(os.path.join(bert_folder,
#                                 'bert_model.ckpt')).assert_consumed()


# Set up epochs and steps
epochs = 10
batch_size = 32
eval_batch_size = 32

train_data_size = len(target_train)
steps_per_epoch = int(train_data_size / batch_size)
num_train_steps = steps_per_epoch * epochs
warmup_steps = int(epochs * train_data_size * 0.1 / batch_size)

# creates an optimizer with learning rate schedule
optimizer = optimization.create_optimizer(2e-5, num_train_steps=num_train_steps, num_warmup_steps=warmup_steps)

# train the model
metrics = [
    tf.keras.metrics.SparseCategoricalAccuracy('accuracy', dtype=tf.float32)
]
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

bert_classifier.compile(optimizer=optimizer, loss=loss, metrics=metrics)

bert_classifier.fit(input_train,
                    target_train,
                    validation_data=(input_val, target_val),
                    batch_size=32,
                    epochs=epochs)
print('over')
