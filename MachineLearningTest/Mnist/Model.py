import torch.nn as nn
import math
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.classifier = nn.Sequential(
            nn.Dropout(p=0.5),
            nn.Linear(64 * 7 * 7, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),
            nn.Linear(512, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),
            nn.Linear(512, 10),
        )
        # 模型参数初始化，其中全连接层的参数使用了xavier初始化方法。
        for m in self.features.children():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

        for m in self.classifier.children():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform(m.weight)
            elif isinstance(m, nn.BatchNorm1d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)

        return x


class DNN(nn.Module):
    def __init__(self):
        super(DNN, self).__init__()
        self.fc1 = nn.Sequential(nn.Linear(784, 512), nn.ReLU())
        self.fc2 = nn.Sequential(nn.Linear(512, 256), nn.ReLU())
        self.fc3 = nn.Sequential(nn.Linear(256, 128), nn.ReLU())
        self.fc4 = nn.Sequential(nn.Linear(128, 64), nn.ReLU())
        self.fc5 = nn.Linear(64, 10)

    def forward(self, x):
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        x = self.fc4(x)
        x = self.fc5(x)
        return x
class Rnn(nn.Module):
    def __init__(self, in_dim, hidden_dim, n_layer, n_class):
        super(Rnn, self).__init__()
        self.n_layer = n_layer
        self.hidden_dim = hidden_dim
        self.lstm = nn.LSTM(in_dim, hidden_dim, n_layer, batch_first=True)
        self.classifier = nn.Linear(hidden_dim, n_class)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        out = self.classifier(out)
        return out


class AutoEncoder(nn.Module):
    def __init__(self):
        super(AutoEncoder, self).__init__()

        self.encoder = nn.Sequential(
            nn.Linear(28 * 28, 128),  # 全连接层
            nn.ReLU(True),  # 激活层

            nn.Linear(128, 64),  # 全连接层
            nn.ReLU(True),  # 激活层

            nn.Linear(64, 32),  # 全连接层
        )

        self.decoder = nn.Sequential(
            nn.Linear(32, 64),
            nn.ReLU(True),

            nn.Linear(64, 128),
            nn.ReLU(True),

            nn.Linear(128, 28 * 28),
            nn.Sigmoid(),  # 结果在[0, 1]
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return encoded, decoded


class ConvAutoencoder(nn.Module):
    def __init__(self):
        super(ConvAutoencoder, self).__init__()

        ## encoder layers ##
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1),  # 卷积层，depth from 1 --> 16, 3x3 kernels, img_size: 28*28 -> 28*28
            nn.ReLU(),  # 激活层
            nn.MaxPool2d(2, 2),  # 池化层, -->16*14*14

            nn.Conv2d(16, 4, 3, padding=1),  # 卷积层，depth from 16 --> 4, 3x3 kernels, img_size: 14*14 -> 14*14
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 池化层, -->4*7*7
        )

        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(4, 16, 2, stride=2),
            # 转置卷积，a kernel of 2 and a stride of 2 will increase the spatial dims by 2
            nn.ReLU(),
            nn.ConvTranspose2d(16, 1, 2, stride=2),
            nn.Sigmoid(),  # 结果在[0, 1]
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return encoded, decoded