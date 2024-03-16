# Surgical_Instrument_Tracking_CS
Our GitHub repository hosts a tool designed for tracking color-coded surgical instruments and performing 3D pose estimation. Built to meet the demands of modern microsurgical environments, this tool seamlessly integrates with quad-cam camera setups, processing four input videos simultaneously.

## System description
For our project, we are using the Arducam 1MP*4 Quadrascopic Camera Bundle Kit paired with the Nvidia Jetson Nano. The four cameras are mounted on stands with a tilt of 40º around the camera's x-axis.

We designed and integrated a custom case and lighting system for protection and reliability purposes. Also, we integrated a dome to be placed on top of the cameras to make color detection more stable.

## Calibration
To achieve a proper 3D pose estimation a good camera calibration is fundamental. After trying different methods using OpenCV without obtaining good results, we opted for Matlab's calibration tool. First, we performed a mono calibration of each single camera in order to get the intrinsic parameters. After that, we used the stereo calibration tool to estimate the pose of each pair in the camera_0 coordinate frame.

To estimate the position of camera_3 in the camera_0 reference frame we weren't able to perform a stable calibration due to the difficulty of getting good synchronized images from both cameras. Therefore, we algebraically performed the transformation using stereo pairs 1-3 and 2-3.

Stereo calibration in Matlab requires fine-tuning the picture selection to optimize and lower reprojection errors. We archived < 0.3 reprojection error in all mono calibrations and < 0.6 in all stereo ones. However, further processing of the calibration results was required to plot an intuitive pose of all cameras to compare with the actual system. With compensation for the rotation of the cameras around the x-axis, we ended up with the following results.

The hole calibration has been performed with dataset1 and you can find our calibration results and a sample code to plot them here: calibration
