import json
import random

# Load the original JSON data
with open("zoro.json", "r") as file:
    original_data = json.load(file)

# Get the keys (IDs) of the original data
keys = list(original_data.keys())

# Shuffle the keys randomly
random.shuffle(keys)

# Calculate the number of entries for each split
total_entries = len(keys)
train_size = int(0.7 * total_entries)
test_size = int(0.15 * total_entries)

# Split the keys into train, test, and validation sets
train_keys = keys[:train_size]
test_keys = keys[train_size:train_size + test_size]
valid_keys = keys[train_size + test_size:]

# Create dictionaries for train, test, and validation sets
train_data = {key: original_data[key] for key in train_keys}
test_data = {key: original_data[key] for key in test_keys}
valid_data = {key: original_data[key] for key in valid_keys}

# Write the split data to separate JSON files
with open("zorozoroTrain.json", "w") as file:
    json.dump(train_data, file, indent=4)

with open("zorozoroTest.json", "w") as file:
    json.dump(test_data, file, indent=4)

with open("zorozoroValid.json", "w") as file:
    json.dump(valid_data, file, indent=4)
