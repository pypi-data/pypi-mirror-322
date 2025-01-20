from pathlib import Path
import numpy as np
import cv2
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor,as_completed
# 可以优化：将xyxy超过了crop区域的目标滤掉，仍保存该txt

class ImageProcessStrategy:
    def resize(self, image):
        raise NotImplementedError
    
    def transform_label(self, labels: np.ndarray, crop_origin_xyxy: tuple):
        raise NotImplementedError
        
    def crop(self, image, crop_origin_xyxy: tuple):
        return image[crop_origin_xyxy[1]:crop_origin_xyxy[3], 
                    crop_origin_xyxy[0]:crop_origin_xyxy[2]]
    def filter_valid(self,xyxy:np.ndarray,crop_origin_xyxy):   
        w,h = crop_origin_xyxy[2] - crop_origin_xyxy[0], crop_origin_xyxy[3] - crop_origin_xyxy[1]
        novalid_num = xyxy[(xyxy[:, 0] <=0)|(xyxy[:, 1] <= 0)|(xyxy[:, 2] >= w) | (xyxy[:, 3] >= h)].shape[0]
        return novalid_num

class Process2160x3840Strategy(ImageProcessStrategy):
    def resize(self, image):
        return cv2.resize(image, (1920, 1080), interpolation=cv2.INTER_NEAREST)
    
    def transform_label(self, labels: np.ndarray, crop_origin_xyxy: tuple):
        return Process1080x1920Strategy().transform_label(labels, crop_origin_xyxy)

class Process1080x1920Strategy(ImageProcessStrategy):
    def resize(self, image):
        return image
    
    def transform_label(self, labels: np.ndarray, crop_origin_xyxy: tuple):
        if labels.shape[0] == 0:
            return None,0
        xywh = labels[:, 1:5].astype(float)
        xywh[:, [0, 2]] *= 1920
        xywh[:, [1, 3]] *= 1080
        xyxy = np.concatenate([xywh[:, :2] - xywh[:, 2:4] / 2, xywh[:, :2] + xywh[:, 2:4] / 2], axis=1)
        xyxy[:, [0, 2]] -= crop_origin_xyxy[0]
        xyxy[:, [1, 3]] -= crop_origin_xyxy[1]
        novalid_num = self.filter_valid(xyxy,crop_origin_xyxy)
        if xyxy.shape[0] == 0:
            return None,novalid_num
        xyxyn = np.zeros_like(xyxy)
        xyxyn[:, [0, 2]] = xyxy[:, [0, 2]] / 960
        xyxyn[:, [1, 3]] = xyxy[:, [1, 3]] / 512
        xywhn = np.concatenate([(xyxyn[:, :2] + xyxyn[:, 2:4]) / 2, xyxyn[:, 2:4] - xyxyn[:, :2]], axis=1)
        labels[:, 1:5] = xywhn
        return labels,novalid_num

class Process1876x2896Strategy(ImageProcessStrategy):
    def resize(self, image):
        image = image[0:1629, 0:2896, :]
        return cv2.resize(image, (1920, 1080), interpolation=cv2.INTER_NEAREST)
    
    def transform_label(self, labels: np.ndarray, crop_origin_xyxy: tuple):
        if labels.shape[0] == 0:
            return None,0
        ratio = 1080/1629 
        ratio_w = 2896* ratio 
        ratio_h = 1876 * ratio 
        xywh = labels[:, 1:5].astype(float)
        xyxy = np.concatenate([xywh[:, :2] - xywh[:, 2:4] / 2, xywh[:, :2] + xywh[:, 2:4] / 2], axis=1)
        xyxy[:, [0, 2]] *= ratio_w
        xyxy[:, [1, 3]] *= ratio_h
        xyxy[:, [0, 2]] -= crop_origin_xyxy[0]
        xyxy[:, [1, 3]] -= crop_origin_xyxy[1]
        novalid_num = self.filter_valid(xyxy,crop_origin_xyxy)
        if xyxy.shape[0] == 0:
            return None,novalid_num
        xyxyn = np.zeros_like(xyxy)
        xyxyn[:, [0, 2]] = xyxy[:, [0, 2]] / 960
        xyxyn[:, [1, 3]] = xyxy[:, [1, 3]] / 512
        xywhn = np.concatenate([(xyxyn[:, :2] + xyxyn[:, 2:4]) / 2, xyxyn[:, 2:4] - xyxyn[:, :2]], axis=1)
        labels[:, 1:5] = xywhn
        return labels,novalid_num

class DatasetCropGestures:
    def __init__(self, dataset_path: str,output_path: str, crop_origin_xyxy: tuple):
        self.dataset_p = Path(dataset_path)
        self.output_img_p = Path(output_path) / 'images'
        self.output_label_p = Path(output_path) / 'labels'
        self.output_img_p.mkdir(parents=True,exist_ok=True)
        self.output_label_p.mkdir(parents=True,exist_ok=True)
        self.crop_origin_xyxy = crop_origin_xyxy
        self.image_size = (1920, 1080)
        
        self.process_strategies = {
            (2160, 3840): Process2160x3840Strategy(),
            (1080, 1920): Process1080x1920Strategy(),
            (1876, 2896): Process1876x2896Strategy(),
        }

    def _crop_image(self, image_path: str, img_size: tuple):
        w, h = img_size
        image = cv2.imread(image_path)
        
        strategy = self.process_strategies.get((h, w))
        if not strategy:
            raise KeyError(f"Image size {h}x{w} is not supported")
        image = strategy.resize(image)
        image = strategy.crop(image, self.crop_origin_xyxy)
        return image
    
    def _crop_label(self, label_path: str, img_source_size: tuple):
        with open(label_path, 'r') as f:
            labels = np.array([l.split(' ') for l in f.readlines()])
            
            w, h = img_source_size
            strategy = self.process_strategies.get((h, w))
            if not strategy:
                raise KeyError(f"Image size {h}x{w} is not supported")
            
            labels,novalid_num = strategy.transform_label(labels, self.crop_origin_xyxy)
            return labels,novalid_num

    def crop(self,image_path:str,label_path:str):
        from PIL import Image
        img_size = Image.open(image_path).size
        image = self._crop_image(image_path,img_size)
        labels,novalid_num = self._crop_label(label_path,img_size)
        return image, labels,novalid_num

    def crop_thread(self, image_path:str,label_path:str):
        image, labels,novalid_num = self.crop(image_path,label_path)
        if novalid_num > 0:
            return
        cv2.imwrite(str(self.output_img_p / Path(image_path).name), image)
        if labels is None:
            (self.output_label_p / Path(label_path).name).write_text("")
        else:
            (self.output_label_p / Path(label_path).name).write_text(
                '\n'.join(f"{' '.join(map(str, label))}" for label in labels)
            )
        is_valid = True if novalid_num == 0 else False
        return is_valid

    def crop_all(self):
        img_root_p = self.dataset_p / 'images'   
        label_root_p = self.dataset_p / 'labels'
        for img_p in tqdm(img_root_p.glob('*.jpg'), total=len(list(img_root_p.glob('*.jpg')))):
            try:
                label_p = label_root_p / img_p.with_suffix('.txt').name
                image, labels,novalid_num = self.crop(str(img_p), str(label_p))
                if novalid_num > 0:
                    continue
                cv2.imwrite(str(self.output_img_p / img_p.name), image)
                if labels is None:
                    (self.output_label_p / label_p.name).write_text("")
                else:
                    (self.output_label_p / label_p.name).write_text(
                        '\n'.join(f"{' '.join(map(str, label))}" for label in labels)
                    )
            except KeyError as e:
                print(e)
                print(img_p)
    def crop_all_thread(self):
        img_root_p = self.dataset_p / 'images'   
        label_root_p = self.dataset_p / 'labels'
        label_ls = list(str(i) for i in label_root_p.glob('*.txt'))
        img_ls  = list( str(img_root_p / Path(i).with_suffix('.jpg').name)  for i in label_ls)
        error_labels = 0
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.crop_thread, img, label) for img, label in zip(img_ls, label_ls)]
            with tqdm(as_completed(futures), total=len(futures), desc="Processing") as pbar:
                for future in pbar:
                    try:
                        is_valid = future.result()  
                        if not is_valid:
                            error_labels += 1
                    except Exception as e:
                        print(f"任务失败: {e}")

        print(f"Total error labels: {error_labels}")
if __name__ == "__main__":
    crop_origin = (480, 284, 1440, 796)
    dataset_path = "/mnt/mydisk/zzl/zn/train_police0120_4nc/val"
    output_path = "/mnt/mydisk/zzl/zn/train_police0120_4nc_crop/val"
    dataset_crop = DatasetCropGestures(dataset_path,output_path,crop_origin)
    dataset_crop.crop_all_thread()