python -m object_detection/inference/infer_detections   --input_tfrecord_paths=data/test.record   --output_tfrecord_path=./evaluation_result/validation_detections.tfrecord-00000-of-0000   --inference_graph=trained_model/frozen_inference_graph.pb   --discard_image_pixels