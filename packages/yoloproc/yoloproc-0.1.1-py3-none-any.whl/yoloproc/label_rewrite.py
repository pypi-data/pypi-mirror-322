from .label_info import LabelInfo
from typing import Dict,Union
from pathlib import Path
from tqdm import tqdm
import argparse

def unify_filter(class_filter_str:Dict[str,int],class_txt:Dict[int,str])->Dict[int,int]:
    """
        将以中文输入的筛选索引转为具体的class_index
    """
    class_filter_int = {}
    class_swap = {v:k for k,v in class_txt.items()}
    for k,v in class_filter_str.items():
        class_filter_int[class_swap[k]]=v
    return class_filter_int


def gen_classes(class_txt:Dict,class_filter:Dict,gen_cls:str):
    """
        生成新的classes.txt文件
    """
    cls_v = sorted(class_filter.items(),key=lambda x:x[1])  #以value排序
    f = open(gen_cls,'w') 
    for i,(key,val) in enumerate(cls_v):
        if i!=val:
            print("索引和val不相同")
            f.write(f'{class_txt[key]}:{val}\n')
        else:
            f.write(class_txt[key]+'\n')
    f.close()


def rewrite_yolo_labels(
        labels_path: str, 
        class_filter: Union[Dict[str,int], Dict[int,int]],
        output_dir: str = 'labels2',
        remove_empty: bool = False,
        custom_output_path: str = None) -> None:
    """
    Rewrite YOLO labels with new class mappings
    
    Args:
        labels_path: Path to the original labels directory
        class_filter: Dictionary mapping old class indices to new ones
        output_dir: Name of the output labels directory
        remove_empty: Whether to remove empty label files
        custom_output_path: Custom output path (if None, uses parent of labels_path)
    """
    gen_p = Path(labels_path).parent / output_dir if custom_output_path is None else Path(custom_output_path)
    gen_p.mkdir(exist_ok=True) 

    label_info = LabelInfo(labels_path)
    class_txt = label_info.parse_classes()
    if class_txt is None:
        raise ValueError("class_txt is None")
    if isinstance(list(class_filter.keys())[0], str):
        class_filter = unify_filter(class_filter, class_txt)
        
    for l_p, label in tqdm(label_info.iterate_labels(), total=len(label_info)):
        n_p = gen_p / l_p.name
        label_str = ''
        for row in label:
            if int(row[0]) in class_filter.keys():
                row[0] = str(class_filter[int(row[0])])
                label_str += ' '.join(row) + '\n'
        if len(label_str) or not remove_empty:
            with open(str(n_p), 'w') as f:
                f.write(label_str)
                
    gen_classes(class_txt, class_filter, gen_p / 'classes.txt')


def filter_parse(x: str) -> Dict:
    """
    Parse class filter from JSON string or file
    
    Args:
        x: JSON string or path to JSON file
        
    Returns:
        Dictionary containing class mappings
    """
    import json
    if Path(x).is_file():
        with open(x) as f:
            x = json.load(f)
        return x 
    else:
        return json.loads(x)

# Only include command line interface when run as script
if __name__ == "__main__":
    def arg_parse():
        parser = argparse.ArgumentParser(description='Rewrite YOLO labels with new class mappings')
        parser.add_argument('--labels_path', type=str, required=True,
                          help='Path to the original labels directory')
        parser.add_argument('--class_filter', type=filter_parse, required=True,
                          help='JSON string or path to JSON file with class mappings')
        parser.add_argument('--output_dir', type=str, default='labels2',
                          help='Name of the output labels directory')
        parser.add_argument('--remove_empty', action='store_true',
                          help='Remove empty label files')
        args = parser.parse_args()  
        return args
    
    opt = arg_parse()
    rewrite_yolo_labels(
        opt.labels_path, 
        opt.class_filter, 
        opt.output_dir, 
        remove_empty=opt.remove_empty
    )
