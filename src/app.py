from pylabel import importer
import os
import shutil
import yaml
from datetime import datetime as dt
import json
from pybboxes import BoundingBox
from PIL import Image

def main():
    input_path = os.path.join('input', 'random_p5')
    input_images = ''
    input_annotations = 'via_bouncy_random_p5_coco.json'
    dataset_name = f'bouncyhoops_random_p5'

    output_root_path = 'output'

    train_pct=0.5
    test_pct=0.25
    val_pct=0.25

    output_dataset_name = f'{dataset_name}_{dt.now().strftime("%Y%m%d_%H%M%S")}'    
    output_path = os.path.join(output_root_path, output_dataset_name)
    output_annotations = f'{output_dataset_name}.yaml'
    
    # Clean images referenced in the annotaion but not on filesystem
    with open(os.path.join(input_path, input_annotations), 'r+') as f:
        input_annotations_dict = json.load(f)
        if 'images' in input_annotations_dict:
            images_to_remove = []
            for image_ in input_annotations_dict['images']:
                if not os.path.exists(os.path.join(input_path, input_images, image_['file_name'])):
                    images_to_remove.append(image_)

            if len(images_to_remove)>0:
                input_annotations_dict['images'] = [x for x in input_annotations_dict['images'] if not x in images_to_remove]
                annotation_to_remove = []
                for annotation in input_annotations_dict['annotations']:
                    if annotation['image_id'] in [x['id'] for x in images_to_remove]:
                        annotation_to_remove.append(annotation)
                if len(annotation_to_remove)>0:
                    input_annotations_dict['annotations'] = [x for x in input_annotations_dict['annotations'] if not x in annotation_to_remove]
                f.seek(0)
                json.dump(input_annotations_dict, f)
                f.truncate() 

    # Reindexing eventually the class ids starting from 0
    with open(os.path.join(input_path, input_annotations), 'r+') as f:
        input_annotations_dict = json.load(f)
        if 'categories' in input_annotations_dict:
            min_num = min(input_annotations_dict['categories'], key=lambda x:x['id'])['id']
            if min_num > 0:
                for category in input_annotations_dict['categories']:                
                    category['id'] = category['id']-min_num
                if 'annotations' in input_annotations_dict:
                    for annotation in input_annotations_dict['annotations']:
                        if 'category_id' in annotation:
                            annotation['category_id'] = annotation['category_id']-min_num

                f.seek(0)
                json.dump(input_annotations_dict, f)
                f.truncate() 

    # Add W and H to the COCO annotations
    # VIA exporting fucke up with images HxW inside the exported json
    with open(os.path.join(input_path, input_annotations), 'r+') as f:
        input_annotations_dict = json.load(f)
        if 'annotations' in input_annotations_dict:
            # Check if the annotations are note already normalized for YOLO
            if len([elem for elem in sum([i['bbox'] for i in input_annotations_dict['annotations']], []) if elem > 1]) > 0:
                if 'images' in input_annotations_dict:
                    images_ = input_annotations_dict['images']
                    for image_ in images_:
                        im = Image.open(os.path.join(input_path, input_images, image_['file_name']))
                        image_['width'] = im.size[0]
                        image_['height'] = im .size[1]

                    f.seek(0)
                    json.dump(input_annotations_dict, f)
                    f.truncate() 

    #Import the dataset into the pylable schema 
    dataset = importer.ImportCoco(os.path.join(input_path, input_annotations), path_to_images=input_images)
    #print(dataset.df.head(5))

    print(f"Number of images: {dataset.analyze.num_images}")
    print(f"Number of classes: {dataset.analyze.num_classes}")
    print(f"Classes:{dataset.analyze.classes}")
    print(f"Class counts: {dataset.analyze.class_counts}")
    #print(f"Path to annotations: '{dataset.path_to_annotations}'")

    dataset.splitter.GroupShuffleSplit(train_pct=train_pct, test_pct=test_pct, val_pct=val_pct, random_state=35)
    dataset.export.ExportToYoloV5(output_path=os.path.join(output_path, 'labels'), yaml_file=output_annotations, copy_images=True, use_splits=True, segmentation=False, cat_id_index=0)

    for _, dirs, _ in os.walk(os.path.join(output_path, 'images')):
        for dir in dirs:
            if not os.path.exists(os.path.join(output_path, dir, 'images')):
                os.makedirs(os.path.join(output_path, dir, 'images'))
            if not os.path.exists(os.path.join(output_path, dir, 'labels')):
                os.makedirs(os.path.join(output_path, dir, 'labels'))

            image_files = os.listdir(os.path.join(output_path, 'images', dir))            
            for image_file in image_files:
                label_file = os.path.splitext(image_file)[0] + '.txt'
                label_path = os.path.join(output_path, 'labels', dir)
                image_path = os.path.join(output_path, 'images', dir)
                image_file_full = os.path.join(image_path, image_file)
                label_file_full = os.path.join(label_path, label_file)
                os.rename(image_file_full, os.path.join(output_path, dir, 'images', image_file))
                os.rename(label_file_full, os.path.join(output_path, dir, 'labels', label_file))
    
    try:
        shutil.rmtree(os.path.join(output_path, 'images'))
    except:
        pass
    try:
        shutil.rmtree(os.path.join(output_path, 'labels'))
    except:
        pass

    with open(os.path.join(output_path, output_annotations), 'r+') as f:
        output_annotations_yaml = yaml.safe_load(f)

        if 'path' in output_annotations_yaml:
            output_annotations_yaml.pop('path')
        if 'train' in output_annotations_yaml:
            output_annotations_yaml['train'] = os.path.join('.', 'data', output_dataset_name, 'train', 'images')
        if 'val' in output_annotations_yaml:
            output_annotations_yaml['val'] = os.path.join('.', 'data', output_dataset_name, 'val', 'images')
        if 'test' in output_annotations_yaml:
            output_annotations_yaml['test'] = os.path.join('.', 'data', output_dataset_name, 'test', 'images')

        f.seek(0)
        yaml.dump(output_annotations_yaml, f)
        f.truncate() 

    os.rename(os.path.join(output_path, output_annotations), os.path.join(output_root_path, output_annotations))

    print(f'Completed')

if __name__ == "__main__":
    main()