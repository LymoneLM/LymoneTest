import json
import os
import sys

import cv2
import numpy as np
import torch
from PIL import Image
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage, QMovie
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFileDialog, QGroupBox,
                             QFrame, QStatusBar, QSizePolicy, QRadioButton, QButtonGroup)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QMovie
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFileDialog, QGroupBox,
                             QFrame, QStatusBar, QSizePolicy, QRadioButton, QButtonGroup)
# 导入模型相关代码
try:
    from moudle.mobilenet import MobileNetV2
except ImportError:
    # 添加父目录到路径中
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from moudle.mobilenet import MobileNetV2

# 定义一个工作线程来处理图像分类，避免UI卡顿
class PredictionThread(QThread):
    prediction_complete = pyqtSignal(str, float)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, model_path, image_path):
        super().__init__()
        self.model_path = model_path
        self.image_path = image_path
        
    def run(self):
        try:
            # 加载类别映射
            json_path = "class_indices.json"
            if not os.path.exists(json_path):
                self.error_occurred.emit("找不到类别映射文件")
                return
                
            with open(json_path, 'r') as f:
                cls_dict = json.load(f)
                
            # 加载模型
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            model = MobileNetV2(num_classes=len(cls_dict))
            
            # 尝试加载模型权重
            try:
                model.load_state_dict(torch.load(self.model_path, map_location=device))
            except Exception as e:
                self.error_occurred.emit(f"加载模型失败: {str(e)}")
                return
                
            model.to(device)
            model.eval()
            
            # 图像预处理
            from torchvision import transforms
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
            
            # 加载并处理图像
            image = Image.open(self.image_path).convert('RGB')
            image_tensor = transform(image).unsqueeze(0).to(device)
            
            # 进行预测
            with torch.no_grad():
                output = torch.squeeze(model(image_tensor)).cpu()
                predict = torch.softmax(output, dim=0)
                predict_cls = torch.argmax(predict).numpy()
                
            # 发送结果信号
            class_name = cls_dict[str(predict_cls)]
            probability = predict[predict_cls].item()
            self.prediction_complete.emit(class_name, probability)
            
        except Exception as e:
            self.error_occurred.emit(f"预测过程中发生错误: {str(e)}")

class VideoThread(QThread):
    """处理视频流的线程"""
    frame_ready = pyqtSignal(np.ndarray)
    video_finished = pyqtSignal()
    connection_error = pyqtSignal(str)
    
    def __init__(self, video_source=0, is_camera=True):
        super().__init__()
        self.video_source = video_source
        self.is_camera = is_camera
        self.running = False
        
    def run(self):
        self.running = True
        cap = cv2.VideoCapture(self.video_source)
        
        if not cap.isOpened():
            self.running = False
            if self.is_camera:
                self.connection_error.emit("无法连接到摄像头，请检查设备")
            else:
                self.connection_error.emit("无法打开视频文件")
            return
            
        while self.running:
            ret, frame = cap.read()
            if not ret:
                if not self.is_camera:  # 如果是视频文件而不是摄像头，播放结束时发出信号
                    self.video_finished.emit()
                    break
                continue
                
            # 发送帧信号给主线程
            self.frame_ready.emit(frame)
            
            # 添加延迟以控制帧率
            self.msleep(30)  # 约30fps
            
        cap.release()
    
    def stop(self):
        self.running = False
        self.wait()

class ImagePredictionThread(QThread):
    """处理图像预测的线程"""
    prediction_complete = pyqtSignal(str, float)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, model_path, pil_image):
        super().__init__()
        self.model_path = model_path
        self.pil_image = pil_image
        
    def run(self):
        try:
            # 加载类别映射
            json_path = "class_indices.json"
            if not os.path.exists(json_path):
                self.error_occurred.emit("找不到类别映射文件")
                return
                
            with open(json_path, 'r') as f:
                cls_dict = json.load(f)
                
            # 加载模型
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            model = MobileNetV2(num_classes=len(cls_dict))
            
            # 尝试加载模型权重
            try:
                model.load_state_dict(torch.load(self.model_path, map_location=device))
            except Exception as e:
                self.error_occurred.emit(f"加载模型失败: {str(e)}")
                return
                
            model.to(device)
            model.eval()
            
            # 图像预处理
            from torchvision import transforms
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
            
            # 处理图像
            image_tensor = transform(self.pil_image).unsqueeze(0).to(device)
            
            # 进行预测
            with torch.no_grad():
                output = torch.squeeze(model(image_tensor)).cpu()
                predict = torch.softmax(output, dim=0)
                predict_cls = torch.argmax(predict).numpy()
                
            # 发送结果信号
            class_name = cls_dict[str(predict_cls)]
            probability = predict[predict_cls].item()
            self.prediction_complete.emit(class_name, probability)
            
        except Exception as e:
            self.error_occurred.emit(f"预测过程中发生错误: {str(e)}")

class SwineFeverDetector(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口标题和大小
        self.setWindowTitle("猪瘟检测系统")
        self.setMinimumSize(1200, 800)  # 增大默认窗口尺寸
        # 设置窗口样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
            QPushButton:pressed {
                opacity: 0.6;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
                margin-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
            }
        """)
        
        # 存储当前路径
        self.current_image_path = ""
        self.current_model_path = ""
        self.prediction_thread = None
        self.video_thread = None
        self.current_frame = None
        self.detection_mode = "image"  # 默认模式：image, video, camera
        
        # 摄像头检测控制参数
        self.camera_detection_active = False
        self.frame_count = 0
        self.detection_interval = 10  # 每10帧检测一次
        
        # 初始化UI
        self.init_ui()
        
        # 搜索可用模型
        self.search_models()
        
    def init_ui(self):
        # 设置中央窗口和主布局
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)  # 增大边距
        main_layout.setSpacing(15)  # 增加间距
        
        # 创建顶部标题区域
        title_frame = QFrame()
        title_frame.setStyleSheet("background-color: #2c3e50; border-radius: 8px;")
        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(20, 20, 20, 20)  # 增加内边距
        
        title_label = QLabel("猪瘟智能检测系统")
        title_label.setStyleSheet("color: white; font-size: 42px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title_label)
        
        # 增加标题区域的高度
        title_frame.setMinimumHeight(120)
        title_frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        main_layout.addWidget(title_frame)
        
        # 添加一些间距
        main_layout.addSpacing(20)
        
        # 创建主内容区域 - 使用水平布局代替分割器
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # 左侧区域 - 模型选择和控制面板
        left_widget = QWidget()
        left_widget.setMinimumWidth(350)  # 设置最小宽度
        left_widget.setMaximumWidth(450)  # 设置最大宽度
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(15)
        
        # 模型选择组
        model_group = QGroupBox("模型选择")
        model_group.setStyleSheet("QGroupBox { border: 2px solid #3498db; }")
        model_layout = QVBoxLayout(model_group)
        model_layout.setContentsMargins(15, 25, 15, 15)
        
        # 移除下拉菜单，直接使用文件选择按钮
        self.browse_model_btn = QPushButton("选择模型文件")
        self.browse_model_btn.setStyleSheet("background-color: #3498db; color: white; padding: 12px; border-radius: 4px; font-size: 16px;")
        self.browse_model_btn.setMinimumHeight(50)
        self.browse_model_btn.clicked.connect(self.browse_model)
        model_layout.addWidget(self.browse_model_btn)
        
        # 模型信息区域
        self.model_info_label = QLabel("未加载模型")
        self.model_info_label.setStyleSheet("padding: 10px; background-color: #f5f5f5; border-radius: 4px; font-size: 14px;")
        self.model_info_label.setWordWrap(True)
        self.model_info_label.setMinimumHeight(60)
        model_layout.addWidget(self.model_info_label)
        
        left_layout.addWidget(model_group)
        
        # 图像选择组
        image_group = QGroupBox("输入选择")
        image_group.setStyleSheet("QGroupBox { border: 2px solid #e74c3c; }")
        image_layout = QVBoxLayout(image_group)
        image_layout.setContentsMargins(15, 25, 15, 15)
        
        # 添加输入模式选择
        mode_widget = QWidget()
        mode_layout = QHBoxLayout(mode_widget)
        mode_layout.setContentsMargins(0, 0, 0, 0)
        mode_layout.setSpacing(20)  # 增加单选按钮之间的间距
        
        self.mode_group = QButtonGroup(self)
        
        self.image_mode_radio = QRadioButton("图像文件")
        self.image_mode_radio.setChecked(True)
        self.image_mode_radio.setStyleSheet("font-size: 16px;")
        self.image_mode_radio.toggled.connect(lambda: self.change_detection_mode("image"))
        
        self.video_mode_radio = QRadioButton("视频文件")
        self.video_mode_radio.setStyleSheet("font-size: 16px;")
        self.video_mode_radio.toggled.connect(lambda: self.change_detection_mode("video"))
        
        self.camera_mode_radio = QRadioButton("摄像头")
        self.camera_mode_radio.setStyleSheet("font-size: 16px;")
        self.camera_mode_radio.toggled.connect(lambda: self.change_detection_mode("camera"))
        
        self.mode_group.addButton(self.image_mode_radio)
        self.mode_group.addButton(self.video_mode_radio)
        self.mode_group.addButton(self.camera_mode_radio)
        
        mode_layout.addWidget(self.image_mode_radio)
        mode_layout.addWidget(self.video_mode_radio)
        mode_layout.addWidget(self.camera_mode_radio)
        mode_layout.addStretch()  # 添加弹性空间，使单选按钮靠左对齐
        
        image_layout.addWidget(mode_widget)
        
        # 添加选择文件按钮 - 用于图像和视频模式
        self.select_image_btn = QPushButton("选择文件")
        self.select_image_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; 
                color: white; 
                padding: 12px; 
                border-radius: 4px; 
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #ec7063;
            }
            QPushButton:pressed {
                background-color: #cb4335;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.select_image_btn.setMinimumHeight(50)
        self.select_image_btn.clicked.connect(self.browse_input)
        image_layout.addWidget(self.select_image_btn)
        
        # =================== 摄像头界面 - 极度简化 ===================
        self.camera_control_widget = QWidget()
        camera_layout = QVBoxLayout(self.camera_control_widget)
        camera_layout.setContentsMargins(0, 0, 0, 0)
        camera_layout.setSpacing(10)
        
        # 仅保留一个大启动按钮，简单明了
        self.camera_btn = QPushButton("启动摄像头")
        self.camera_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; 
                color: white; 
                padding: 15px; 
                border-radius: 4px; 
                font-size: 18px; 
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.camera_btn.setMinimumHeight(60)
        self.camera_btn.clicked.connect(self.toggle_camera)
        camera_layout.addWidget(self.camera_btn)
        
        # 隐藏摄像头选择器，始终使用默认摄像头
        self.current_camera_index = 0
        
        self.camera_control_widget.setVisible(False)
        image_layout.addWidget(self.camera_control_widget)
        
        # 文件路径/状态显示
        self.image_path_label = QLabel("未选择文件")
        self.image_path_label.setStyleSheet("padding: 10px; background-color: #f5f5f5; border-radius: 4px; font-size: 14px;")
        self.image_path_label.setWordWrap(True)
        self.image_path_label.setMinimumHeight(60)
        image_layout.addWidget(self.image_path_label)
        
        left_layout.addWidget(image_group)
        
        # 操作按钮组
        action_group = QGroupBox("操作")
        action_group.setStyleSheet("QGroupBox { border: 2px solid #9b59b6; }")
        action_layout = QVBoxLayout(action_group)
        action_layout.setContentsMargins(15, 25, 15, 15)
        
        # 添加控制按钮
        self.detect_btn = QPushButton("开始检测")
        self.detect_btn.setStyleSheet("background-color: #9b59b6; color: white; padding: 15px; border-radius: 4px; font-size: 18px; font-weight: bold;")
        self.detect_btn.setMinimumHeight(60)
        self.detect_btn.clicked.connect(self.perform_detection)
        self.detect_btn.setEnabled(False)  # 初始禁用
        action_layout.addWidget(self.detect_btn)
        
        left_layout.addWidget(action_group)
        
        # 添加弹簧，将小部件推到顶部
        left_layout.addStretch()
        
        # 右侧区域 - 图像显示和结果
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(15)
        
        # 图像显示区
        display_group = QGroupBox("图像预览")
        display_group.setStyleSheet("QGroupBox { border: 2px solid #f39c12; }")
        display_layout = QVBoxLayout(display_group)
        display_layout.setContentsMargins(15, 25, 15, 15)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: #ecf0f1; border-radius: 4px; font-size: 16px;")
        self.image_label.setMinimumHeight(350)
        self.image_label.setText("请选择输入源")
        display_layout.addWidget(self.image_label)
        
        right_layout.addWidget(display_group)
        
        # 结果显示区
        results_group = QGroupBox("检测结果")
        results_group.setStyleSheet("QGroupBox { border: 2px solid #1abc9c; }")
        results_layout = QHBoxLayout(results_group)
        results_layout.setContentsMargins(15, 25, 15, 15)
        
        # 结果图标 - 减小尺寸
        self.result_icon_label = QLabel()
        self.result_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_icon_label.setFixedSize(60, 60)
        
        # 结果信息容器
        result_info_widget = QWidget()
        result_info_layout = QVBoxLayout(result_info_widget)
        
        # 结果标签
        self.result_class_label = QLabel("未检测")
        self.result_class_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        result_info_layout.addWidget(self.result_class_label)
        
        self.result_prob_label = QLabel("")
        self.result_prob_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        result_info_layout.addWidget(self.result_prob_label)
        
        # 添加到水平布局
        results_layout.addWidget(self.result_icon_label)
        results_layout.addWidget(result_info_widget)
        
        right_layout.addWidget(results_group)
        
        # 将左右两侧添加到主内容布局
        content_layout.addWidget(left_widget)
        content_layout.addWidget(right_widget)
        
        # 将内容区域添加到主布局
        main_layout.addWidget(content_widget, 1)
        
        # 添加状态栏
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet("background-color: #ecf0f1; font-size: 14px;")
        self.statusBar.setMinimumHeight(30)
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("系统准备就绪", 5000)
        
        # 加载动画
        self.loading_movie = QMovie("loading.gif")
        if not os.path.exists("loading.gif"):
            # 如果没有loading.gif，则使用文本
            self.loading_movie = None
    
    def search_models(self):
        """这个方法已不再使用，但保留以兼容现有代码"""
        pass
    
    def update_model_info(self, model_path, model_name):
        """更新模型信息显示"""
        if model_path:
            self.current_model_path = model_path
            
            model_info = f"选择的模型: {model_name}\n路径: {model_path}"
            self.model_info_label.setText(model_info)
            self.update_detect_button()
    
    def browse_model(self):
        """浏览选择模型文件"""
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("PyTorch模型 (*.pth)")
        file_dialog.setWindowTitle("选择模型文件")
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                model_path = selected_files[0]
                model_name = os.path.basename(model_path)
                self.update_model_info(model_path, model_name)
    
    def change_detection_mode(self, mode):
        """切换检测模式"""
        self.detection_mode = mode
        
        # 停止任何正在进行的视频流
        if self.video_thread is not None and self.video_thread.isRunning():
            self.stop_video()
        
        # 更新UI元素
        if mode == "image":
            self.camera_control_widget.setVisible(False)
            self.select_image_btn.setVisible(True)
            self.select_image_btn.setText("选择图像文件")
            self.select_image_btn.setEnabled(True)
            self.image_path_label.setText("未选择图像")
        elif mode == "video":
            self.camera_control_widget.setVisible(False)
            self.select_image_btn.setVisible(True)
            self.select_image_btn.setText("选择视频文件")
            self.select_image_btn.setEnabled(True)
            self.image_path_label.setText("未选择视频")
        elif mode == "camera":
            self.camera_control_widget.setVisible(True)
            self.select_image_btn.setVisible(False)
            
            # 重置摄像头控件状态
            self.camera_btn.setText("启动摄像头")
            self.camera_btn.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60; 
                    color: white; 
                    padding: 15px; 
                    border-radius: 4px; 
                    font-size: 18px; 
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #2ecc71;
                }
            """)
            self.image_path_label.setText("摄像头状态: 未启动")
            
        # 清除预览图像
        self.image_label.setText("请选择输入源")
        self.current_image_path = ""
        
        # 更新检测按钮状态
        self.update_detect_button()
    
    def browse_input(self):
        """浏览选择输入文件（图像或视频）"""
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        
        if self.detection_mode == "image":
            file_dialog.setNameFilter("图像文件 (*.jpg *.jpeg *.png)")
            file_dialog.setWindowTitle("选择图像文件")
        elif self.detection_mode == "video":
            file_dialog.setNameFilter("视频文件 (*.mp4 *.avi *.mov *.mkv)")
            file_dialog.setWindowTitle("选择视频文件")
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                self.current_image_path = file_path
                self.image_path_label.setText(f"已选择文件: {os.path.basename(file_path)}")
                
                if self.detection_mode == "image":
                    # 显示图像预览
                    pixmap = QPixmap(file_path)
                    if not pixmap.isNull():
                        # 适应label大小，保持比例
                        pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(), 
                                            Qt.AspectRatioMode.KeepAspectRatio, 
                                            Qt.TransformationMode.SmoothTransformation)
                        self.image_label.setPixmap(pixmap)
                    else:
                        self.image_label.setText("无法加载图像")
                elif self.detection_mode == "video":
                    # 显示视频第一帧作为预览
                    cap = cv2.VideoCapture(file_path)
                    if cap.isOpened():
                        ret, frame = cap.read()
                        if ret:
                            self.display_cv_image(frame)
                        else:
                            self.image_label.setText("无法获取视频帧")
                        cap.release()
                    else:
                        self.image_label.setText("无法打开视频文件")
                
                self.update_detect_button()
    
    def toggle_camera(self):
        """切换摄像头状态"""
        if self.video_thread is not None and self.video_thread.isRunning():
            # 如果摄像头正在运行，停止它
            self.stop_video()
            self.camera_btn.setText("启动摄像头")
            self.camera_btn.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60; 
                    color: white; 
                    padding: 15px; 
                    border-radius: 4px; 
                    font-size: 18px; 
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #2ecc71;
                }
            """)
        else:
            # 启动摄像头 - 总是使用默认摄像头
            self.video_thread = VideoThread(self.current_camera_index, True)
            self.video_thread.frame_ready.connect(self.update_frame)
            self.video_thread.connection_error.connect(self.handle_camera_error)
            self.video_thread.start()
            
            # 更新UI
            self.camera_btn.setText("停止摄像头")
            self.camera_btn.setStyleSheet("""
                QPushButton {
                    background-color: #c0392b; 
                    color: white; 
                    padding: 15px; 
                    border-radius: 4px; 
                    font-size: 18px; 
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #e74c3c;
                }
            """)
            self.image_path_label.setText("摄像头状态: 正在连接...")
            
            # 如果已选择模型，则启用检测按钮
            self.update_detect_button()
    
    def handle_camera_error(self, error_message):
        """处理摄像头连接错误"""
        self.statusBar.showMessage(error_message, 5000)
        self.image_path_label.setText("摄像头状态: 连接失败")
        self.image_label.setText(error_message)
        
        # 重置视频线程
        if self.video_thread is not None:
            self.video_thread.stop()
            self.video_thread = None
            
        # 重置UI状态
        self.camera_btn.setText("启动摄像头")
        self.camera_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; 
                color: white; 
                padding: 15px; 
                border-radius: 4px; 
                font-size: 18px; 
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.update_detect_button()
    
    def stop_video(self):
        """停止视频/摄像头流"""
        if self.video_thread is not None and self.video_thread.isRunning():
            self.video_thread.stop()
            self.video_thread = None
            
        # 如果是摄像头模式，清除当前帧和更新UI
        if self.detection_mode == "camera":
            self.current_frame = None
            self.camera_detection_active = False
            self.image_label.setText("摄像头已停止")
            self.image_path_label.setText("摄像头状态: 已停止")
            
        self.update_detect_button()
    
    def start_camera(self):
        """已弃用 - 现在使用toggle_camera()"""
        self.toggle_camera()
    
    def update_frame(self, frame):
        """更新视频帧"""
        self.current_frame = frame.copy()
        self.display_cv_image(frame)
        
        # 第一帧接收到，说明摄像头已成功连接
        if self.detection_mode == "camera" and not self.camera_detection_active:
            self.image_path_label.setText("摄像头状态: 已连接")
            
            # 如果已经有模型，自动开始检测
            if self.current_model_path:
                self.camera_detection_active = True
                self.detect_btn.setText("暂停检测")
                self.statusBar.showMessage("摄像头已启动，自动开始检测...", 3000)
        
        # 检查是否需要对摄像头帧进行检测
        if self.detection_mode == "camera" and self.camera_detection_active:
            self.frame_count += 1
            if self.frame_count >= self.detection_interval:
                self.frame_count = 0
                # 进行检测
                self.process_camera_frame(frame)
    
    def display_cv_image(self, cv_img):
        """显示OpenCV图像在QLabel上"""
        # 转换BGR到RGB
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        
        # 创建QImage
        qt_image = QImage(rgb_image.data, w, h, w * ch, QImage.Format.Format_RGB888)
        
        # 转换为QPixmap并显示
        pixmap = QPixmap.fromImage(qt_image)
        pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(),
                              Qt.AspectRatioMode.KeepAspectRatio,
                              Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
    
    def update_detect_button(self):
        """更新检测按钮状态"""
        if self.detection_mode == "image":
            # 图像模式：需要选择模型和图像
            self.detect_btn.setText("开始检测")
            if self.current_image_path and self.current_model_path:
                self.detect_btn.setEnabled(True)
            else:
                self.detect_btn.setEnabled(False)
        elif self.detection_mode == "video":
            # 视频模式：需要选择模型和视频
            self.detect_btn.setText("开始检测")
            if self.current_image_path and self.current_model_path:
                self.detect_btn.setEnabled(True)
            else:
                self.detect_btn.setEnabled(False)
        elif self.detection_mode == "camera":
            # 摄像头模式：需要选择模型并且摄像头运行中
            if self.camera_detection_active:
                self.detect_btn.setText("暂停检测")
            else:
                self.detect_btn.setText("开始检测")
                
            if self.current_model_path and self.video_thread is not None and self.video_thread.isRunning():
                self.detect_btn.setEnabled(True)
            else:
                self.detect_btn.setEnabled(False)
    
    def perform_detection(self):
        """执行检测操作"""
        if not self.current_model_path:
            self.statusBar.showMessage("请先选择模型", 5000)
            return
            
        # 禁用按钮，防止重复点击
        self.detect_btn.setEnabled(False)
        
        if self.detection_mode == "image":
            # 图像模式
            if not self.current_image_path:
                self.statusBar.showMessage("请先选择图像", 5000)
                self.detect_btn.setEnabled(True)
                return
                
            self.statusBar.showMessage("正在进行图像检测...")
            
            # 显示加载动画
            if self.loading_movie:
                self.result_icon_label.setMovie(self.loading_movie)
                self.loading_movie.start()
            else:
                self.result_class_label.setText("检测中...")
                self.result_prob_label.setText("")
            
            # 创建并启动预测线程
            self.prediction_thread = PredictionThread(self.current_model_path, self.current_image_path)
            self.prediction_thread.prediction_complete.connect(self.handle_prediction_result)
            self.prediction_thread.error_occurred.connect(self.handle_prediction_error)
            self.prediction_thread.finished.connect(lambda: self.detect_btn.setEnabled(True))
            self.prediction_thread.start()
            
        elif self.detection_mode == "video":
            # 视频模式
            if not self.current_image_path:
                self.statusBar.showMessage("请先选择视频", 5000)
                self.detect_btn.setEnabled(True)
                return
                
            self.statusBar.showMessage("正在启动视频检测...")
            
            # 先检查是否已经有视频在运行
            if self.video_thread is not None and self.video_thread.isRunning():
                self.stop_video()
            
            # 创建视频线程
            self.video_thread = VideoThread(self.current_image_path, False)
            self.video_thread.frame_ready.connect(self.process_video_frame)
            self.video_thread.video_finished.connect(self.handle_video_finished)
            self.video_thread.start()
            
            # 更新UI
            self.stop_camera_btn.setText("停止视频")
            self.stop_camera_btn.setEnabled(True)
            self.detect_btn.setEnabled(True)
            
        elif self.detection_mode == "camera":
            # 摄像头模式
            if self.video_thread is None or not self.video_thread.isRunning():
                self.statusBar.showMessage("请先启动摄像头", 5000)
                self.detect_btn.setEnabled(True)
                return
                
            self.statusBar.showMessage("正在启动摄像头检测...")
            
            # 切换摄像头检测状态
            if self.camera_detection_active:
                # 如果检测正在进行，停止检测
                self.camera_detection_active = False
                self.detect_btn.setText("开始检测")
                self.statusBar.showMessage("摄像头检测已暂停", 3000)
            else:
                # 开始检测
                self.camera_detection_active = True
                self.detect_btn.setText("暂停检测")
                self.statusBar.showMessage("摄像头检测已启动", 3000)
            
            self.detect_btn.setEnabled(True)
    
    def process_video_frame(self, frame):
        """处理视频帧进行检测"""
        # 显示当前帧
        self.display_cv_image(frame)
        
        # 每隔几帧进行一次检测，以提高效率
        # 这里可以添加一个帧计数器，每N帧检测一次
        
        # 进行检测
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # 创建图像预测线程
        self.image_prediction_thread = ImagePredictionThread(self.current_model_path, pil_image)
        self.image_prediction_thread.prediction_complete.connect(self.handle_frame_prediction)
        self.image_prediction_thread.error_occurred.connect(self.handle_prediction_error)
        self.image_prediction_thread.start()
    
    def process_camera_frame(self, frame):
        """处理摄像头帧进行检测"""
        # 检查是否已有检测线程正在运行
        if hasattr(self, 'image_prediction_thread') and self.image_prediction_thread.isRunning():
            return  # 如果上一个检测还未完成，则跳过这一帧的检测
            
        # 进行检测
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # 创建图像预测线程
        self.image_prediction_thread = ImagePredictionThread(self.current_model_path, pil_image)
        self.image_prediction_thread.prediction_complete.connect(self.handle_frame_prediction)
        self.image_prediction_thread.error_occurred.connect(self.handle_prediction_error)
        self.image_prediction_thread.start()
    
    def handle_frame_prediction(self, class_name, probability):
        """处理帧预测结果"""
        # 显示结果但不需要停止视频
        self.result_class_label.setText(f"检测结果: {class_name}")
        self.result_prob_label.setText(f"置信度: {probability:.2%}")
        
        # 更新结果图标
        if class_name == "health":
            self.result_icon_label.setStyleSheet("""
                background-color: #2ecc71; 
                border-radius: 30px;
                min-width: 60px; 
                min-height: 60px;
                border: 2px solid #27ae60;
            """)
            self.result_class_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2ecc71;")
        elif class_name == "swine_fever":
            self.result_icon_label.setStyleSheet("""
                background-color: #e74c3c; 
                border-radius: 30px;
                min-width: 60px; 
                min-height: 60px;
                border: 2px solid #c0392b;
            """)
            self.result_class_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #e74c3c;")
    
    def handle_video_finished(self):
        """处理视频播放结束"""
        self.statusBar.showMessage("视频检测完成", 5000)
        self.stop_video()
        self.detect_btn.setEnabled(True)
    
    def handle_prediction_result(self, class_name, probability):
        """处理预测结果"""
        if self.loading_movie:
            self.loading_movie.stop()
            
        # 显示结果
        self.result_class_label.setText(f"检测结果: {class_name}")
        self.result_prob_label.setText(f"置信度: {probability:.2%}")
        
        # 显示相应图标 - 使用更简洁的样式
        if class_name == "health":
            self.result_icon_label.setStyleSheet("""
                background-color: #2ecc71; 
                border-radius: 30px;
                min-width: 60px; 
                min-height: 60px;
                border: 2px solid #27ae60;
            """)
            self.result_class_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2ecc71;")
        elif class_name == "swine_fever":
            self.result_icon_label.setStyleSheet("""
                background-color: #e74c3c; 
                border-radius: 30px;
                min-width: 60px; 
                min-height: 60px;
                border: 2px solid #c0392b;
            """)
            self.result_class_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #e74c3c;")
        
        self.statusBar.showMessage(f"检测完成: {class_name} ({probability:.2%})", 5000)
    
    def handle_prediction_error(self, error_message):
        """处理预测错误"""
        if self.loading_movie:
            self.loading_movie.stop()
            
        self.result_class_label.setText("检测失败")
        self.result_class_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #e74c3c;")
        self.result_prob_label.setText(error_message)
        self.result_icon_label.setStyleSheet("")
        self.statusBar.showMessage(f"检测失败: {error_message}", 5000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 使用Fusion风格，在所有平台上看起来一致
    
    window = SwineFeverDetector()
    window.show()
    
    sys.exit(app.exec()) 