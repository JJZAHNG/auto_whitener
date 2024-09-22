import os
import cv2
import numpy as np
from pathlib import Path


def process_images():
    print('SYSTEM PROCESSING...')
    try:
        print('FINDER PROCESSING...')
        # 获取用户的主目录
        home_dir = str(Path.home())
        # 拼接 Downloads 文件夹路径
        downloads_folder = os.path.join(home_dir, 'Downloads')

        # 提示用户输入输入和输出文件夹名称
        input_folder_name = input("请输入包含图像的文件夹名称（位于 Downloads 文件夹中）：")
        output_folder_name = input("请输入输出文件夹的名称（将创建在 Downloads 文件夹中）：")

        # 构建完整的输入和输出文件夹路径
        input_folder = os.path.join(downloads_folder, input_folder_name)
        output_folder = os.path.join(downloads_folder, output_folder_name)

        # 验证输入文件夹是否存在
        if not os.path.exists(input_folder):
            raise FileNotFoundError(f"输入文件夹不存在：{input_folder}")

        # 如果输出文件夹不存在，则创建它
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 遍历输入文件夹中的所有文件
        for filename in os.listdir(input_folder):
            # 构建完整的文件路径
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 检查文件是否为图像文件
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                try:
                    # 读取图像
                    image = cv2.imread(input_path)

                    # 检查图像是否读取成功
                    if image is None:
                        print(f"无法读取图像文件：{input_path}")
                        continue

                    # ---------------- 美白处理 ----------------
                    # 转换为HSV颜色空间
                    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                    h, s, v = cv2.split(img_hsv)

                    # 增加亮度（Value通道）
                    v = cv2.add(v, 30)  # 数值可以调整，控制美白程度
                    v = np.clip(v, 0, 255)

                    # 合并通道
                    img_hsv_whitened = cv2.merge([h, s, v])

                    # 转换回BGR颜色空间
                    final_image = cv2.cvtColor(img_hsv_whitened, cv2.COLOR_HSV2BGR)

                    # ---------------- 可选：添加美白滤镜 ----------------
                    # 创建一个全白的图像，与原图混合
                    # 如果您觉得需要进一步美白，可以取消以下代码的注释

                    # white_image = np.full(image.shape, 255, dtype=np.uint8)
                    # alpha = 0.05  # 控制美白滤镜的强度，数值在0-1之间
                    # final_image = cv2.addWeighted(final_image, 1 - alpha, white_image, alpha, 0)

                    # 保存处理后的图像
                    cv2.imwrite(output_path, final_image)
                    print(f"已处理并保存：{output_path}")

                except Exception as e:
                    print(f"处理文件 {input_path} 时出错：{e}")
            else:
                print(f"跳过非图像文件：{input_path}")

    except Exception as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    process_images()
