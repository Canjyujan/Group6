项目功能：
将图像灰度化并统一为 64x64 尺寸
对图像分块执行二维 DCT，屏蔽 DC 分量
利用高斯滤波的随机矩阵与 DCT 加权值进行哈希生成
比较图像间哈希值距离，判断是否一致

使用技术：
	OpenCV：图像读取、灰度转换、DCT 计算
	NumPy：矩阵计算
	SciPy：高斯滤波器生成随机矩阵
	Python 标准库：文件操作、随机数等

目录结构：
project/
│
├── images/              # 存放要比较的图像文件（.jpg/.png/.jpeg）
├── image_hash.py        # 主程序
├── tempCodeRunnerFile.py
└── README.md            # 使用说明文档

环境依赖：
请先安装以下依赖库（建议使用 Python 3.7+）：
pip install numpy opencv-python scipy

使用方法：
1.	准备图像数据：将多张图像放入 images/ 文件夹中（支持 .jpg, .jpeg, .png 格式）
2.	运行主程序：python image_hash.py
3.	输出结果示例：
基准图像: ./images\2.jpg
比对图像: ./images\1.jpg, Hamming 距离: 两幅图片一致
比对图像: ./images\3.jpg, Hamming 距离: 两幅图片不一致

参数说明：
在 main() 函数中你可以根据需要修改以下参数：
N = 100           # 随机矩阵数量
key = 12345       # 随机种子（保证复现）
tau = 0.1         # 相似度阈值，小于 tau 判为一致

哈希过程说明：
1.	图像预处理：灰度转换 + 缩放至 64x64
2.	分块 DCT 变换 + DC 分量归零
3.	构造加权矩阵 M 以提升低频区域权重
4.	使用 N 个高斯滤波后的随机矩阵作为哈希投影基
5.	哈希结果通过正负号转为二进制比特
6.	比较两组哈希的归一化汉明距离
