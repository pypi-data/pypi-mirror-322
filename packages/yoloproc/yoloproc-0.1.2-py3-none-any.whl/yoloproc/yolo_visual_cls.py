from pathlib import Path
from shutil import copy,move
from typing import Dict, List, Optional
from rich.progress import track
from concurrent.futures import ThreadPoolExecutor

class LabelOrganizer:
    """Organizes YOLO dataset labels and images into class-specific directories."""
    
    def __init__(self, dataset_root: str, class_file: Optional[str] = None) -> None:
        """
        Initialize the LabelOrganizer.
        
        Args:
            dataset_root: Root directory of the dataset
            class_file: Path to the class mapping file (optional)
        """
        self.dataset_root = Path(dataset_root)
        self.output_root = self.dataset_root.parent / f'{self.dataset_root.stem}_split'
        self.labels_dir = self.dataset_root / 'labels'
        self.images_dir = self.dataset_root / 'images'
        self.class_file = Path(class_file) if class_file else self.labels_dir / 'classes.txt'

        # Create output directories

        self.class_map = self.load_class_mapping()

    def load_class_mapping(self) -> Dict[int, str]:
        """Load class ID to class name mapping from the class file."""
        with self.class_file.open('r') as f:
            return {i: line.strip() for i, line in enumerate(f)}

    def _read_label_file(self, label_path: Path) -> List[List[str]]:
        """Read and parse a YOLO label file."""
        with label_path.open('r') as f:
            return [line.strip().split() for line in f if line.strip()]

    def _organize_label_and_image(self, label_path: Path, labels: List[List[str]],is_move:bool=False,filter_class_id:Optional[List]=None) -> None:
        """
        Organize a single label file and its corresponding image into class-specific directories.
        
        Args:
            label_path: Path to the label file
            labels: List of parsed label lines
        """
        if not labels:
            class_name = 'no_label'
        else:
            class_id = int(labels[0][0])
            class_name = self.class_map.get(class_id)
        if not class_name:
            print(f"Warning: Unknown class ID {class_id} in file {label_path}")
            return

        # Create class-specific directories
        output_dirs = {
            'labels': self.output_root / class_name / 'labels' ,
            'images': self.output_root  / class_name / 'images'
        }
        for dir_path in output_dirs.values():
            dir_path.mkdir(exist_ok=True,parents=True)

        # Write labels
        if is_move:
            move(label_path, output_dirs['labels'] / label_path.name)
        else:
            copy(label_path, output_dirs['labels'] / label_path.name)

        # Copy classes.txt to the labels directory
        classes_txt_path = output_dirs['labels'] / 'classes.txt'
        if not classes_txt_path.exists():
            if is_move:
                move(self.class_file, classes_txt_path)
            else:   
                copy(self.class_file, classes_txt_path)

        # Copy image if it exists
        image_path = self.images_dir / f"{label_path.stem}.jpg"
        if image_path.exists():
            if is_move:
                move(image_path, output_dirs['images'] / image_path.name)
            else:
                copy(image_path, output_dirs['images'] / image_path.name)

    def organize_labels(self, is_move: bool = False, batch_size: int = 1000) -> None:
        """Organize all label files and their corresponding images using multi-threading."""
        label_files = [f for f in self.labels_dir.glob('*.txt') if f.name != 'classes.txt']
        
        # 预先创建所有可能的输出目录
        class_dirs = {class_name: {
            'labels': self.output_root / class_name / 'labels',
            'images': self.output_root / class_name / 'images'
        } for class_name in self.class_map.values()}
        class_dirs['no_label'] = {
            'labels': self.output_root / 'no_label' / 'labels',
            'images': self.output_root / 'no_label' / 'images'
        }
        
        # 批量创建目录并复制 classes.txt
        for dirs in class_dirs.values():
            for dir_path in dirs.values():
                dir_path.mkdir(parents=True, exist_ok=True)
            # 为每个类别目录复制 classes.txt
            classes_txt_dest = dirs['labels'] / 'classes.txt'
            if not classes_txt_dest.exists():
                copy(self.class_file, classes_txt_dest)

        def process_batch(batch_files: List[Path]) -> List[tuple]:
            moves = []
            for label_path in batch_files:
                try:
                    with label_path.open('r') as f:
                        labels = [line.strip().split() for line in f if line.strip()]
                    
                    if not labels:
                        class_name = 'no_label'
                    else:
                        class_id = int(labels[0][0])
                        class_name = self.class_map.get(class_id)
                        if not class_name:
                            print(f"Warning: Unknown class ID {class_id} in file {label_path}")
                            continue
                    
                    output_dirs = class_dirs[class_name]
                    
                    # 只添加标签文件移动任务
                    moves.append((label_path, output_dirs['labels'] / label_path.name))
                    
                    # 添加图像文件移动任务（如果存在）
                    image_path = self.images_dir / f"{label_path.stem}.jpg"
                    if image_path.exists():
                        moves.append((image_path, output_dirs['images'] / image_path.name))
                except Exception as e:
                    print(f"Error processing {label_path}: {str(e)}")
            return moves

        # 计算最优线程数
        max_workers = 32
        print(f"Using {max_workers} workers")

        # 批量处理文件
        batches = [label_files[i:i + batch_size] for i in range(0, len(label_files), batch_size)]
        all_moves = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            batch_results = list(track(
                executor.map(process_batch, batches),
                description="[green]Calculating moves",
                total=len(batches)
            ))
            all_moves = [move for batch in batch_results for move in batch]

        # 执行文件操作
        def execute_moves(moves: List[tuple]) -> None:
            for src, dest in moves:
                try:
                    if not dest.exists():  # 避免重复复制
                        if is_move:
                            move(src, dest)
                        else:
                            copy(src, dest)
                except Exception as e:
                    print(f"Error moving {src} to {dest}: {str(e)}")

        # 批量执行文件操作
        move_batches = [all_moves[i:i + batch_size] for i in range(0, len(all_moves), batch_size)]
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            list(track(
                executor.map(execute_moves, move_batches),
                description="[green]Moving files",
                total=len(move_batches)
            ))

    def get_label_count(self) -> int:
        """Return the total number of label files (excluding classes.txt)."""
        return len(list(self.labels_dir.glob('*.txt'))) - 1

if __name__ == "__main__":
    organizer = LabelOrganizer('/data/police_gesture_seqs/train_police1231_4nc/train_merge')
    print(f"Class mapping: {organizer.class_map}")
    organizer.organize_labels(is_move=True)