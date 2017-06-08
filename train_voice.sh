#!/bin/bash

SPK_RCG_PY=./speaker-recognition/src/speaker-recognition.py
RAW_DATA_PATH=./data/voice_raw
SOXED_DATA_PATH=./data/voice_train

# preprocessing raw voice data using sox
rm -rf $SOXED_DATA_PATH
cp -R $RAW_DATA_PATH $SOXED_DATA_PATH
for people in $SOXED_DATA_PATH/*; do
    for wav in $people/*.wav;do
        echo $wav
        sox -c 1 $wav $wav.new.wav
        rm -f $wav
        mv $wav.new.wav $wav
    done
done

# train
$SPK_RCG_PY -t enroll -i "$SOXED_DATA_PATH/*" -m voice.model
