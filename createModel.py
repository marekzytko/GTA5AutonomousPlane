from tensorflow.keras import layers, models, optimizers, regularizers, metrics, callbacks
import numpy as np

N_FILES = 37
PATH = r'D:\github\GTA5AutonomusPlane'
MODEL_NAME = r'\gta5.model'
#Frame size (after previous resizing [getData])
RESIZE = (180, 120)

#Model parameters:
BATCH_SIZE = 8
LR = 0.01
EPOCHS = 10

#TODO
#Modify using ConvLSTM2D

model = models.Sequential()

model.add(layers.Conv2D(filters=32, activation='relu', kernel_size=(3, 3), input_shape=(RESIZE[1], RESIZE[0], 3), activity_regularizer=regularizers.l1(0.02)))

model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(filters=64, activation='relu', kernel_size=(3, 3), activity_regularizer=regularizers.l2(0.02)))

model.add(layers.Conv2D(filters=64, activation='relu', kernel_size=(3, 3), activity_regularizer=regularizers.l2(0.02)))

model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(filters=96, activation='relu', kernel_size=(3, 3)))

model.add(layers.Conv2D(filters=96, activation='relu', kernel_size=(3, 3), activity_regularizer=regularizers.l2(0.02)))

model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())

model.add(layers.Dense(units=128, activation='relu', activity_regularizer=regularizers.l1(0.02)))
#Output layer:
model.add(layers.Dense(units=5, activation='softmax'))

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
    data = np.load(fr'{PATH}\data{i}.npz', allow_pickle=True)
    data = data['arr_0']

    data_x.append([x[0] for x in data])
    data_y.append([x[1] for x in data])
    print(f'data{i}.npz loaded!')

data_x = np.asarray(data_x).reshape(-1, RESIZE[1], RESIZE[0], 3)
data_y = np.asarray(data_y).reshape(-1, 5)

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
    epochs=EPOCHS,
    validation_split=0.2,
    callbacks=[
        callbacks.TerminateOnNaN(),
        callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            patience=3,
            mode='auto',
            verbose=True
            ),
        ]
    )

model.save(rf"{PATH}{MODEL_NAME}")
