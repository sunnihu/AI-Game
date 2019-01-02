import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (7,7) # Enlarge the figures

from keras.datasets import mnist
from keras.models import Model
from keras.layers import Dense, Input
from keras.utils import to_categorical

from tensorboardX import FileWriter, summary
import datetime

# create tensorboardX writer for tensorboard output
output_directory = "./tmp/{}/{}".format("Aufgabe-1", datetime.datetime.now())
writer = FileWriter(output_directory)


# writes metrics to log file, is called after each epoch is finished
def log_history(hist, epoch):
    for ep in hist.epoch:
        for val in hist.history:
            writer.add_summary(
                summary=summary.scalar("nn/" + val, hist.history[val][ep]), global_step=epoch
            )


# MNIST has classes 0 to 9
nb_classes = 10

# download MNIST data
(x_train_orig, y_train_orig), (x_test_orig, y_test_orig) = mnist.load_data()

# convert 28x28 images to vectors and normalize them between 0 and 1
# training set contains 60k images, test/validation set contains 10k images
x_train = x_train_orig.reshape(60000, 784).astype(np.float32) / 255.0
x_test = x_test_orig.reshape(10000, 784).astype(np.float32) / 255.0

# convert class labels to one hot encoded vectors
Y_train = to_categorical(y_train_orig, nb_classes)
Y_test = to_categorical(y_test_orig, nb_classes)

#######
# Hier Aufgabe 1 implementieren
#######

# neural network definition here:
input_layer = Input(shape=(784,), name='input')
hidden_layer = Dense(100, activation='relu')(input_layer)
hidden_layer = Dense(100, activation='relu')(hidden_layer)
hidden_layer = Dense(100, activation='relu')(hidden_layer)
hidden_layer = Dense(100, activation='relu')(hidden_layer)
output_layer = Dense(10, activation='softmax')(hidden_layer)
model = Model(inputs=input_layer, outputs=output_layer)

# compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc', 'mae'])

# print a summary of the model
print(model.summary())

# train the model
for epoch in range(10):
    history = model.fit(x_train, Y_train, batch_size=128, epochs=1, verbose=1, validation_data=(x_test, Y_test))
    log_history(history, epoch)

print("Training finished!")

# evaluate the models performance
print("Validation accuracy: {:.2f}%".format(model.evaluate(x_test, Y_test, verbose=0)[1] * 100.0))

# display 10 examples with predictions
for i in range(10):
    image = x_test_orig[i]
    label = y_test_orig[i]
    image_vector = x_test[i]
    image_vector = image_vector.reshape(1, 784)

    plt.imshow(image, cmap='gray', interpolation='none')
    plt.title("Class: {} | Prediction: {}".format(label, np.argmax(model.predict(image_vector))))
    plt.show()