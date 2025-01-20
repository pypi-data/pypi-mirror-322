from pathlib import Path
from typing import Dict
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
    
    def iterate_labels(self):
        """Iterate through label files and yield (path, labels) pairs.
        
        Yields:
            tuple: (Path, List[List[str]])
                - Path: Path object pointing to the label file
                - List[List[str]]: List of labels, where each label is a list of strings
                  First element is class id, followed by bbox coordinates
                  May be empty if label file contains no data
        """
        label_files = (p for p in Path(self.labels_path).rglob('*.txt') 
                      if p.name != 'classes.txt')
        
        for label_p in label_files:
            with label_p.open('r') as f:
                labels = [line.strip().split() for line in f if line.strip()]
            yield label_p, labels
    def __len__(self):
        return len([i for i in Path(self.labels_path).glob('*.txt') if i.name not in ('classes.txt',)])
    




if __name__ == "__main__":
    pass
