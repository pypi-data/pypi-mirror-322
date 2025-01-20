from label_info import LabelInfo
from typing import List,Union,Tuple
import numpy as np
import cv2
from pathlib import Path
from tqdm import tqdm
import argparse

class LabelPaint():
    """
    A class for visualizing labeled images with bounding boxes.
    
    Args:
        labels_path (str): Path to the labels directory or file
        class_path (str, optional): Path to the class names file
    """
    def __init__(self, labels_path: str, class_path: Union[str, None] = None,backend='yolo') -> None:
        self.label_info = LabelInfo(labels_path, class_path=class_path)
        names = self.label_info.parse_classes() 
        if names is None:
            raise ValueError(f"No class names found in {class_path}")
        if backend == 'yolo':
            self.paint = PaintProc(names)
        elif backend == 'mpl':
            self.paint = MPLPaintProc(names)

    def _xywh2xyxy(self, x: np.ndarray, shape: Tuple[int, int]) -> np.ndarray:
        y = np.copy(x)
        y[..., 0] = x[..., 0] - x[..., 2] / 2 
        y[..., 1] = x[..., 1] - x[..., 3] / 2 
        y[..., 2] = x[..., 0] + x[..., 2] / 2 
        y[..., 3] = x[..., 1] + x[..., 3] / 2 
        return y*[shape[1], shape[0], shape[1], shape[0]]

    def visual(self, images_path: Union[str, Path], visuals_path: Union[str, Path, None] = None, interval: int = 1) -> None:
        Path(visuals_path).mkdir(exist_ok=True)
        len_ls = len(self.label_info)
        pbar = tqdm(self.label_info.gen_label(), total=len_ls)
        pbar.set_description(f"Processing {len_ls} images, visualizing {len_ls//interval} images")
        
        for i,(label_path,label) in enumerate(pbar):
            try:
                if i%interval!=0:
                    continue
                image_p = Path(images_path) / Path(label_path).with_suffix('.jpg').name
                visual_p = Path(visuals_path) / image_p.name
                if visual_p.exists():
                    continue
                im = cv2.imread(str(image_p))
                im_shape = im.shape[:2]
                label = np.array(label,dtype=float)
                if len(label):  # 如果标注信息为空
                    bbox = self._xywh2xyxy(label[...,1:],im_shape)
                    det = np.concatenate((bbox,np.expand_dims(label[:,0], axis=-1)),axis=-1)
                    im=self.paint(im,det)
                cv2.imwrite(str(visual_p),im)
            except:
                print(f"{image_p} is not a image file")
class PaintProc():
    """
    A class for drawing bounding boxes on single images.

    Args:
        names (Union[List, str]): List of class names or path to class names file
    """
    def __init__(self, names: Union[List[str], str]) -> None:
        if isinstance(names,str) and names.endswith('txt'):
            with open(names,'r',encoding='utf-8') as f:
                names = f.readlines()
        self.names = names

    def proc(self, im: np.ndarray, det: np.ndarray) -> np.ndarray:
        from ultralytics.utils.plotting import Annotator,colors
        annotator = Annotator(im,line_width=3)
        for *xyxy,label in det:
            label = int(label)
            bbox_tag = f'{self.names[label]}'
            annotator.box_label(xyxy,bbox_tag,color=colors(label,True))
        im0 = annotator.result()
        return im0
    

    __call__ = proc

class MPLPaintProc():
    """
    A class for drawing bounding boxes on single images using matplotlib colormaps.
    
    Args:
        names (Union[List, str]): List of class names or path to class names file
        cmap_name (str): Name of matplotlib colormap (default: 'rainbow')
                        Try: 'viridis', 'plasma', 'inferno', 'magma', 'cividis',
                             'rainbow', 'hsv', 'tab20', 'Set3', etc.
    """
    def __init__(self, names: Union[List[str], str], cmap_name: str = 'rainbow') -> None:
        if isinstance(names, str) and names.endswith('txt'):
            with open(names, 'r', encoding='utf-8') as f:
                names = [line.strip() for line in f.readlines()]
        self.names = names
        
        import matplotlib.pyplot as plt
        # 获取色盘并生成颜色列表
        cmap = plt.get_cmap(cmap_name)
        self.colors = [
            tuple(int(255 * c) for c in cmap(i / (len(names) ))[:3][::-1])  # RGB->BGR
            for i in range(len(names))
        ]
    
    def proc(self, im: np.ndarray, det: np.ndarray) -> np.ndarray:
        im0 = im.copy()
        for *xyxy, label in det:
            label = int(label)
            color = self.colors[label]
            x1, y1, x2, y2 = map(int, xyxy)
            
            # 绘制边界框
            cv2.rectangle(im0, (x1, y1), (x2, y2), color, 2)
            
            # 添加标签
            text = self.names[label]
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            thickness = 2
            
            # 获取文本大小
            (text_width, text_height), baseline = cv2.getTextSize(
                text, font, font_scale, thickness)
            
            # 绘制标签背景
            cv2.rectangle(im0, 
                         (x1, y1 - text_height - baseline - 5),
                         (x1 + text_width, y1),
                         color, -1)
            
            # 绘制文本
            cv2.putText(im0, text,
                       (x1, y1 - baseline - 2),
                       font, font_scale, (255, 255, 255),
                       thickness)
        
        return im0

    __call__ = proc

def arg_parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='图片可视化')
    parser.add_argument('--labels_path',type=str,required=True)
    parser.add_argument('--images_path',type=str,required=False)
    parser.add_argument('--visuals_path',type=str,required=False)
    parser.add_argument('--class_path',type=str,required=False)
    parser.add_argument('--interval',type=int,required=False,default=1)
    args = parser.parse_args()  
    if args.visuals_path is None:
        args.visuals_path = Path(args.labels_path).parent / 'visuals'
    if args.images_path is None:
        args.images_path = Path(args.labels_path).parent / 'images'

    return args

def create_visualizer(
    labels_path: Union[str, Path],
    images_path: Union[str, Path, None] = None,
    visuals_path: Union[str, Path, None] = None,
    class_path: Union[str, Path, None] = None,
    interval: int = 1,
    backend: str = 'yolo'
) -> None:
    """
    Convenience function to create and run the visualizer.

    Args:
        labels_path (str): Path to the labels directory
        images_path (str, optional): Path to the images directory
        visuals_path (str, optional): Path to save visualized images
        class_path (str, optional): Path to the class names file
        interval (int, optional): Process every nth image. Defaults to 1
        backend (str, optional):  Backend for drawing bounding boxes (yolo,mpl). Defaults to 'yolo'
    """
    if images_path is None:
        images_path = Path(labels_path).parent / 'images'
    if visuals_path is None:
        visuals_path = Path(labels_path).parent / 'visuals'

    lp = LabelPaint(labels_path, class_path,backend)
    lp.visual(images_path, visuals_path, interval=interval)

# Optional CLI support
def main():
    args = arg_parse()
    create_visualizer(
        args.labels_path,
        args.images_path,
        args.visuals_path,
        args.class_path,
        args.interval
    )

if __name__ == "__main__":
    # main()
    labels_path = '/home/seekychan/Desktop/project/yoloProcess/yoloproc/test/crop/labels'
    images_path = '/home/seekychan/Desktop/project/yoloProcess/yoloproc/test/crop/images'
    visuals_path = '/home/seekychan/Desktop/project/yoloProcess/yoloproc/test/crop/visuals'
    create_visualizer(labels_path,images_path,visuals_path,backend='mpl')