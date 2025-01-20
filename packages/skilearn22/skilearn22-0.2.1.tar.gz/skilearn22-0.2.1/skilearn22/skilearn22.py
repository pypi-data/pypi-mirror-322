questions = {1: {'code': "\ndata = pd.read_csv('regression/bike_cnt.csv')\n\nX = data.drop(columns=['cnt', 'dteday'])\ny = data['cnt']\n\ncategorical_cols = X.drop(columns=['temp', 'atemp', 'hum', 'windspeed']).columns\nnumerical_cols = X.drop(columns=categorical_cols).columns\n\n\nX_processed = preprocessor.fit_transform(X).toarray() "},

             2: {'code': '\nclass Model(nn.Module):\n    def __init__(self):\n        super(Model, self).__init__()\n        self.network = nn.Sequential(\n            nn.Linear(X_train.shape[1], 64),\n            nn.BatchNorm1d(64),\n            nn.ReLU(),\n            nn.Dropout(0.5),\n            nn.Linear(64, 32),\n            nn.BatchNorm1d(32),\n            nn.ReLU(),\n            nn.Dropout(0.5),\n            nn.Linear(32, 16),\n            nn.ReLU(),\n            nn.Linear(16, 1)\n        )\n\n    def forward(self, x):\n        return self.network(x) '},
             3: {'code': "\nmodel = Model()\ncriterion = nn.MSELoss()\noptimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)\n\ntest_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)\n\ntest_losses = []\ntrain_losses = []\n"},
             4: {'code': '\nfor epoch in range(epochs):\n    model.train()\n    epoch_loss = 0\n    y_pred_train = []\n    y_true_train = []\n    for batch_X, batch_y in train_loader:\n        optimizer.zero_grad()\n\n        outputs = model(batch_X)\n\n        loss = criterion(outputs, batch_y)\n        loss.backward()\n        optimizer.step()\n\n        epoch_loss += loss.item()\n\n        y_pred_train.extend(batch_y.tolist())\n        y_true_train.extend(outputs.tolist())\n '},
             5: {'code': "\n    train_loss = epoch_loss / len(train_loader)\n    train_losses.append(train_loss)\n\n    model.eval()\n    test_loss = 0\n    y_pred_test = []\n    y_true_test = []\n    with torch.no_grad():\n        for batch_X, batch_y in test_loader:\n            outputs = model(batch_X)\n            loss = criterion(outputs, batch_y)\n            test_loss += loss\n    test_loss = test_loss / len(test_loader)\n    test_losses.append(test_loss)\n\n    if (epoch+1) % print_every == 0:\n        print(f'Epoch {epoch+1}/{epochs}, Train Loss: {train_loss:.4f}, Test Loss: {test_loss:.4f}')\n "},
             6: {'code': "\nplt.figure(figsize = (10, 6))\nplt.plot(range(1, epochs + 1), train_losses, label = 'Train Loss')\nplt.plot(range(1, epochs + 1), test_losses, label = 'Test Loss')\nplt.xlabel('Epoch')\nplt.ylabel('Loss')\nplt.legend()\nplt.grid()\nplt.show()\n "},
             7: {'code': '\nfrom sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score\n\nmodel.eval()\nwith torch.no_grad():\n    outputs = model(X_test)\n    r2 = r2_score(y_test.numpy(), outputs.numpy())\n    mse = mean_squared_error(y_test.numpy(), outputs.numpy())\n    mae = r2_score(y_test.numpy(), outputs.numpy())\nr2, mse, mae\n '},
             8: {'code': "\nfrom sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder\nfrom sklearn.metrics import f1_score\n\ndata = pd.read_csv('classification/bank.csv')\n\nX = data.drop(columns=['deposit'])\ny = data['deposit']\nle = LabelEncoder()\ny = le.fit_transform(y)\n\ncategorical_cols = X.drop(columns=['age', 'balance', 'duration', 'campaign', 'pdays', 'previous']).columns\nnumerical_cols = X.drop(columns=categorical_cols).columns\n\nX_processed = preprocessor.fit_transform(X).toarray()\nX_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42, stratify=y) \n "},
             9: {'code': '\nclass Model(nn.Module):\n    def __init__(self):\n        super(Model, self).__init__()\n        self.model = nn.Sequential(\n            nn.Linear(X_train.shape[1], 64),\n            nn.BatchNorm1d(64),\n            nn.ReLU(),\n            nn.Dropout(0.5),  # chance 50%\n            nn.Linear(64, 1)\n        )\n\n    def forward(self, x):\n        return self.model(x).squeeze() # нужен squeeze либо здесь, либо для outputs\n '},
             10: {'code': '\nfrom sklearn.utils.class_weight import compute_class_weight\n\nclasses = np.array([0, 1])\n\n# Compute class weights\nclass_weights = compute_class_weight(class_weight=\'balanced\', classes=classes, y=y)\n\nfor i, weight in enumerate(class_weights):\n    print(f"Class {classes[i]}: {weight}")\n '},
             11: {'code': '\nclass_weights_tensor = torch.tensor(class_weights, dtype=torch.float32)\n\nmodel = Model()\ncriterion = nn.BCEWithLogitsLoss(pos_weight=class_weights_tensor[1] / class_weights_tensor[0])\noptimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-3)\n\ntest_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)\n\ntrain_losses = []\ntest_losses = []\ntrain_f1_scores = []\ntest_f1_scores = []\n '},
             12: {'code': '\nfor epoch in range(epochs):\n    model.train()\n    epoch_loss = 0.0\n\n    y_true_train = []\n    y_pred_train = []\n\n    for batch_X, batch_y in train_loader:\n        optimizer.zero_grad()\n        outputs = model(batch_X)\n        loss = criterion(outputs, batch_y)\n        loss.backward()\n        optimizer.step()\n        epoch_loss += loss.item()\n\n        y_true_train.extend(batch_y.tolist())\n        y_pred_train.extend((torch.sigmoid(outputs) > 0.7).float().tolist()) \n '},
             13: {'code': '\n    # считаем потери и f1 за эпоху\n    train_loss = epoch_loss / len(train_loader)\n    train_losses.append(train_loss)\n    train_f1 = f1_score(y_true_train, y_pred_train)\n    train_f1_scores.append(train_f1)\n\n    # тест\n    model.eval()\n    running_loss = 0.0\n    y_true_test = []\n    y_pred_test = []\n '},
             14: {'code': "\n    with torch.no_grad():\n        for batch_x, batch_y in test_loader:\n            outputs = model(batch_x)\n\n            loss = criterion(outputs, batch_y)\n\n            running_loss += loss.item()\n\n            y_true_test.extend(batch_y.tolist())\n            y_pred_test.extend((torch.sigmoid(outputs) > 0.7).float().tolist()) # Применяем сигмоиду для получения вероятностей (для классификации)\n\n    test_loss = running_loss / len(test_loader)\n    test_losses.append(test_loss)\n    test_f1 = f1_score(y_true_test, y_pred_test)\n    test_f1_scores.append(test_f1)\n\n    if (epoch+1) % print_every == 0:\n        print(f'Epoch {epoch+1}/{epochs}, Train_Loss: {train_loss:.4f}, Test_Loss: {test_loss:.4f}, Train_F1: {train_f1:.4f}, Test_F1: {test_f1:.4f}')\n\n "},
             15: {'code': "\n# Построение графиков\nplt.figure(figsize=(12, 5))\n\nplt.subplot(1, 2, 1)\nplt.plot(train_losses, label='Train Loss')\nplt.plot(test_losses, label='Test Loss')\nplt.xlabel('Epoch')\nplt.ylabel('Loss')\nplt.title('Loss over Epochs')\nplt.legend()\n "},
             16: {'code': "\nplt.subplot(1, 2, 2)\nplt.plot(train_f1_scores, label='Train F1 Score')\nplt.plot(test_f1_scores, label='Test F1 Score')\nplt.xlabel('Epoch')\nplt.ylabel('F1 Score')\nplt.title('F1 Score over Epochs')\nplt.legend()\n\nplt.show()\n\n# Вывод итогового F1 score\nfinal_test_f1 = f1_score(y_true_test, y_pred_test)\nprint(f'Final Test F1 Score: {final_test_f1:.4f}')\n "},
             17: {'code': '\nfrom torch.utils.data import DataLoader, random_split, TensorDataset, Dataset\nfrom torchvision import datasets, transforms\nfrom sklearn.metrics import f1_score, accuracy_score\nfrom tqdm import tqdm\n\ndata_dir = "sign_language/"\n\n# Загрузка данных\nfull_dataset = ImageFolder(data_dir, transform=transforms.Compose([\n                                                                transforms.ToTensor(),\n                                                                transforms.Resize((64, 64))   # тут картинки разного размера есть,\n                                                                                                # 64 из головы\n]))\ndataloader = DataLoader(full_dataset, batch_size=batch_size)\n'},
             18: {'code': '\nmean = 0\nstd = 0\nnb_samples = 0\n\nfor img, _ in tqdm(dataloader):\n    batch_samples = img.size(0)\n    img = img.view(batch_samples, img.size(1), -1)\n    mean += img.mean(2).sum(0)\n    std += img.std(2).sum(0)\n    nb_samples += batch_samples\n\nmean /= nb_samples\nstd /= nb_samples\n'},
             19: {'code': '\n# Предобработка изображений\ntransform_train = transforms.Compose([\n    transforms.RandomHorizontalFlip(),\n    transforms.RandomRotation(degrees=15),\n    transforms.Normalize(mean, std),\n])\n\ntransform_test = transforms.Compose([\n    transforms.Normalize(mean, std)\n])\n'},
             20: {'code': '\ntrain_size = int(0.7 * len(full_dataset))\ntest_size = len(full_dataset) - train_size\ntrain_dataset, test_dataset = torch.utils.data.random_split(full_dataset, [train_size, test_size])\n\ntrain_dataset = TransformDataset(train_dataset, transform=transform_train)\ntest_dataset = TransformDataset(test_dataset, transform=transform_test)\n\ntrain_loader = DataLoader(train_dataset, batch_size=batch_size)\ntest_loader = DataLoader(test_dataset, batch_size=batch_size)\n'},
             21: {'code': '\n    def __init__(self, nclasses):\n        super(CNN, self).__init__()\n        self.conv_layers = nn.Sequential(\n            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1),\n            nn.ReLU(),\n            nn.MaxPool2d(kernel_size=2, stride=2),\n\n            nn.Conv2d(32, 16, kernel_size=3, stride=1, padding=1),\n            nn.ReLU(),\n            nn.MaxPool2d(kernel_size=2, stride=2),\n        )\n\n        self.fc_layers = nn.Sequential(\n            nn.Flatten(),\n            nn.Linear(16 * 16 * 16, 32),  # какого-то хуя тут была ошибка хотя он реально 16*16*16\n            nn.ReLU(),\n            nn.Linear(32, nclasses)\n        )\n'},
             22: {'code': '\n    def forward(self, x):\n        x = self.conv_layers(x)\n        fc_input_size = x.size(1) * x.size(2) * x.size(3) # поэтому пусть он сам считает сколько там надо\n        self.fc_layers[1] = nn.Linear(fc_input_size, 32).to(x.device)\n        x = self.fc_layers(x)\n        return x\n'},
             23: {'code': '\nmodel = CNN(len(full_dataset.classes))\ncriterion = nn.CrossEntropyLoss()\noptimizer = optim.Adam(model.parameters(), lr=0.1)\nepochs = 10\nprint_every = 1\n\ntrain_losses = []\ntest_losses = []\n'},
             24: {'code': '\nfor epoch in range(epochs):\n    model.train()\n    train_loss = 0\n    for batch_x, batch_y in train_loader:\n        optimizer.zero_grad()\n        outputs = model(batch_x)\n        loss = criterion(outputs, batch_y)\n        loss.backward()\n        optimizer.step()\n        train_loss += loss.item()\n    train_loss /= len(train_loader)\n    train_losses.append(train_loss)\n\n    model.eval()\n    test_loss = 0\n'},
             25: {'code': "\n    with torch.no_grad():\n        for batch_x, batch_y in test_loader:\n            outputs = model(batch_x)\n            loss = criterion(outputs, batch_y)\n            test_loss += loss.item()\n    test_loss /= len(test_loader)\n    test_losses.append(test_loss)\n\n    if (epoch + 1) % print_every == 0:\n        print(f'Epoch: {epoch+1}: Train Loss {train_loss}, Test Loss {test_loss}')\n"},
             26: {'code': "\nplt.figure(figsize = (10, 6))\nplt.plot(range(1, epochs + 1), train_losses, label = 'Train Loss')\nplt.plot(range(1, epochs + 1), test_losses, label = 'Test Loss')\nplt.xlabel('Epoch')\nplt.ylabel('Loss')\nplt.legend()\nplt.grid()\nplt.show()\n"},
             27: {'code': "\nmodel.eval()\ny_pred_test = []\ny_true_test = []\nwith torch.no_grad():\n    for batch_x, batch_y in test_loader:\n        output = model(batch_x)\n        output = torch.argmax(output, dim=1)\n        y_pred_test.extend(output.tolist())\n        y_true_test.extend(batch_y.tolist())\nprint(f'accuracy: {accuracy_score(y_true_test, y_pred_test)}')\n"},
             28: {'code': ''},
             29: {'code': ''},
             30: {'code': ''},
             }

themes = '''
Регрессия
1. Предобработка до трейн/тест
2. Model 
3. Параметры
4. Обучение ч.1
5. Обучение ч.2
6. График
7. Метрики

Классификация 
8. Предобработка
9. Model
10. Class weights
11. Параметры
12. Обучение ч.1
13. Обучение ч.2
14. Обучение ч.3
15. Ошибка
16. f1 score

CNN
17. Данные
18. вычисление mean std
19. Предобработка
20. Загрузка в трейн/тест
21. Model init
22. Model foward
23. Параметры
24. Обучение ч.1
25. Обучение ч.2
26. График
27. Метрики
'''
m_to_dict = {0: 'theory', 1: 'code'}

import pyperclip as pc


def info():
    '''
    Добавляет в буфер обмена список тем, по которым потом обращаться при помощи функции get(n, m), где n - номер темы, m = 0 => теория, m = 1 => практика
    '''
    pc.copy(themes)


def info_cl():
    '''
    Создает класс, в документации которого список тем, по которым потом обращаться при помощи функции get(n, m), где n - номер темы, m = 0 => теория, m = 1 => практика
    '''

    class sol():
        __doc__ = themes

    return sol()


def get(n, m: int):
    '''
    Добавляет в буфер обмена ответ по теме (n - номер темы; m = 0 => теория, m = 1 => практика)
    '''
    if 0 < n < 37:
        if -1 < m < 2:
            pc.copy(questions[n][m_to_dict[m]])
        else:
            pc.copy('Неправильный выбор типа задания')
    else:
        pc.copy('Неправильный выбор номера темы')


def get_cl(n, m):
    '''
    Создает объект класса, в документации (shift + tab) которого лежит ответ по теме (n - номер темы; m = 0 => теория, m = 1 => практика)
    '''

    class sol:
        def __init__(self, n, m):
            self.n = n
            self.m = m
            self.doc = questions[self.n][m_to_dict[self.m]]

        @property
        def __doc__(self):
            return self.doc

    return sol(n, m)