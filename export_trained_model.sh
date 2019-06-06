CUDA_VISIBLE_DEVICES=0 python object_detection/export_inference_graph.py     --input_type=image_tensor     --pipeline_config_path=./data/faster_rcnn_resnet101_pets.config     --trained_checkpoint_prefix=./cigarette_data/model.ckpt-10763     --output_directory=./trained_cigarette_model

