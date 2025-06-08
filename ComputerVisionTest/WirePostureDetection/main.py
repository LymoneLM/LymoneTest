import sys
import cv2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QGroupBox, QFileDialog, QSplitter, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QFont

from src.image_grayscale_inversion import get_invert_grayscale
from src.guided_filter_enhancement import get_guided_filter_enhancement
from src.bilateral_filter_enhancement import get_bilateral_filter_enhancement
from src.bouguet_stereo_rectification import get_stereo_rectification
from src.canny import get_canny_edge_detection
from src.pointpoint import generate_line_plot


class ImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("输电线舞动重建智能终端")
        self.setGeometry(100, 100, 1200, 700)

        # 初始化变量
        self.is_stereo = False
        self.original_image = None
        self.processed_image = None
        self.processed_left = None
        self.processed_right = None
        self.left_mask = None
        self.right_mask = None
        self.left_image = None
        self.right_image = None

        # 创建主界面
        self.initUI()

    def initUI(self):
        # 创建主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)

        # 创建标题的水平布局
        title_layout = QHBoxLayout()

        # 左侧LOGO
        left_logo_label = QLabel()
        left_logo_pixmap = QPixmap("./assets/1.png").scaledToHeight(50, Qt.SmoothTransformation)
        left_logo_label.setPixmap(left_logo_pixmap)
        left_logo_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_layout.addWidget(left_logo_label)

        # 标题
        title_label = QLabel("输电线舞动重建智能终端")
        title_font = QFont("Arial", 16, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("background-color: #2c3e50; color: white; padding: 10px;")
        main_layout.addWidget(title_label)

        title_layout.addWidget(title_label, 1)  # 添加伸缩因子使标题居中

        # 右侧LOGO
        right_logo_label = QLabel()
        right_logo_pixmap = QPixmap("./assets/2.png").scaledToHeight(50, Qt.SmoothTransformation)
        right_logo_label.setPixmap(right_logo_pixmap)
        right_logo_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        title_layout.addWidget(right_logo_label)

        # 将标题布局添加到主布局
        main_layout.addLayout(title_layout)

        # 内容区域
        content_layout = QHBoxLayout()

        # 左侧控制面板
        control_panel = QGroupBox("控制面板")
        control_panel.setMaximumWidth(300)
        control_layout = QVBoxLayout()

        # 图片导入区
        import_group = QGroupBox("相机控制")
        import_layout = QVBoxLayout()

        self.import_stereo_btn = QPushButton("导入图像")
        self.import_stereo_btn.setStyleSheet("background-color: #3498db; color: white; font-weight: bold;")
        self.import_stereo_btn.clicked.connect(self.import_stereo_images)

        self.transfer_btn = QPushButton("回置输出")
        self.transfer_btn.setToolTip("将输出图像移动到输入区")
        self.transfer_btn.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold;")
        self.transfer_btn.clicked.connect(self.transfer_result_to_input)

        self.save_image_btn = QPushButton("保存")
        self.save_image_btn.setStyleSheet("background-color: #00dd00; color: white; font-weight: bold;")
        self.save_image_btn.clicked.connect(self.save_image)

        self.exit_btn = QPushButton("退出")
        self.exit_btn.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
        self.exit_btn.clicked.connect(self.close)

        import_layout.addWidget(self.import_stereo_btn)
        import_layout.addWidget(self.transfer_btn)
        import_layout.addWidget(self.save_image_btn)
        import_layout.addWidget(self.exit_btn)
        import_group.setLayout(import_layout)

        # 功能选择区
        function_group = QGroupBox("功能选择")
        function_layout = QVBoxLayout()

        # 创建功能按钮
        self.gray_invert_btn = QPushButton("灰度反转")
        self.gray_invert_btn.setStyleSheet("background-color: #3498db; color: white;")
        self.gray_invert_btn.clicked.connect(lambda: self.process_image("灰度反转"))

        self.denoise_btn = QPushButton("图像去噪")
        self.denoise_btn.setStyleSheet("background-color: #3498db; color: white;")
        self.denoise_btn.clicked.connect(lambda: self.process_image("图像去噪"))

        self.stereo_rectify_btn = QPushButton("图像立体矫正")
        self.stereo_rectify_btn.setStyleSheet("background-color: #3498db; color: white;")
        self.stereo_rectify_btn.clicked.connect(lambda: self.process_image("图像立体矫正"))

        self.canny_edge_btn = QPushButton("边缘检测")
        self.canny_edge_btn.setStyleSheet("background-color: #3498db; color: white;")
        self.canny_edge_btn.clicked.connect(lambda: self.process_image("边缘检测"))

        self.generate_line_btn = QPushButton("曲线拟合")
        self.generate_line_btn.setStyleSheet("background-color: #3498db; color: white;")
        self.generate_line_btn.clicked.connect(lambda: self.process_image("曲线拟合"))

        # 添加到布局
        function_layout.addWidget(self.gray_invert_btn)
        function_layout.addWidget(self.denoise_btn)
        function_layout.addWidget(self.stereo_rectify_btn)
        function_layout.addWidget(self.canny_edge_btn)
        function_layout.addWidget(self.generate_line_btn)

        function_group.setLayout(function_layout)

        # 添加到控制面板
        control_layout.addWidget(import_group)
        control_layout.addWidget(function_group)
        control_layout.addStretch()
        control_panel.setLayout(control_layout)

        # 图像显示区
        image_panel = QGroupBox("图像显示")
        image_layout = QVBoxLayout()

        # 使用分割器以便调整大小
        splitter = QSplitter(Qt.Horizontal)

        # 原始图像显示 - 添加垂直布局包含图像和文字
        original_container = QWidget()
        original_layout = QVBoxLayout(original_container)
        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignCenter)
        self.original_label.setMinimumSize(400, 400)
        self.original_label.setStyleSheet("background-color: #ecf0f1; border: 1px solid #bdc3c7;")
        self.original_label.setText("原始图像显示区")

        # 添加原始图像文字说明
        original_text = QLabel("原图（左目）")
        original_text.setAlignment(Qt.AlignCenter)
        original_text.setFixedHeight(20)
        original_text.setStyleSheet("font-weight: bold; color: #2c3e50; background-color: #ecf0f1;")

        original_layout.addWidget(self.original_label)
        original_layout.addWidget(original_text)

        # 处理结果图像显示 - 添加垂直布局包含图像和文字
        processed_container = QWidget()
        processed_layout = QVBoxLayout(processed_container)
        self.processed_label = QLabel()
        self.processed_label.setAlignment(Qt.AlignCenter)
        self.processed_label.setMinimumSize(400, 400)
        self.processed_label.setStyleSheet("background-color: #ecf0f1; border: 1px solid #bdc3c7;")
        self.processed_label.setText("处理结果图像显示区")

        # 添加处理结果文字说明 - 初始状态
        self.processed_text = QLabel("处理结果")
        self.processed_text.setAlignment(Qt.AlignCenter)
        self.processed_text.setFixedHeight(20)
        self.processed_text.setStyleSheet("font-weight: bold; color: #2c3e50; background-color: #ecf0f1;")

        processed_layout.addWidget(self.processed_label)
        processed_layout.addWidget(self.processed_text)

        splitter.addWidget(original_container)
        splitter.addWidget(processed_container)
        splitter.setSizes([500, 500])

        image_layout.addWidget(splitter)
        image_panel.setLayout(image_layout)

        # 添加到内容布局
        content_layout.addWidget(control_panel)
        content_layout.addWidget(image_panel)

        main_layout.addLayout(content_layout)

        # 状态栏
        self.statusBar().showMessage("就绪")

    def transfer_result_to_input(self):
        if self.processed_image is None:
            QMessageBox.warning(self, "警告", "没有可转移的处理结果")
            return

        self.left_image = self.processed_left
        self.right_image = self.processed_right

        # 更新原始图像区显示左目图像
        self.display_image(self.left_image, self.original_label)

        # 清空处理结果区
        self.processed_image = None
        self.processed_label.clear()
        self.processed_label.setText("处理结果图像显示区")

        self.statusBar().showMessage("已将处理结果转移到输入区")


    def import_stereo_images(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "选择图像(双目图像先选左目后右目)", "", "图像文件 (*.png *.jpg *.bmp *.tif)"
        )

        if len(file_paths) >= 2:
            self.is_stereo = True
            self.left_image = cv2.imread(file_paths[0])
            self.right_image = cv2.imread(file_paths[1])

            if self.left_image is not None and self.right_image is not None:
                # 只显示左目图像在原始图像区
                self.display_image(self.left_image, self.original_label)
                self.statusBar().showMessage(f"已加载图像: {file_paths[0]} 和 {file_paths[1]}")
            else:
                QMessageBox.warning(self, "错误", "无法加载图像")
        else:
            self.is_stereo = False
            self.left_image = cv2.imread(file_paths[0])
            if self.left_image is not None:
                self.display_image(self.left_image, self.original_label)
                self.statusBar().showMessage(f"已加载图像: {file_paths[0]}")
            else:
                QMessageBox.warning(self, "错误", "无法加载图像")

    def save_image(self):
        if self.processed_left is None or self.processed_right is None:
            QMessageBox.warning(self, "警告", "无输出，保存失败")
            return
        output_path = "./output"
        cv2.imwrite(output_path+"/ui_output_left.png", self.processed_left)
        cv2.imwrite(output_path+"/ui_output_right.png", self.processed_right)

        self.statusBar().showMessage(f"已将处理结果保存到{output_path}")

    def process_image(self, function_name):
        if function_name == "图像立体矫正" and self.is_stereo == False:
            QMessageBox.warning(self, "警告", "请先导入双目图像")
            return

        # 根据功能名称设置处理结果文字说明
        text_map = {
            "灰度反转": "灰度反转结果",
            "图像去噪": "图像去噪结果",
            "图像立体矫正": "图像立体矫正结果",
            "边缘检测": "边缘检测结果",
            "曲线拟合": "曲线拟合结果"
        }
        self.processed_text.setText(text_map.get(function_name, "处理结果"))

        self.statusBar().showMessage(f"正在处理: {function_name}...")
        QApplication.processEvents()  # 更新UI

        try:
            if function_name == "灰度反转":
                self.processed_left = get_invert_grayscale(self.left_image)
                if self.is_stereo:
                    self.processed_right = get_invert_grayscale(self.right_image)
                self.processed_image = self.processed_left

            elif function_name == "图像去噪":
                self.processed_left = get_guided_filter_enhancement(self.left_image)
                if self.is_stereo:
                    # self.processed_right = get_guided_filter_enhancement(self.right_image)
                    self.processed_right = get_bilateral_filter_enhancement(self.right_image)
                self.processed_image = self.processed_left

            elif function_name == "图像立体矫正":
                self.processed_left, self.processed_right, self.left_mask, self.right_mask = get_stereo_rectification(
                    self.left_image, self.right_image
                )
                self.processed_image = self.processed_left

            elif function_name == "边缘检测":
                self.processed_left = get_canny_edge_detection(self.left_image)
                if self.left_mask is not None:
                    self.processed_left = cv2.bitwise_and(self.processed_left, self.left_mask)
                if self.is_stereo:
                    self.processed_right = get_canny_edge_detection(self.right_image)
                    if self.right_mask is not None:
                        self.processed_right = cv2.bitwise_and(self.processed_right, self.right_mask)
                self.processed_image = self.processed_left

            elif function_name == "曲线拟合":
                self.processed_left = generate_line_plot()
                if self.is_stereo:
                    self.processed_right = generate_line_plot()
                self.processed_image = self.processed_left

            # 显示处理结果
            self.display_image(self.processed_image, self.processed_label)
            self.statusBar().showMessage(f"{function_name} 处理完成")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理过程中发生错误: {str(e)}")
            self.statusBar().showMessage("处理失败")

    def display_image(self, image, label):
        """在QLabel上显示OpenCV图像"""
        if image is None:
            return

        # 将OpenCV BGR图像转换为RGB格式
        if len(image.shape) == 2:  # 灰度图像
            q_img = QImage(image.data, image.shape[1], image.shape[0],
                           image.strides[0], QImage.Format_Grayscale8)
        else:  # 彩色图像
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # 缩放图像以适应标签大小
        pixmap = QPixmap.fromImage(q_img)
        scaled_pixmap = pixmap.scaled(
            label.width() - 20, label.height() - 20,
            Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        """窗口大小改变时更新图像显示"""
        super().resizeEvent(event)
        if self.original_image is not None:
            self.display_image(self.original_image, self.original_label)
        if self.processed_image is not None:
            self.display_image(self.processed_image, self.processed_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())