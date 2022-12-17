import pyhik.hikvision
import logging

from decouple import config
# camera = pyhik.hikvision.HikCamera(ip, port, usr, pwd)



import cv2

# Set the URL of the stream
STREAMING_URL = config("STREAMING_URL")

# # Open the RTSP link using cv2.VideoCapture
# cap = cv2.VideoCapture(STREAMING_URL)

# # Loop indefinitely
# # while True:
# # Capture the next frame from the stream
# ret, frame = cap.read()


# # If the frame was successfully captured, display it
# if ret:
#     cv2.imwrite("image.jpg", frame)
    
# # # Wait for the user to press a key
# # key = cv2.waitKey(1)

# # # If the user pressed the 'q' key, break out of the loop and if s key is pressed save the image
# # if key == ord("q"):

# #     break
# # if key == ord("s"):
# #     cv2.imwrite("image.jpg", frame)
# #     print("Image saved")

# # Close the window and release the camera
# cap.release()
# cv2.destroyAllWindows()