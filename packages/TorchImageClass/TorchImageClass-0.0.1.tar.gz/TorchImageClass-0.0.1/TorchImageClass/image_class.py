import os
import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import DataLoader, random_split
from torchvision import models, transforms, datasets
from torchvision.models import ResNet50_Weights
from torchmetrics import Accuracy, Precision, Recall
from tqdm import tqdm

def train_model(
    base_dir: str,
    num_epochs: int = 10,
    image_size: tuple = (224, 224),
    batch_size: int = 8,
    num_classes: int = 2,
    patience: int = 5,
    val_split: float = 0.2,
    model_save_path: str = "best_model.pth"
):
    """
    Treina um modelo de classificação de imagens (ResNet50) com transfer learning.

    Parâmetros:
    -----------
    base_dir : str
        Caminho para a pasta base que contém subpastas `train/` e `test/`.
    num_epochs : int
        Quantidade máxima de épocas de treinamento.
    image_size : tuple
        Tamanho do Resize das imagens (largura, altura).
    batch_size : int
        Tamanho do batch nos DataLoaders.
    num_classes : int
        Número de classes a serem preditas.
    patience : int
        Número de épocas sem melhora no val_loss para encerrar o treino (early stopping).
    val_split : float
        Fração (0.0 a 1.0) para dividir o dataset de treino em validação.
    model_save_path : str
        Caminho/nome do arquivo para salvar os melhores pesos do modelo.

    Retorna:
    --------
    model : nn.Module
        O modelo treinado (estado final).
    metrics_history : list
        Histórico de métricas de treino e validação a cada época.
    """

    # Escolhe device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[TorchImageClass] Device selecionado: {device}")

    # Diretórios esperados
    train_dir = os.path.join(base_dir, "train")
    test_dir = os.path.join(base_dir, "test")

    # Transforms para treino (com augmentations)
    train_transforms = transforms.Compose([
        transforms.Resize(image_size),
        transforms.RandomRotation(20),
        transforms.RandomHorizontalFlip(),
        transforms.RandomAffine(0, translate=(0.2, 0.2)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225]),
    ])

    # Transforms para validação/teste (sem augmentations)
    val_transforms = transforms.Compose([
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225]),
    ])

    # Carrega dataset de treino (com augmentations)
    full_train_dataset = datasets.ImageFolder(train_dir, transform=train_transforms)
    # Carrega dataset de teste (sem augmentations)
    test_dataset = datasets.ImageFolder(test_dir, transform=val_transforms)

    # Divide em treino e validação
    total_size = len(full_train_dataset)
    train_size = int((1 - val_split) * total_size)
    val_size = total_size - train_size

    train_dataset, val_dataset = random_split(full_train_dataset, [train_size, val_size])

    # Força transforms de validação no dataset de validação
    val_dataset.dataset.transform = val_transforms

    # DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    print(f"[TorchImageClass] Tamanho do train_loader: {len(train_loader)} batches.")
    print(f"[TorchImageClass] Tamanho do val_loader:   {len(val_loader)} batches.")
    print(f"[TorchImageClass] Tamanho do test_loader:  {len(test_loader)} batches.")

    # Definição do modelo
    class CustomResNet50(nn.Module):
        def __init__(self, num_classes):
            super().__init__()
            # Carrega ResNet50 com pesos do ImageNet
            self.resnet = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)

            # Congela as primeiras camadas (até a 7a)
            ct = 0
            for child in self.resnet.children():
                ct += 1
                if ct < 7:
                    for param in child.parameters():
                        param.requires_grad = False

            # Ajusta a camada final
            num_ftrs = self.resnet.fc.in_features
            self.resnet.fc = nn.Sequential(
                nn.Linear(num_ftrs, 128),
                nn.BatchNorm1d(128),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(128, 64),
                nn.BatchNorm1d(64),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(64, 32),
                nn.BatchNorm1d(32),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(32, num_classes)
            )

        def forward(self, x):
            return self.resnet(x)

    model = CustomResNet50(num_classes=num_classes).to(device)

    # Otimizador e loss
    optimizer = Adam(model.parameters(), lr=1e-4, weight_decay=0.01)
    criterion = nn.CrossEntropyLoss()

    # Métricas
    accuracy = Accuracy(task="multiclass", num_classes=num_classes).to(device)
    precision = Precision(task="multiclass", num_classes=num_classes).to(device)
    recall = Recall(task="multiclass", num_classes=num_classes).to(device)

    def train_epoch(model, loader):
        model.train()
        total_loss = 0
        total_acc = 0
        total_prec = 0
        total_rec = 0

        for data, targets in tqdm(loader, desc="[Train Batch]"):
            data, targets = data.to(device), targets.to(device)

            optimizer.zero_grad()
            outputs = model(data)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            total_acc += accuracy(outputs, targets)
            total_prec += precision(outputs, targets)
            total_rec += recall(outputs, targets)

        n_batches = len(loader)
        return {
            "loss": total_loss / n_batches,
            "accuracy": total_acc / n_batches,
            "precision": total_prec / n_batches,
            "recall": total_rec / n_batches,
        }

    def validate_epoch(model, loader):
        model.eval()
        total_loss = 0

        with torch.no_grad():
            for data, targets in tqdm(loader, desc="[Val Batch]"):
                data, targets = data.to(device), targets.to(device)
                outputs = model(data)
                loss = criterion(outputs, targets)
                total_loss += loss.item()

        val_loss = total_loss / len(loader)
        return val_loss

    # Early Stopping configs
    best_val_loss = float("inf")
    patience_counter = 0

    metrics_history = []

    print("[TorchImageClass] Iniciando treino...")

    for epoch in range(1, num_epochs + 1):
        print(f"\n[Epoch {epoch}/{num_epochs}]")
        train_metrics = train_epoch(model, train_loader)
        val_loss = validate_epoch(model, val_loader)

        print(f"Train => {train_metrics}")
        print(f"Val   => {{'val_loss': {val_loss:.4f}}}")

        # Salvar métricas no histórico
        metrics_history.append({
            "epoch": epoch,
            "train_loss": train_metrics["loss"],
            "train_acc": float(train_metrics["accuracy"]),
            "train_precision": float(train_metrics["precision"]),
            "train_recall": float(train_metrics["recall"]),
            "val_loss": val_loss
        })

        # Early stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            torch.save(model.state_dict(), model_save_path)
            print(f"  -> Novo melhor modelo salvo em: {model_save_path}")
        else:
            patience_counter += 1
            print(f"  -> Patience: {patience_counter}/{patience}")
            if patience_counter >= patience:
                print("[Early stopping] Critério de paciência atingido.")
                break

    print("[TorchImageClass] Treinamento finalizado!")

    return model, metrics_history
