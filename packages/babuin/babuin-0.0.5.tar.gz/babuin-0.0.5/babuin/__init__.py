import os

class test2:
    def __init__(self):
        self.sklad= {
            'imp':'''
import pandas as pd
import numpy as np

import torch
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader, TensorDataset

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

import matplotlib.pyplot as plt''',


                        
                        'bike':'''from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

data = pd.read_csv('bike_cnt.csv')
data = data.iloc[:, 1:]
# Выделение признаков и целевой переменной
X = data.drop(columns=['cnt'])
y = data['cnt']
# Нормализация целевой переменной
max_y = y.max()
y = y / max_y

# Указание категориальных и числовых столбцов
categorical_cols = ['dteday', 'season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit']
numerical_cols = ['temp', 'atemp', 'hum', 'windspeed']

# Предобработка данных
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(), categorical_cols)
    ])

X_processed = preprocessor.fit_transform(X).toarray()

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

# Преобразование данных в тензоры
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1)

train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

# Определение нейронной сети
class BikeDemandModel(nn.Module):
    def __init__(self, input_dim):
        super(BikeDemandModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.fc(x)

# Параметры обучения
input_dim = X_train.shape[1]
model = BikeDemandModel(input_dim)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

batch_size = 64
epochs = 100
print_every = 10

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# Список для хранения значений функции потерь
losses = []

# Список для хранения значений функции потерь на обучении и тесте
train_losses = []
test_losses = []

for epoch in range(epochs):
    epoch_loss = 0
    i = 0
    model.train()
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        predictions = model(batch_X)
        loss = criterion(predictions, batch_y)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
        i += 1

    epoch_loss = epoch_loss / i
    train_losses.append(epoch_loss)

    # Оценка на тестовом наборе
    model.eval()
    with torch.no_grad():
        test_predictions = model(X_test)
        test_loss = criterion(test_predictions, y_test).item()
    test_losses.append(test_loss)

    if (epoch + 1) % print_every == 0:
        print(f'Epoch {epoch+1}/{epochs}, Train Loss: {epoch_loss:.4f}, Test Loss: {test_loss:.4f}')

# Результаты на обучающем наборе
with torch.no_grad():
    y_train_pred = model(X_train).numpy()
    y_train_true = y_train.numpy()
train_mse = mean_squared_error(y_train_true, y_train_pred)
train_mae = mean_absolute_error(y_train_true, y_train_pred)
train_r2 = r2_score(y_train_true, y_train_pred)
print(f"Результаты на обучающем наборе: MSE: {train_mse:.4f}, MAE: {train_mae:.4f}, R2: {train_r2:.4f}")

# Результаты на тестовом наборе
with torch.no_grad():
    y_test_pred = model(X_test).numpy()
    y_test_true = y_test.numpy()
test_mse = mean_squared_error(y_test_true, y_test_pred)
test_mae = mean_absolute_error(y_test_true, y_test_pred)
test_r2 = r2_score(y_test_true, y_test_pred)
print(f"Результаты на тестовом наборе: MSE: {test_mse:.4f}, MAE: {test_mae:.4f}, R2: {test_r2:.4f}")

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(range(1, epochs + 1), train_losses, label="Train Loss")
plt.plot(range(1, epochs + 1), test_losses, label="Test Loss", linestyle='--')
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("Изменение функции потерь на обучающем и тестовом наборах в процессе обучения")
plt.legend()
plt.show()
''',



                        
                        'bike-o':'''from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

data = pd.read_csv('bike_cnt.csv')
data = data.iloc[:, 1:]
# Выделение признаков и целевой переменной
X = data.drop(columns=['cnt'])
y = data['cnt']

# Нормализация целевой переменной
max_y = y.max()
y = y / max_y

# Указание категориальных и числовых столбцов
categorical_cols = ['dteday', 'season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit']
numerical_cols = ['temp', 'atemp', 'hum', 'windspeed']

# Предобработка данных
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(), categorical_cols)
    ])

X_processed = preprocessor.fit_transform(X).toarray()

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

# Преобразование данных в тензоры
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1)

train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

# Определение нейронной сети
class BikeDemandModel(nn.Module):
    def __init__(self, input_dim):
        super(BikeDemandModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.fc(x)

# Параметры обучения
input_dim = X_train.shape[1]
batch_size = 64
epochs = 100
print_every = 10

# Список оптимизаторов для сравнения
optimizers = {
    'SGD': lambda params: torch.optim.SGD(params, lr=0.01),
    'Adam': lambda params: torch.optim.Adam(params, lr=0.001),
    'AdamW': lambda params: torch.optim.AdamW(params, lr=0.001, weight_decay=0.01),
    'RMSprop': lambda params: torch.optim.RMSprop(params, lr=0.001),
    'Adagrad': lambda params: torch.optim.Adagrad(params, lr=0.01)
}

# Результаты для каждого оптимизатора
results = {}
losses_per_optimizer_train = {}
losses_per_optimizer_test = {}

for opt_name, opt_func in optimizers.items():
    print(f"Training with {opt_name} optimizer")

    # Инициализация модели и оптимизатора
    model = BikeDemandModel(input_dim)
    criterion = nn.MSELoss()
    optimizer = opt_func(model.parameters())

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # Списки для хранения значений функции потерь
    train_losses = []
    test_losses = []

    for epoch in range(epochs):
        epoch_loss = 0
        i = 0
        model.train()
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_X)
            loss = criterion(predictions, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            i += 1

        epoch_loss = epoch_loss / i
        train_losses.append(epoch_loss)

        # Оценка функции потерь на тестовом наборе
        model.eval()
        with torch.no_grad():
            test_predictions = model(X_test)
            test_loss = criterion(test_predictions, y_test).item()
        test_losses.append(test_loss)

        if (epoch + 1) % print_every == 0:
            print(f'Epoch {epoch+1}/{epochs}, Train Loss: {epoch_loss:.4f}, Test Loss: {test_loss:.4f}')

    # Сохранение потерь для каждого оптимизатора
    losses_per_optimizer_train[opt_name] = train_losses
    losses_per_optimizer_test[opt_name] = test_losses

    # Оценка метрик на обучающем и тестовом наборах
    with torch.no_grad():
        y_train_pred = model(X_train).numpy()
        y_train_true = y_train.numpy()
        y_test_pred = model(X_test).numpy()
        y_test_true = y_test.numpy()

    train_mse = mean_squared_error(y_train_true, y_train_pred)
    train_mae = mean_absolute_error(y_train_true, y_train_pred)
    train_r2 = r2_score(y_train_true, y_train_pred)

    test_mse = mean_squared_error(y_test_true, y_test_pred)
    test_mae = mean_absolute_error(y_test_true, y_test_pred)
    test_r2 = r2_score(y_test_true, y_test_pred)

    results[opt_name] = {
        'Train': {'MSE': train_mse, 'MAE': train_mae, 'R2': train_r2},
        'Test': {'MSE': test_mse, 'MAE': test_mae, 'R2': test_r2}
    }

# Итоговые результаты
print("Final Comparison:")
for opt_name, metrics in results.items():
    print(f"{opt_name}:")
    print(f"  Train: MSE={metrics['Train']['MSE']:.4f}, MAE={metrics['Train']['MAE']:.4f}, R2={metrics['Train']['R2']:.4f}")
    print(f"  Test:  MSE={metrics['Test']['MSE']:.4f}, MAE={metrics['Test']['MAE']:.4f}, R2={metrics['Test']['R2']:.4f}")

# Построение графиков функции потерь
plt.figure(figsize=(12, 8))

# Графики для обучающего набора
plt.subplot(2, 1, 1)
for opt_name, train_losses in losses_per_optimizer_train.items():
    plt.plot(range(1, epochs + 1), train_losses, label=f"{opt_name} (Train)")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("Training Loss for Different Optimizers")
plt.legend()

# Графики для тестового набора
plt.subplot(2, 1, 2)
for opt_name, test_losses in losses_per_optimizer_test.items():
    plt.plot(range(1, epochs + 1), test_losses, label=f"{opt_name} (Test)", linestyle='--')
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("Validation Loss for Different Optimizers")
plt.legend()

plt.tight_layout()
plt.show()
''',

                        'bike-n':'''from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

data = pd.read_csv('bike_cnt.csv')
data = data.iloc[:, 1:]
# Выделение признаков и целевой переменной
X = data.drop(columns=['cnt'])
y = data['cnt']
# Нормализация целевой переменной
max_y = y.max()
y = y / max_y

# Указание категориальных и числовых столбцов
categorical_cols = ['dteday', 'season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit']
numerical_cols = ['temp', 'atemp', 'hum', 'windspeed']

# Предобработка данных
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(), categorical_cols)
    ])

X_processed = preprocessor.fit_transform(X).toarray()

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

# Преобразование данных в тензоры
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1)

train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

# Определение различных архитектур
class SimpleModel(nn.Module):
    def __init__(self, input_dim):
        super(SimpleModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.fc(x)

class MediumModel(nn.Module):
    def __init__(self, input_dim):
        super(MediumModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.fc(x)

class ComplexModel(nn.Module):
    def __init__(self, input_dim):
        super(ComplexModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.fc(x)

# Параметры обучения
input_dim = X_train.shape[1]
batch_size = 64
epochs = 100
print_every = 10

# Словарь моделей для сравнения
models = {
    'Simple': SimpleModel(input_dim),
    'Medium': MediumModel(input_dim),
    'Complex': ComplexModel(input_dim)
}

# Словари для сохранения результатов
train_losses_dict = {}
test_losses_dict = {}
metrics_dict = {}

# Обучение и тестирование каждой модели
for model_name, model in models.items():
    print(f"Training {model_name} model...")
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    train_losses = []
    test_losses = []

    for epoch in range(epochs):
        # Обучение
        model.train()
        epoch_loss = 0
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_X)
            loss = criterion(predictions, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        train_losses.append(epoch_loss / len(train_loader))

        # Оценка на тестовой выборке
        model.eval()
        with torch.no_grad():
            test_predictions = model(X_test)
            test_loss = criterion(test_predictions, y_test).item()
        test_losses.append(test_loss)

    train_losses_dict[model_name] = train_losses
    test_losses_dict[model_name] = test_losses

    # Оценка метрик
    with torch.no_grad():
        y_train_pred = model(X_train).numpy()
        y_test_pred = model(X_test).numpy()

    train_mse = mean_squared_error(y_train.numpy(), y_train_pred)
    test_mse = mean_squared_error(y_test.numpy(), y_test_pred)
    train_mae = mean_absolute_error(y_train.numpy(), y_train_pred)
    test_mae = mean_absolute_error(y_test.numpy(), y_test_pred)
    train_r2 = r2_score(y_train.numpy(), y_train_pred)
    test_r2 = r2_score(y_test.numpy(), y_test_pred)

    metrics_dict[model_name] = {
        'train_mse': train_mse,
        'test_mse': test_mse,
        'train_mae': train_mae,
        'test_mae': test_mae,
        'train_r2': train_r2,
        'test_r2': test_r2
    }
    print(f"{model_name} Results: Train MSE={train_mse:.4f}, Test MSE={test_mse:.4f}")

# Построение графиков
plt.figure(figsize=(12, 8))
for model_name, train_losses in train_losses_dict.items():
    plt.plot(train_losses, label=f"{model_name} - Train")
    plt.plot(test_losses_dict[model_name], label=f"{model_name} - Test", linestyle='--')

plt.title("Изменение функции потерь для различных архитектур")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.grid()
plt.show()

# Вывод метрик
for model_name, metrics in metrics_dict.items():
    print(f"{model_name} Metrics:")
    for metric_name, value in metrics.items():
        print(f"  {metric_name}: {value:.4f}")
''',



                        
                        'gold':'''from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Загрузка данных
data = pd.read_csv('gold.csv')

# Выделение признаков и целевой переменной
target_columns = ['Gold_T-7', 'Gold_T-14', 'Gold_T-22', 'Gold_T+22']
X = data.drop(columns=target_columns)
y = data[target_columns]

# Нормализация целевой переменной
scaler_y = StandardScaler()
y_scaled = scaler_y.fit_transform(y)

# Нормализация признаков
scaler_X = StandardScaler()
X_scaled = scaler_X.fit_transform(X)

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# Преобразование данных в тензоры
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)

train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

# Определение нейронной сети
class GoldPredictorModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(GoldPredictorModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, output_dim)
        )

    def forward(self, x):
        return self.fc(x)

# Параметры обучения
input_dim = X_train.shape[1]
output_dim = y_train.shape[1]
model = GoldPredictorModel(input_dim, output_dim)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

batch_size = 64
epochs = 100
print_every = 10

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# Списки для хранения значений функции потерь
train_losses = []
test_losses = []

for epoch in range(epochs):
    epoch_loss = 0
    model.train()
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        predictions = model(batch_X)
        loss = criterion(predictions, batch_y)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()

    train_losses.append(epoch_loss / len(train_loader))

    # Оценка на тестовом наборе
    model.eval()
    with torch.no_grad():
        test_predictions = model(X_test)
        test_loss = criterion(test_predictions, y_test).item()
    test_losses.append(test_loss)

    if (epoch + 1) % print_every == 0:
        print(f'Epoch {epoch+1}/{epochs}, Train Loss: {epoch_loss / len(train_loader):.4f}, Test Loss: {test_loss:.4f}')

# Оценка модели
with torch.no_grad():
    y_train_pred = scaler_y.inverse_transform(model(X_train).numpy())
    y_train_true = scaler_y.inverse_transform(y_train.numpy())
    y_test_pred = scaler_y.inverse_transform(model(X_test).numpy())
    y_test_true = scaler_y.inverse_transform(y_test.numpy())

train_mse = mean_squared_error(y_train_true, y_train_pred)
train_mae = mean_absolute_error(y_train_true, y_train_pred)
train_r2 = r2_score(y_train_true, y_train_pred)
test_mse = mean_squared_error(y_test_true, y_test_pred)
test_mae = mean_absolute_error(y_test_true, y_test_pred)
test_r2 = r2_score(y_test_true, y_test_pred)

print(f"Результаты на обучающем наборе: MSE: {train_mse:.4f}, MAE: {train_mae:.4f}, R2: {train_r2:.4f}")
print(f"Результаты на тестовом наборе: MSE: {test_mse:.4f}, MAE: {test_mae:.4f}, R2: {test_r2:.4f}")

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(range(1, epochs + 1), train_losses, label="Train Loss")
plt.plot(range(1, epochs + 1), test_losses, label="Test Loss", linestyle='--')
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("Изменение функции потерь на обучающем и тестовом наборах в процессе обучения")
plt.legend()
plt.show()''',







                        
                        'gold-o':'''from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Загрузка данных
data = pd.read_csv('gold.csv')

# Выделение признаков и целевых переменных
target_columns = ['Gold_T-7', 'Gold_T-14', 'Gold_T-22', 'Gold_T+22']
X = data.drop(columns=target_columns)
y = data[target_columns]

# Нормализация данных
scaler_X = StandardScaler()
X_scaled = scaler_X.fit_transform(X)

scaler_y = StandardScaler()
y_scaled = scaler_y.fit_transform(y)

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# Преобразование данных в тензоры
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)

train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

# Определение нейронной сети
class GoldPredictorModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(GoldPredictorModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, output_dim)
        )

    def forward(self, x):
        return self.fc(x)

# Параметры обучения
input_dim = X_train.shape[1]
output_dim = y_train.shape[1]
batch_size = 64
epochs = 100
print_every = 10

# Список оптимизаторов для сравнения
optimizers = {
    'SGD': lambda params: torch.optim.SGD(params, lr=0.01),
    'Adam': lambda params: torch.optim.Adam(params, lr=0.001),
    'AdamW': lambda params: torch.optim.AdamW(params, lr=0.001, weight_decay=0.01),
    'RMSprop': lambda params: torch.optim.RMSprop(params, lr=0.001),
    'Adagrad': lambda params: torch.optim.Adagrad(params, lr=0.01)
}

# Результаты для каждого оптимизатора
results = {}
losses_per_optimizer_train = {}
losses_per_optimizer_test = {}

for opt_name, opt_func in optimizers.items():
    print(f"Training with {opt_name} optimizer")

    # Инициализация модели и оптимизатора
    model = GoldPredictorModel(input_dim, output_dim)
    criterion = nn.MSELoss()
    optimizer = opt_func(model.parameters())

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # Списки для хранения значений функции потерь
    train_losses = []
    test_losses = []

    for epoch in range(epochs):
        epoch_loss = 0
        i = 0
        model.train()
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_X)
            loss = criterion(predictions, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            i += 1

        epoch_loss = epoch_loss / i
        train_losses.append(epoch_loss)

        # Оценка функции потерь на тестовом наборе
        model.eval()
        with torch.no_grad():
            test_predictions = model(X_test)
            test_loss = criterion(test_predictions, y_test).item()
        test_losses.append(test_loss)

        if (epoch + 1) % print_every == 0:
            print(f'Epoch {epoch+1}/{epochs}, Train Loss: {epoch_loss:.4f}, Test Loss: {test_loss:.4f}')

    # Сохранение потерь для каждого оптимизатора
    losses_per_optimizer_train[opt_name] = train_losses
    losses_per_optimizer_test[opt_name] = test_losses

    # Оценка метрик на обучающем и тестовом наборах
    with torch.no_grad():
        y_train_pred = scaler_y.inverse_transform(model(X_train).numpy())
        y_train_true = scaler_y.inverse_transform(y_train.numpy())
        y_test_pred = scaler_y.inverse_transform(model(X_test).numpy())
        y_test_true = scaler_y.inverse_transform(y_test.numpy())

    train_mse = mean_squared_error(y_train_true, y_train_pred)
    train_mae = mean_absolute_error(y_train_true, y_train_pred)
    train_r2 = r2_score(y_train_true, y_train_pred)

    test_mse = mean_squared_error(y_test_true, y_test_pred)
    test_mae = mean_absolute_error(y_test_true, y_test_pred)
    test_r2 = r2_score(y_test_true, y_test_pred)

    results[opt_name] = {
        'Train': {'MSE': train_mse, 'MAE': train_mae, 'R2': train_r2},
        'Test': {'MSE': test_mse, 'MAE': test_mae, 'R2': test_r2}
    }

# Итоговые результаты
print("Final Comparison:")
for opt_name, metrics in results.items():
    print(f"{opt_name}:")
    print(f"  Train: MSE={metrics['Train']['MSE']:.4f}, MAE={metrics['Train']['MAE']:.4f}, R2={metrics['Train']['R2']:.4f}")
    print(f"  Test:  MSE={metrics['Test']['MSE']:.4f}, MAE={metrics['Test']['MAE']:.4f}, R2={metrics['Test']['R2']:.4f}")

# Построение графиков функции потерь
plt.figure(figsize=(12, 8))

# Графики для обучающего набора
plt.subplot(2, 1, 1)
for opt_name, train_losses in losses_per_optimizer_train.items():
    plt.plot(range(1, epochs + 1), train_losses, label=f"{opt_name} (Train)")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("Training Loss for Different Optimizers")
plt.legend()

# Графики для тестового набора
plt.subplot(2, 1, 2)
for opt_name, test_losses in losses_per_optimizer_test.items():
    plt.plot(range(1, epochs + 1), test_losses, label=f"{opt_name} (Test)", linestyle='--')
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("Validation Loss for Different Optimizers")
plt.legend()

plt.tight_layout()
plt.show()''',







                        
                        'gold-n':'''from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Загрузка данных
data = pd.read_csv('gold.csv')

# Выделение признаков и целевой переменной
target_columns = ['Gold_T-7', 'Gold_T-14', 'Gold_T-22', 'Gold_T+22']
X = data.drop(columns=target_columns)
y = data[target_columns]

# Нормализация целевой переменной
scaler_y = StandardScaler()
y_scaled = scaler_y.fit_transform(y)

# Нормализация признаков
scaler_X = StandardScaler()
X_scaled = scaler_X.fit_transform(X)

# Преобразование в тензоры
X_scaled = torch.tensor(X_scaled, dtype=torch.float32)
y_scaled = torch.tensor(y_scaled, dtype=torch.float32)

# Разделение на обучающую и тестовую выборки
dataset = TensorDataset(X_scaled, y_scaled)
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

# Определение архитектур моделей
class SimpleModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(SimpleModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, output_dim)
        )

    def forward(self, x):
        return self.fc(x)

class MediumModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(MediumModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, output_dim)
        )

    def forward(self, x):
        return self.fc(x)

class ComplexModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(ComplexModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, output_dim)
        )

    def forward(self, x):
        return self.fc(x)

# Параметры обучения
input_dim = X_scaled.shape[1]
output_dim = y_scaled.shape[1]
batch_size = 64
epochs = 100
print_every = 10

models = {
    'Simple': SimpleModel(input_dim, output_dim),
    'Medium': MediumModel(input_dim, output_dim),
    'Complex': ComplexModel(input_dim, output_dim)
}

train_losses_dict = {}
test_losses_dict = {}
metrics_dict = {}

# Обучение моделей
for model_name, model in models.items():
    print(f"Training {model_name} model...")
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    train_losses = []
    test_losses = []

    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_X)
            loss = criterion(predictions, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        train_losses.append(epoch_loss / len(train_loader))

        # Оценка на тестовой выборке
        model.eval()
        with torch.no_grad():
            test_predictions = model(torch.stack([x[0] for x in test_dataset]))
            test_loss = criterion(test_predictions, torch.stack([x[1] for x in test_dataset])).item()
        test_losses.append(test_loss)

    train_losses_dict[model_name] = train_losses
    test_losses_dict[model_name] = test_losses

    # Вычисление метрик
    with torch.no_grad():
        y_train_pred = model(torch.stack([x[0] for x in train_dataset]))
        y_test_pred = model(torch.stack([x[0] for x in test_dataset]))

    y_train_actual = torch.stack([x[1] for x in train_dataset]).numpy()
    y_test_actual = torch.stack([x[1] for x in test_dataset]).numpy()

    train_mse = mean_squared_error(y_train_actual, y_train_pred.numpy())
    test_mse = mean_squared_error(y_test_actual, y_test_pred.numpy())
    train_mae = mean_absolute_error(y_train_actual, y_train_pred.numpy())
    test_mae = mean_absolute_error(y_test_actual, y_test_pred.numpy())
    train_r2 = r2_score(y_train_actual, y_train_pred.numpy())
    test_r2 = r2_score(y_test_actual, y_test_pred.numpy())

    metrics_dict[model_name] = {
        'train_mse': train_mse,
        'test_mse': test_mse,
        'train_mae': train_mae,
        'test_mae': test_mae,
        'train_r2': train_r2,
        'test_r2': test_r2
    }
    print(f"{model_name} Results: Train MSE={train_mse:.4f}, Test MSE={test_mse:.4f}")

# Построение графиков
plt.figure(figsize=(12, 8))
for model_name, train_losses in train_losses_dict.items():
    plt.plot(train_losses, label=f"{model_name} - Train")
    plt.plot(test_losses_dict[model_name], label=f"{model_name} - Test", linestyle='--')

plt.title("Изменение функции потерь для различных архитектур")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.grid()
plt.show()

# Вывод метрик
for model_name, metrics in metrics_dict.items():
    print(f"{model_name} Metrics:")
    for metric_name, value in metrics.items():
        print(f"  {metric_name}: {value:.4f}")''',







                        
                        'bank':'''from sklearn.metrics import classification_report, confusion_matrix

# Загрузка данных
data = pd.read_csv('bank.csv')
X = data.drop(columns=['deposit'])
y = (data['deposit'] == 'yes').astype(np.float32)

# Предобработка данных
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(),
         ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']),
        ('cat', OneHotEncoder(sparse_output=False),
         ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'poutcome'])
    ]
)
X_processed = preprocessor.fit_transform(X)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

# Преобразование данных в тензоры PyTorch
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train.values, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test.values, dtype=torch.float32)

# Создание PyTorch Dataset
train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

# Определение модели
class Model(nn.Module):
    def __init__(self, input_size):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.5)  # Dropout для регуляризации
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc3(x)
        return self.sigmoid(x)

# Гиперпараметры
batch_size = 64
epochs = 100
learning_rate = 0.0005
print_every = 10

# Определение модели, функции потерь и оптимизатора
input_size = X_train.shape[1]
model = Model(input_size)
criterion = nn.BCELoss()
optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9)

# DataLoader для обучения
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# Списки для хранения значений функции потерь
train_losses = []
test_losses = []

# Цикл обучения
for epoch in range(epochs):
    model.train()
    epoch_loss = 0

    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        outputs = model(batch_X).squeeze()
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()

    # Средняя потеря на обучающей выборке за эпоху
    average_train_loss = epoch_loss / len(train_loader)
    train_losses.append(average_train_loss)

    # Оценка модели на тестовой выборке
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test).squeeze()
        test_loss = criterion(test_outputs, y_test).item()
        test_losses.append(test_loss)

    if (epoch + 1) % print_every == 0:
        print(f'Epoch {epoch + 1}/{epochs}, Train Loss: {average_train_loss:.4f}, Test Loss: {test_loss:.4f}')

# Графики значений функции потерь
plt.plot(range(1, epochs + 1), train_losses, label="Потери на обучающей выборке")
plt.plot(range(1, epochs + 1), test_losses, label="Потери на тестовой выборке")
plt.xlabel("Эпохи")
plt.ylabel("Потери")
plt.title("График потерь")
plt.legend()
plt.show()

# Оценка модели на тестовой и обучающей выборках
model.eval()
with torch.no_grad():
    y_train_pred = model(X_train).squeeze()
    y_train_pred_class = (y_train_pred >= 0.5).float()
    y_test_pred = model(X_test).squeeze()
    y_test_pred_class = (y_test_pred >= 0.5).float()

# Confusion Matrix и Classification Report для обучающей выборки
print("Classification Report (Обучающая выборка):")
print(classification_report(y_train.numpy(), y_train_pred_class.numpy()))
print("Confusion Matrix (Обучающая выборка):")
print(confusion_matrix(y_train.numpy(), y_train_pred_class.numpy()))

# Confusion Matrix и Classification Report для тестовой выборки
print("Classification Report (Тестовая выборка):")
print(classification_report(y_test.numpy(), y_test_pred_class.numpy()))
print("Confusion Matrix (Тестовая выборка):")
print(confusion_matrix(y_test.numpy(), y_test_pred_class.numpy()))''',







                        
                        'bank-o':'''from sklearn.metrics import classification_report, confusion_matrix

# Загрузка данных
data = pd.read_csv('bank.csv')
X = data.drop(columns=['deposit'])
y = (data['deposit'] == 'yes').astype(np.float32)

# Предобработка данных
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(),
         ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']),
        ('cat', OneHotEncoder(sparse_output=False),
         ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'poutcome'])
    ]
)
X_processed = preprocessor.fit_transform(X)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

# Преобразование данных в тензоры PyTorch
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train.values, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test.values, dtype=torch.float32)

# Создание PyTorch Dataset
train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

# Определение модели
class Model(nn.Module):
    def __init__(self, input_size):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=0.5)  # Dropout для регуляризации
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc3(x)
        return self.sigmoid(x)

# Гиперпараметры
batch_size = 64
epochs = 50
learning_rate = 0.0005
print_every = 10

# Оптимизаторы для сравнения
optimizers = {
    'SGD': lambda params: optim.SGD(params, lr=learning_rate, momentum=0.9),
    'Adam': lambda params: optim.Adam(params, lr=learning_rate),
    'RMSprop': lambda params: optim.RMSprop(params, lr=learning_rate)
}

# 'AdamW': lambda params: optim.AdamW(params, lr=learning_rate, weight_decay=0.01)
# 'Adagrad': lambda params: optim.Adagrad(params, lr=learning_rate)

# Словари для хранения потерь
train_losses_dict = {}
test_losses_dict = {}
metrics_dict = {}

# Сравнение оптимизаторов
for opt_name, opt_fn in optimizers.items():
    print(f"Training with {opt_name} optimizer...")
    model = Model(X_train.shape[1])
    criterion = nn.BCELoss()
    optimizer = opt_fn(model.parameters())
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    train_losses = []
    test_losses = []

    for epoch in range(epochs):
        model.train()
        epoch_loss = 0

        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_X).squeeze()
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        # Средняя потеря на обучающей выборке за эпоху
        average_train_loss = epoch_loss / len(train_loader)
        train_losses.append(average_train_loss)

        # Оценка модели на тестовой выборке
        model.eval()
        with torch.no_grad():
            test_outputs = model(X_test).squeeze()
            test_loss = criterion(test_outputs, y_test).item()
            test_losses.append(test_loss)

        if (epoch + 1) % print_every == 0:
            print(f'Epoch {epoch + 1}/{epochs}, Train Loss: {average_train_loss:.4f}, Test Loss: {test_loss:.4f}')

    train_losses_dict[opt_name] = train_losses
    test_losses_dict[opt_name] = test_losses

    # Вычисление метрик
    with torch.no_grad():
        y_train_pred = model(X_train).squeeze()
        y_train_pred_class = (y_train_pred >= 0.5).float()
        y_test_pred = model(X_test).squeeze()
        y_test_pred_class = (y_test_pred >= 0.5).float()

    metrics_dict[opt_name] = {
        'train_report': classification_report(y_train.numpy(), y_train_pred_class.numpy(), output_dict=True),
        'test_report': classification_report(y_test.numpy(), y_test_pred_class.numpy(), output_dict=True)
    }

# Построение графиков потерь
plt.figure(figsize=(12, 8))
for opt_name, train_losses in train_losses_dict.items():
    plt.plot(train_losses, label=f"{opt_name} - Train")
    plt.plot(test_losses_dict[opt_name], label=f"{opt_name} - Test", linestyle='--')

plt.title("Графики потерь для различных оптимизаторов")
plt.xlabel("Эпохи")
plt.ylabel("Потери")
plt.legend()
plt.grid()
plt.show()

# Вывод метрик
for opt_name, metrics in metrics_dict.items():
    print(f"Metrics for {opt_name} optimizer:")
    print("Training Report:")
    train_report_df = pd.DataFrame(metrics['train_report']).transpose()
    print(train_report_df)
    print("Test Report:")
    test_report_df = pd.DataFrame(metrics['test_report']).transpose()
    print(test_report_df)''',






                        
                        'bank-n':'''from sklearn.metrics import classification_report, confusion_matrix

# Загрузка данных
data = pd.read_csv('bank.csv')
X = data.drop(columns=['deposit'])
y = (data['deposit'] == 'yes').astype(np.float32)

# Предобработка данных
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(),
         ['age', 'balance', 'day', 'duration', 'campaign', 'pdays', 'previous']),
        ('cat', OneHotEncoder(sparse_output=False),
         ['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'poutcome'])
    ]
)
X_processed = preprocessor.fit_transform(X)

# Разделение данных
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

# Преобразование в тензоры
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train.values, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test.values, dtype=torch.float32)

train_dataset = TensorDataset(X_train, y_train)
test_dataset = TensorDataset(X_test, y_test)

# Определение различных моделей
class SimpleModel(nn.Module):
    def __init__(self, input_size):
        super(SimpleModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_size, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.fc(x)

class MediumModel(nn.Module):
    def __init__(self, input_size):
        super(MediumModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.fc(x)

class ComplexModel(nn.Module):
    def __init__(self, input_size):
        super(ComplexModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.fc(x)

# Сравнение моделей
models = {
    'SimpleModel': SimpleModel(X_train.shape[1]),
    'MediumModel': MediumModel(X_train.shape[1]),
    'ComplexModel': ComplexModel(X_train.shape[1]),
}

batch_size = 64
epochs = 50
learning_rate = 0.001
results = {}

for model_name, model in models.items():
    print(f"Training {model_name}...")
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    train_losses = []
    test_losses = []

    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_X).squeeze()
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        train_losses.append(epoch_loss / len(train_loader))

        model.eval()
        with torch.no_grad():
            test_outputs = model(X_test).squeeze()
            test_loss = criterion(test_outputs, y_test).item()
            test_losses.append(test_loss)

    # Оценка
    model.eval()
    with torch.no_grad():
        y_test_pred = model(X_test).squeeze()
        y_test_pred_class = (y_test_pred >= 0.5).float()

    print(classification_report(y_test.numpy(), y_test_pred_class.numpy()))
    results[model_name] = (train_losses, test_losses)

# Графики
plt.figure(figsize=(12, 6))
for model_name, (train_losses, test_losses) in results.items():
    plt.plot(train_losses, label=f"{model_name} Train Loss")
    plt.plot(test_losses, label=f"{model_name} Test Loss", linestyle="--")

plt.title("Comparison of Model Losses")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid()
plt.show()''',






                        
                        'bank-c':'''from sklearn.utils.class_weight import compute_class_weight

# Вычисление весов классов
classes = np.array([0, 1])  # Map 'no' -> 0, 'yes' -> 1
y_values = (data['deposit'] == 'yes').astype(int).values
class_weights = compute_class_weight(class_weight='balanced', classes=classes, y=y_values)
class_weights_tensor = torch.tensor(class_weights, dtype=torch.float32)

# Определение модели, функции потерь и оптимизатора
input_size = X_train.shape[1]
model = Model(input_size)
criterion = nn.BCELoss(weight=class_weights_tensor[y_train.long()])  # Учет весов классов
optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9)

# DataLoader для обучения
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

# Списки для хранения значений функции потерь
train_losses = []
test_losses = []

# Цикл обучения
for epoch in range(epochs):
    model.train()
    epoch_loss = 0

    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()

        # Прямой проход
        outputs = model(batch_X).squeeze()

        # Применение весов классов к каждому элементу в батче
        weights = class_weights_tensor[batch_y.long()]
        loss = nn.BCELoss(weight=weights)(outputs, batch_y)

        # Обратное распространение и обновление параметров
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()

    # Средняя потеря на обучающей выборке за эпоху
    average_train_loss = epoch_loss / len(train_loader)
    train_losses.append(average_train_loss)

    # Оценка модели на тестовой выборке
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test).squeeze()
        test_weights = class_weights_tensor[y_test.long()]
        test_loss = nn.BCELoss(weight=test_weights)(test_outputs, y_test).item()
        test_losses.append(test_loss)

    if (epoch + 1) % print_every == 0:
        print(f'Epoch {epoch + 1}/{epochs}, Train Loss: {average_train_loss:.4f}, Test Loss: {test_loss:.4f}')

# Графики значений функции потерь
plt.plot(range(1, epochs + 1), train_losses, label="Потери на обучающей выборке")
plt.plot(range(1, epochs + 1), test_losses, label="Потери на тестовой выборке")
plt.xlabel("Эпохи")
plt.ylabel("Потери")
plt.title("График потерь")
plt.legend()
plt.show()

# Оценка модели на тестовой и обучающей выборках
model.eval()
with torch.no_grad():
    y_train_pred = model(X_train).squeeze()
    y_train_pred_class = (y_train_pred >= 0.5).float()
    y_test_pred = model(X_test).squeeze()
    y_test_pred_class = (y_test_pred >= 0.5).float()

# Confusion Matrix и Classification Report для обучающей выборки
print("Classification Report (Обучающая выборка):")
print(classification_report(y_train.numpy(), y_train_pred_class.numpy()))
print("Confusion Matrix (Обучающая выборка):")
print(confusion_matrix(y_train.numpy(), y_train_pred_class.numpy()))

# Confusion Matrix и Classification Report для тестовой выборки
print("Classification Report (Тестовая выборка):")
print(classification_report(y_test.numpy(), y_test_pred_class.numpy()))
print("Confusion Matrix (Тестовая выборка):")
print(confusion_matrix(y_test.numpy(), y_test_pred_class.numpy()))'''}



        self.themes = [{value: key} for key, value in self.sklad.items()]

    def search(self, text):
        ress = []
        for theme in self.themes:
            for key, value in theme.items():
                if text in key:
                    ress.append(f"{key} : {value}")
        return ress








class test3:
    def __init__(self):
        self.sklad = {
            'imp':'''import zipfile
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import datasets, transforms
from PIL import Image
from sklearn.metrics import f1_score
import numpy as np
import matplotlib.pyplot as plt
import random

with zipfile.ZipFile('chars.zip', 'r') as zip_ref:
    zip_ref.extractall('images')

data_dir = 'images/chars'
for root, dirs, files in os.walk(data_dir):
    print(f"В директории: {root}")
    print("Поддиректории:", dirs)
    print("Файлы:", files[:10])
    print('Количество файлов:', len(files))
    print("-" * 50)''',












            
            'chars':'''image_size = 256

base_transform = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

augmented_transform = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])
################
batch_size = 16

dataset = datasets.ImageFolder(data_dir, transform=base_transform)
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
################
class SimpleCNN(nn.Module):
    def __init__(self, num_classes, image_size):
        super(SimpleCNN, self).__init__()
        # Сверточные слои
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(2, 2)
        # Полносвязные слои
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(32 * (image_size // 4) * (image_size // 4), 128)
        self.fc2 = nn.Linear(128, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.maxpool(x)
        x = self.relu(self.conv2(x))
        x = self.maxpool(x)
        x = self.flatten(x)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)

        return self.sigmoid(x)
################
num_classes = len(dataset.classes)
model = SimpleCNN(num_classes, image_size)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
num_epochs = 10
print(num_classes, dataset.classes)
################
def train_model(model, loader, criterion, optimizer, epochs):
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for i, (images, labels) in enumerate(loader):
            optimizer.zero_grad()

            # Прямой проход
            outputs = model(images)

            # Применяем squeeze, чтобы привести размерность выходных данных к (batch_size,)
            outputs = outputs.view(-1)

            # Преобразуем labels в (batch_size,)
            labels = labels.float().view(-1)

            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        epoch_loss = running_loss / len(loader)
        print(f"Эпоха [{epoch+1}/{epochs}], Потери: {epoch_loss:.4f}")

def evaluate_model(model, loader):
    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for images, labels in loader:
            outputs = model(images)

            # Применяем squeeze для получения вероятности
            outputs = outputs.view(-1)  # Преобразуем в одномерный тензор

            # Применяем порог 0.5 для бинарной классификации
            preds = (outputs > 0.5).long()

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    return f1_score(all_labels, all_preds, average='weighted')
#################
train_model(model, train_loader, criterion, optimizer, num_epochs)
f1_base = evaluate_model(model, test_loader)
print("F1 на базовом наборе данных:", f1_base) #4 мин 50 сек
#################
train_dataset.dataset.transform = augmented_transform
train_model(model, train_loader, criterion, optimizer, num_epochs)
f1_augmented = evaluate_model(model, test_loader)
print("F1 на расширенном наборе данных:", f1_augmented) #4 мин 37 сек''',








            
            'eng':'''transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=3),
    transforms.Resize(224),
    transforms.CenterCrop(224),  # Вырезаем центральную часть изображения
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
#################
dataset = datasets.ImageFolder(root=data_dir, transform=transform)

train_size = int(0.7 * len(dataset))
val_size = int(0.15 * len(dataset))
test_size = len(dataset) - train_size - val_size

train_dataset, val_dataset, test_dataset = random_split(dataset, [train_size, val_size, test_size])

batch_size = 32
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
##################
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(128*28*28, 512)  # Размер после Conv слоев (224x224 -> 28x28)
        self.fc2 = nn.Linear(512, 26)  # 26 классов (буквы от A до Z)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.max_pool2d(x, 2)
        x = torch.relu(self.conv2(x))
        x = torch.max_pool2d(x, 2)
        x = torch.relu(self.conv3(x))
        x = torch.max_pool2d(x, 2)
        x = x.view(x.size(0), -1)  # Разворачиваем тензор
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x
###################
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
###################
model = CNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
def calculate_micro_f1(y_true, y_pred):
    return f1_score(y_true, y_pred, average='micro')

def early_stop(val_f1, best_val_f1, epochs_without_improvement, patience):
    if val_f1 > best_val_f1:
        best_val_f1 = val_f1
        epochs_without_improvement = 0
    else:
        epochs_without_improvement += 1

    stop = epochs_without_improvement >= patience
    return stop, best_val_f1, epochs_without_improvement
###################
best_val_f1 = 0
epochs_without_improvement = 0
max_epochs = 50
early_stop_patience = 3

for epoch in range(max_epochs):
    model.train()
    running_loss = 0.0
    y_true, y_pred = [], []

    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    model.eval()
    val_y_true, val_y_pred = [], []
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            val_y_true.extend(labels.cpu().numpy())
            val_y_pred.extend(predicted.cpu().numpy())

    val_f1 = calculate_micro_f1(np.array(val_y_true), np.array(val_y_pred))

    print(f'Эпоха [{epoch+1}/{max_epochs}], Функция потерь: {running_loss/len(train_loader):.4f}, Val Micro F1: {val_f1:.4f}')

    stop, best_val_f1, epochs_without_improvement = early_stop(
        val_f1, best_val_f1, epochs_without_improvement, early_stop_patience
    )

    if stop:
        print("Early stopping")
        break
###################
model.eval()
test_y_true, test_y_pred = [], []
with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)
        test_y_true.extend(labels.cpu().numpy())
        test_y_pred.extend(predicted.cpu().numpy())

test_f1 = calculate_micro_f1(np.array(test_y_true), np.array(test_y_pred))
print(f'Test Micro F1: {test_f1:.4f}')''',



            
            'clothes':'''
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

dataset = datasets.ImageFolder(root=data_dir, transform=transform)

class_names = dataset.classes
color_to_idx = {}
item_to_idx = {}
colors = set()
items = set()

for class_name in class_names:
    color, item = class_name.split('_')
    colors.add(color)
    items.add(item)

color_to_idx = {color: idx for idx, color in enumerate(sorted(colors))}
item_to_idx = {item: idx for idx, item in enumerate(sorted(items))}

def get_color_and_item_labels(target):
    class_name = class_names[target]
    color, item = class_name.split('_')
    return color_to_idx[color], item_to_idx[item]

class MultiLabelDataset(torch.utils.data.Dataset):
    def __init__(self, dataset):
        self.dataset = dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        img, target = self.dataset[idx]
        color_label, item_label = get_color_and_item_labels(target)
        return img, torch.tensor([color_label, item_label])

multi_label_dataset = MultiLabelDataset(dataset)

train_size = int(0.8 * len(multi_label_dataset))
test_size = len(multi_label_dataset) - train_size
train_dataset, test_dataset = random_split(multi_label_dataset, [train_size, test_size])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
#################
class ClothesCNN(nn.Module):
    def __init__(self, num_colors, num_items):
        super(ClothesCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.fc1 = nn.Linear(64 * 32 * 32, 128)
        self.fc_color = nn.Linear(128, num_colors)
        self.fc_item = nn.Linear(128, num_items)

    def forward(self, x):
        x = self.pool(nn.functional.relu(self.conv1(x)))
        x = self.pool(nn.functional.relu(self.conv2(x)))
        x = x.view(-1, 64 * 32 * 32)
        x = nn.functional.relu(self.fc1(x))
        color_output = self.fc_color(x)
        item_output = self.fc_item(x)
        return color_output, item_output
##################
num_colors = len(color_to_idx)
num_items = len(item_to_idx)
model = ClothesCNN(num_colors, num_items)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
##################
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
##################
num_epochs = 10
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images = images.to(device)
        color_labels = labels[:, 0].to(device)
        item_labels = labels[:, 1].to(device)

        optimizer.zero_grad()
        color_output, item_output = model(images)
        loss = criterion(color_output, color_labels) + criterion(item_output, item_labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}")
#########################
model.eval()
all_color_preds = []
all_color_labels = []
all_item_preds = []
all_item_labels = []

with torch.no_grad():
    for images, labels in train_loader:
        images = images.to(device)
        color_labels = labels[:, 0].to(device)
        item_labels = labels[:, 1].to(device)

        color_output, item_output = model(images)
        _, color_preds = torch.max(color_output, 1)
        _, item_preds = torch.max(item_output, 1)

        all_color_preds.extend(color_preds.cpu().numpy())
        all_color_labels.extend(color_labels.cpu().numpy())
        all_item_preds.extend(item_preds.cpu().numpy())
        all_item_labels.extend(item_labels.cpu().numpy())

train_color_f1 = f1_score(all_color_labels, all_color_preds, average='weighted')
train_item_f1 = f1_score(all_item_labels, all_item_preds, average='weighted')
print(f"Train F1 Score - Color: {train_color_f1:.4f}, Item: {train_item_f1:.4f}")
########################
model.eval()
all_color_preds = []
all_color_labels = []
all_item_preds = []
all_item_labels = []

with torch.no_grad():
    for images, labels in test_loader:
        images = images.to(device)
        color_labels = labels[:, 0].to(device)
        item_labels = labels[:, 1].to(device)

        color_output, item_output = model(images)
        _, color_preds = torch.max(color_output, 1)
        _, item_preds = torch.max(item_output, 1)

        all_color_preds.extend(color_preds.cpu().numpy())
        all_color_labels.extend(color_labels.cpu().numpy())
        all_item_preds.extend(item_preds.cpu().numpy())
        all_item_labels.extend(item_labels.cpu().numpy())

test_color_f1 = f1_score(all_color_labels, all_color_preds, average='macro')
test_item_f1 = f1_score(all_item_labels, all_item_preds, average='macro')
print(f"Test F1 Score - Color: {test_color_f1:.4f}, Item: {test_item_f1:.4f}")''',




            
            'sign':'''transform = transforms.Compose([
    transforms.Resize((100, 100)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
#################
dataset = datasets.ImageFolder(root=data_dir, transform=transform)

train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
###################
class CNN(nn.Module):
    def __init__(self, num_conv_blocks):
        super(CNN, self).__init__()
        self.conv_blocks = nn.ModuleList()
        in_channels = 3
        out_channels = 32

        for _ in range(num_conv_blocks):
            self.conv_blocks.append(
                nn.Sequential(
                    nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
                    nn.ReLU(),
                    nn.MaxPool2d(kernel_size=2, stride=2)
                )
            )
            in_channels = out_channels
            out_channels *= 2

        self.feature_size = self._get_conv_output((3, 100, 100))

        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(self.feature_size, 128),
            nn.ReLU(),
            nn.Linear(128, len(dataset.classes))
        )

    def _get_conv_output(self, shape):
        with torch.no_grad():
            input = torch.zeros(1, *shape)
            for block in self.conv_blocks:
                input = block(input)
            return int(torch.prod(torch.tensor(input.size()[1:])))

    def forward(self, x):
        for block in self.conv_blocks:
            x = block(x)
        x = self.fc(x)
        return x
#####################
def calculate_micro_f1(model, data_loader):
    model.eval()
    y_true = []
    y_pred = []
    with torch.no_grad():
        for inputs, labels in data_loader:
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            y_true.extend(labels.numpy())
            y_pred.extend(predicted.numpy())
    return f1_score(y_true, y_pred, average='micro')
################
num_conv_blocks_list = [1, 2, 3, 4]
micro_f1_scores = []

for num_conv_blocks in num_conv_blocks_list:
    model = CNN(num_conv_blocks)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    num_epochs = 5
    for epoch in range(num_epochs):
        model.train()
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

    # Оцениваем качество на тестовой выборке
    micro_f1 = calculate_micro_f1(model, test_loader)
    micro_f1_scores.append(micro_f1)
    print(f"Количество сверточных блоков: {num_conv_blocks}, Micro F1: {micro_f1}")
#########################
plt.plot(num_conv_blocks_list, micro_f1_scores, marker='o')
plt.xlabel('Количество сверточных блоков')
plt.ylabel('Micro F1')
plt.title('Зависимость качества от количества сверточных блоков')
plt.grid(True)
plt.show()''',







            
            'sign-pca':'''import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np

def extract_features(model, data_loader):
    """
    Извлечение скрытых представлений после свёрточных блоков.
    """
    model.eval()
    features = []
    labels = []
    with torch.no_grad():
        for inputs, targets in data_loader:
            for block in model.conv_blocks:
                inputs = block(inputs)
            inputs = torch.flatten(inputs, start_dim=1)  # Выравниваем признаки
            features.append(inputs.cpu().numpy())
            labels.extend(targets.cpu().numpy())
    features = np.vstack(features)
    return features, np.array(labels)

# Выбираем модель с определенным количеством свёрточных блоков
num_conv_blocks = 3
model = CNN(num_conv_blocks)

# Извлекаем признаки
hidden_features, targets = extract_features(model, test_loader)

# Уменьшаем размерность до 2D с помощью PCA
pca = PCA(n_components=2)
reduced_features = pca.fit_transform(hidden_features)

# Визуализация
plt.figure(figsize=(10, 8))
for class_idx in np.unique(targets):
    plt.scatter(
        reduced_features[targets == class_idx, 0],
        reduced_features[targets == class_idx, 1],
        label=f'Class {class_idx}',
        alpha=0.7
    )

plt.title(f'PCA Visualization of Features (Blocks: {num_conv_blocks})')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.show()'''}

        self.themes = [{value: key} for key, value in self.sklad.items()]

    def search(self, text):
        ress = []
        for theme in self.themes:
            for key, value in theme.items():
                if text in key:
                    ress.append(f"{key} : {value}")
        return ress










#test2_instance = test2()
#print(test2_instance.themes)  # Вывод themes
#print(test2_instance.sklad["imp"])  # Поиск по ключу "imp"

# Работа с test3
test3_instance = test3()
print(test3_instance.themes)  # Вывод themes
print(test3_instance.sklad["imp"])  # Поиск по ключу "imp"
