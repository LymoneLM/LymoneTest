import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QTableWidget, QTableWidgetItem, QFrame, QHeaderView,
                            QFileDialog, QMessageBox)
from PyQt6.QtGui import QPixmap, QIcon, QColor
from PyQt6.QtCore import Qt, QSize

from utils.detection_history import get_detection_records, delete_detection_record


class HistoryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # 初始化变量
        self.history_records = []
        self.selected_record_id = None
        
        # 初始化UI
        self.init_ui()
        
    def init_ui(self):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 顶部标题
        title_label = QLabel("检测历史")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(title_label)
        
        # 历史记录表格
        self.create_history_table()
        main_layout.addWidget(self.history_table)
        
        # 底部按钮区域
        bottom_panel = QFrame()
        bottom_panel.setStyleSheet("background-color: #f8f9fa; border-radius: 8px; padding: 10px;")
        bottom_layout = QHBoxLayout(bottom_panel)
        
        # 左侧预览区
        self.preview_label = QLabel("选择记录查看预览")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("background-color: #ecf0f1; border-radius: 4px; padding: 10px;")
        self.preview_label.setMinimumSize(300, 200)
        self.preview_label.setMaximumSize(300, 200)
        bottom_layout.addWidget(self.preview_label)
        
        # 按钮容器
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)
        
        # 详情信息
        self.detail_label = QLabel("未选择记录")
        self.detail_label.setStyleSheet("font-size: 16px; color: #34495e; margin-bottom: 20px;")
        self.detail_label.setWordWrap(True)
        buttons_layout.addWidget(self.detail_label)
        
        # 按钮区域
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db; 
                color: white; 
                padding: 10px 20px; 
                border-radius: 4px; 
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.refresh_btn.clicked.connect(self.load_history)
        
        self.export_btn = QPushButton("导出所选")
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71; 
                color: white; 
                padding: 10px 20px; 
                border-radius: 4px; 
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.export_btn.clicked.connect(self.export_record)
        self.export_btn.setEnabled(False)
        
        self.delete_btn = QPushButton("删除所选")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; 
                color: white; 
                padding: 10px 20px; 
                border-radius: 4px; 
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_record)
        self.delete_btn.setEnabled(False)
        
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.delete_btn)
        
        buttons_layout.addWidget(btn_container)
        buttons_layout.addStretch()
        
        bottom_layout.addWidget(buttons_widget)
        
        main_layout.addWidget(bottom_panel)
        
        # 加载历史记录
        self.load_history()
        
    def create_history_table(self):
        """创建历史记录表格"""
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["ID", "检测结果", "置信度", "检测时间", "检测类型"])
        
        # 设置表格样式
        self.history_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                gridline-color: #dee2e6;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #dee2e6;
                color: #2c3e50;
                background-color: white;
            }
            QTableWidget::item:hover {
                background-color: #f8f9fa;
            }
            QTableWidget::item:selected {
                background-color: #2c3e50;
                color: white;
                font-weight: bold;
                border-left: 4px solid #3498db;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)
        
        # 设置列宽
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        
        # 设置选择行为
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.history_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # 连接信号
        self.history_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.history_table.cellClicked.connect(self.on_cell_clicked)
        
        # 禁用行交替颜色
        self.history_table.setAlternatingRowColors(False)
        
    def load_history(self):
        """加载历史记录"""
        print("正在加载历史记录...")
        # 重置表格
        self.history_table.setRowCount(0)
        self.history_records = []
        
        # 从数据库或文件加载记录
        records = get_detection_records()
        
        if not records:
            print("未找到历史记录")
            self.detail_label.setText("暂无历史记录")
            return
            
        self.history_records = records
        print(f"加载到{len(records)}条历史记录")
        
        # 填充表格
        self.history_table.setRowCount(len(records))
        
        for row, record in enumerate(records):
            # ID
            id_item = QTableWidgetItem(str(record["id"]))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 0, id_item)
            
            # 结果
            result = record["result"]
            # 将英文结果转换为中文显示
            display_result = "健康" if result == "health" else "猪瘟"
            result_item = QTableWidgetItem(display_result)
            result_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # 根据结果设置颜色，使用更高对比度的颜色
            if result == "health":
                result_item.setForeground(QColor("#157a3c"))  # 更深的绿色
            elif result == "swine_fever":
                result_item.setForeground(QColor("#c0392b"))  # 更深的红色
                
            self.history_table.setItem(row, 1, result_item)
            
            # 置信度
            confidence = "{:.2%}".format(record["confidence"])
            confidence_item = QTableWidgetItem(confidence)
            confidence_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 2, confidence_item)
            
            # 时间
            time_item = QTableWidgetItem(record["timestamp"])
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 3, time_item)
            
            # 类型 - 将英文类型转换为中文显示
            type_text = "图像"
            if record["type"] == "video":
                type_text = "视频"
                
            type_item = QTableWidgetItem(type_text)
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_table.setItem(row, 4, type_item)
        
        # 确保每个单元格文字颜色正确
        self.reset_all_text_colors()
        
    def on_selection_changed(self):
        """表格选择变化处理"""
        # 先恢复所有行的文字颜色，再处理新选中行
        self.reset_all_text_colors()
        
        selected_items = self.history_table.selectedItems()
        
        if not selected_items:
            # 重置预览和按钮状态
            self.preview_label.setText("选择记录查看预览")
            self.detail_label.setText("未选择记录")
            self.export_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
            self.selected_record_id = None
            return
            
        # 获取选中行
        row = self.history_table.currentRow()
        if row >= 0 and row < len(self.history_records):
            record = self.history_records[row]
            self.selected_record_id = record["id"]
            
            # 确保选中行的所有文字都是白色，增加可见性
            for col in range(self.history_table.columnCount()):
                item = self.history_table.item(row, col)
                if item:
                    item.setForeground(QColor("white"))
            
            # 显示图像预览
            if os.path.exists(record["image_path"]):
                pixmap = QPixmap(record["image_path"])
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(self.preview_label.width(), self.preview_label.height(),
                                         Qt.AspectRatioMode.KeepAspectRatio,
                                         Qt.TransformationMode.SmoothTransformation)
                    self.preview_label.setPixmap(pixmap)
                else:
                    self.preview_label.setText("无法加载图像")
                    print(f"无法加载图像: {record['image_path']}")
            else:
                self.preview_label.setText("图像文件不存在")
                print(f"图像文件不存在: {record['image_path']}")
                
            # 显示详情
            result_name = "健康" if record["result"] == "health" else "猪瘟"
            
            type_text = "图像"
            if record["type"] == "video":
                type_text = "视频"
            
            detail_text = (f"检测结果: {result_name}\n"
                          f"置信度: {record['confidence']:.2%}\n"
                          f"检测时间: {record['timestamp']}\n"
                          f"检测类型: {type_text}")
            self.detail_label.setText(detail_text)
            
            # 启用按钮
            self.export_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
        
    def on_cell_clicked(self, row, column):
        """单元格点击处理"""
        # 先重置所有文字颜色
        self.reset_all_text_colors()
        
        # 确保选中行的所有文字为白色
        for col in range(self.history_table.columnCount()):
            item = self.history_table.item(row, col)
            if item:
                item.setForeground(QColor("white"))
        
    def export_record(self):
        """导出所选记录"""
        if self.selected_record_id is None:
            QMessageBox.warning(self, "导出失败", "请先选择要导出的记录")
            return
            
        # 找到选中的记录
        record = next((r for r in self.history_records if r["id"] == self.selected_record_id), None)
        if not record:
            QMessageBox.warning(self, "导出失败", "找不到所选记录")
            return
            
        # 选择保存路径
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("图像文件 (*.jpg *.png)")
        file_dialog.setDefaultSuffix("jpg")
        file_dialog.setWindowTitle("导出检测结果")
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        result_text = "health" if record["result"] == "health" else "swine_fever"
        default_name = f"detection_{result_text}_{timestamp}.jpg"
        file_dialog.selectFile(default_name)
        
        if file_dialog.exec():
            save_path = file_dialog.selectedFiles()[0]
            
            # 检查源图像是否存在
            if os.path.exists(record["image_path"]):
                # 复制图像文件
                from shutil import copyfile
                try:
                    copyfile(record["image_path"], save_path)
                    QMessageBox.information(self, "导出成功", "检测结果已成功导出")
                except Exception as e:
                    QMessageBox.warning(self, "导出失败", f"导出失败: {str(e)}")
            else:
                QMessageBox.warning(self, "导出失败", "源图像文件不存在")
    
    def delete_record(self):
        """删除所选记录"""
        if self.selected_record_id is None:
            QMessageBox.warning(self, "删除失败", "请先选择要删除的记录")
            return
            
        # 确认删除
        reply = QMessageBox.question(self, "确认删除", 
                                    "确定要删除此检测记录吗？",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # 删除记录
            success = delete_detection_record(self.selected_record_id)
            
            if success:
                self.load_history()  # 重新加载列表
                self.preview_label.setText("选择记录查看预览")
                self.detail_label.setText("未选择记录")
                self.export_btn.setEnabled(False)
                self.delete_btn.setEnabled(False)
                self.selected_record_id = None
                QMessageBox.information(self, "删除成功", "检测记录已成功删除")
            else:
                QMessageBox.warning(self, "删除失败", "删除记录时发生错误")
                
    def reset_all_text_colors(self):
        """
        重置所有行的文字颜色
        - 检测结果列使用特殊颜色（健康为绿色，猪瘟为红色）
        - 其他列使用深灰色
        该方法在选择变化、点击和加载数据时都会被调用，确保颜色一致性
        """
        for row in range(self.history_table.rowCount()):
            # 对于检测结果列(索引1)，根据内容设置特定颜色
            result_item = self.history_table.item(row, 1)
            if result_item:
                result_text = result_item.text()
                if result_text == "健康":
                    result_item.setForeground(QColor("#157a3c"))  # 更深的绿色
                elif result_text == "猪瘟":
                    result_item.setForeground(QColor("#c0392b"))  # 更深的红色
            
            # 其他列使用黑色
            for col in range(self.history_table.columnCount()):
                if col != 1:  # 跳过检测结果列
                    item = self.history_table.item(row, col)
                    if item:
                        item.setForeground(QColor("#2c3e50"))  # 深灰色，比纯黑色柔和 