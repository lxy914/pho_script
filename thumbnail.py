"""
此脚本用于将旧照片生成pho读取的缩略图
"""
import os
from PIL import Image,ImageOps
from datetime import datetime

# 获取照片的拍摄日期
def get_img_datatime(file_path):
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            # 根据exif中的拍摄日期信息获取日期
            if 36867 in exif_data:
                date_str = exif_data[36867].strip().replace(" ", "")
                # print("info:",date_str)
                date_time = datetime.strptime(date_str, "%Y:%m:%d%H:%M:%S").date()
            else:
                # 如果获取不到则获取照片的最后修改日期
                date_time = datetime.fromtimestamp(os.path.getmtime(file_path)).date()
    except (AttributeError, KeyError, IndexError, OSError,TypeError):
        # 如果获取不到则获取照片的最后修改日期
        date_time = datetime.fromtimestamp(os.path.getmtime(file_path)).date()
    return date_time
def generate_thumbnail(photo_folder,thumbnail_size = (200, 200)):
    # 遍历文件夹中的每个日期文件夹
    for root, dirs, files in os.walk(photo_folder):
        # 过滤缩略图文件夹不处理
        if ".thumbnail" in root:
            continue
        for file in files:
            # 获取图片文件路径
            file_path = os.path.join(root, file)
            
            # 仅处理图片文件
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # 获取照片的拍摄日期
                date_time=get_img_datatime(file_path)
                # 生成缩略图的文件夹路径
                thumbnail_folder = os.path.join(photo_folder, ".thumbnail", str(date_time.year), str(date_time.month).zfill(2), str(date_time.day).zfill(2))
                if not os.path.exists(thumbnail_folder):
                    os.makedirs(thumbnail_folder)
                # 缩略图照片的路径
                thumbnail_path = os.path.join(thumbnail_folder, file)
                # 缩略图存在则跳过不处理
                if os.path.exists(thumbnail_path):
                    continue

                # 生成缩略图并保存
                try:
                    with Image.open(file_path) as img:
                        img = ImageOps.exif_transpose(img)
                        img.thumbnail(thumbnail_size)
                        img = img.convert("RGB")
                        img.save(thumbnail_path)
                        print(thumbnail_path)
                except OSError as e:
                    print(f"Error processing {file}: {e}")

# 定义照片文件夹和缩略图尺寸
photo_folder = r"D:\微云照片"


# 生成缩略图
generate_thumbnail(photo_folder)

print("缩略图生成完成！")
