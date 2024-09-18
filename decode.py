import os
import sys
from tqdm import tqdm
import uncompyle6

def walk_dir(dir, topdown=True):
    words = ['asyncio.', 'attr.', 'bs4.', 'chardet.', 'Crypto.', 'chardet.', 'concurrent.', 'ctypes.', 'dateutil.', 'distutils.', 'email.', 'et_xmlfile.', 'fiona.', 'geographiclib.', 'geojson.', 'geopandas.', 'geopy.', 'html.', 'http.', 'importlib.', 'jinja2.', 'multiprocessing.', 'numpy.', 'openpyxl.', 'pandas.', 'pkg_resources.', 'pyecharts.', 'pyproj.', 'pytz.', 'requests.', 'setuptools.', 'shapely.', 'simplejson.', 'soupsieve.', 'sqlalchemy.', 'unittest.', 'urllib3.', 'xlsxwriter.', 'xml.', 'xlrd.']
    
    pyc_files = []
    for root, dirs, files in os.walk(dir, topdown):
        for name in files:
            if name.endswith('.pyc'):
                pyc_files.append(os.path.join(root, name))
    
    for pyc_file in tqdm(pyc_files, desc="正在反编译"):
        part_name = os.path.splitext(pyc_file)[0]
        part_file_name = part_name.replace("\\", "/")
        
        isconvert = True
        for w in words:
            if os.path.basename(pyc_file).startswith(w):
                isconvert = False
                break
        
        if isconvert:
            try:
                # 确保输出目录存在
                output_dir = os.path.dirname(part_file_name)
                os.makedirs(output_dir, exist_ok=True)
                
                # 执行反编译
                with open(f"{part_file_name}.py", 'w', encoding='utf-8') as py_file:
                    uncompyle6.decompile_file(pyc_file, py_file)
                print(f"已反编译: {part_file_name}")
            except Exception as e:
                print(f"反编译失败: {part_file_name}, 错误: {str(e)}")

if __name__ == "__main__":
    walk_dir(os.getcwd())