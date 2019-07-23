import cv2
import os
import time
import json

MOV_D = 50
def detect_move(name, labeled_video_path, original_video_path):
    path = name+'_bound_dic'
    print path
    bound_dic = None
    try:
        f=open(path)
        bound_dic = json.loads(f.read())
        f.close()
    except IOError:
        print "File is not found."
        return
    index_bound = bound_dic.items()
    index_bound.sort(cmp=lambda x,y: cmp(int(x[0]), int(y[0])))
    prev_i,prev_b = 0,0
    prev_center = 0,0 
    count = 0

    b = False
    select_list = []
    for i,b in index_bound:
        if int(i) - int(prev_i) == 2:
            #print int(i)-1
            select_list.append(int(i)-1)
            count += 1
        if b == False:
            b = True
            prev_i,prev_b = index_bound[0]
            prev_center = (prev_b[0]+prev_b[1])/2,(prev_b[2]+prev_b[3])/2
        else:
            center = (b[0]+b[1])/2,(b[2]+b[3])/2
            if ((center[0]-prev_center[0])**2+(center[1]-prev_center[1])**2)**0.5 >= MOV_D:
                count += 1
                #print i
                select_list.append(int(i))
                prev_i = i
                prev_center = center

    print 'total frame count is ', count

    cap = cv2.VideoCapture(labeled_video_path+name+'.avi')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)

    print original_video_path+name
    original_cap = cv2.VideoCapture(original_video_path+name)
    original_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    original_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)

    video_path = name+'_to_lable.avi'
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    video = cv2.VideoWriter( video_path, fourcc, 30.0, (1920,1080))

    os.system('rm -r  '+name+'_selected_to_label')
    os.system('mkdir  '+name+'_selected_to_label')

    i = 0
    j = 0
    while True:
        i += 1
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        ret, image_np = cap.read()
        ret, original_image_np = original_cap.read()
        if original_image_np is None:
            print 'read original image error'
            exit()
        if image_np is None:
            break
        if i in select_list:
            video.write(image_np)
            if name != 'VID_20190131_135048.mp4':
                (h,w) = original_image_np.shape[:2]
                center = (w//2, h//2)
                M = cv2.getRotationMatrix2D(center, 180,1.0)
                original_image_np = cv2.warpAffine(original_image_np,M,(w,h))
            cv2.imwrite(name+'_selected_to_label/'+str(1000000+i)+'.jpg',original_image_np)
            j += 1
            if j % 10 == 0:
                print j

    cap.release()
    video.release()

original_video_path = './to_label_video/'
labeled_video_path = './0215_result/'
filelist = os.listdir(original_video_path)
print filelist
for name in filelist:
    if name != 'VID_20190131_135048.mp4':
        continue
    detect_move(name, labeled_video_path, original_video_path)
