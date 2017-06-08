#!/bin/bash

FEATURE_PATH=./data/train/
ALIGNED_PATH=./data/aligned
OPENFACE_PATH=./openface_pi

# Preprocess the raw images
for N in {1..8}; do $OPENFACE_PATH/util/align-dlib.py $FEATURE_PATH align outerEyesAndNose $ALIGNED_PATH --size 96 & done

# Generate Representations
$OPENFACE_PATH/batch-represent/main.lua -outDir $FEATURE_PATH -data $ALIGNED_PATH

# Create the Classification Model
$OPENFACE_PATH/demos/classifier.py train $FEATURE_PATH
