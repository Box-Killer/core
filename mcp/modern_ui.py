#!/usr/bin/env python3
"""
现代化UI组件库
提供各种美化的UI组件和工具函数
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os


class ModernUI:
    """现代化UI工具类"""
    
    def __init__(self, root, style):
        self.root = root
        self.style = style
        self.setup_colors()
        self.setup_styles()
    
    def setup_colors(self):
        """设置颜色主题"""
        self.colors = {
            'primary': '#3498db',
            'primary_dark': '#2980b9',
            'secondary': '#2ecc71',
            'secondary_dark': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#2c3e50',
            'white': '#ffffff',
            'gray': '#95a5a6',
            'gray_light': '#bdc3c7'
        }
    
    def setup_styles(self):
        """设置现代化样式"""
        # 主框架样式
        self.style.configure('Main.TFrame', 
                           background=self.colors['light'])
        
        # 卡片样式
        self.style.configure('Card.TFrame',
                           background=self.colors['white'],
                           relief='solid',
                           borderwidth=1)
        
        # 标签样式
        self.style.configure('Title.TLabel',
                           background=self.colors['white'],
                           font=('Segoe UI', 16, 'bold'),
                           foreground=self.colors['dark'])
        
        self.style.configure('Subtitle.TLabel',
                           background=self.colors['white'],
                           font=('Segoe UI', 12),
                           foreground=self.colors['gray'])
        
        self.style.configure('Label.TLabel',
                           background=self.colors['white'],
                           font=('Segoe UI', 10),
                           foreground=self.colors['dark'])
        
        # 按钮样式
        self.style.configure('Primary.TButton',
                           font=('Segoe UI', 10, 'bold'),
                           padding=(20, 12),
                           background=self.colors['primary'],
                           foreground=self.colors['white'])
        
        self.style.configure('Secondary.TButton',
                           font=('Segoe UI', 10, 'bold'),
                           padding=(20, 12),
                           background=self.colors['secondary'],
                           foreground=self.colors['white'])
        
        self.style.configure('Danger.TButton',
                           font=('Segoe UI', 10, 'bold'),
                           padding=(20, 12),
                           background=self.colors['danger'],
                           foreground=self.colors['white'])
        
        # 输入框样式
        self.style.configure('Modern.TEntry',
                           font=('Segoe UI', 10),
                           padding=(12, 10),
                           fieldbackground=self.colors['white'],
                           borderwidth=2,
                           relief='solid')
        
        # 下拉框样式
        self.style.configure('Modern.TCombobox',
                           font=('Segoe UI', 10),
                           padding=(12, 10),
                           fieldbackground=self.colors['white'],
                           borderwidth=2,
                           relief='solid')
        
        # 复选框样式
        self.style.configure('Modern.TCheckbutton',
                           font=('Segoe UI', 10),
                           background=self.colors['white'],
                           foreground=self.colors['dark'])
        
        # 单选按钮样式
        self.style.configure('Modern.TRadiobutton',
                           font=('Segoe UI', 10),
                           background=self.colors['white'],
                           foreground=self.colors['dark'])
    
    def create_card(self, parent, title=None, subtitle=None):
        """创建卡片容器"""
        card = ttk.Frame(parent, style='Card.TFrame')
        card.pack(fill='both', expand=True, padx=20, pady=20)
        
        if title:
            title_label = ttk.Label(card, text=title, style='Title.TLabel')
            title_label.pack(pady=(20, 5))
        
        if subtitle:
            subtitle_label = ttk.Label(card, text=subtitle, style='Subtitle.TLabel')
            subtitle_label.pack(pady=(0, 20))
        
        return card
    
    def create_input_group(self, parent, label_text, entry_type='text', **kwargs):
        """创建输入组件组"""
        frame = ttk.Frame(parent, style='Main.TFrame')
        frame.pack(fill='x', pady=10)
        
        # 标签
        label = ttk.Label(frame, text=label_text, style='Label.TLabel')
        label.pack(anchor='w', pady=(0, 5))
        
        # 输入组件
        if entry_type == 'text':
            entry = ttk.Entry(frame, style='Modern.TEntry', **kwargs)
        elif entry_type == 'password':
            entry = ttk.Entry(frame, style='Modern.TEntry', show='*', **kwargs)
        elif entry_type == 'combobox':
            entry = ttk.Combobox(frame, style='Modern.TCombobox', **kwargs)
        elif entry_type == 'text_area':
            entry = tk.Text(frame, font=('Segoe UI', 10), 
                          height=4, relief='solid', borderwidth=2)
        
        entry.pack(fill='x')
        
        return entry
    
    def create_button_group(self, parent, buttons):
        """创建按钮组"""
        frame = ttk.Frame(parent, style='Main.TFrame')
        frame.pack(fill='x', pady=20)
        
        button_widgets = []
        
        for i, (text, style_type, command) in enumerate(buttons):
            btn = ttk.Button(frame, text=text, 
                           style=f'{style_type}.TButton', 
                           command=command)
            btn.pack(side='right', padx=(10, 0) if i > 0 else (0, 0))
            button_widgets.append(btn)
        
        return button_widgets
    
    def create_checkbox_group(self, parent, options):
        """创建复选框组"""
        frame = ttk.Frame(parent, style='Main.TFrame')
        frame.pack(fill='x', pady=10)
        
        checkboxes = []
        for text in options:
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(frame, text=text, variable=var, 
                               style='Modern.TCheckbutton')
            cb.pack(anchor='w', pady=2)
            checkboxes.append((cb, var))
        
        return checkboxes
    
    def create_radio_group(self, parent, options, variable=None):
        """创建单选按钮组"""
        frame = ttk.Frame(parent, style='Main.TFrame')
        frame.pack(fill='x', pady=10)
        
        if variable is None:
            variable = tk.StringVar()
        
        radio_buttons = []
        for text, value in options:
            rb = ttk.Radiobutton(frame, text=text, value=value, 
                               variable=variable, style='Modern.TRadiobutton')
            rb.pack(anchor='w', pady=2)
            radio_buttons.append(rb)
        
        return radio_buttons, variable
    
    def show_message(self, title, message, message_type='info'):
        """显示消息框"""
        if message_type == 'info':
            messagebox.showinfo(title, message)
        elif message_type == 'warning':
            messagebox.showwarning(title, message)
        elif message_type == 'error':
            messagebox.showerror(title, message)
        elif message_type == 'question':
            return messagebox.askyesno(title, message)
    
    def center_window(self, width=None, height=None):
        """居中显示窗口"""
        self.root.update_idletasks()
        
        if width is None:
            width = self.root.winfo_width()
        if height is None:
            height = self.root.winfo_height()
        
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def set_window_icon(self):
        """设置窗口图标"""
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass


def create_modern_ui_example():
    """创建现代化UI示例"""
    def main(root, tk, ttk, style, create_modern_frame):
        # 创建现代化UI工具
        ui = ModernUI(root, style)
        
        # 设置窗口属性
        root.title("现代化用户界面示例")
        root.geometry("600x500")
        ui.center_window(600, 500)
        ui.set_window_icon()
        
        # 创建主卡片
        card = ui.create_card(root, "用户注册", "请填写以下信息完成注册")
        
        # 创建输入组件
        username_entry = ui.create_input_group(card, "用户名 *", 'text')
        email_entry = ui.create_input_group(card, "邮箱地址 *", 'text')
        password_entry = ui.create_input_group(card, "密码 *", 'password')
        confirm_password_entry = ui.create_input_group(card, "确认密码 *", 'password')
        
        # 创建下拉选择
        gender_options = ['请选择', '男', '女', '其他']
        gender_combo = ui.create_input_group(card, "性别", 'combobox', 
                                           values=gender_options, state='readonly')
        gender_combo.set('请选择')
        
        # 创建复选框
        interests = ['编程', '设计', '音乐', '运动', '阅读']
        interest_checkboxes = ui.create_checkbox_group(card, interests)
        
        # 创建单选按钮
        experience_options = [('初学者', 'beginner'), ('有经验', 'experienced'), ('专家', 'expert')]
        experience_radios, experience_var = ui.create_radio_group(card, experience_options)
        
        # 创建按钮
        def submit_form():
            # 验证表单
            if not username_entry.get().strip():
                ui.show_message("错误", "请输入用户名", "error")
                return
            
            if not email_entry.get().strip():
                ui.show_message("错误", "请输入邮箱地址", "error")
                return
            
            if not password_entry.get().strip():
                ui.show_message("错误", "请输入密码", "error")
                return
            
            if password_entry.get() != confirm_password_entry.get():
                ui.show_message("错误", "两次输入的密码不一致", "error")
                return
            
            # 获取选中的兴趣
            selected_interests = []
            for cb, var in interest_checkboxes:
                if var.get():
                    selected_interests.append(cb.cget('text'))
            
            # 获取选中的经验水平
            experience = experience_var.get()
            
            ui.show_message("成功", "注册信息已提交！", "info")
            root.quit()
        
        def reset_form():
            username_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            confirm_password_entry.delete(0, tk.END)
            gender_combo.set('请选择')
            
            for cb, var in interest_checkboxes:
                var.set(False)
            
            experience_var.set('')
        
        buttons = [
            ("重置", "Secondary", reset_form),
            ("提交", "Primary", submit_form)
        ]
        
        ui.create_button_group(card, buttons)
        
        root.mainloop()
        
        # 返回表单数据
        selected_interests = []
        for cb, var in interest_checkboxes:
            if var.get():
                selected_interests.append(cb.cget('text'))
        
        return {
            "username": username_entry.get(),
            "email": email_entry.get(),
            "password": password_entry.get(),
            "gender": gender_combo.get(),
            "interests": selected_interests,
            "experience": experience_var.get()
        }
    
    return main 