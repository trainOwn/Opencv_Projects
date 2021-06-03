from __future__ import print_function
import cv2 as cv
import argparse
parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
parser.add_argument('--save_video',
		type=bool,
		default=False,
		help='Set to True, if you want to save output.')

args = parser.parse_args()
if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()
capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
if not capture.isOpened():
    print('Unable to open: ' + args.input)
    exit(0)

force_stop = False
ret, frame = capture.read()
print((frame.shape[1], frame.shape[0]))
if args.save_video is True:
    # Initialize the video writer
    fourcc = cv.VideoWriter_fourcc(*"MJPG")
    writer = cv.VideoWriter("./output_video.avi", fourcc, 10,
                    (frame.shape[1], frame.shape[0]), True)
while True:
    ret, frame = capture.read()
    if frame is None:
        break

    fgMask = backSub.apply(frame)


    cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))


    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)
    save = cv.cvtColor(fgMask, cv.COLOR_GRAY2RGB)
    if args.save_video is True:
        # print("writing data")
        writer.write(save)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        if args.save_video is True:
            writer.release()
            # pass
        capture.release()
        force_stop = True
        cv.destroyAllWindows()
        break

#to release instance
if not force_stop:
    if args.save_video is True:
        writer.release()
    capture.release()
    cv.destroyAllWindows()