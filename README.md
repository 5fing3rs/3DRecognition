# SSAD Team 35

## Team Members:

- Rohan Chacko
- AadilMehdi
- Priyank Modi
- Antony Martin

## Problem Statement:

    To detect and track objects using their corresponding 3D mesh models

## Directory Structure

.
output

### Files included:

- `main.py`
- `match.py`
- `Config.py`
- `Item.py`
- `Projection.py`
- `requirements.txt`

`main.py` - Main file which runs the whole software
`match.py` - Contains functions for generating edge templates from video and matching with best possible models
`Config.py` - Global constants declaration
`Item.py` - Contains classes for all models
`Projection.py` - Generates edge templates based on video of edge template

## Install prerequisites

pip3 install -r requirements.txt

## Generate edge templates of mesh models

- `python3 Projection.py`

## Run Software

- `python3 main.py <--templatedir> <path-to-template-directory> [--videofile] [path-to-video-file]`

### Notes

- By default the software takes input from the web camera of the device. If a pre-recorded video needs to be used, videofile path has to be specified along with the `--videofile` argument.

- Currently, data directory has only syringe and heart edge templates generated. Edge templates of other mesh models can be generated using the Projection script with a provided video file of the projected 3D mesh model
