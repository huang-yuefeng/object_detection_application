#Guide to make object detection application.
##Step 1
label object with solid line, and convert label data to csv file by label2csv.py.
##Step 2
git the work folder of tensorflow object detection api home folder https://github.com/tensorflow/models/tree/master/research/object_detection.
cd models/research/object_detection/
convert csv file to tfrecord file for tensorflow trainning by generate_tfrecord.py.
##Step 3
make data folder, and put tfrecord data inside this folder, copy configuration file faster_rcnn_resnet101_pets.config and db_map.pbtxt file.
modifying conig and pbtxt file for special training.
just run training shell, such as train_phone_detection.sh 
##Step 4 
export trained model to pb file for mobile phone by run export_trained_model.sh.
##Step 5
test pf file by run detect_single_threaded.py.

*python file is used to as backup file FYI.
