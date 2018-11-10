# SSAD Team 35

## Team Members

-Rohan Chacko
-AadilMehdi
-Priyank Modi
-Antony Martin

## Problem Statement:

- To detect and track objects using their corresponding 3D mesh models

## Directory Structure
```bash
.
├── data
│   ├── heart
│   │   ├── mesh
│   │   │   └── meshmodel
│   │   ├── templates
│   │   │   ├── heart_templatenumber
│   │   └── training_video
│   │       ├── heart_videonumber
│   └── syringe
│       ├── templates
│       │   ├── syringe_templatenumber
│       └── training_video
│           ├── syringe_body_videonumber
├── document
│   ├── milestone.odt
│   ├── Presenation draft
│   ├── Product Design.pdf
│   ├── Project Synopsis.jpg
│   ├── R2 presentation
│   ├── ReleaseThemesInitiatives.xlsx
│   ├── Requirements.docx
│   ├── StatusTracker_1.xlsx
│   ├── Test_Planner_and_Tracker.xlsx
│   └── UML diagrams
│       ├── WhatsApp_Image_2018-09-19_at_10.38.54_PM.jpeg
│       ├── WhatsApp_Image_2018-09-19_at_10.38.55_PM.jpeg
│       ├── WhatsApp_Image_2018-09-19_at_10.53.44_PM.jpeg
│       └── WhatsApp_Image_2018-09-19_at_10.53.50_PM.jpeg
├── meeting_minutes
│   ├── Client
│   │   ├── 11_08.md
│   │   ├── 25_10.md
│   │   ├── 26_08.md
│   │   └── 29_09.md
│   ├── TA
│   │   ├── 07_08.md
│   │   └── 24_08.md
│   └── Team
│       ├── 01_10.md
│       ├── 11_09.md
│       ├── 19_08.md
│       ├── 19_09.md
│       ├── 2_11.md
│       └── 27_10.md
├── README.md
└── src
    ├── Config.py
    ├── detector.py
    ├── Item.py
    ├── main.py
    ├── match.py
    ├── requirements.txt
    ├── template_generator.py
    ├── tests
    │   ├── test_template_generator.py
    │   └── test_videostream_reception.py
    ├── utilities.py
    ├── video_utils.py
    ├── video_writer.py
    └── window.py
```
### src

`main.py` - Main file which runs the whole software
`match.py` - Contains functions for generating edge templates from video and matching with best possible models
`Config.py` - Global constants declaration
`Item.py` - Contains classes for all models
`template_generator.py` - Generates edge templates based on video of edge template
`utilities.py` - Used for printing progress bars to provide a better UI
`video_utils.py` - Contains functions to change the resolution of the video
`video_writer.py` - Writes the output video
`window.py` - Defines the specifications and design of the bounding box

## Install prerequisites

`pip3 install -r requirements.txt`

## Generate edge templates of mesh models

`python3 template_generator.py -tv <path-to-training-video>`

## Run Software

`python3 main.py <--templatedir> <path-to-template-directory> [--videofile][path-to-video-file]``

## Notes

- By default the software takes input from the web camera of the device. If a pre-recorded video needs to be used, videofile path has to be specified along with the --videofile(or -v) argument.

- Currently, data directory has only syringe and heart edge templates generated. Edge templates of other mesh models can be generated using the Projection script with a provided video file of the projected 3D mesh model
