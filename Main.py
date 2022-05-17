import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector

cam = cv2.VideoCapture(0)
# detector
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (1280,720))

while cam.isOpened():
    # read video feed
    success, frame = cam.read()
    # fshape = frame.shape
    # fheight = fshape[0]
    # fwidth = fshape[1]
    # print(fheight, fwidth)

    # detect and mash face
    FaceMesh = FaceMeshDetector(maxFaces=1)
    frame, faces = FaceMesh.findFaceMesh(frame)

    # if there is a face
    if faces:
        face = faces[0]
        leftEye = face[145]
        rightEye = face[374]
        cv2.circle(frame, leftEye, 4, (0,100,0), 4)
        cv2.circle(frame, rightEye, 4, (0,100,0), 4)

        # distance of eyes in pixels
        dEye, _ = FaceMesh.findDistance(leftEye, rightEye)

        # distance of eyes in cm
        DEye = 7

        # Focal length calibrate
        # assume distance is 50 cm find f
        # f = dEye*50/DEye
        # print(f)

        # Calibrated focal length
        f = 535

        # calculate depth distance in cm
        D = f*DEye/dEye

        # show depth on img
        cvzone.putTextRect(frame,f'Depth {int(D)} cm',(face[10][0]-100,face[10][1]), scale=2,thickness=2,colorT=(255,255,255),colorR=(0,100,20))

    out.write(frame)
    cv2.imshow("video", frame)
    cv2.waitKey(1)
else:
    cam.release()
    out.release()