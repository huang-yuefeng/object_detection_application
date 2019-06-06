import cv2
import os
import csv
import time

hand_result = []
phone_result = []
cigarette_result = []
home = './data_label/'
source = './data_source/'
target = './data_target/'

def run(cpuid, paths):
	image_i = 0
	for path in paths:
		images = os.listdir(home+path)
		total_image_count = len(images)
		for item in images:
			image_i += 1
			start = time.time()
			hand_x_min = 100000
			hand_x_max = -1
			hand_y_min = 100000
			hand_y_max = -1

			phone_x_min = 100000
			phone_x_max = -1
			phone_y_min = 100000
			phone_y_max = -1

			cigarette_x_min = 100000
			cigarette_x_max = -1
			cigarette_y_min = 100000
			cigarette_y_max = -1


			img = cv2.imread(home+path+'/'+item)
			print home+path+item
			if img is None:
				print 'error'
			for i,x in enumerate(img):
				for j,y in enumerate(x):
					if y[0]==0 and y[1] == 0 and y[2] == 255:
						hand_y_max = max(hand_y_max, j)
						hand_y_min = min(hand_y_min, j)
						hand_x_max = max(hand_x_max, i)
						hand_x_min = min(hand_x_min, i)
					if y[0]==0 and y[1] == 255 and y[2] == 0:
						phone_y_max = max(phone_y_max, j)
						phone_y_min = min(phone_y_min, j)
						phone_x_max = max(phone_x_max, i)
						phone_x_min = min(phone_x_min, i)
					if y[0]==255 and y[1] == 0 and y[2] == 0:
						cigarette_y_max = max(cigarette_y_max, j)
						cigarette_y_min = min(cigarette_y_min, j)
						cigarette_x_max = max(cigarette_x_max, i)
						cigarette_x_min = min(cigarette_x_min, i)

			target_name = str((100+cpuid)*1000000)+'_'+str(image_i)+'.png'
			name_part=[target_name,1920,1080]
			if hand_x_max != -1:
				hand_result.append([])
				hand_result[-1] += name_part
				hand_result[-1] += ['hand',hand_y_min,hand_x_min,hand_y_max,hand_x_max]
				os.system('touch ./hand/'+target_name)
				os.system('cp '+source+path[1:]+'/'+item+' ./hand/'+target_name)
			if phone_x_max != -1:
				phone_result.append([])
				phone_result[-1] += name_part
				phone_result[-1] += ['phone',phone_y_min,phone_x_min,phone_y_max,phone_x_max]
				os.system('touch ./phone/'+target_name)
				os.system('cp '+source+path[1:]+'/'+item+' ./phone/'+target_name)
			if cigarette_x_max != -1:
				cigarette_result.append([])
				cigarette_result[-1]+= name_part
				cigarette_result[-1] += ['cigarette',cigarette_y_min,cigarette_x_min,cigarette_y_max,cigarette_x_max]
				os.system('touch ./cigarette/'+target_name)
				os.system('cp '+source+path[1:]+'/'+item+' ./cigarette/'+target_name)
			print 'hand_box', hand_y_max, hand_y_min, hand_x_max, hand_x_min
			print 'phone_box',phone_y_max, phone_y_min, phone_x_max, phone_x_min
			print 'cigarette_box',cigarette_y_max, cigarette_y_min, cigarette_x_max, cigarette_x_min
			end = time.time()
			print 'cpuid = ', cpuid, 'time cost = ', end-start, 'done percent = ', image_i, 'total = ', total_image_count
#			return
def preprocess(cpuid, paths):
	run(cpuid, paths)
	csv_result = open(str(cpuid)+'hand.csv','w' )
	writer = csv.writer(csv_result)
	print 'hand count ', len(hand_result)
	for i in range(len(hand_result)):
			writer.writerow(hand_result[i])
	csv_result.close()

	csv_result = open(str(cpuid)+'phone.csv','w')
	writer = csv.writer(csv_result)
	print 'phone count ', len(phone_result)
	for i in range(len(phone_result)):
			writer.writerow(phone_result[i])
	csv_result.close()

	csv_result = open(str(cpuid)+'cigarette.csv','w')
	writer = csv.writer(csv_result)
	print 'cigarette count ', len(cigarette_result)
	for i in range(len(cigarette_result)):
			writer.writerow(cigarette_result[i])
	csv_result.close()

paths1 = ['c/IMG_1970.MOV_selected_to_label/', 'c/IMG_1973.MOV_selected_to_label/', 'c/IMG_1974.MOV_selected_to_label/']
cpuid1 = 1
#paths21 = ['c/IMG_1976_1.MOV_selected_to_label/']
#cpuid21 = 21
#paths22 = ['c/IMG_1976_2.MOV_selected_to_label/']
#cpuid22 = 22
#paths31 = ['b/IMG_1979_1.MOV_selected_to_label/']
#cpuid31 = 31
#paths32 = ['b/IMG_1979_2.MOV_selected_to_label/']
#cpuid32 = 32
#paths4 = ['b/IMG_1980.MOV_selected_to_label/']
#cpuid4 = 4
#paths5 = ['d/IMG_1971.MOV_selected_to_label/', 'd/IMG_1972.MOV_selected_to_label/','d/IMG_1978.MOV_selected_to_label/']
#cpuid5 = 5
#paths61 = ['d/IMG_1975_1.MOV_selected_to_label/']
#cpuid61 = 61
#paths62 = ['d/IMG_1975_2.MOV_selected_to_label/']
#cpuid62 = 62
#paths7 = ['a/IMG_1968.MOV_selected_to_label/', 'a/VID_20190131_135048.mp4_selected_to_label/']
#cpuid7 = 7

preprocess(cpuid1, paths1)
#preprocess(cpuid21, paths21)
#preprocess(cpuid22, paths22)
#preprocess(cpuid31, paths31)
#preprocess(cpuid32, paths32)
#preprocess(cpuid4, paths4)
#preprocess(cpuid5, paths5)
#preprocess(cpuid61, paths61)
#preprocess(cpuid62, paths62)
#preprocess(cpuid7, paths7)
