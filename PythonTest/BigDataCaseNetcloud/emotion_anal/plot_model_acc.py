import numpy as np
import matplotlib.pyplot as plt

figure = plt.figure()
x = np.arange(4)
y = [0.702, 0.754, 0.784, 0.769]
sorted_y = sorted(y, reverse=True)
print(sorted_y)
plt.bar(x, y)
plt.xlabel('Model ame')
plt.ylabel('Model accuracy')
plt.xticks(x, ['SVM', 'Bayes', 'LSTM', 'BERT'])
plt.ylim(0.6, 0.8)
plt.show()
