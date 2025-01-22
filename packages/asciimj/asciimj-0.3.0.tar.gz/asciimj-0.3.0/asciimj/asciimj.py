from PIL import Image

def convert_image_to_ascii(image, output_width=100):
    """
    将图像转换为 ASCII 艺术字符串。
    
    :param image: PIL.Image 对象
    :param output_width: 输出 ASCII 艺术的宽度
    :return: ASCII 艺术字符串
    """
    
    # 将图像调整为指定宽度
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(output_width * aspect_ratio)
    resized_image = image.resize((output_width, new_height))
    
    # 将图像转换为灰度图
    grayscale_image = resized_image.convert("L")
    
    # 定义 ASCII 字符
    ascii_chars = "@%#*+=-:. "
    pixels = grayscale_image.getdata()
    
    # 将像素值映射到 ASCII 字符
    ascii_str = "".join([ascii_chars[pixel // 32] for pixel in pixels])
    
    # 将 ASCII 字符串分行
    ascii_str_len = len(ascii_str)
    ascii_art = "\n".join([ascii_str[i:i+output_width] for i in range(0, ascii_str_len, output_width)])
    
    return ascii_art
