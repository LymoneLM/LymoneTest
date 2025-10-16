import sys
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QStackedWidget, QLabel, QFrame,
                            QSizePolicy)
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt, QSize

from ui.detection_page import DetectionPage
from ui.history_page import HistoryPage
from ui.analysis_page import AnalysisPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 设置窗口标题和大小
        self.setWindowTitle("猪瘟智能检测系统")
        self.setMinimumSize(1200, 800)
        
        # 设置应用样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QPushButton {
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #5dade2;
                color: white;
            }
            QPushButton#activeButton {
                background-color: #3498db;
                color: white;
                border-left: 5px solid #2980b9;
            }
        """)
        
        # 创建中央窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建主布局
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 创建左侧导航栏
        self.create_sidebar()
        
        # 创建右侧内容区域
        self.create_content_area()
        
        # 默认显示检测页面
        self.show_detection_page()
        
    def create_sidebar(self):
        """创建左侧导航栏"""
        # 侧边栏容器
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setStyleSheet("""
            #sidebar {
                background-color: #34495e;
                min-width: 220px;
                max-width: 220px;
            }
        """)
        
        # 侧边栏布局
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # 应用标题 - 使用最简单的方式
        title_container = QFrame()
        title_container.setStyleSheet("background-color: #2c3e50;")
        title_container.setMinimumHeight(120)
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(15, 15, 15, 15)
        
        # 使用两个标签，一个是中文"猪瘟"，一个是中文"智能检测系统"
        label1 = QLabel("猪瘟")
        label1.setStyleSheet("color: white; font-size: 24px; font-weight: bold; letter-spacing: 2px;")
        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label2 = QLabel("智能检测系统")
        label2.setStyleSheet("color: white; font-size: 20px; font-weight: bold; letter-spacing: 1px;")
        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 添加一个英文标题作为备选
        label_en = QLabel("SWINE FEVER DETECTION")
        label_en.setStyleSheet("color: #3498db; font-size: 12px; margin-top: 5px; letter-spacing: 1px;")
        label_en.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_layout.addWidget(label1)
        title_layout.addWidget(label2)
        title_layout.addWidget(label_en)
        sidebar_layout.addWidget(title_container)
        
        # 导航按钮
        self.detection_btn = QPushButton("识别检测")
        try:
            self.detection_btn.setIcon(QIcon("icons/detect.png"))
            self.detection_btn.setIconSize(QSize(22, 22))
        except:
            print("无法加载检测图标")
        
        self.history_btn = QPushButton("检测历史")
        try:
            self.history_btn.setIcon(QIcon("icons/history.png"))
            self.history_btn.setIconSize(QSize(22, 22))
        except:
            print("无法加载历史图标")
        
        self.analysis_btn = QPushButton("可视化分析")
        try:
            self.analysis_btn.setIcon(QIcon("icons/analysis.png"))
            self.analysis_btn.setIconSize(QSize(22, 22))
        except:
            print("无法加载分析图标")
        
        # 设置样式和点击事件
        for btn in [self.detection_btn, self.history_btn, self.analysis_btn]:
            btn.setStyleSheet("color: white; padding-left: 20px;")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)  # 设置鼠标悬停时的光标形状
        
        # 确保正确连接信号和槽
        self.detection_btn.clicked.connect(self.show_detection_page)
        self.history_btn.clicked.connect(self.show_history_page)
        self.analysis_btn.clicked.connect(self.show_analysis_page)
        
        sidebar_layout.addWidget(self.detection_btn)
        sidebar_layout.addWidget(self.history_btn)
        sidebar_layout.addWidget(self.analysis_btn)
        
        # 底部填充
        sidebar_layout.addStretch()
        
        # 添加到主布局
        self.main_layout.addWidget(self.sidebar)
        
    def create_content_area(self):
        """创建右侧内容区域"""
        # 内容区域容器
        self.content_area = QFrame()
        self.content_area.setStyleSheet("background-color: white;")
        
        # 内容区域布局
        content_layout = QVBoxLayout(self.content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # 堆叠式窗口部件，用于切换不同的页面
        self.stacked_widget = QStackedWidget()
        
        # 创建各个页面
        self.detection_page = DetectionPage(self)
        self.history_page = HistoryPage(self)
        self.analysis_page = AnalysisPage(self)
        
        # 添加页面到堆叠窗口部件
        self.stacked_widget.addWidget(self.detection_page)
        self.stacked_widget.addWidget(self.history_page)
        self.stacked_widget.addWidget(self.analysis_page)
        
        content_layout.addWidget(self.stacked_widget)
        
        # 添加到主布局
        self.main_layout.addWidget(self.content_area, 1)  # 1表示拉伸因子，使内容区域填充剩余空间
    
    def show_detection_page(self):
        """显示检测页面"""
        print("切换到检测页面")  # 调试信息
        self.stacked_widget.setCurrentWidget(self.detection_page)
        self.set_active_button(self.detection_btn)
        
    def show_history_page(self):
        """显示历史页面"""
        print("切换到历史页面")  # 调试信息
        self.stacked_widget.setCurrentWidget(self.history_page)
        self.set_active_button(self.history_btn)
        
    def show_analysis_page(self):
        """显示分析页面"""
        print("切换到分析页面")  # 调试信息
        self.stacked_widget.setCurrentWidget(self.analysis_page)
        self.set_active_button(self.analysis_btn)
        
    def set_active_button(self, active_button):
        """设置当前活动按钮样式"""
        # 重置所有按钮样式
        for btn in [self.detection_btn, self.history_btn, self.analysis_btn]:
            btn.setObjectName("")
            btn.setStyleSheet("color: white; padding-left: 20px;")
            
        # 设置活动按钮样式
        active_button.setObjectName("activeButton")
        active_button.setStyleSheet("color: white; padding-left: 20px;")
        active_button.style().unpolish(active_button)
        active_button.style().polish(active_button) 