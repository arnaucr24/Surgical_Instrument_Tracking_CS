import cv2
import numpy as np

class DetectGreen:
    def __init__(self):
        # Define the lower and upper bounds for the color green in HSV format
        self.lower_green = np.array([50, 70, 80])
        self.upper_green = np.array([80, 150, 255])

    def detect(self, frame):
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create a mask using the defined green color range
        mask = cv2.inRange(hsv, self.lower_green, self.upper_green)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

        green_centers = []
        for contour in contours:
            # Calculate the center of the contour
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                green_centers.append((cX, cY))
                # Draw a small circle at the center
                cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
        green_point = None
        if green_centers:
            green_centers = np.array(green_centers)
            green_point = np.mean(green_centers, axis=0)
            cv2.circle(frame, (int(green_point[0]), int(green_point[1])), 20, (255, 0, 0), -1)
        
        return frame, green_point

# Example usage:
# Create an instance of DetectGreen
detector = DetectGreen()

# Assuming 'frame' is your input frame, you can call the detect method
# and it will return the modified frame with green contours and the green point
# frame, green_point = detector.detect(frame)
