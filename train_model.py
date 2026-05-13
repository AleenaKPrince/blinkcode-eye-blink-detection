import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

print("Training Blink Classifier...")

# load dataset
data = pd.read_csv("blink_dataset.csv")

X = data[["ear","duration"]]
y = data["label"]

# split dataset
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

# train model
model = RandomForestClassifier()
model.fit(X_train,y_train)

# predictions
y_pred = model.predict(X_test)

# accuracy
accuracy = accuracy_score(y_test,y_pred)
print("Model Accuracy:",accuracy)

# classification report
print("\nClassification Report")
print(classification_report(y_test,y_pred))

# confusion matrix
cm = confusion_matrix(y_test,y_pred)

plt.figure(figsize=(5,4))
sns.heatmap(cm,annot=True,fmt="d",cmap="Blues",
            xticklabels=["dot","dash"],
            yticklabels=["dot","dash"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# save model
pickle.dump(model,open("blink_model.pkl","wb"))
print("Model saved as blink_model.pkl")