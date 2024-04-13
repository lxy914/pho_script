# pho_script
此脚本用于将旧照片转换成pho读取的格式

共分为两步：
1. 运行build.py，把旧照片按照拍摄日期转换成"年/月/日"格式的路径，注意需要修改photo_folder和target_folder为你的路径
2. 运行thumbnail.py，按照".thumbnail/年/月/日"格式生成缩略图，photo_folder为第1步中target_folder的路径
