# via-to-yolo

This pseudo-script aims to produce a valid data set suitable for YOLO (this is tested only for v7) [[2]](#2), starting from a json annotion file, in COCO format (<i> ... COCO is a large-scale object detection, segmentation, and captioning dataset ... </i> [[5]](#5)), exported by the web application VGG Image Annotator (VIA) [[1]](#1). 
The walkthrough from VIA to YOLO requires intermediate processing and conversion steps, accomplished through the libraries such as PyLabel [[4]](#4) and PIL [[3]](#3).

VIA is an extreme light-weight and powerful HTML/js tool as starting point for custom training object detection problems. [[1]](#1)
>VGG Image Annotator is a simple and standalone manual annotation software for image, audio and video. VIA runs in a web browser and does not require any installation or setup. The complete VIA software fits in a single self-contained HTML page of size less than 400 Kilobyte that runs as an offline application in most modern web browsers.

Some problems arise, when the object detection network you need to train, needs different annotation file format.

Furhermore object detection networks can require a peculiar dataset filesystem tree, where dataset files need to be arragned according to some specific rules.

## References
<a id="1" target="_blank" rel="noopener noreferrer" href="https://github.com/WongKinYiu/yolov7">[1]</a> 
Wang, Chien-Yao and Bochkovskiy, Alexey and Liao, Hong-Yuan Mark. 2022. YOLOv7: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors. arXiv preprint arXiv:2207.02696. <a target="_blank" rel="noopener noreferrer" href="https://github.com/WongKinYiu/yolov7">GitHub</a>

<a id="2" target="_blank" rel="noopener noreferrer" href="https://www.robots.ox.ac.uk/~vgg/software/via/">[2]</a> Abhishek Dutta and Andrew Zisserman. 2019. The VIA Annotation Software for Images, Audio and Video. In Proceedings of the 27th ACM International Conference on Multimedia (MM ’19), October 21–25, 2019, Nice, France. ACM, New York, NY, USA, 4 pages. https://doi.org/10.1145/3343031.3350535. <a target="_blank" rel="noopener noreferrer" href="https://github.com/ox-vgg/via">GitHub</a>

<a id="3" target="_blank" rel="noopener noreferrer" href="https://github.com/python-pillow/Pillow">[3]</a> Jeffrey A. Clark (Alex) and contributors. <a target="_blank" rel="noopener noreferrer" href="https://github.com/python-pillow/Pillow"> Pillow - GitHub </a>

<a id="4" target="_blank" rel="noopener noreferrer" href="https://github.com/pylabel-project/pylabel">[4]</a> Jeremy Fraenkel, Alex Heaton, and Derek Topper. <a target="_blank" rel="noopener noreferrer" href="https://github.com/pylabel-project/pylabel"> PyLabel - GitHub </a>

<a id="5" target="_blank" rel="noopener noreferrer" href="https://cocodataset.org/#home">[5]</a> COCO. <a target="_blank" rel="noopener noreferrer" href="https://cocodataset.org/#home">Home Page </a>