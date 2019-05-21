import os
import coco
import json
import argparse
import cv2
import numpy as np
from skimage import measure
from pycocotools import mask
from mrcnn import model as modellib
import tensorflow as tf 

# Function definitions START ***********************************

def random_colors(N):
    np.random.seed(1)
    colors = [tuple(255 * np.random.rand(3)) for _ in range(N)]
    return colors

def apply_mask(image, mask, color, alpha=0.5):
    """apply mask to image"""
    for n, c in enumerate(color):
        image[:, :, n] = np.where(
            mask == 1,
            image[:, :, n] * (1 - alpha) + alpha * c,
            image[:, :, n]
        )
    return image

def display_instances(image, boxes, masks, ids, names, scores):
    """
        take the image and results and apply the mask, box, and Label
    """

    n_instances = boxes.shape[0]

    if not n_instances:
        print('NO INSTANCES TO DISPLAY')
    else:
        assert boxes.shape[0] == masks.shape[-1] == ids.shape[0]

    for i in range(n_instances):
        if not np.any(boxes[i]):
            continue

        y1, x1, y2, x2 = boxes[i]
        label = names[ids[i]]
        color = class_dict[label]
        score = scores[i] if scores is not None else None
        caption = '{} {:.2f}'.format(label, score) if score else label
        mask = masks[:, :, i]

        rows = mask.shape[0]
        columns = mask.shape[1]

        image = apply_mask(image, mask, color)
        image = cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        image = cv2.putText(
            image, caption, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.7, color, 2
        )
    return image

# Function definitions END ***********************************

class IMA():
    def __init__(self, cfg):

        # Initialize the config
        class InferenceConfig(coco.CocoConfig):
            GPU_COUNT = cfg['GPU_COUNT']
            IMAGES_PER_GPU = cfg['IMAGES_PER_GPU']
            DETECTION_MIN_CONFIDENCE = cfg['DETECTION_MIN_CONFIDENCE']
            IMAGE_RESIZE_MODE = "square"
            NUM_CLASSES = cfg["NUM_CLASSES"]

        # Initialize the MaskRCNN Model and load weights
        self.model = modellib.MaskRCNN(mode="inference", model_dir=os.path.join(os.getcwd(), "logs"), config=InferenceConfig())

        # Load weights into the model
        for weights in cfg["initial_weights"]:
            self.model.load_weights("weights/{}".format(weights), by_name=True)

        # Define class names. TODO: Load class names from the .h5 file itself for more flexibility
        self.class_names = [
            'BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
            'bus', 'train', 'truck', 'boat', 'traffic light',
            'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
            'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
            'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
            'suitcase', 'frisbee', 'skis' , 'snowboard', 'sports ball',
            'kite', 'baseball bat', 'baseball glove', 'skateboard',
            'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
            'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
            'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
            'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
            'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
            'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
            'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
            'teddy bear', 'hair drier', 'toothbrush'
        ]

        self.colors = random_colors(len(self.class_names))
        self.class_dict = { name: color for name, color in zip(self.class_names, self.colors) }

    
    def save_inference_json(self, image_path):
        
        capture = cv2.imread(image_path)
        r = self.model.detect([capture], verbose=0)[0]
        
        inference_json = {
            "images": [], 
            "annotations": []
        }

        n_instances = r['rois'].shape[0]

        if not n_instances:
            print('NO INSTANCES TO DISPLAY')
        else:
            assert r['rois'].shape[0] == r['masks'].shape[-1] == r['class_ids'].shape[0]
        
        num_letters = len(image_path)

        for letter in image_path[::-1]:
            if letter is not "/":
                num_letters = num_letters - 1
            else:
                break
        
        this_image = {
            "file_name": image_path[num_letters:], 
            "height": np.shape(r['masks'])[1], 
            "width": np.shape(r['masks'])[0], 
            "id": 0
        }

        inference_json["images"].append(this_image)

        for i in range(n_instances):
            if not np.any(r['rois'][i]):
                continue
            
            y1, x1, y2, x2 = r['rois'][i]
            this_mask = r['masks'][:, :, i]
            label = self.class_names[r['class_ids'][i]]

            binary_mask_to_int = this_mask.astype(np.uint8)
            fortran_ground_truth_binary_mask = np.asfortranarray(binary_mask_to_int)
            encoded_ground_truth = mask.encode(fortran_ground_truth_binary_mask)
            ground_truth_area = mask.area(encoded_ground_truth)
            ground_truth_bounding_box = mask.toBbox(encoded_ground_truth)
            contours = measure.find_contours(this_mask, 0.5)

            # Create annotation
            annotation = {
                    "segmentation": [],
                    "area": ground_truth_area.tolist(),
                    "iscrowd": 0,
                    "image_id": 0,
                    "bbox": ground_truth_bounding_box.tolist(),
                    "category_id": int(r['class_ids'][i]),
                    "id": 100
                }

            # Add segmentations to each annotation
            for contour in contours:
                contour = np.flip(contour, axis=1)
                segmentation = contour.ravel().tolist()
                annotation["segmentation"].append(segmentation)
            
            # Add annotation to annotations array
            inference_json["annotations"].append(annotation)
        
        return inference_json