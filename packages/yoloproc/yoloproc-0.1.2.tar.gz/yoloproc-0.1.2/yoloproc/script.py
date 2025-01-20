from pathlib import Path
import shutil
from typing import Optional,Union, Dict, Callable
from tqdm import tqdm  # 添加tqdm导入

def merge_yolo_data(root_path:Union[str,Path], output_path:Union[str,Path], is_move:Optional[str]=False):
    """
    该函数用于整理YOLO数据集,将分散在不同子目录下的图片和标注文件
    统一收集到指定目录的images和labels文件夹中。

    Args:
        root_path (Union[str, Path]): 源数据根目录路径，将递归搜索该目录下的所有文件
        output_path (Union[str, Path]): 输出目录路径,将在该目录下创建images和labels子目录
        is_move (Optional[str], optional): 是否移动文件而不是复制。默认为False
            当设置为True时,将移动文件到目标目录
            当设置为False时,将复制文件到目标目录

    Note:
        - 函数会递归遍历root_path下的所有jpg和txt文件
        - 图片文件(.jpg)将被放置在output_path/images目录下
        - 标注文件(.txt)将被放置在output_path/labels目录下
        - 如果目标目录不存在，将自动创建

    Example:
        >>> merge_yolo_data('/path/to/dataset', '/path/to/output')  # 复制文件
        >>> merge_yolo_data('/path/to/dataset', '/path/to/output', is_move=True)  # 移动文件
    """
    # 创建输出路径对象
    gen_p = Path(output_path)
    root_im_p = gen_p / 'images'
    root_l_p = gen_p / 'labels'
    root_im_p.mkdir(exist_ok=True,parents=True)
    root_l_p.mkdir(exist_ok=True)

    
    # 收集所有文件并显示进度
    image_files = list(Path(root_path).rglob('*.jpg'))
    label_files = list(Path(root_path).rglob('*.txt'))
    
    for im_p in tqdm(image_files, desc="Processing images"):
        try:
            if is_move:
                shutil.move(im_p,root_im_p)
            else:
                shutil.copy(im_p,root_im_p)    
        except Exception as e:
            print(f"Error moving image file {im_p}: {e}")
            
    for l_p in tqdm(label_files, desc="Processing labels"):
        try:
            if is_move:
                shutil.move(l_p,root_l_p)
            else:
                shutil.copy(l_p,root_l_p)
        except Exception as e:
            print(f"Error moving label file {l_p}: {e}")

def remove_irrelevant_data(root_path:Union[str,Path],tmp_path:Union[None,str,Path]=None,remove_type:str='*.txt'):
    """
    该函数用于清理数据集中不配对的文件。例如，当处理图像标注数据时，
    可以删除没有对应txt标注文件的jpg图片,或删除没有对应jpg图片的txt标注文件。

    Args:
        root_path (Union[str, Path]): 需要处理的根目录路径
        tmp_path (Union[None, str, Path], optional): 临时文件存储路径。
            如果为None,将在root_path的父目录下创建名为'tmp'的临时目录。默认为None
        remve_type (str, optional): 要删除的文件类型。默认为'*.txt'
            当设置为'*.txt'时会检查对应的jpg文件是否存在
            当设置为'*.jpg'时会检查对应的txt文件是否存在

    Note:
        - 函数会递归遍历root_path下的所有文件
        - 如果文件没有对应的配对文件(例如:没有对应的jpg或txt),该文件将被移动到临时目录
        - 支持的文件类型对为:jpg和txt
        - 文件配对是基于文件名（不含扩展名）进行的

    Example:
        >>> remove_irrelevant_data('/path/to/dataset')  # 移除没有对应jpg的txt文件
        >>> remove_irrelevant_data('/path/to/dataset', remve_type='*.jpg')  # 移除没有对应txt的jpg文件
    """
    if tmp_path is None:
        tmp_path = Path(root_path).parent / 'tmp'
        tmp_path.mkdir(exist_ok=True)

    suffix = '*.jpg' if remove_type == '*.txt'  else '*.txt'
    exist_set = set()
    
    suffix_files = list(Path(root_path).rglob(suffix))
    for t_p in tqdm(suffix_files, desc=f"Collecting {suffix} files"):
        exist_set.add(t_p.stem)
    
    remove_files = list(Path(root_path).rglob(remove_type))
    for t_p in tqdm(remove_files, desc=f"Processing {remove_type} files"):
        if t_p.stem not in exist_set:
            shutil.move(t_p,tmp_path)
    print('remove irrelevant data done!')

def remove_files_by_stem(stem_dir: Union[str, Path], target_dir: Union[str, Path], 
                        tmp_path: Optional[Union[str, Path]] = None):
    """
    根据stem_dir目录下的文件名(stem),移除target_dir目录下所有同名文件到临时目录。

    Args:
        stem_dir (Union[str, Path]): 用于获取文件stem的参考目录
        target_dir (Union[str, Path]): 需要处理的目标目录
        tmp_path (Optional[Union[str, Path]], optional): 临时文件存储路径。
            如果为None，将在target_dir的父目录下创建名为'tmp'的临时目录。默认为None

    Note:
        - 函数会递归遍历stem_dir下的所有文件获取stem集合
        - 然后遍历target_dir下的所有文件,如果文件的stem在集合中,就移动到临时目录
        - 支持所有类型的文件

    Example:
        >>> remove_files_by_stem('/path/to/stem_dir', '/path/to/target_dir')
    """
    # 设置临时目录
    if tmp_path is None:
        tmp_path = Path(target_dir).parent / 'tmp'
        tmp_path.mkdir(exist_ok=True)
    else:
        tmp_path = Path(tmp_path)
        tmp_path.mkdir(exist_ok=True)

    # 获取stem集合，添加进度条
    stem_files = [p for p in Path(stem_dir).rglob('*') if p.is_file()]
    stem_set = set()
    for p in tqdm(stem_files, desc="Collecting file stems"):
        stem_set.add(p.stem)
    
    # 移动匹配的文件，添加进度条
    target_files = [p for p in Path(target_dir).rglob('*') if p.is_file()]
    for file_path in tqdm(target_files, desc="Processing target files"):
        if file_path.stem in stem_set:
            try:
                shutil.move(str(file_path), str(tmp_path))
            except Exception as e:
                print(f"Error moving file {file_path}: {e}")
    
    print('Remove files by stem completed!')

def extract_ordered_frames(
    image_dir: Union[str, Path],
    output_dir: Union[str, Path],
    frame_interval: int = 10,
    label_dir: Optional[Union[str, Path]] = None,
    sort_key: Optional[Callable[[Path]]] = None
) -> Dict[str, int]:
    """
    从排序后的图片序列中抽取帧，并处理相应的标注文件。

    Args:
        image_dir (Union[str, Path]): 图片文件所在目录
        output_dir (Union[str, Path]): 输出目录，将在该目录下创建images和labels子目录
        frame_interval (int, optional): 抽帧间隔，默认每30张抽取1张
        label_dir (Optional[Union[str, Path]], optional): 标注文件目录，如果有的话
        sort_key (Optional[Callable[[Path], Any]], optional): 自定义排序函数，
            接收Path对象作为参数，返回排序依据。默认按文件名排序

    Returns:
        Dict[str, int]: 包含处理统计信息的字典，包括总图片数和保存的帧数

    Raises:
        ValueError: 当frame_interval小于1时抛出
        FileNotFoundError: 当输入目录不存在时抛出
    """
    # 参数验证
    if frame_interval < 1:
        raise ValueError("Frame interval must be greater than 0")
    
    image_dir = Path(image_dir)
    output_dir = Path(output_dir)
    
    if not image_dir.exists():
        raise FileNotFoundError(f"Image directory not found: {image_dir}")
    
    if label_dir and not Path(label_dir).exists():
        raise FileNotFoundError(f"Label directory not found: {label_dir}")

    # 创建输出目录结构
    output_structure = {
        'images': output_dir / 'images',
        'labels': output_dir / 'labels'
    }
    
    for dir_path in output_structure.values():
        dir_path.mkdir(parents=True, exist_ok=True)

    # 定义支持的图片格式
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp'}
    
    # 收集和排序图片
    image_paths = [
        p for p in image_dir.rglob('*')
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    ]
    
    if not image_paths:
        print(f"No images found in {image_dir}")
        return {'total_images': 0, 'saved_frames': 0}

    image_paths.sort(key=sort_key if sort_key else None)
    
    # 处理图片和标注，添加进度条
    stats = {'total_images': len(image_paths), 'saved_frames': 0}
    
    for idx, img_path in tqdm(enumerate(image_paths), total=len(image_paths), desc="Extracting frames"):
        if idx % frame_interval == 0:
            try:
                # 生成新的文件名
                new_name = f"frame_{stats['saved_frames']:06d}{img_path.suffix}"
                
                # 复制图片
                shutil.copy(
                    img_path, 
                    output_structure['images'] / new_name
                )
                
                # 处理对应的标注文件
                if label_dir:
                    label_path = Path(label_dir) / f"{img_path.stem}.txt"
                    if label_path.exists():
                        shutil.copy(
                            label_path,
                            output_structure['labels'] / f"frame_{stats['saved_frames']:06d}.txt"
                        )
                
                stats['saved_frames'] += 1
                
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
                continue

    print(f"Processed {stats['total_images']} images: extracted {stats['saved_frames']} frames")
    return stats

def generate_empty_annotations(image_dir: Union[str, Path], label_dir: Union[str, Path]):
    """
    根据图片的 stem 名称生成空的标注文件。

    Args:
        image_dir (Union[str, Path]): 图片文件所在目录
        label_dir (Union[str, Path]): 标注文件存储目录

    Note:
        - 函数会递归遍历 image_dir 下的所有图片文件
        - 对于每个图片文件，在 label_dir 中创建相应的空标注文件（.txt）
        - 如果标注文件已存在，则不会重复创建

    Example:
        >>> generate_empty_annotations('/path/to/images', '/path/to/labels')
    """
    image_dir = Path(image_dir)
    label_dir = Path(label_dir)
    label_dir.mkdir(parents=True, exist_ok=True)

    # 定义支持的图片格式
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp'}

    # 收集所有图片文件
    image_paths = [
        p for p in image_dir.rglob('*')
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    ]

    # 生成空的标注文件，添加进度条
    for img_path in tqdm(image_paths, desc="Generating empty annotation files"):
        label_path = label_dir / f"{img_path.stem}.txt"
        if not label_path.exists():
            label_path.touch()


def labels_count_info(labels_path: str, class_path: str = None):
    """
    统计指定路径下的标签文件中每个类别的实例数量，并打印结果。

    参数：
        labels_path (str): 标签文件所在的目录路径。
        class_path (str, 可选): 类别文件 `classes.txt` 的路径。如果未指定，将使用 `labels_path` 下的 `classes.txt`。

    功能：
    - 解析 `classes.txt` 文件，获取类别映射字典。
    - 遍历所有标签文件，统计每个类别的实例数量。
    - 按顺序打印每个类别的实例数量及其名称。

    示例：
    ```python
    labels_count_info('/path/to/labels', '/path/to/classes.txt')
    ```
    """
    from .label_info import LabelInfo
    from collections import defaultdict
    label_info = LabelInfo(labels_path, class_path)
    classes = label_info.parse_classes()
    if classes is None:
        class_count = defaultdict(int)
    else:
        class_count = {i: 0 for i in classes.keys()}
    
    for _, labels in label_info.iterate_labels():
        for label in labels:
            class_id = int(label[0])
            class_count[class_id] += 1

    print("每个类别的实例数量:")
    for class_id, count in sorted(class_count.items()):
        class_name = classes[class_id] if classes else class_id
        print(f"类别 {class_id} ({class_name}): {count}")
