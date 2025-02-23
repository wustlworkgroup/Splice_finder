import keras
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

# Print Keras version
print("Keras version:", keras.__version__)

# Create a simple model to test functionality
model = Sequential([
    Dense(10, activation='relu', input_shape=(5,)),  # Input layer with 5 features
    Dense(5, activation='relu'),  # Hidden layer
    Dense(1, activation='sigmoid')  # Output layer (binary classification)
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Generate some random test data
X_test = np.random.rand(10, 5)  # 10 samples, 5 features each
y_test = np.random.randint(0, 2, 10)  # 10 binary labels

# Run a test prediction
predictions = model.predict(X_test)

# Print model summary and predictions
model.summary()
print("\nTest predictions:\n", predictions)

