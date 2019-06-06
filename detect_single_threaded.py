from utils import detector_utils as detector_utils
import cv2
import tensorflow as tf
import datetime
import argparse
import os
import json

detection_graph, sess = detector_utils.load_inference_graph()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-sth',
        '--scorethreshold',
        dest='score_thresh',
        type=float,
        default=0.2,
        help='Score threshold for displaying bounding boxes')
    parser.add_argument(
        '-fps',
        '--fps',
        dest='fps',
        type=int,
        default=1,
        help='Show FPS on detection/display visualization')
    parser.add_argument(
        '-src',
        '--source',
        dest='video_source',
        default=0,
        help='Device index of the camera.')
    parser.add_argument(
        '-wd',
        '--width',
        dest='width',
        type=int,
        default=320,
        help='Width of the frames in the video stream.')
    parser.add_argument(
        '-ht',
        '--height',
        dest='height',
        type=int,
        default=180,
        help='Height of the frames in the video stream.')
    parser.add_argument(
        '-ds',
        '--display',
        dest='display',
        type=int,
        default=0,
        help='Display the detected images using OpenCV. This reduces FPS')
    parser.add_argument(
        '-num-w',
        '--num-workers',
        dest='num_workers',
        type=int,
        default=4,
        help='Number of workers.')
    parser.add_argument(
        '-q-size',
        '--queue-size',
        dest='queue_size',
        type=int,
        default=5,
        help='Size of the queue.')
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.video_source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    start_time = datetime.datetime.now()
    num_frames = 0
    im_width, im_height = (cap.get(3), cap.get(4))
    # max number of hands we want to detect/track
    #num_hands_detect = 2
    num_hands_detect = 1

    #cv2.namedWindow('Single-Threaded Detection', cv2.WINDOW_NORMAL)

    i = 0
    bound_dic = {}    
    while True:
        i += 1
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        ret, image_np = cap.read()
        if image_np is None:
            break
        if args.video_source != 'VID_20190131_135048.mp4':
        #image_np = cv2.flip(image_np, 1)
            (h,w) = image_np.shape[:2]
            center = (w//2, h//2)
            M = cv2.getRotationMatrix2D(center, 180,1.0)
            image_np = cv2.warpAffine(image_np,M,(w,h))
        try:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        except:
            print("Error converting to RGB")

        # Actual detection. Variable boxes contains the bounding box cordinates for hands detected,
        # while scores contains the confidence for each of these boxes.
        # Hint: If len(boxes) > 1 , you may assume you have found atleast one hand (within your score threshold)

        boxes, scores = detector_utils.detect_objects(image_np,
                                                      detection_graph, sess)

        b_should_be_labeled = False
        # draw bounding boxes on frame
        b_draw = detector_utils.draw_box_on_image(num_hands_detect, args.score_thresh,
                                         scores, boxes, im_width, im_height,
                                         image_np)
        for j in range(num_hands_detect):
                if (scores[j] > args.score_thresh):
                    bound= (left, right, top, bottom) = (boxes[j][1] * im_width, 
                            boxes[j][3] * im_width,boxes[j][0] * im_height, boxes[j][2] * im_height)
                    bound_dic[i]=bound

        if b_draw:
            image_np_rgb = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            cv2.imwrite('./to_label/'+str(1000000+i)+'.png',image_np_rgb)

        # Calculate Frames per second (FPS)
        num_frames += 1
        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        fps = num_frames / elapsed_time

        if (args.display > 0):
            # Display FPS on frame
            if (args.fps > 0):
                detector_utils.draw_fps_on_image("FPS : " + str(int(fps)),
                                                 image_np)

            cv2.imshow('Single-Threaded Detection',
                       cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        else:
            print("frames processed: ", num_frames, "elapsed time: ",
                  elapsed_time, "fps: ", str(int(fps)))
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            cv2.imwrite('./frame_result/'+str(1000000+i)+'.png',image_np)
            #if i == 100:
                    #break
cap.release()

f=open('./bound_dic','w')
data = json.dumps(bound_dic)
f.write(data)
f.close()

video_path = './detect_db.avi'
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
video = cv2.VideoWriter( video_path, fourcc, 30.0, (1920,1080))

filelist = os.listdir('./frame_result/')
i = 0
for item in filelist:
        item = './frame_result/{}.png'.format(1000000+i)
        img = cv2.imread(item)
        video.write(img)
        i +=1
        print i
video.release()
