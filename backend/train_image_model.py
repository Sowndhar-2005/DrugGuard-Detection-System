"""
train_image_model.py
DrugGuard — Local Image Model Training Script

Fine-tunes MobileNetV2 on drug vs safe images.
Includes structure to compile to ONNX format.
"""

import os
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "drug_images")

def main():
    if not os.path.exists(IMAGE_DIR):
        print(f"❌ Image directory not found at: {IMAGE_DIR}.")
        print("Please structure your dataset as:")
        print("  backend/drug_images/train/drug/")
        print("  backend/drug_images/train/safe/")
        print("  backend/drug_images/val/drug/")
        print("  backend/drug_images/val/safe/")
        return

    print("Setting up transforms...")
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Load datasets
    train_dataset = datasets.ImageFolder(os.path.join(IMAGE_DIR, "train"), transform=train_transform)
    val_dataset = datasets.ImageFolder(os.path.join(IMAGE_DIR, "val"), transform=val_transform)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

    print(f"Loaded {len(train_dataset)} training images and {len(val_dataset)} validation images.")

    # Initialize MobileNetV2
    print("Loading pretrained MobileNetV2...")
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)

    # Freeze feature layers
    for param in model.features.parameters():
        param.requires_grad = False

    # Redefine classifier head
    model.classifier = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(model.last_channel, 256),
        nn.ReLU(),
        nn.Dropout(0.2),
        nn.Linear(256, 2)
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.classifier.parameters(), lr=0.001)

    print(f"Fine-tuning classifier on {device}...")
    num_epochs = 5
    best_acc = 0.0

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            _, preds = torch.max(outputs, 1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        epoch_loss = running_loss / len(train_dataset)
        epoch_acc = correct / total

        # Validation
        model.eval()
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                val_correct += (preds == labels).sum().item()
                val_total += labels.size(0)

        val_acc = val_correct / val_total
        print(f"Epoch {epoch+1}/{num_epochs} - Loss: {epoch_loss:.4f} - Train Acc: {epoch_acc*100:.2f}% - Val Acc: {val_acc*100:.2f}%")

        if val_acc > best_acc:
            best_acc = val_acc
            # Export to ONNX
            train_out_dir = os.path.join(BASE_DIR, "train")
            os.makedirs(train_out_dir, exist_ok=True)
            onnx_path = os.path.join(train_out_dir, "image_model.onnx")
            print(f"Exporting best model to ONNX: {onnx_path}...")
            model.eval()
            dummy_input = torch.randn(1, 3, 224, 224).to(device)
            torch.onnx.export(
                model,
                dummy_input,
                onnx_path,
                input_names=["image"],
                output_names=["logits"],
                dynamic_axes={"image": {0: "batch_size"}, "logits": {0: "batch_size"}},
                opset_version=11
            )
            
            # Save classes
            classes_path = os.path.join(train_out_dir, "image_classes.json")
            with open(classes_path, "w") as f:
                json.dump({
                    "classes": train_dataset.classes,
                    "class_to_idx": train_dataset.class_to_idx
                }, f)
            print(f"Saved classes mapping to: {classes_path}")

if __name__ == "__main__":
    main()
