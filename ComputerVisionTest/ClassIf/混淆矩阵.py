import os
import torch
import numpy as np  # Import numpy
import matplotlib.pyplot as plt
from torchvision import transforms, datasets
from torch.utils.data import DataLoader
from sklearn.metrics import confusion_matrix, precision_score
import seaborn as sns
from tqdm import tqdm


from moudle.mobilenet import MobileNetV2



def plot_confusion_matrix(cm, class_names, class_precisions, model_name):
    """
    Plots the confusion matrix with class precisions.
    Parameters:
        cm (array): Confusion matrix.
        class_names (list): Names of the classes.
        class_precisions (list): Precision of each class.
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(cm, annot=True, fmt='.2f', ax=ax, cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)

    # # Annotation with class precision
    # for i, precision in enumerate(class_precisions):
    #     ax.text(i + 0.5, len(class_names) + 0.2, f'Precision: {precision:.2f}',
    #             ha='center', va='center', fontweight='bold', fontsize=9)

    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title('Confusion Matrix (Normalized to Probabilities)')
    plt.savefig('./logs/' + model_name + '/confusion_matrix_with_precision1.png')


def main():
    model_name = "mobilenet"

    log_root = "./logs/" + model_name
    if not os.path.exists(log_root):
        os.makedirs(log_root)

    # Class names
    class_names = ["health", "swine_fever"]

    # Data transformations
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Load dataset
    test_dataset = datasets.ImageFolder(root='./datasets/val', transform=transform)
    test_loader = DataLoader(dataset=test_dataset, batch_size=64, shuffle=False)

    # Load model
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


    if model_name == "mobilenet":
        # 定义模型MobileNetV2
        model = MobileNetV2(num_classes=len(class_names))
        weight_path = 'logs/' + model_name + "/best.pth"
        model.load_state_dict(torch.load(weight_path, map_location=device))



    model.to(device)
    model.eval()

    predlist = torch.zeros(0, dtype=torch.long, device='cpu')
    lbllist = torch.zeros(0, dtype=torch.long, device='cpu')

    with torch.no_grad():
        for images, labels in tqdm(test_loader):
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)

            predlist = torch.cat([predlist, preds.view(-1).cpu()])
            lbllist = torch.cat([lbllist, labels.view(-1).cpu()])

    cm = confusion_matrix(lbllist.numpy(), predlist.numpy())
    class_precisions = precision_score(lbllist.numpy(), predlist.numpy(), average=None)

    # Normalize confusion matrix to probabilities
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plot_confusion_matrix(cm_normalized, class_names, class_precisions, model_name)


if __name__ == '__main__':
    main()
