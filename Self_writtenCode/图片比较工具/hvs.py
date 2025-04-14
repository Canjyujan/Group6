import numpy as np
import cv2
from scipy.ndimage import gaussian_filter
import os
import random


# 图片预处理
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换为灰度图片

    # cv2.resize()默认使用双线性插值   将灰度图重采样为64*64
    resized_image = cv2.resize(gray_image, (64, 64))

    return resized_image


# 对图片的64个8*8子块进行二维离散余弦变换，并将每一个子块的DC系数置为0
def dct_image(image):
    # 创建一个与image有相同形状和数据类型的全零数组用以储存结果
    dct_blocks = np.zeros_like(image)
    for i in range(0, image.shape[0], 8):
        for j in range(0, image.shape[1], 8):
            block = image[i : i + 8, j : j + 8]  # i:i+8 是从i到i+8之前，所以加8
            block = np.array(block)
            dct_block = cv2.dct(block.astype(np.float32))
            dct_block[0, 0] = 0  # 将DC系数（图像块的平均亮度）置为0
            dct_blocks[i : i + 8, j : j + 8] = dct_block
    return dct_blocks


def generate_random_matrices(
    N, key, sigma=1.0, iterations=2
):  # sigma通常取1,次数暂时选择2
    # 设置密钥保证矩阵可复现
    np.random.seed(key)
    matrices = []
    for _ in range(N):
        Y = np.random.randn(64, 64)  # 生成N个服从正态分布的64*64矩阵
        for _ in range(iterations):
            Y = gaussian_filter(Y, sigma=sigma)  # 用高斯低通滤波器进行迭代滤波
        matrices.append(Y)
    return matrices


def reshape_m():
    m = np.array(
        [
            [71.43, 99.01, 86.21, 60.24, 41.67, 29.16, 20.88, 15.24],
            [99.01, 68.97, 75.76, 65.79, 50.00, 36.90, 27.25, 20.28],
            [86.21, 75.76, 44.64, 38.61, 33.56, 27.47, 21.74, 17.01],
            [60.24, 65.79, 38.61, 26.53, 21.98, 18.87, 15.92, 13.16],
            [41.67, 50.00, 33.56, 21.98, 16.26, 13.14, 11.48, 9.83],
            [29.16, 36.90, 27.47, 18.87, 13.14, 10.40, 8.64, 7.40],
            [20.88, 27.25, 21.74, 15.92, 11.48, 8.64, 6.90, 5.78],
            [15.24, 20.28, 17.01, 13.16, 9.83, 7.40, 5.78, 4.73],
        ]
    )
    M = np.tile(m, (8, 8))
    return M


def compute_hash(image_path, N, key, M):
    processed_image = preprocess_image(image_path)
    dct_blocks = dct_image(processed_image)
    matrices = generate_random_matrices(N, key)
    Y = np.array([np.sum(dct_blocks * P * M) for P in matrices])
    hash_bits = (Y >= 0).astype(int)
    return hash_bits


# 计算汉明距离
def compute_hamming_distance(hash_vec1, hash_vec2):
    norm_vec1 = np.linalg.norm(hash_vec1)
    norm_vec2 = np.linalg.norm(hash_vec2)
    distance = np.linalg.norm(
        (hash_vec1 - hash_vec2) / (2 * np.sqrt(norm_vec1 * norm_vec2))
    )
    return distance


def compare_hash(image_path1, image_path2, N, key, tau):
    M = reshape_m()
    hash_vec1 = compute_hash(image_path1, N, key, M)
    hash_vec2 = compute_hash(image_path2, N, key, M)
    distance = compute_hamming_distance(hash_vec1, hash_vec2)
    if distance < tau:
        return "两幅图片一致"
    else:
        return "两幅图片不一致"


def main(dataset_path):
    N = 100
    key = 12345
    tau = 0.1

    image_files = [
        os.path.join(dataset_path, f)
        for f in os.listdir(dataset_path)
        if f.endswith((".jpg", ".png", ".jpeg"))
    ]

    base_image_path = random.choice(image_files)
    print(f"基准图像: {base_image_path}")

    results = []
    for img_path in image_files:
        if img_path == base_image_path:
            continue  # 跳过基准图自身
        distance = compare_hash(base_image_path, img_path, N, key, tau)
        results.append((img_path, distance))

    # 按距离排序（从最相似到最不相似）
    results.sort(key=lambda x: x[1])

    # 输出比对结果
    for img_path, dist in results:
        print(f"比对图像: {img_path}, Hamming 距离: {dist}")


if __name__ == "__main__":
    dataset_folder = "./images"  # 替换为你的数据集路径
    main(dataset_folder)
