import cv2
import numpy as np
from calibration import Calibration_parameters
from detector_green import DetectGreen
from plot_3d import Plot3DPoints
from weighted_mean import WeightedMeanCalculator

def triangulation(p_0, p_1, Imtx_0, Imtx_1,R_0, T_0, R_1, T_1):
    if p_0.shape != (2, ) or p_1.shape != (2, ):
        raise TypeError("The input points for triangulation are not in the right dimension (2, )")
    
    Pmtx_0 = Imtx_0 @ np.hstack((R_0, T_0))
    Pmtx_1 = Imtx_1 @ np.hstack((R_1, T_1))

    # The point is in homogenous coordinates
    point_4d = cv2.triangulatePoints(Pmtx_0, Pmtx_1, p_0, p_1)
    point_3d = point_4d[:3] / point_4d[3]

    return point_3d

def rotate_points(points, r_matrix):
    r_point_list = []
    for p in points:
        # Make sure points has the correct shape
        if p.shape[0] != 3:
            raise ValueError("Input points must have shape (3, N)")
        
        # Apply the rotation transformation
        rotated_points = np.dot(r_matrix, p)

        r_point_list.append(rotated_points)

    return r_point_list

def main():
    calibration = Calibration_parameters()
    detector = DetectGreen()
    plotter = Plot3DPoints(calibration)
    wm = WeightedMeanCalculator()
    weights = [1, 1, 1, 1, 1, 1]

    # Read the video files
    cap_0 = cv2.VideoCapture('/Users/arnaucompanyroig/Documents/Pràctiques/CS_TUM/Videos/cam0__2024-03-12_22-51-55.mp4')
    cap_1 = cv2.VideoCapture('/Users/arnaucompanyroig/Documents/Pràctiques/CS_TUM/Videos/cam1__2024-03-12_22-51-55.mp4')
    cap_2 = cv2.VideoCapture('/Users/arnaucompanyroig/Documents/Pràctiques/CS_TUM/Videos/cam2__2024-03-12_22-51-55.mp4')
    cap_3 = cv2.VideoCapture('/Users/arnaucompanyroig/Documents/Pràctiques/CS_TUM/Videos/cam3__2024-03-12_22-51-55.mp4')

    points_3d_01 = []
    points_3d_02 = []
    points_3d_03 = []
    points_3d_12 = []
    points_3d_31 = []
    points_3d_32 = []
    points_3d = []
    
    while cap_0.isOpened() and cap_1.isOpened():
        ret_0, vid_0 = cap_0.read()
        ret_1, vid_1 = cap_1.read()
        ret_2, vid_2 = cap_2.read()
        ret_3, vid_3 = cap_3.read()
        
        if not ret_0 or not ret_1 or not ret_2 or not ret_3:
            break
        
        modified_frame_0, d_p0 = detector.detect(vid_0)
        modified_frame_1, d_p1 = detector.detect(vid_1)
        modified_frame_2, d_p2 = detector.detect(vid_2)
        modified_frame_3, d_p3 = detector.detect(vid_3)

        cv2.namedWindow("Original_0", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Original_0", 500, 315)
        cv2.moveWindow("Original_0", 700, 500)

        cv2.namedWindow("Original_1", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Original_1", 500, 315)
        cv2.moveWindow("Original_1", 100, 100)

        cv2.namedWindow("Original_2", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Original_2", 500, 315)
        cv2.moveWindow("Original_2", 700, 100)

        cv2.namedWindow("Original_3", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Original_3", 500, 315)
        cv2.moveWindow("Original_3", 100, 500)

        
        cv2.imshow('Original_1', modified_frame_1)
        cv2.imshow('Original_2', modified_frame_2)
        cv2.imshow('Original_3', modified_frame_3)
        cv2.imshow('Original_0', modified_frame_0)
        
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        if d_p0 is not None and d_p1 is not None and d_p2 is not None and d_p3 is not None:
            d_p3d_01 = triangulation(d_p0, d_p1, calibration.mtx0, calibration.mtx1, np.eye(3), np.zeros((3, 1)), calibration.R_1, calibration.T_1)
            d_p3d_02 = triangulation(d_p0, d_p2, calibration.mtx0, calibration.mtx2, np.eye(3), np.zeros((3, 1)), calibration.R_2, calibration.T_2)
            d_p3d_03 = triangulation(d_p0, d_p3, calibration.mtx0, calibration.mtx3, np.eye(3), np.zeros((3, 1)), calibration.R_3, calibration.T_3)
            d_p3d_12 = triangulation(d_p1, d_p2, calibration.mtx1, calibration.mtx2, calibration.R_1, calibration.T_1, calibration.R_2, calibration.T_2)
            d_p3d_31 = triangulation(d_p3, d_p3, calibration.mtx3, calibration.mtx1, calibration.R_3, calibration.T_3, calibration.R_1, calibration.T_1)
            d_p3d_32 = triangulation(d_p0, d_p3, calibration.mtx0, calibration.mtx3, calibration.R_3, calibration.T_3, calibration.R_2, calibration.T_2)
            mean_points = wm.weighted_mean([d_p3d_01,d_p3d_02,d_p3d_03,d_p3d_12,d_p3d_31,d_p3d_32], weights)
            rotated_result = np.dot(calibration.rotation_matrix, mean_points)
            points_3d.append(rotated_result)
            
            points_3d_01.append(d_p3d_01)
            points_3d_02.append(d_p3d_02)
            points_3d_03.append(d_p3d_03)
            points_3d_12.append(d_p3d_12)
            points_3d_31.append(d_p3d_31)
            points_3d_32.append(d_p3d_32)
           
    rotated_points_3da = rotate_points(points_3d_12, calibration.rotation_matrix)
    rotated_points_3db = rotate_points(points_3d_31, calibration.rotation_matrix)
    rotated_points_3dc = rotate_points(points_3d_32, calibration.rotation_matrix)
    rotated_points_3dd = rotate_points(points_3d_01, calibration.rotation_matrix)
    rotated_points_3de = rotate_points(points_3d_02, calibration.rotation_matrix)
    rotated_points_3df = rotate_points(points_3d_03, calibration.rotation_matrix)

        
    plotter.plot(rotated_points_3dd,rotated_points_3de,rotated_points_3df,rotated_points_3da,rotated_points_3db,rotated_points_3dc,points_3d)
    cap_0.release()
    cap_1.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()