import sys
import os
import numpy as np
import matplotlib
matplotlib.use('QtAgg')

# 设置中文字体支持
from matplotlib import font_manager
try:
    # 优先使用系统中的中文字体
    chinese_fonts = ['SimHei', 'Microsoft YaHei', 'SimSun', 'KaiTi', 'FangSong']
    available_fonts = [f.name for f in font_manager.fontManager.ttflist]
    
    # 查找可用的中文字体
    font_found = False
    for chinese_font in chinese_fonts:
        if chinese_font in available_fonts:
            matplotlib.rcParams['font.family'] = [chinese_font]
            matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
            font_found = True
            print(f"使用中文字体: {chinese_font}")
            break
    
    if not font_found:
        print("未找到合适的中文字体，尝试使用默认字体...")
        # 如果找不到中文字体，尝试使用默认无衬线字体
        matplotlib.rcParams['font.family'] = 'sans-serif'
except Exception as e:
    print(f"配置中文字体时出错: {str(e)}")
    # 出错时使用默认字体
    matplotlib.rcParams['font.family'] = 'sans-serif'

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QFrame, QComboBox, QGridLayout, QGroupBox, QMessageBox)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
from datetime import datetime

from utils.detection_history import get_detection_statistics, get_detection_records


class MatplotlibCanvas(FigureCanvas):
    """用于显示Matplotlib图表的画布"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # 添加更多间距，避免文字被截断
        self.fig.subplots_adjust(left=0.18, right=0.92, bottom=0.22, top=0.85)
        self.axes = self.fig.add_subplot(111)
        super(MatplotlibCanvas, self).__init__(self.fig)


class AnalysisPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # 初始化UI
        self.init_ui()
        
    def init_ui(self):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 顶部标题
        title_label = QLabel("可视化分析")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(title_label)
        
        # 控制面板
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)
        
        # 图表区域
        charts_container = QFrame()
        charts_container.setStyleSheet("background-color: white; border-radius: 8px; border: 1px solid #ddd;")
        charts_layout = QGridLayout(charts_container)
        charts_layout.setContentsMargins(20, 20, 20, 20)  # 增加更多内边距
        charts_layout.setSpacing(30)  # 增加更多图表间距
        
        # 创建图表
        # 1. 检测结果分布
        result_distribution_group = QGroupBox("检测结果分布")
        result_distribution_group.setMinimumHeight(300)  # 设置最小高度
        result_layout = QVBoxLayout(result_distribution_group)
        result_layout.setContentsMargins(10, 25, 10, 10)  # 增加顶部边距，为标题留出空间
        self.result_canvas = MatplotlibCanvas(width=5, height=4)
        result_layout.addWidget(self.result_canvas)
        
        # 2. 检测置信度分布
        confidence_group = QGroupBox("置信度分布")
        confidence_group.setMinimumHeight(300)  # 设置最小高度
        confidence_layout = QVBoxLayout(confidence_group)
        confidence_layout.setContentsMargins(10, 25, 10, 10)  # 增加顶部边距
        self.confidence_canvas = MatplotlibCanvas(width=5, height=4)
        confidence_layout.addWidget(self.confidence_canvas)
        
        # 3. 检测时间趋势
        time_trend_group = QGroupBox("检测时间趋势")
        time_trend_group.setMinimumHeight(330)  # 增加高度为日期标签提供更多空间
        time_layout = QVBoxLayout(time_trend_group)
        time_layout.setContentsMargins(10, 25, 10, 10)  # 增加顶部边距
        self.time_canvas = MatplotlibCanvas(width=5, height=4)
        time_layout.addWidget(self.time_canvas)
        
        # 4. 检测类型分布
        type_distribution_group = QGroupBox("检测类型分布")
        type_distribution_group.setMinimumHeight(330)  # 增加高度为类型标签提供更多空间
        type_layout = QVBoxLayout(type_distribution_group)
        type_layout.setContentsMargins(10, 25, 10, 10)  # 增加顶部边距
        self.type_canvas = MatplotlibCanvas(width=5, height=4)
        type_layout.addWidget(self.type_canvas)
        
        # 添加到网格布局中
        charts_layout.addWidget(result_distribution_group, 0, 0)
        charts_layout.addWidget(confidence_group, 0, 1)
        charts_layout.addWidget(time_trend_group, 1, 0)
        charts_layout.addWidget(type_distribution_group, 1, 1)
        
        main_layout.addWidget(charts_container)
        
        # 加载初始数据
        QMessageBox.information(self, "提示", "正在加载分析数据，首次加载可能需要一些时间...")
        self.update_charts()
        
    def create_control_panel(self):
        """创建控制面板"""
        control_panel = QFrame()
        control_panel.setStyleSheet("background-color: #f8f9fa; border-radius: 8px; padding: 10px; margin-bottom: 20px;")
        control_layout = QHBoxLayout(control_panel)
        
        # 时间范围选择
        period_label = QLabel("时间范围:")
        period_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        
        self.period_combo = QComboBox()
        self.period_combo.addItems(["全部时间", "今天", "最近7天", "最近30天"])
        self.period_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 6px;
                min-width: 150px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.period_combo.currentIndexChanged.connect(self.update_charts)
        
        # 刷新按钮
        self.refresh_btn = QPushButton("刷新数据")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db; 
                color: white; 
                padding: 8px 16px; 
                border-radius: 4px; 
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.refresh_btn.clicked.connect(self.update_charts)
        
        # 导出按钮
        self.export_btn = QPushButton("导出图表")
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71; 
                color: white; 
                padding: 8px 16px; 
                border-radius: 4px; 
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.export_btn.clicked.connect(self.export_charts)
        
        # 添加到布局
        control_layout.addWidget(period_label)
        control_layout.addWidget(self.period_combo)
        control_layout.addStretch()
        control_layout.addWidget(self.refresh_btn)
        control_layout.addWidget(self.export_btn)
        
        return control_panel
    
    def update_charts(self):
        """更新所有图表"""
        # 获取选择的时间范围
        period = self.period_combo.currentText()
        print(f"正在更新图表，选择的时间范围: {period}")
        
        # 禁用刷新按钮，防止重复点击
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setText("加载中...")
        
        # 获取数据
        try:
            stats = get_detection_statistics(period)
            records = get_detection_records(period)
            
            if not records:
                print("未找到检测记录，显示空图表")
                # 没有数据时显示空图表
                self.show_empty_charts()
                self.refresh_btn.setEnabled(True)
                self.refresh_btn.setText("刷新数据")
                return
                
            print(f"加载到{len(records)}条检测记录")
            
            # 更新结果分布饼图
            self.update_result_distribution(stats)
            
            # 更新置信度直方图
            self.update_confidence_histogram(records)
            
            # 更新时间趋势
            self.update_time_trend(records)
            
            # 更新类型分布
            self.update_type_distribution(stats)
        except Exception as e:
            print(f"更新图表时发生错误: {str(e)}")
            QMessageBox.warning(self, "更新失败", f"更新图表时发生错误: {str(e)}")
            self.show_empty_charts()
        finally:
            # 恢复刷新按钮
            self.refresh_btn.setEnabled(True)
            self.refresh_btn.setText("刷新数据")
    
    def update_result_distribution(self, stats):
        """更新结果分布饼图"""
        ax = self.result_canvas.axes
        ax.clear()
        
        labels = ['健康', '猪瘟']
        sizes = [stats.get('health_count', 0), stats.get('swine_fever_count', 0)]
        
        if sum(sizes) == 0:
            ax.text(0.5, 0.5, '暂无数据', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=14)
            self.result_canvas.draw()
            return
            
        colors = ['#2ecc71', '#e74c3c']
        explode = (0.1, 0)  # 突出猪瘟部分
        
        try:
            # 将标题移到顶部中央位置
            ax.set_title('检测结果分布', fontsize=14, pad=15)
            
            # 绘制饼图，并获取返回值
            wedges, texts, autotexts = ax.pie(sizes, explode=explode, colors=colors, 
                                          autopct='%1.1f%%', shadow=True, startangle=90,
                                          textprops={'fontsize': 12})
            
            # 手动调整标签位置
            # 将标签放在饼图外部而不是直接在饼图上
            ax.legend(wedges, labels, loc='upper right', fontsize=12)
            
            # 移除原始标签
            for text in texts:
                text.set_visible(False)
                
            # 增大自动标签字体
            for autotext in autotexts:
                autotext.set_fontsize(11)
                
            ax.axis('equal')  # 保证饼图是圆的
        except Exception as e:
            print(f"绘制结果分布图时发生错误: {str(e)}")
            ax.text(0.5, 0.5, f'绘图错误: {str(e)}', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        
        self.result_canvas.draw()
        
    def update_confidence_histogram(self, records):
        """更新置信度直方图"""
        ax = self.confidence_canvas.axes
        ax.clear()
        
        if not records:
            ax.text(0.5, 0.5, '暂无数据', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=14)
            self.confidence_canvas.draw()
            return
        
        try:
            # 分别获取健康和猪瘟的置信度
            health_confidences = [r['confidence'] for r in records if r['result'] == 'health']
            swine_fever_confidences = [r['confidence'] for r in records if r['result'] == 'swine_fever']
            
            bins = np.linspace(0, 1, 11)  # 0到1之间10个区间
            
            # 将标题放在顶部，增加边距
            ax.set_title('置信度分布', fontsize=14, pad=15)
            
            if health_confidences:
                ax.hist(health_confidences, bins=bins, alpha=0.7, label='健康', color='#2ecc71')
            
            if swine_fever_confidences:
                ax.hist(swine_fever_confidences, bins=bins, alpha=0.7, label='猪瘟', color='#e74c3c')
            
            ax.set_xlabel('置信度', fontsize=12, labelpad=10)
            ax.set_ylabel('检测数量', fontsize=12, labelpad=10)
            ax.legend(fontsize=10, loc='upper right')
            ax.grid(True, linestyle='--', alpha=0.6)
            
            # 设置刻度标签字体大小
            ax.tick_params(axis='both', which='major', labelsize=10)
            
            # 确保图表内容不会被截断
            ax.set_xlim(-0.05, 1.05)  # 添加一些边距
            
            # 确保Y轴的最大值有足够空间，不被截断
            _, ymax = ax.get_ylim()
            ax.set_ylim(0, ymax * 1.2)  # 增加20%的空间
        except Exception as e:
            print(f"绘制置信度直方图时发生错误: {str(e)}")
            ax.text(0.5, 0.5, f'绘图错误: {str(e)}', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        
        self.confidence_canvas.draw()
        
    def update_time_trend(self, records):
        """更新时间趋势图"""
        ax = self.time_canvas.axes
        ax.clear()
        
        if not records:
            ax.text(0.5, 0.5, '暂无数据', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=14)
            self.time_canvas.draw()
            return
        
        try:
            # 按日期排序
            records.sort(key=lambda x: x['timestamp'])
            
            # 提取日期和结果
            dates = [r['timestamp'].split()[0] for r in records]  # 只取日期部分
            results = [1 if r['result'] == 'health' else -1 for r in records]  # 健康为1，猪瘟为-1
            
            # 为了方便显示，找出唯一的日期
            unique_dates = sorted(list(set(dates)))
            date_indices = {date: i for i, date in enumerate(unique_dates)}
            
            # 按日期统计健康和猪瘟的数量
            health_counts = [0] * len(unique_dates)
            swine_fever_counts = [0] * len(unique_dates)
            
            for i, record in enumerate(records):
                date = dates[i]
                idx = date_indices[date]
                if results[i] > 0:
                    health_counts[idx] += 1
                else:
                    swine_fever_counts[idx] += 1
            
            # 简化日期格式，只保留月-日，使标签更短
            short_dates = []
            for date in unique_dates:
                parts = date.split('-')
                if len(parts) >= 3:
                    short_dates.append(f"{parts[1]}-{parts[2]}")  # 只显示月-日
                else:
                    short_dates.append(date)  # 如果格式不匹配，保持原样
            
            # 绘制堆叠柱状图
            x = np.arange(len(unique_dates))
            width = 0.6  # 适当调整柱状图宽度
            
            # 将标题放在顶部，增加边距
            ax.set_title('检测时间趋势', fontsize=14, pad=15)
            
            ax.bar(x, health_counts, width, label='健康', color='#2ecc71')
            ax.bar(x, swine_fever_counts, width, bottom=health_counts, label='猪瘟', color='#e74c3c')
            
            ax.set_xlabel('日期', fontsize=12, labelpad=10)
            ax.set_ylabel('检测数量', fontsize=12, labelpad=10)
            
            # 处理X轴刻度和标签
            if len(unique_dates) > 0:
                ax.set_xticks(x)
                
                # 根据日期数量调整显示策略
                if len(unique_dates) <= 6:
                    # 少于6个日期，全部显示简化后的日期
                    ax.set_xticklabels(short_dates, fontsize=10)
                else:
                    # 日期过多，采用首尾和均匀采样结合策略
                    step = max(1, len(unique_dates) // 5)
                    
                    # 计算需要显示标签的索引
                    indices_to_show = set(range(0, len(unique_dates), step))
                    # 确保显示第一个和最后一个日期
                    indices_to_show.add(0)
                    indices_to_show.add(len(unique_dates) - 1)
                    indices_to_show = sorted(list(indices_to_show))
                    
                    # 创建标签列表
                    labels = [''] * len(unique_dates)
                    for idx in indices_to_show:
                        labels[idx] = short_dates[idx]
                    
                    ax.set_xticklabels(labels, fontsize=10)
            
            # 让图例显示在最佳位置
            ax.legend(fontsize=10, loc='best')
            ax.grid(True, linestyle='--', alpha=0.6)
            
            # 确保Y轴刻度标签不被截断
            ax.tick_params(axis='y', which='major', labelsize=10)
            
            # 确保Y轴的最大值有足够空间
            _, ymax = ax.get_ylim()
            ax.set_ylim(0, ymax * 1.2)  # 增加20%的空间
        except Exception as e:
            print(f"绘制时间趋势图时发生错误: {str(e)}")
            ax.text(0.5, 0.5, f'绘图错误: {str(e)}', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        
        self.time_canvas.draw()
        
    def update_type_distribution(self, stats):
        """更新检测类型分布图"""
        ax = self.type_canvas.axes
        ax.clear()
        
        types = ['图像', '视频']
        counts = [
            stats.get('image_count', 0),
            stats.get('video_count', 0)
        ]
        
        if sum(counts) == 0:
            ax.text(0.5, 0.5, '暂无数据', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=14)
            self.type_canvas.draw()
            return
        
        try:
            colors = ['#3498db', '#9b59b6']
            
            # 将标题放在顶部，增加边距
            ax.set_title('检测类型分布', fontsize=14, pad=15)
            
            # 创建柱状图，进一步减小宽度，避免文字遮挡
            bars = ax.bar(types, counts, color=colors, width=0.3)
            
            # 为X轴添加更多空间
            ax.set_xlabel('检测类型', fontsize=12, labelpad=15)
            ax.set_ylabel('检测数量', fontsize=12, labelpad=10)
            
            # X轴标签字体大小
            ax.set_xticklabels(types, fontsize=12)
            
            # 添加数值标签，位置更高一些，避免被遮挡
            for i, (bar, v) in enumerate(zip(bars, counts)):
                height = bar.get_height()
                # 增加标签与柱形顶部的距离，防止遮挡
                ax.text(bar.get_x() + bar.get_width()/2., height + (max(counts) * 0.05),
                       str(v),
                       ha='center', va='bottom', fontsize=11)
                
            # 添加网格线，但只在Y轴方向
            ax.grid(True, axis='y', linestyle='--', alpha=0.6)
            
            # 设置刻度标签字体大小
            ax.tick_params(axis='both', which='major', labelsize=10)
            
            # 调整Y轴范围，确保有足够空间显示数值标签
            y_max = max(counts) if counts else 1
            ax.set_ylim(0, y_max * 1.3)  # 增加30%的空间
            
            # 确保X轴有足够的间距
            ax.margins(x=0.25)
        except Exception as e:
            print(f"绘制类型分布图时发生错误: {str(e)}")
            ax.text(0.5, 0.5, f'绘图错误: {str(e)}', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        
        self.type_canvas.draw()
    
    def show_empty_charts(self):
        """显示空图表"""
        for canvas in [self.result_canvas, self.confidence_canvas, 
                     self.time_canvas, self.type_canvas]:
            ax = canvas.axes
            ax.clear()
            ax.text(0.5, 0.5, '暂无数据', horizontalalignment='center', 
                  verticalalignment='center', transform=ax.transAxes, fontsize=14)
            canvas.draw()
    
    def export_charts(self):
        """导出图表为图像文件"""
        try:
            # 创建导出目录
            export_dir = "exports"
            os.makedirs(export_dir, exist_ok=True)
            
            # 导出每个图表
            period = self.period_combo.currentText().replace(" ", "_")
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            
            # 结果分布
            self.result_canvas.fig.savefig(f"{export_dir}/result_distribution_{period}_{timestamp}.png", 
                                         dpi=150, bbox_inches='tight', pad_inches=0.5)
            
            # 置信度分布
            self.confidence_canvas.fig.savefig(f"{export_dir}/confidence_histogram_{period}_{timestamp}.png", 
                                             dpi=150, bbox_inches='tight', pad_inches=0.5)
            
            # 时间趋势
            self.time_canvas.fig.savefig(f"{export_dir}/time_trend_{period}_{timestamp}.png", 
                                       dpi=150, bbox_inches='tight', pad_inches=0.5)
            
            # 类型分布
            self.type_canvas.fig.savefig(f"{export_dir}/type_distribution_{period}_{timestamp}.png", 
                                       dpi=150, bbox_inches='tight', pad_inches=0.5)
            
            # 显示成功消息
            QMessageBox.information(self, "导出成功", f"图表已成功导出到 {export_dir} 目录")
        except Exception as e:
            print(f"导出图表时发生错误: {str(e)}")
            QMessageBox.warning(self, "导出失败", f"导出图表失败: {str(e)}") 