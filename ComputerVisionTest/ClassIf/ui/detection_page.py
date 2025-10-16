import sys
import os
import json
import cv2
import torch
import numpy as np
from PIL import Image
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QFileDialog, QGroupBox, QRadioButton, QButtonGroup, 
                            QFrame, QGridLayout, QSizePolicy, QMessageBox)
from PyQt6.QtGui import QPixmap, QImage, QMovie
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QTimer
from datetime import datetime

from utils.detection_history import add_detection_record

# 如果moudle目录不在Python路径中，则添加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from moudle.mobilenet import MobileNetV2
except ImportError:
    print("Error: 找不到MobileNetV2模型")

# 检测结果暂时存储
class DetectionResult:
    def __init__(self, result=None, confidence=0, timestamp=None, detection_type=None, image_path=None):
        self.result = result
        self.confidence = confidence
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.type = detection_type
        self.image_path = image_path
        
    def is_valid(self):
        return self.result is not None and self.image_path is not None


class VideoThread(QThread):
    """处理视频流的线程"""
    frame_ready = pyqtSignal(np.ndarray)
    video_finished = pyqtSignal()
    connection_error = pyqtSignal(str)
    
    def __init__(self, video_source=0, is_camera=False):
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


class DetectionPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # 初始化变量
        self.current_image_path = ""
        self.current_model_path = ""
        self.prediction_thread = None
        self.video_thread = None
        self.current_frame = None
        self.detection_mode = "image"  # 默认模式：image, video, camera
        
        # 初始化UI
        self.init_ui()
        
    def init_ui(self):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 顶部标题
        title_label = QLabel("识别检测")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(title_label)
        
        # 内容区域
        content_layout = QHBoxLayout()
        
        # 左侧控制面板
        control_panel = self.create_control_panel()
        content_layout.addWidget(control_panel)
        
        # 右侧预览与结果区域
        preview_panel = self.create_preview_panel()
        content_layout.addWidget(preview_panel, 1)  # 预览区域占据更多空间
        
        main_layout.addLayout(content_layout)
        
    def create_control_panel(self):
        """创建左侧控制面板"""
        control_panel = QFrame()
        control_panel.setObjectName("controlPanel")
        control_panel.setStyleSheet("""
            #controlPanel {
                background-color: #f8f9fa;
                border-radius: 10px;
                max-width: 350px;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-top: 15px;
                font-weight: bold;
                font-size: 14px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        control_layout = QVBoxLayout(control_panel)
        
        # 模型选择组
        model_group = QGroupBox("模型选择")
        model_layout = QVBoxLayout(model_group)
        
        self.select_model_btn = QPushButton("选择模型文件")
        self.select_model_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db; 
                color: white; 
                padding: 12px; 
                border-radius: 4px; 
                font-size: 14px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.select_model_btn.clicked.connect(self.browse_model)
        model_layout.addWidget(self.select_model_btn)
        
        self.model_info_label = QLabel("未加载模型")
        self.model_info_label.setStyleSheet("padding: 10px; background-color: #f5f5f5; border-radius: 4px; font-size: 13px;")
        self.model_info_label.setWordWrap(True)
        model_layout.addWidget(self.model_info_label)
        
        control_layout.addWidget(model_group)
        
        # 输入选择组
        input_group = QGroupBox("输入选择")
        input_layout = QVBoxLayout(input_group)
        
        # 输入模式选择
        mode_widget = QWidget()
        mode_layout = QHBoxLayout(mode_widget)
        mode_layout.setContentsMargins(0, 0, 0, 0)
        
        self.mode_group = QButtonGroup(self)
        
        self.image_mode_radio = QRadioButton("图像")
        self.image_mode_radio.setChecked(True)  # 默认选中
        self.image_mode_radio.toggled.connect(lambda: self.change_detection_mode("image"))
        
        self.video_mode_radio = QRadioButton("视频")
        self.video_mode_radio.toggled.connect(lambda: self.change_detection_mode("video"))
        
        self.camera_mode_radio = QRadioButton("摄像头")
        self.camera_mode_radio.toggled.connect(lambda: self.change_detection_mode("camera"))
        
        self.mode_group.addButton(self.image_mode_radio)
        self.mode_group.addButton(self.video_mode_radio)
        self.mode_group.addButton(self.camera_mode_radio)
        
        mode_layout.addWidget(self.image_mode_radio)
        mode_layout.addWidget(self.video_mode_radio)
        mode_layout.addWidget(self.camera_mode_radio)
        mode_layout.addStretch()
        
        input_layout.addWidget(mode_widget)
        
        # 文件选择按钮
        self.select_file_btn = QPushButton("选择文件")
        self.select_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; 
                color: white; 
                padding: 12px; 
                border-radius: 4px; 
                font-size: 14px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.select_file_btn.clicked.connect(self.browse_input)
        input_layout.addWidget(self.select_file_btn)
        
        # 文件信息/状态标签
        self.file_info_label = QLabel("未选择文件")
        self.file_info_label.setStyleSheet("padding: 10px; background-color: #f5f5f5; border-radius: 4px; font-size: 13px;")
        self.file_info_label.setWordWrap(True)
        input_layout.addWidget(self.file_info_label)
        
        control_layout.addWidget(input_group)
        
        # 检测按钮
        self.detect_btn = QPushButton("开始检测")
        self.detect_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6; 
                color: white; 
                padding: 15px; 
                border-radius: 4px; 
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.detect_btn.clicked.connect(self.perform_detection)
        self.detect_btn.setEnabled(False)
        control_layout.addWidget(self.detect_btn)
        
        # 填充底部空间
        control_layout.addStretch()
        
        return control_panel
    
    def create_preview_panel(self):
        """创建右侧预览与结果面板"""
        preview_panel = QFrame()
        preview_panel.setObjectName("previewPanel")
        preview_panel.setStyleSheet("""
            #previewPanel {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
        """)
        
        preview_layout = QVBoxLayout(preview_panel)
        
        # 图像预览区
        preview_container = QFrame()
        preview_container.setStyleSheet("""
            background-color: #f8f9fa;
            border-radius: 8px;
            border: 1px dashed #bdc3c7;
            padding: 10px;
        """)
        preview_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        preview_container_layout = QVBoxLayout(preview_container)
        
        self.image_label = QLabel("请选择输入源")
        self.image_label.setStyleSheet("color: #7f8c8d; font-size: 16px;")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumHeight(400)
        preview_container_layout.addWidget(self.image_label)
        
        preview_layout.addWidget(preview_container, 1)
        
        # 检测结果区
        results_container = QFrame()
        results_container.setStyleSheet("""
            background-color: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #ddd;
            max-height: 150px;
        """)
        
        results_layout = QHBoxLayout(results_container)
        
        # 结果图标
        self.result_icon_label = QLabel()
        self.result_icon_label.setFixedSize(80, 80)
        self.result_icon_label.setStyleSheet("border-radius: 40px;")
        results_layout.addWidget(self.result_icon_label)
        
        # 结果文本
        result_text_container = QWidget()
        result_text_layout = QVBoxLayout(result_text_container)
        
        self.result_class_label = QLabel("未进行检测")
        self.result_class_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        result_text_layout.addWidget(self.result_class_label)
        
        self.result_prob_label = QLabel("")
        self.result_prob_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        result_text_layout.addWidget(self.result_prob_label)
        
        # 添加保存结果按钮
        self.save_result_btn = QPushButton("保存结果")
        self.save_result_btn.setStyleSheet("""
            QPushButton {
                background-color: #2980b9; 
                color: white; 
                padding: 8px 12px; 
                border-radius: in, 4px; 
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)
        self.save_result_btn.setVisible(False)  # 初始隐藏
        self.save_result_btn.clicked.connect(self.save_detection_result)
        result_text_layout.addWidget(self.save_result_btn)
        
        result_text_layout.addStretch()
        results_layout.addWidget(result_text_container, 1)
        
        preview_layout.addWidget(results_container)
        
        # 状态栏
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("color: #7f8c8d; padding: 5px;")
        preview_layout.addWidget(self.status_label)
        
        return preview_panel
    
    def browse_model(self):
        """浏览选择模型文件"""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("PyTorch模型 (*.pth)")
        file_dialog.setWindowTitle("选择模型文件")
        
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                model_path = selected_files[0]
                model_name = os.path.basename(model_path)
                self.update_model_info(model_path, model_name)
    
    def update_model_info(self, model_path, model_name):
        """更新模型信息显示"""
        if model_path:
            self.current_model_path = model_path
            model_info = f"选择的模型: {model_name}\n路径: {model_path}"
            self.model_info_label.setText(model_info)
            self.status_label.setText(f"已加载模型: {model_name}")
            self.update_detect_button()
    
    def change_detection_mode(self, mode):
        """切换检测模式"""
        self.detection_mode = mode
        
        # 停止任何正在进行的视频流
        if self.video_thread is not None and self.video_thread.isRunning():
            self.stop_video()
        
        # 更新UI元素
        if mode == "image":
            self.select_file_btn.setVisible(True)
            self.select_file_btn.setText("选择图像文件")
            self.select_file_btn.setEnabled(True)
            self.file_info_label.setText("未选择图像")
            self.status_label.setText("图像模式已选择")
        elif mode == "video":
            self.select_file_btn.setVisible(True)
            self.select_file_btn.setText("选择视频文件")
            self.select_file_btn.setEnabled(True)
            self.file_info_label.setText("未选择视频")
            self.status_label.setText("视频模式已选择")
        elif mode == "camera":
            self.select_file_btn.setVisible(True)
            self.select_file_btn.setText("摄像头测试")
            self.select_file_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e67e22; 
                    color: white; 
                    padding: 12px; 
                    border-radius: 4px; 
                    font-size: 14px;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: #d35400;
                }
            """)
            self.select_file_btn.clicked.disconnect()  # 断开原有连接
            self.select_file_btn.clicked.connect(self.debug_camera)  # 连接到调试方法
            self.file_info_label.setText("摄像头模式：点击检测按钮启动摄像头")
            self.status_label.setText("摄像头模式已选择")
            
            # 检测摄像头是否可用
            self.status_label.setText("正在检测可用摄像头...")
            print("开始尝试检测摄像头...")
            
            # 尝试多个摄像头ID
            available_cameras = []
            for camera_id in range(3):  # 尝试0, 1, 2三个ID
                try:
                    print(f"尝试检测摄像头ID: {camera_id}")
                    cap = cv2.VideoCapture(camera_id)
                    if cap.isOpened():
                        # 读取一帧确认可用
                        ret, _ = cap.read()
                        if ret:
                            available_cameras.append(camera_id)
                            print(f"找到可用摄像头，ID: {camera_id}")
                    cap.release()
                except Exception as e:
                    print(f"检测摄像头ID {camera_id} 时出错: {str(e)}")
            
            if available_cameras:
                self.current_image_path = available_cameras[0]  # 使用第一个可用的摄像头
                self.status_label.setText(f"摄像头已连接 (ID:{self.current_image_path})，可以启动")
                self.file_info_label.setText(f"摄像头模式：已找到可用摄像头 (ID:{self.current_image_path})")
                print(f"将使用摄像头ID: {self.current_image_path}")
            else:
                self.current_image_path = None
                self.status_label.setText("未检测到可用摄像头")
                self.file_info_label.setText("摄像头模式：未检测到可用摄像头")
                print("未找到任何可用摄像头")
            
            # 在摄像头模式下，直接启用检测按钮
            self.update_detect_button()
            
        # 清除预览图像
        self.image_label.setText("请选择输入源")
        if mode != "camera":
            self.current_image_path = ""
        
        # 重置检测结果
        self.reset_detection_result()
        
        # 更新检测按钮状态
        self.update_detect_button()
    
    def browse_input(self):
        """浏览选择输入文件"""
        file_dialog = QFileDialog()
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
                file_name = os.path.basename(file_path)
                self.file_info_label.setText(f"已选择文件: {file_name}")
                self.status_label.setText(f"已选择文件: {file_name}")
                
                # 重置检测结果
                self.reset_detection_result()
                
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
                        self.status_label.setText("错误: 无法加载图像")
                elif self.detection_mode == "video":
                    # 显示视频第一帧作为预览
                    cap = cv2.VideoCapture(file_path)
                    if cap.isOpened():
                        ret, frame = cap.read()
                        if ret:
                            self.display_cv_image(frame)
                        else:
                            self.image_label.setText("无法获取视频帧")
                            self.status_label.setText("错误: 无法获取视频帧")
                        cap.release()
                    else:
                        self.image_label.setText("无法打开视频文件")
                        self.status_label.setText("错误: 无法打开视频文件")
                
                self.update_detect_button()
    
    def stop_video(self):
        """停止视频/摄像头流"""
        if self.video_thread is not None and self.video_thread.isRunning():
            self.video_thread.stop()
            self.video_thread = None
            
        self.current_frame = None
        
        if self.detection_mode == "camera":
            self.image_label.setText("摄像头已停止")
            self.status_label.setText("摄像头已停止")
            self.file_info_label.setText("摄像头模式：点击检测按钮启动摄像头")
        else:
            self.image_label.setText("视频已停止")
            self.status_label.setText("视频已停止")
            
        self.update_detect_button()
    
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
            # 摄像头模式：需要选择模型且检测到摄像头
            self.detect_btn.setText("启动摄像头")
            if self.current_model_path and self.current_image_path is not None:
                self.detect_btn.setEnabled(True)
                print("摄像头模式：检测按钮已启用")
            else:
                if not self.current_model_path:
                    print("摄像头模式：未选择模型，按钮禁用")
                if self.current_image_path is None:
                    print("摄像头模式：未检测到摄像头，按钮禁用")
                self.detect_btn.setEnabled(False)
    
    def perform_detection(self):
        """执行检测操作"""
        if not self.current_model_path:
            self.status_label.setText("请先选择模型")
            return
            
        # 禁用按钮，防止重复点击
        self.detect_btn.setEnabled(False)
        
        if self.detection_mode == "image":
            # 图像模式
            if not self.current_image_path:
                self.status_label.setText("请先选择图像")
                self.detect_btn.setEnabled(True)
                return
                
            self.status_label.setText("正在进行图像检测...")
            
            # 加载图像
            try:
                image = Image.open(self.current_image_path).convert('RGB')
                
                # 创建图像预测线程
                self.prediction_thread = ImagePredictionThread(self.current_model_path, image)
                self.prediction_thread.prediction_complete.connect(self.handle_prediction_result)
                self.prediction_thread.error_occurred.connect(self.handle_prediction_error)
                self.prediction_thread.finished.connect(lambda: self.detect_btn.setEnabled(True))
                self.prediction_thread.start()
            except Exception as e:
                self.status_label.setText(f"错误: {str(e)}")
                self.detect_btn.setEnabled(True)
            
        elif self.detection_mode == "video":
            # 视频模式
            if not self.current_image_path:
                self.status_label.setText("请先选择视频")
                self.detect_btn.setEnabled(True)
                return
                
            self.status_label.setText("正在启动视频检测...")
            
            # 先检查是否已经有视频在运行
            if self.video_thread is not None and self.video_thread.isRunning():
                self.stop_video()
            
            # 创建视频线程
            self.video_thread = VideoThread(self.current_image_path, False)
            self.video_thread.frame_ready.connect(self.process_video_frame)
            self.video_thread.video_finished.connect(self.handle_video_finished)
            self.video_thread.start()
            
            # 更新UI
            self.detect_btn.setEnabled(True)
            
        elif self.detection_mode == "camera":
            # 摄像头模式
            self.status_label.setText("正在启动摄像头...")
            
            # 先检查是否已经有视频在运行
            if self.video_thread is not None and self.video_thread.isRunning():
                self.stop_video()
                self.detect_btn.setText("启动摄像头")
                self.detect_btn.setEnabled(True)
                return
            
            # 创建视频线程，使用之前确认可用的摄像头ID
            try:
                print(f"尝试启动摄像头，ID: {self.current_image_path}")
                self.video_thread = VideoThread(self.current_image_path, True)  # 设置is_camera为True
                self.video_thread.frame_ready.connect(self.process_video_frame)
                # 仅使用一个错误处理，避免冲突
                self.video_thread.connection_error.connect(lambda msg: 
                    QMessageBox.critical(self, "摄像头错误", f"无法启动摄像头: {msg}"))
                # 开始线程
                self.video_thread.start()
            except Exception as e:
                QMessageBox.critical(self, "系统错误", f"启动摄像头时发生错误: {str(e)}")
                self.detect_btn.setEnabled(True)
                return
            
            # 更新UI
            self.detect_btn.setText("停止摄像头")
            self.detect_btn.setEnabled(True)
            self.file_info_label.setText("摄像头正在运行...")
    
    def process_video_frame(self, frame):
        """处理视频帧进行检测"""
        # 显示当前帧
        self.display_cv_image(frame)
        
        # 进行检测
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # 创建图像预测线程
        self.image_prediction_thread = ImagePredictionThread(self.current_model_path, pil_image)
        self.image_prediction_thread.prediction_complete.connect(self.handle_frame_prediction)
        self.image_prediction_thread.error_occurred.connect(self.handle_prediction_error)
        self.image_prediction_thread.start()
    
    def handle_prediction_result(self, class_name, probability):
        """处理预测结果"""
        # 将英文结果转为中文显示
        result_cn = "健康" if class_name == "health" else "猪瘟"
        
        # 显示结果
        self.result_class_label.setText(f"检测结果: {result_cn}")
        self.result_prob_label.setText(f"置信度: {probability:.2%}")
        
        # 显示相应图标
        if class_name == "health":
            self.result_icon_label.setStyleSheet("""
                background-color: #2ecc71; 
                border-radius: 40px;
                min-width: 80px; 
                min-height: 80px;
                border: 2px solid #27ae60;
            """)
            self.result_class_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2ecc71;")
        elif class_name == "swine_fever":
            self.result_icon_label.setStyleSheet("""
                background-color: #e74c3c; 
                border-radius: 40px;
                min-width: 80px; 
                min-height: 80px;
                border: 2px solid #c0392b;
            """)
            self.result_class_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #e74c3c;")
        
        self.status_label.setText(f"检测完成: {result_cn} ({probability:.2%})")
        
        # 显示保存结果按钮
        self.save_result_btn.setVisible(True)
        
        # 存储当前检测结果
        self.current_detection_result = {
            "class_name": class_name,
            "probability": probability,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": self.detection_mode
        }
    
    def handle_frame_prediction(self, class_name, probability):
        """处理帧预测结果"""
        # 将英文结果转为中文显示
        result_cn = "健康" if class_name == "health" else "猪瘟"
        
        # 显示结果但不需要停止视频
        self.result_class_label.setText(f"检测结果: {result_cn}")
        self.result_prob_label.setText(f"置信度: {probability:.2%}")
        
        # 更新结果图标
        if class_name == "health":
            self.result_icon_label.setStyleSheet("""
                background-color: #2ecc71; 
                border-radius: 40px;
                min-width: 80px; 
                min-height: 80px;
                border: 2px solid #27ae60;
            """)
            self.result_class_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2ecc71;")
        elif class_name == "swine_fever":
            self.result_icon_label.setStyleSheet("""
                background-color: #e74c3c; 
                border-radius: 40px;
                min-width: 80px; 
                min-height: 80px;
                border: 2px solid #c0392b;
            """)
            self.result_class_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #e74c3c;")
        
        # 显示保存结果按钮
        self.save_result_btn.setVisible(True)
        
        # 存储当前检测结果
        self.current_detection_result = {
            "class_name": class_name,
            "probability": probability,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": self.detection_mode
        }
        
        # 更新状态栏
        detection_type = "视频检测" if self.detection_mode == "video" else "摄像头检测"
        self.status_label.setText(f"{detection_type}: {result_cn} ({probability:.2%})")
    
    def handle_video_finished(self):
        """处理视频播放结束"""
        self.status_label.setText("视频检测完成")
        self.stop_video()
        self.detect_btn.setEnabled(True)
    
    def handle_prediction_error(self, error_message):
        """处理预测错误"""
        self.result_class_label.setText("检测失败")
        self.result_class_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #e74c3c;")
        self.result_prob_label.setText(error_message)
        self.result_icon_label.setStyleSheet("")
        self.status_label.setText(f"检测失败: {error_message}")
    
    def reset_detection_result(self):
        """重置检测结果"""
        self.result_class_label.setText("未进行检测")
        self.result_class_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        self.result_prob_label.setText("")
        self.result_icon_label.setStyleSheet("")
        self.save_result_btn.setVisible(False)
        self.current_detection_result = None
    
    def save_detection_result(self):
        """保存检测结果到历史记录"""
        if hasattr(self, 'current_detection_result') and self.current_detection_result:
            # 获取图像或当前帧的截图
            if self.detection_mode == "image":
                image_path = self.current_image_path
                # 调用工具函数保存记录
                success = add_detection_record(
                    self.current_detection_result["class_name"],
                    self.current_detection_result["probability"],
                    self.current_detection_result["timestamp"],
                    self.detection_mode,
                    image_path
                )
            else:  # 视频模式
                if self.current_frame is not None:
                    # 为当前帧创建临时文件路径
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    temp_dir = "temp_frames"
                    os.makedirs(temp_dir, exist_ok=True)
                    temp_path = os.path.join(temp_dir, f"frame_{timestamp}.jpg")
                    
                    # 保存当前帧
                    cv2.imwrite(temp_path, self.current_frame)
                    
                    # 调用工具函数保存记录
                    success = add_detection_record(
                        self.current_detection_result["class_name"],
                        self.current_detection_result["probability"],
                        self.current_detection_result["timestamp"],
                        self.detection_mode,
                        temp_path
                    )
                else:
                    success = False
                    print("无法保存检测结果：没有可用的图像帧")
            
            if success:
                self.status_label.setText("检测结果已保存到历史记录")
                self.save_result_btn.setVisible(False)
                
                # 通知用户可以查看历史记录
                QMessageBox.information(self, "保存成功", 
                                       "检测结果已成功保存！\n可以在'检测历史'页面查看。")
            else:
                self.status_label.setText("保存检测结果失败")
                QMessageBox.warning(self, "保存失败", 
                                   "保存检测结果失败，请重试。")
        else:
            self.status_label.setText("没有可保存的检测结果")
            QMessageBox.warning(self, "保存失败", 
                               "没有可保存的检测结果，请先进行检测。")
    
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

    def update_frame(self, frame):
        """更新视频帧"""
        self.current_frame = frame.copy()
        self.display_cv_image(frame)

    def debug_camera(self):
        """调试摄像头问题"""
        print("\n===== 摄像头调试信息 =====")
        print(f"当前检测模式: {self.detection_mode}")
        print(f"当前摄像头ID: {self.current_image_path}")
        print(f"摄像头按钮状态: {'启用' if self.detect_btn.isEnabled() else '禁用'}")
        print(f"模型路径: {self.current_model_path}")
        
        # 尝试直接用OpenCV测试摄像头
        for i in range(3):  # 测试ID 0,1,2
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        print(f"摄像头ID {i} 可用，成功读取一帧")
                        # 保存测试图像
                        test_dir = "camera_tests"
                        os.makedirs(test_dir, exist_ok=True)
                        test_path = os.path.join(test_dir, f"camera_{i}_test.jpg")
                        cv2.imwrite(test_path, frame)
                        print(f"已保存测试图像到 {test_path}")
                    else:
                        print(f"摄像头ID {i} 打开成功但无法读取帧")
                else:
                    print(f"摄像头ID {i} 无法打开")
                cap.release()
            except Exception as e:
                print(f"测试摄像头ID {i} 时出错: {str(e)}")
                
        print("===== 调试信息结束 =====\n")
        
        # 显示结果
        QMessageBox.information(self, "摄像头调试", "摄像头调试信息已输出到控制台\n请查看控制台了解详情") 