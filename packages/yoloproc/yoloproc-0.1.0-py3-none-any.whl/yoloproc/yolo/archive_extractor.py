from pathlib import Path
from typing import Dict, Callable, Union
import zipfile
import py7zr

class ArchiveExtractor:
    """
    压缩文件解压工具类,支持zip和7z格式的批量解压。
    
    Attributes:
        _extractors (Dict[str, Callable]): 支持的文件格式及其对应的解压方法
    
    Example:
        >>> extractor = ArchiveExtractor()
        >>> extractor.extract_all('/path/to/archives', '/path/to/output')
    """
    
    def __init__(self):
        """初始化解压器，设置支持的文件格式及其处理方法"""
        self._extractors: Dict[str, Callable] = {
            '.zip': self._extract_zip,
            '.7z': self._extract_7z
        }

    @staticmethod
    def _extract_zip(file_path: Path, output_dir: Path) -> None:
        """
        解压ZIP文件到指定目录
        
        Args:
            file_path (Path): ZIP文件路径
            output_dir (Path): 输出目录路径
        """
        with zipfile.ZipFile(str(file_path), 'r') as zip_ref:
            zip_ref.extractall(str(output_dir))

    @staticmethod
    def _extract_7z(file_path: Path, output_dir: Path) -> None:
        """
        解压7Z文件到指定目录
        
        Args:
            file_path (Path): 7Z文件路径
            output_dir (Path): 输出目录路径
        """
        with py7zr.SevenZipFile(str(file_path), mode='r') as z:
            z.extractall(path=str(output_dir))

    def extract_all(self, source_dir: Union[str, Path], output_dir: Union[str, Path]) -> None:
        """
        批量解压目录中的压缩文件
        
        Args:
            source_dir (Union[str, Path]): 包含压缩文件的源目录
            output_dir (Union[str, Path]): 解压输出根目录
            
        Note:
            - 会为每个压缩文件在输出目录下创建同名子目录
            - 当前支持.zip和.7z格式
            - 遇到不支持的文件格式会跳过并打印提示
        """
        source_path = Path(source_dir)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)

        for file_path in source_path.iterdir():
            if not file_path.is_file():
                continue

            extract_subdir = output_path / file_path.stem
            extract_subdir.mkdir(exist_ok=True)

            if file_path.suffix.lower() in self._extractors:
                print(f'Extracting {file_path.name} to {extract_subdir}...')
                self._extractors[file_path.suffix.lower()](file_path, extract_subdir)
            else:
                print(f'Skipping unsupported file type: {file_path.name}')

# 使用示例：
if __name__ == '__main__':
    extractor = ArchiveExtractor()
    extractor.extract_all(
        source_dir='/data/police_gesture_seqs/zip',
        output_dir='/data/police_gesture_seqs/output'
    )