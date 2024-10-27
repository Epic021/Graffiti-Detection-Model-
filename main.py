import time

import cv2
import numpy as np
from datetime import datetime
from send_sms import send_trigger_sms
from imageTransfer import send_email_attach
from project_config import *
from threading import Timer


# Camera configuration
CAMERA_DEVICE_ID = 0
IMAGE_WIDTH = 320
IMAGE_HEIGHT = 240
MOTION_BLUR = True

RECTANGLE_X = 80
RECTANGLE_Y = 20
RECTANGLE_WIDTH = 120
RECTANGLE_HEIGHT = 120

FRAME_COUNT = 0
CHANGE_FRAME_COUNT = 0
PRE_EVENT_COUNT = 0
EVENT_COUNT = 0
NOTIFICATION_FLAG = 0


def mse(image_a, image_b):
    err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])
    return err


def timer_notification_flag():
    global NOTIFICATION_FLAG
    print("Inside timer. Resetting notification flag")
    NOTIFICATION_FLAG = 0
    timerAlarm.cancel()


if __name__ == "__main__":
    try:
        cap = cv2.VideoCapture(CAMERA_DEVICE_ID)
        cap.set(3, IMAGE_WIDTH)
        cap.set(4, IMAGE_HEIGHT)

        while True:
            _, frame_raw = cap.read()

            if MOTION_BLUR:
                frame = cv2.GaussianBlur(frame_raw, (3,3),0)
            else:
                frame = frame_raw

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rectangle_image = cv2.rectangle(frame_gray, (RECTANGLE_X,RECTANGLE_Y), (RECTANGLE_X + RECTANGLE_WIDTH,RECTANGLE_Y + RECTANGLE_HEIGHT), (255, 0, 0), 2)
            cv2.putText(rectangle_image, 'ROI', (RECTANGLE_X, RECTANGLE_Y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (36, 43, 12), 2)

            # Cropped image
            roi_frame = frame_gray[RECTANGLE_Y:RECTANGLE_Y + RECTANGLE_HEIGHT, RECTANGLE_X:RECTANGLE_X + RECTANGLE_WIDTH]
            roi_image = cv2.Canny(roi_frame,100,200)

            cv2.imshow('RT', rectangle_image)
            cv2.imshow('ROI', roi_image)

            if FRAME_COUNT == 5:
                reference_roi_image = roi_frame
                print("==============================")
                print("Reference image stored")
                print("==============================")

            if FRAME_COUNT > 10:

                if mse(roi_frame, reference_roi_image) > 100:
                    print('Frame{0}: Change detected. Increasing frame_change count'.format(CHANGE_FRAME_COUNT))
                    CHANGE_FRAME_COUNT += 1

                    if CHANGE_FRAME_COUNT > EXTDEF_EVENT_CHECK_FRAMES:
                        print("Change triggered")
                        PRE_EVENT_COUNT += 1
                        CHANGE_FRAME_COUNT = 0

                        if PRE_EVENT_COUNT >= EXTDEF_SUSTAINED_EVENT_VERIFICATION_RUNS:
                            print("Event triggered")
                            PRE_EVENT_COUNT = 0

                            with open(EXTDEF_EVENT_LOG, 'a') as evfonj:
                                evfonj.writelines("event at " + str(datetime.now().strftime("%d%m%Y_%H%M%S")))
                                evfonj.writelines("\n")

                            if EXTDEF_UPDATE_IMAGE_FLAG == True and EVENT_COUNT >= 5:
                                print("Persistant change. Update reference image")
                                reference_roi_image = roi_frame

                            if NOTIFICATION_FLAG == 0:
                                print("Sending notification")

                                EVENT_COUNT += 1

                                # Save image to disk and send email + SMS
                                img_name = "event_" + str(datetime.now().strftime("%d%m%Y_%H%M%S")) + ".jpg"
                                cv2.imwrite(EXTDEF_TOSEND_PATH + img_name, frame)
                                final_img_name = EXTDEF_TOSEND_PATH + str(img_name)

                                if EXTDEF_ENABLE_SMS:
                                    try:
                                        send_trigger_sms()
                                    except:
                                        print("SMS: Tx Error")
                                        
                                if EXTDEF_ENABLE_EMAIL:
                                    try:
                                        send_email_attach(final_img_name)
                                    except:
                                        print("Email: TX Error")
                                        
                                NOTIFICATION_FLAG = 1
                                timerAlarm = Timer(EXTDEF_NOTIFICATION_GAP_IN_SECONDS, timer_notification_flag)
                                timerAlarm.start()
                            else:
                                print("Notification block")
                                time.sleep(5)

                else:
                    CHANGE_FRAME_COUNT = 0
                    PRE_EVENT_COUNT = 0
                    EVENT_COUNT = 0

            FRAME_COUNT += 1
            print("Frame Number: " + str(FRAME_COUNT))
            if cv2.waitKey(1)== 27:
                break

    except Exception as e:
        print(e)
    finally:
        cv2.destroyAllWindows()
        cap.release()
