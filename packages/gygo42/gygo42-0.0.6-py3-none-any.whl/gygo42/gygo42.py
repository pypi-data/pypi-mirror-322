from mistralai import Mistral
import pyperclip
import random

questions = {0: {'code': '\nfrom torch.utils.data import DataLoader, TensorDataset\nfrom sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.compose import ColumnTransformer\nfrom sklearn.metrics import accuracy_score\nfrom torch.utils.data import DataLoader\nfrom torchvision import transforms\nfrom torchvision.datasets import ImageFolder'},
             1: {'code': '\ndata = pd.read_csv("")\ndata.head()'},
             2: {'code': '\nfrom torchvision.datasets import ImageFolder\ndata_dir = ""\nfull_dataset = ImageFolder(data_dir)'},
             3: {'code': '\nloader = DataLoader(full_dataset, batch_size=64, shuffle=False)\nmean, std = 0.0, 0.0\nfor images, labels in loader:\n    mean += images.mean([0, 2, 3])  # Среднее по каналам\n    std += images.std([0, 2, 3])    # Стандартное отклонение по каналам\nmean /= len(loader)\nstd /= len(loader)'},
             4: {'code': '\ntransform = transforms.Compose([transforms.Resize((300, 300)),\n                                transforms.ToTensor(),\n                                transforms.Normalize(mean=mean, std=std)])\n\nfull_dataset = ImageFolder(data_dir, transform=transform)'},
             5: {'code': '\ntrain_size = int(0.7 * len(full_dataset))\ntest_size = len(full_dataset) - train_size\ntrain_dataset, test_dataset = torch.utils.data.random_split(full_dataset, [train_size, test_size])'},
             6: {'code': '\nclass CNN(nn.Module):\n    def __init__(self, dataset):\n        super(CNN, self).__init__()\n        self.network = nn.Sequential(\n            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1),\n            nn.ReLU(),\n            nn.MaxPool2d(kernel_size=2, stride=2),\n            nn.Flatten(),  # Приведение тензора к двумерному формату\n            nn.Linear(32 * 150 * 150, 256),  # Параметры изменены в зависимости от выходных данных\n            nn.ReLU(),\n            nn.Linear(256, len(dataset.classes))\n            )\n\n    def forward(self, x):\n        return self.network(x)'},
             7: {'code': '\ndef compute_accuracy(loader, model):\n    with torch.no_grad():\n        correct = 0\n        total = 0\n        for images, labels in loader:\n            preds = model(images)\n            predicted = preds.argmax(dim=1)\n            correct += (predicted == labels).sum().item()\n            total += labels.size(0)\n    return correct / total'},
             8: {'code': '\nbatch_size = 64\nnum_epochs = 100\nprint_every = 10\nnum_classes = len(full_dataset.classes)'},
             9: {'code': '\nmodel = CNN(full_dataset)\ncriterion = nn.CrossEntropyLoss()\noptimizer = optim.Adam(model.parameters(), lr = 0.001)\n\nacc_train, los_train, acc_test = [], [], []'},
             10: {'code': '\ntrain_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)\ntest_loader = DataLoader(test_dataset, batch_size=batch_size)\n\nfor epoch in range(num_epochs):\n    epoch_loss = 0\n    model.train()\n    for batch_X, batch_y in train_loader:\n        batch_X = batch_X.to(device)\n        batch_y = batch_y.to(device)\n        optimizer.zero_grad()\n        preds = model(batch_X)\n        loss_value = criterion(preds, batch_y)\n        loss_value.backward()\n        optimizer.step()\n        epoch_loss += loss_value.item()'},
             11: {'code': '\n    los_train += [(epoch_loss / len(train_loader))]\n    train_accuracy = compute_accuracy(train_loader, model)\n    test_accuracy = compute_accuracy(test_loader, model)\n    acc_train += [train_accuracy]\n    acc_test += [test_accuracy]\n    if (epoch+1) % print_every == 0:\n        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}, ...")'},
             12: {'code': ''},
             13: {'code': ''},
             14: {'code': ''},
             15: {'code': ''},
             16: {'code': ''},
             17: {'code': ''},
             18: {'code': ''},
             19: {'code': ''},
             20: {'code': '\nX = data.drop(columns=[""])\ny = LabelEncoder().fit_transform(data[""])'},
             21: {'code': '\ncat_cols = []\nnum_cols = []\n\npreprocessor = ColumnTransformer(\n    transformers=[\n        ("num", StandardScaler(), num_cols),\n        ("cat", OneHotEncoder(), cat_cols)\n    ]\n)\n\nX_processed = preprocessor.fit_transform(X).toarray()'},
             22: {'code': '\nX_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=.2, random_state=9)\n\nX_train = torch.tensor(X_train, dtype=torch.float32).to(device)\nX_test = torch.tensor(X_test, dtype=torch.float32).to(device)\ny_train = torch.tensor(y_train, dtype=torch.long).to(device)\ny_test = torch.tensor(y_test, dtype=torch.long).to(device)\n\ntrain_dataset = TensorDataset(X_train, y_train)\ntest_dataset = TensorDataset(X_test, y_test)'},
             23: {'code': '\nbatch_size = 64\nepochs = 100\nprint_every = 20\n\ntrain_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)'},
             24: {'code': '\noptimizers = {\n    "SGD": lambda params: torch.optim.SGD(params, lr=0.0001, momentum = 0.9),\n    "Adam": lambda params: torch.optim.Adam(params, lr= 0.001),\n    "AdamW": lambda params: torch.optim.AdamW(params, lr= 0.001)}'},
             25: {'code': '\nclass Model(nn.Module):\n    def __init__(self, num_params):\n        super(Model, self).__init__()\n        self.network = nn.Sequential(\n             nn.Linear(num_params, 64),\n             nn.Sigmoid(),\n             nn.Linear(64, 128),\n             nn.Sigmoid(),\n             nn.Linear(128, 64),\n             nn.Sigmoid(),\n             nn.Linear(64, 16),\n             nn.Sigmoid(),\n             nn.Linear(16, 2)\n           )\n\n    def forward(self, x):\n        return self.network(x)'},
             26: {'code': '\nresults = {}\n\ndef train(opt_name, opt_fn):\n    global results\n    print(f"Обучение с {opt_name}")\n    model = Model(X_train.shape[1]).to(device)\n    optim = opt_fn(model.parameters())\n    crit = nn.CrossEntropyLoss()\n\n    train_losses = []\n    val_losses = []\n\n    for epoch in tqdm(range(epochs)):\n        model.train()\n        epoch_loss = 0\n        for batch_X, batch_y in train_loader:\n            optim.zero_grad()\n            pred = model(batch_X)\n            loss = crit(pred, batch_y)\n            loss.backward()\n            optim.step()\n            epoch_loss += loss.item()\n\n        train_losses.append(epoch_loss / len(train_loader))'},
             27: {'code': '\n        model.eval\n        with torch.no_grad():\n            val_pred = model(X_test)\n            val_loss = crit(val_pred, y_test)\n            val_losses.append(val_loss)\n        if (epoch + 1) % print_every == 0:\n            print(f"Эпоха {epoch+1}/{epochs}, Train Loss: {train_losses[-1]:.2f}, Val Loss: {val_losses[-1]:.2f}")\n    results[opt_name] = {\n        "": \n        "train_losses": train_losses,\n        "val_losses": val_losses,\n        "model": model\n    }'},
             28: {'code': '\ntrain("Adam", optimizers["Adam"])'},
             29: {'code': '\nfor opt_name, res in results.items():\n    train_losses = [loss.cpu().item() if torch.is_tensor(loss) else loss for loss in res["train_losses"]]\n    val_losses = [loss.cpu().item() if torch.is_tensor(loss) else loss for loss in res["val_losses"]]\n    plt.plot(train_losses[5:], label=f"{opt_name} Train Loss")\n    plt.plot(val_losses[5:], label=f"{opt_name} Val Loss")\n\nplt.xlabel("Epochs")\nplt.ylabel("Loss")\nplt.legend()\nplt.title("Training and Validation Loss Curves")\nplt.show()'},
             30: {'code': '\nfor opt_name, result in results.items():\n    model = result["model"]\n    model.eval()\n    with torch.no_grad():\n        test_predictions = model(X_test).squeeze()\n        Y_test = test_predictions.argmax(dim=1)\n        accuracy = accuracy_score(y_test.cpu(), Y_test.cpu())\n\n    print(f"Результаты для {opt_name}:")\n    print(accuracy)'},
             31: {'code': '\nfrom imblearn.over_sampling import SMOTE\nX_processed, y_processed = SMOTE().fit_resample(X_processed, y_processed)'},
             32: {'code': '\nX = data.drop(columns=[""])\ny = data[""]'},
             33: {'code': '\ncorr_matrix = data.drop(columns=[""]).corr()\nsns.heatmap(corr_matrix, annot=True, cmap="coolwarm")'},
             34: {'code': '\ncat_cols = [""]\nnum_cols = [""]\n\npreprocessor = ColumnTransformer(\n    transformers=[\n        ("num", StandardScaler(), num_cols),\n        ("cat", OneHotEncoder(), cat_cols)\n    ]\n)\n\nX_processed = preprocessor.fit_transform(X).toarray()'},
             35: {'code': '\nX_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=.2, random_state=9)\n\nX_train = torch.tensor(X_train, dtype=torch.float32).to(device)\nX_test = torch.tensor(X_test, dtype=torch.float32).to(device)\ny_train = torch.tensor(y_train.values, dtype=torch.float32).view(-1,1).to(device)\ny_test = torch.tensor(y_test.values, dtype=torch.float32).view(-1,1).to(device)\n\ntrain_dataset = TensorDataset(X_train, y_train)\ntest_dataset = TensorDataset(X_test, y_test)'},
             36: {'code': '\nbatch_size = 32\nepochs = 100\nprint_every = 10\n\ntrain_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)'},
             37: {'code': '\noptimizers = {\n    "SGD": lambda params: torch.optim.SGD(params, lr=0.00005, momentum = 0.9),\n    "Adam": lambda params: torch.optim.Adam(params, lr= 0.001),\n    "AdamW": lambda params: torch.optim.AdamW(params, lr= 0.001)}'},
             38: {'code': '\nclass Model(nn.Module):\n    def __init__(self, num_params):\n        super(Model, self).__init__()\n        self.network = nn.Sequential(\n            nn.Linear(num_params, 256),\n            nn.BatchNorm1d(256),\n            nn.ReLU(),\n            nn.Linear(256, 128),\n            nn.BatchNorm1d(128),\n            nn.ReLU(),\n            nn.Linear(128, 64),\n            nn.BatchNorm1d(64),\n            nn.ReLU(),\n            nn.Linear(64, 1)\n        )\n\n    def forward(self, x):\n        return self.network(x)'},
             39: {'code': '\nresults = {}\n\ndef train(opt_name, opt_fn):\n    global results\n    print(f"Обучение с {opt_name}")\n    model = Model(X_train.shape[1]).to(device)\n    optim = opt_fn(model.parameters())\n    crit = nn.MSELoss()\n\n    train_losses = []\n    val_losses = []\n\n    for epoch in tqdm(range(epochs)):\n        model.train()\n        epoch_loss = 0\n        for batch_X, batch_y in train_loader:\n            optim.zero_grad()\n            pred = model(batch_X)\n            loss = crit(pred, batch_y)\n            loss.backward()\n            optim.step()\n            epoch_loss += loss.item()\n\n        train_losses.append(epoch_loss / len(train_loader))'},
             40: {'code': '\n        model.eval\n        with torch.no_grad():\n            val_pred = model(X_test)\n            val_loss = crit(val_pred, y_test)\n            val_losses.append(val_loss)\n\n        if (epoch + 1) % print_every == 0:\n            print(f"Эпоха {epoch+1}/{epochs}, Train Loss: {train_losses[-1]:.2f}, Val Loss: {val_losses[-1]:.2f}")\n\n    results[opt_name] = {\n       "train_losses": train_losses,\n        "val_losses": val_losses,\n        "model": model\n    }'},
             41: {'code': '\ntrain("", optimizers[""])'},
             42: {'code': '\nfor opt_name, res in results.items():\n    # Переместите тензоры на CPU перед использованием numpy\n    train_losses = [loss.cpu().item() if torch.is_tensor(loss) else loss for loss in res["train_losses"]]\n    val_losses = [loss.cpu().item() if torch.is_tensor(loss) else loss for loss in res["val_losses"]]\n    plt.plot(train_losses[5:], label=f"{opt_name} Train Loss")\n    plt.plot(val_losses[5:], label=f"{opt_name} Val Loss")\n\nplt.xlabel("Epochs")\nplt.ylabel("Loss")\nplt.legend()\nplt.title("Training and Validation Loss Curves")\nplt.show()'},
             43: {'code': '\nfor opt_name, result in results.items():\n    model = result["model"]\n    model.eval()\n    with torch.no_grad():\n        test_predictions = model(X_test).squeeze()\n        mse = mean_squared_error(y_test.cpu(), test_predictions.cpu())\n        mae = mean_absolute_error(y_test.cpu(), test_predictions.cpu())\n        r2 = r2_score(y_test.cpu(), test_predictions.cpu())\n\n    print(f"\nРезультаты для {opt_name}:")\n    print(f"MSE: {mse:.4f}, MAE: {mae:.4f}, R2: {r2:.4f}")'},
             44: {'code': ''},
             45: {'code': ''},
             46: {'code': ''},
             47: {'code': ''},
             48: {'code': ''},
             }

themes = '''
Содержание:
0. Библиотеки
1. Открытие .csv файла
CNN:
2. Открытие директории с изображениями
3. Рассчитываем среднее и стандартное отклонение для нормализации
4. Обрезка, нормализация
5. train_dataset, test_dataset
6. CNN
7. compute_accuracy
8. Гиперпараметры
9. Инициализация CNN
10. Цикл обучения (1 часть)
11. Цикл обучения (2 часть)
12. 
13. 
14. 
15. 
16. 
17. 
18. 
19. 
Classification:
20. X, y
21. Preprocessor
22. train_test_split
23. Гиперпараметры
24. optimizers
25. Инициализация модели
26. Цикл обучения (1 часть)
27. Цикл обучения (2 часть)
28. Обучение
29. Визуализация
30. accuracy
31. SMOTE
Regression:
32. X, y
33. corr_matrix
34. preprocessor
35. train_test_split
36. Гиперпараметры
37. optimizers
38. Инициализация модели
39. Цикл обучения (1 часть)
40. Цикл обучения (2 часть)
41. Обучение
42. Визуализация
43. MSE, MAE, R2
44. 
45. 
46. 
47. 
'''

m_to_dict = {0 : 'theory', 1 : 'code'}
api_keys = ['uQwjntCIJ9omN9z8jLTV1VOUvYlbaDIv',
            'tgPxn1rFujtuJe1H0j4PQTSjbLthvjyO',
            'Z0XHjxUHj6QXJblxACLxDhJoQAUreqt4',
            'iOSObqKAYAliBWRglH4gpZb7JN0KF91j',
            'E42w9TME0Ykm1WMsVwdzS6DxV9q2Xhgx',
            'uQmDdzM1nrw3cbmksP1BWhRnjOKGLWi1',
            'AhRiKjuHaXm4WccJ0BDI0NRBJ1X9RxSE',
            'mtddNQsqAMbL5GNHroRNRsSOwOr8vusH',
            'tpxt5xsU7jetD1x9u9r0IiKxqwajlTXO',
            'bSJCJVsREAKubT9AgGfgYL6pojIzoK11',
            'icjd6jfH7hmPxNMSEyD70UKg13kbtaB5',
            'Oxz67oTMVHw48CJhJZOKLkHw1eAlTwki',
            'zVrmIUh4z2wEjS1ze9XpJtfbGQTGognI',
            'ez9voi9pZb7CwPbqrglrTSL59GgUZFCX',
            'BQUqloQ3WynP4ySfHhTOxz44Diidniq1'
            ]
model = "mistral-large-latest"



def info():
    '''
    Добавляет в буфер обмена список тем, по которым потом обращаться при помощи функции get(n, m), где n - номер темы, m = 0 => теория, m = 1 => практика
    '''
    pyperclip.copy(themes)

def info_cl():
    '''
    Создает класс, в документации которого список тем, по которым потом обращаться при помощи функции get(n, m), где n - номер темы, m = 0 => теория, m = 1 => практика
    '''
    class sol():
        __doc__ = themes
        
    return sol()

def get(n, m : int):
    '''
    Добавляет в буфер обмена ответ по теме (n - номер темы; m = 0 => теория, m = 1 => практика)
    '''
    if 0 < n < len(questions) + 1:
        if -1 < m < 2:
            pyperclip.copy(questions[n][m_to_dict[m]])
        else:
            pyperclip.copy('Неправильный выбор типа задания')
    else:
        pyperclip.copy('Неправильный выбор номера темы')


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

def m_get(message, n):
    '''
    message: запрос, n = 0 => теория, n = 1 => практика
    '''
    taskk = {0 : ' В твоем ответе не должно быть никакого кода, только теория', 1 : " В твоем ответе не должно быть ничего, кроме кода, решающего задачу."}
    # Выбираем случайный API ключ из списка
    api_key = random.choice(api_keys)

    # Инициализируем клиент Mistral AI
    client = Mistral(api_key=api_key)

    # Отправляем запрос
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": message + taskk[n],
                },
            ]
        )
        # Получаем ответ
        response_content = chat_response.choices[0].message.content
    except:
        response_content = 'неправильный выбор типа задания'

    # Копируем ответ в буфер обмена
    pyperclip.copy(response_content)

class m_get_cl:
    def __init__(self, message, n):
        '''
        message: запрос, n = 0 => теория, n = 1 => практика
        '''
        taskk = {0 : ' В твоем ответе не должно быть никакого кода, только теория', 1 : " В твоем ответе не должно быть ничего, кроме кода, решающего задачу."}
        # Выбираем случайный API ключ из списка
        api_key = random.choice(api_keys)
    
        # Инициализируем клиент Mistral AI
        client = Mistral(api_key=api_key)
    
        # Отправляем запрос
        try:
            chat_response = client.chat.complete(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": message + taskk[n],
                    },
                ]
            )
            response_content = chat_response.choices[0].message.content
        except:
            response_content = 'неправильный выбор типа задания'
    

        self.answer = response_content

    @property
    def __doc__(self):
        return self.answer
