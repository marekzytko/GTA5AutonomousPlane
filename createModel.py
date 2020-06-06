from tensorflow.keras import layers, models, optimizers, regularizers, metrics
import numpy as np

N_FILES = 14
PATH = r'D:\AutonomusGTA5Plane'
MODEL_NAME = r'\gta5.model'
#Frame size (after previous resizing [getData])
SIZE = (120, 80)

#Model parameters:
BATCH_SIZE = 8
LR = 0.001
EPOCHS = 10

#TODO
#Modify using ConvLSTM2D

model = models.Sequential()

model.add(layers.Conv2D(filters=32, activation='relu', kernel_size=(3, 3), input_shape=(80, 120, 3), activity_regularizer=regularizers.l1(0.001)))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(filters=64, activation='relu', kernel_size=(3, 3), activity_regularizer=regularizers.l2(0.001)))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(filters=128, activation='relu', kernel_size=(3, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())

model.add(layers.Dense(units=256, activation='relu'))
#Output layer:
model.add(layers.Dense(units=8, activation='softmax'))

model.summary()

model.compile(
    optimizer=optimizers.Adagrad(learning_rate=LR),
    loss='binary_crossentropy',
    metrics=['accuracy', metrics.binary_crossentropy]
    )

data_x = []
data_y = []

print('Loading data!')

for i in range(1, N_FILES + 1):
    data = np.load(fr'D:\gta_ai_autlopilot\data{i}.npz', allow_pickle=True)
    data = data['arr_0']

    data_x.append([x[0] for x in data])
    data_y.append([x[1] for x in data])
    print(f'data{i}.npz loaded!')

data_x = np.asarray(data_x).reshape(-1, SIZE[1], SIZE[0], 3)
data_y = np.asarray(data_y).reshape(-1, 8)

print(data_x.shape)
print(data_y.shape)

print(len(data_x), len(data_y))

#Checking if data contains NaN (to prevent stupid errors causing loss explosions)
assert not np.any(np.isnan(data_x))
assert not np.any(np.isnan(data_y))

model.fit(
    x=data_x,
    y=data_y,
    batch_size=BATCH_SIZE,
    shuffle=True,
    use_multiprocessing=True,
    epochs=EPOCHS
    )

model.save(rf"{PATH}{MODEL_NAME}")
