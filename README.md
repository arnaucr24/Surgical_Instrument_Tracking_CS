# Surgical_Instrument_Tracking_CS
Our GitHub repository hosts a tool designed for tracking color-coded surgical instruments and performing 3D pose estimation. Built to meet the demands of modern microsurgical environments, this tool seamlessly integrates with quad-cam camera setups, processing four input videos simultaneously.

## System description
For our project, we are using the Arducam 1MP*4 Quadrascopic Camera Bundle Kit paired with the Nvidia Jetson Nano. The four cameras are mounted on stands with a tilt of 40º around the camera's x-axis.

We designed and integrated a custom case and lighting system for protection and reliability purposes. Also, we integrated a dome to be placed on top of the cameras to make color detection more stable.

## Calibration
To achieve a proper 3D pose estimation a good camera calibration is fundamental. 
