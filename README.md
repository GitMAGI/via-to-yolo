# via-to-yolo

This pseudo-script aims to produce a valid data set suitable for YOLO (this is tested only for v7) [[2]](#2), starting from a json annotation file, in COCO format (<i> ... COCO is a large-scale object detection, segmentation, and captioning dataset ... </i> [[5]](#5)), exported by the web application VGG Image Annotator (VIA) [[1]](#1). 
The walkthrough from VIA to YOLO requires intermediate processing and conversion steps, accomplished through the libraries such as PyLabel [[4]](#4) and PIL [[3]](#3).


## VGG Image Annotator

VIA is an extreme light-weight and powerful HTML/js tool as starting point for training object detection tools with custom datasets. [[1]](#1)
>VGG Image Annotator is a simple and standalone manual annotation software for image, audio and video. VIA runs in a web browser and does not require any installation or setup. The complete VIA software fits in a single self-contained HTML page of size less than 400 Kilobyte that runs as an offline application in most modern web browsers.

Some problems arise, when the object detection network you need to train, needs different annotation file format.

Furhermore object detection networks can require a peculiar dataset filesystem tree, where dataset files need to be arragned according to some specific rules.


### Use VIA to create the annotations file in COCO format

* Define an attribute of type "dropdown" and add options with id and description.
* Go to settings and set the "project name" and the absolute path of the images folder to annotate.
* Select the folder path of the images folder to annotate through the "add files" button.
* Add region shapes of type "rectangle" to images and assign to these region shape the right class option through the dropdown list of the classe defined previuosly.
* Save the annotations json file of the project.
* Export the annotaiton json file in COCO format through the menu Annotation/Export Annotations (COCO format).


## via-to-yolo script

The object of this script is create: 
1. yaml annotation file in YOLO format 
2. annotations in txt file as the YOLO format (x_center, y_center, width, heigh)
>In yolo, a bounding box is represented by four values [x_center, y_center, width, height]. x_center and y_center are the normalized coordinates of the center of the bounding box. To make coordinates normalized, we take pixel values of x and y, which marks the center of the bounding box on the x- and y-axis. Then we divide the value of x by the width of the image and value of y by the height of the image. width and height represent the width and the height of the bounding box. They are normalized as well.
3. a dataset in a filesystem tree as 
```
<dataset-name>
├── test
│   ├── images
│   │   ├── file_test_1.jpg
│   │   ├── file_test_2.jpg
│   │   ├── file_test_3.jpg
│   │   └── file_test_4.jpg
│   └── labels
│       ├── file_test_1.txt
│       ├── file_test_2.txt
│       ├── file_test_3.txt
│       └── file_test_4.txt
├── train
│   ├── images
│   │   ├── file_train_1.jpg
│   │   ├── file_train_2.jpg
│   │   ├── file_train_3.jpg
│   │   └── file_train_4.jpg
│   └── labels
│       ├── file_train_1.txt
│       ├── file_train_2.txt
│       ├── file_train_3.txt
│       └── file_train_4.txt
└── val
    ├── images
    │   ├── file_val_1.jpg
    │   ├── file_val_2.jpg
    │   ├── file_val_3.jpg
    │   └── file_val_4.jpg
    └── labels
        ├── file_val_1.txt
        ├── file_val_2.txt
        ├── file_val_3.txt
        └── file_val_4.txt
```

### Execute the script

Edit the app.py file in src folder with the appropriate arguments:

* input_path **path of the input data (images and COCO annotation file)**
* input_images **if images path has is different from the input_path**
* input_annotations **COCO annotation file**
* dataset_name **the name of the dataset**
* output_root_path **path of the results**
* train_pct **amount of data for the training set (percentage)**
* test_pct **amount of data for the test set (percentage)**
* val_pct **amount of data for the validation set (percentage)**

```python 
    input_path = os.path.join('input', 'random_p5')
    input_images = ''
    input_annotations = 'via_bouncy_random_p5_coco.json'
    dataset_name = f'bouncyhoops_random_p5'

    output_root_path = 'output'

    train_pct=0.5
    test_pct=0.25
    val_pct=0.25
```

Execute the script and check the output path.

## YOLO

Once you have the annotaion yaml file and the dataset folder outcame from the previous step, copy those to the data folder of the yolo project path.

The values of the parameters (like epochs, worker threads and GPU enabled) specified in the next code snippets are just related to the enviroment capabilities available during the test.


### Use YOLO to train the network

```bash
export dataset_yaml_name=<dataset_name>
echo ${dataset_yaml_name}.yaml
python train.py --batch 8 --epochs 80 --img 640 --workers 18 --device 0 --hyp data/hyp.scratch.tiny.yaml --data data/${dataset_yaml_name}.yaml --cfg cfg/training/yolov7.yaml --weights 'yolov7-tiny.pt' --name ${dataset_yaml_name}
```

### Use YOLO to test detection
```bash
export video_to_detect=<path>/<video-name>.<video-extension>
python detect.py --weights runs/train/${dataset_yaml_name}/weights/best.pt --conf 0.25 --img-size 640 --source ${video_to_detect}
```

## References
<a id="1" target="_blank" rel="noopener noreferrer" href="https://github.com/WongKinYiu/yolov7">[1]</a> 
Wang, Chien-Yao and Bochkovskiy, Alexey and Liao, Hong-Yuan Mark. 2022. YOLOv7: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors. arXiv preprint arXiv:2207.02696. <a target="_blank" rel="noopener noreferrer" href="https://github.com/WongKinYiu/yolov7">GitHub</a>

<a id="2" target="_blank" rel="noopener noreferrer" href="https://www.robots.ox.ac.uk/~vgg/software/via/">[2]</a> Abhishek Dutta and Andrew Zisserman. 2019. The VIA Annotation Software for Images, Audio and Video. In Proceedings of the 27th ACM International Conference on Multimedia (MM ’19), October 21–25, 2019, Nice, France. ACM, New York, NY, USA, 4 pages. https://doi.org/10.1145/3343031.3350535. <a target="_blank" rel="noopener noreferrer" href="https://github.com/ox-vgg/via">GitHub</a>

<a id="3" target="_blank" rel="noopener noreferrer" href="https://github.com/python-pillow/Pillow">[3]</a> Jeffrey A. Clark (Alex) and contributors. <a target="_blank" rel="noopener noreferrer" href="https://github.com/python-pillow/Pillow"> Pillow - GitHub </a>

<a id="4" target="_blank" rel="noopener noreferrer" href="https://github.com/pylabel-project/pylabel">[4]</a> Jeremy Fraenkel, Alex Heaton, and Derek Topper. <a target="_blank" rel="noopener noreferrer" href="https://github.com/pylabel-project/pylabel"> PyLabel - GitHub </a>

<a id="5" target="_blank" rel="noopener noreferrer" href="https://cocodataset.org/#home">[5]</a> COCO. <a target="_blank" rel="noopener noreferrer" href="https://cocodataset.org/#home">Home Page </a>
