import pickle
import numpy as np

model = pickle.load(open("blink_model.pkl","rb"))

print("Blink ML Model Tester")

while True:

    ear = float(input("Enter EAR: "))
    duration = float(input("Enter blink duration: "))

    features = np.array([[ear,duration]])

    prediction = model.predict(features)

    print("Predicted Morse:",prediction[0])