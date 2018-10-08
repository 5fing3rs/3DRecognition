# SSAD Team 35

## Team Members
  -Rohan Chacko
  -AadilMehdi
  -Priyank Modi
  -Antony Martin

## Problem Statement:
  - ###To detect and track objects using their corresponding 3D mesh models


## Directory Structure
    .
    ├── data
    │   ├── heart
    │   │   ├── mesh
    │   │   │   └── meshmodel
    │   │   ├── templates
    │   │   │   ├── heart_4_0.jpg
    │   │   │   ├── heart_4_180.jpg
    │   │   │   ├── heart_4_270.jpg
    │   │   │   ├── heart_4_360.jpg
    │   │   │   └── heart_4_90.jpg
    │   │   └── training_video
    │   │       ├── heart_1.avi
    │   │       ├── heart_2.avi
    │   │       ├── heart_3.avi
    │   │       └── heart_4.avi
    │   └── syringe_body
    │       ├── templates
    │       │   ├── syringe_body_2_0.jpg
    │       │   ├── syringe_body_2_180.jpg
    │       │   ├── syringe_body_2_270.jpg
    │       │   ├── syringe_body_2_360.jpg
    │       │   └── syringe_body_2_90.jpg
    │       └── training_video
    │           ├── syringe_body_1.avi
    │           ├── syringe_body_2.avi
    │           ├── syringe_body_3.avi
    │           └── syringe_body_4.avi
    ├── document
    │   ├── milestone.odt
    │   ├── Presenation draft
    │   ├── Project Synopsis.jpg
    │   ├── ReleaseThemesInitiatives.xlsx
    │   ├── Requirements.docx
    │   ├── StatusTracker_1.xlsx
    │   └── Test_Planner_and_Tracker.xlsx
    ├── meeting_minutes
    │   ├── Client
    │   │   ├── 11_08.md
    │   │   ├── 26_08.md
    │   │   └── 29_09.md
    │   ├── TA
    │   │   ├── 07_08.md
    │   │   └── 24_08.md
    │   └── Team
    │       ├── 01_10.md
    │       ├── 11_09.md
    │       ├── 19_08.md
    │       └── 19_09.md
    ├── output
    │   └── heart
    │       └── 1
    │           └── log.json
    ├── README.md
    └── src
        ├── Config.py
        ├── Item.py
        ├── main.py
        ├── match.py
        ├── Projection.py
        ├── __pycache__
        │   ├── Config.cpython-35.pyc
        │   ├── Config.cpython-36.pyc
        │   ├── Item.cpython-35.pyc
        │   └── Item.cpython-36.pyc
        └── requirements.txt

### src
  `main.py` - Main file which runs the whole software
  `match.py` - Contains functions for generating edge templates from video and matching with best possible models
  `Config.py` - Global constants declaration
  `Item.py` - Contains classes for all models
  `Projection.py` - Generates edge templates based on video of edge template


## Install prerequisites
  `pip3 install -r requirements.txt`

## Generate edge templates of mesh models
  `python3  Projection.py`

## Run Software
  `python3 main.py <--templatedir> <path-to-template-directory> [--videofile] [path-to-video-file]``

## Notes
  - By default the software takes input from the web camera of the device. If a pre-recorded video needs to be used,    videofile path has to be specified along with the --videofile argument.

  - Currently, data directory has only syringe and heart edge templates generated. Edge templates of other mesh models can be generated using the Projection script with a provided video file of the projected 3D mesh model
