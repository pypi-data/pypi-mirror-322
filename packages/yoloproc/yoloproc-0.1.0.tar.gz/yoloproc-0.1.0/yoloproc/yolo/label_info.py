from pathlib import Path
from typing import List, Dict, Union
from collections import defaultdict

class LabelInfo():

    def __init__(self,labels_path:str,class_path:str=None) -> None:
        self.class_map = None
        self.labels_path = labels_path
        self.class_path = class_path
        if class_path is None:
            self.class_path = Path(labels_path) / 'classes.txt'

    def parse_classes(self) -> Dict[int,str]:
        class_p = Path(self.class_path)
        if class_p.is_file():
            with class_p.open('r') as f:
                self.class_map = {i:cla.strip() for i,cla in enumerate(f.readlines())}
            return self.class_map
        return None
    
    def gen_label(self):
        """
            label_p:Path,labels:list[list]
            如果label为空,返回数据可能为空,需要做进一步判断
        """
        for label_path in Path(self.labels_path).rglob('*.txt'):
            if label_path.name in ('classes.txt',):
                continue
            with Path(label_path).open('r') as f:
                label = [i.strip().split() for i in f.readlines()]
            yield label_path,label
            
    def __len__(self):
        return len([i for i in Path(self.labels_path).glob('*.txt') if i.name not in ('classes.txt',)])
    

def labels_info(labels_path:str,class_path:str=None):
    label_info = LabelInfo(labels_path,class_path)
    classes = label_info.parse_classes()
    if classes is None:
        class_count = defaultdict(int) 
    else:
        class_count = {i: 0 for i in classes.keys()}
    
    for _, labels in label_info.gen_label():
        for label in labels:
            class_id = int(label[0])
            class_count[class_id] += 1

    print("Number of instances for each class:")
    for class_id, count in sorted(class_count.items()):
            class_name = classes[class_id] if classes else class_id
            print(f"Class {class_id} ({class_name}): {count}")


if __name__ == "__main__":
    labels_path = '/data/police_gesture_seqs/output_pooling/train_split_0115_frame2/train_split_frame/labels'
    labels_info(labels_path)
