#!/usr/bin/env python3
"""
生成一个简单的图标文件用于美化界面
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    def create_icon():
        """创建一个简单的图标"""
        # 创建一个 32x32 的图像
        size = (32, 32)
        image = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # 绘制一个圆形背景
        draw.ellipse([2, 2, 30, 30], fill='#3498db', outline='#2980b9', width=2)
        
        # 绘制一个简单的 "UI" 文字
        try:
            # 尝试使用系统字体
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", 12)
            except:
                font = ImageFont.load_default()
        
        # 绘制文字
        text = "UI"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        draw.text((x, y), text, fill='white', font=font)
        
        # 保存为ICO文件
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        image.save(icon_path, format='ICO', sizes=[(32, 32)])
        print(f"图标已创建: {icon_path}")
        
    if __name__ == "__main__":
        create_icon()
        
except ImportError:
    print("PIL 未安装，跳过图标创建")
    print("可以通过运行 'pip install pillow' 来安装") 