import csv
import random

print("Generating blink dataset...")

file = open("blink_dataset.csv", "w", newline="")
writer = csv.writer(file)

# header
writer.writerow(["ear","duration","label"])

# generate DOT samples
for i in range(150):
    ear = round(random.uniform(0.17,0.23),3)
    duration = round(random.uniform(0.15,0.35),3)
    writer.writerow([ear,duration,"dot"])

# generate DASH samples
for i in range(150):
    ear = round(random.uniform(0.15,0.22),3)
    duration = round(random.uniform(0.5,1.0),3)
    writer.writerow([ear,duration,"dash"])

file.close()

print("Dataset created: blink_dataset.csv")