import os
import json
import shutil
from datetime import datetime, timedelta

# 历史记录文件路径
HISTORY_FILE = "detection_history.json"
HISTORY_IMAGE_DIR = "history_images"

def ensure_directories():
    """确保历史记录目录存在"""
    os.makedirs(HISTORY_IMAGE_DIR, exist_ok=True)

def add_detection_record(result, confidence, timestamp, detection_type, image_path):
    """添加新的检测记录"""
    ensure_directories()
    
    # 读取现有历史记录
    records = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                records = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError):
            # 如果文件损坏，创建新的
            records = []
    
    # 为新记录创建唯一ID
    new_id = 1
    if records:
        new_id = max(record.get('id', 0) for record in records) + 1
    
    # 复制图像到历史记录目录
    image_filename = f"detection_{new_id}_{os.path.basename(image_path)}"
    history_image_path = os.path.join(HISTORY_IMAGE_DIR, image_filename)
    
    try:
        shutil.copy2(image_path, history_image_path)
        print(f"已保存图像: {image_path} -> {history_image_path}")
    except Exception as e:
        print(f"保存图像失败: {str(e)}")
        # 如果图像保存失败，尝试直接使用原始图像路径
        history_image_path = image_path
    
    # 创建新记录
    new_record = {
        'id': new_id,
        'result': result,
        'confidence': confidence,
        'timestamp': timestamp,
        'type': detection_type,
        'image_path': history_image_path
    }
    
    # 添加记录并保存
    records.append(new_record)
    
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        print(f"保存记录成功: ID={new_id}, 结果={result}")
        return True
    except Exception as e:
        print(f"保存记录失败: {str(e)}")
        return False

def get_detection_records(period=None):
    """获取检测记录，可以按时间段筛选"""
    ensure_directories()
    
    if not os.path.exists(HISTORY_FILE):
        print("历史记录文件不存在")
        return []
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            records = json.load(f)
        print(f"成功加载{len(records)}条历史记录")
    except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError) as e:
        print(f"读取历史记录失败: {str(e)}")
        return []
    
    # 根据时间段筛选
    if period and period != "全部时间":
        now = datetime.now()
        cutoff_date = None
        
        if period == "今天":
            cutoff_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "最近7天":
            cutoff_date = now - timedelta(days=7)
        elif period == "最近30天":
            cutoff_date = now - timedelta(days=30)
            
        if cutoff_date:
            filtered_records = []
            for record in records:
                try:
                    record_time = datetime.strptime(record['timestamp'], "%Y-%m-%d %H:%M:%S")
                    if record_time >= cutoff_date:
                        filtered_records.append(record)
                except ValueError:
                    # 如果时间戳格式不正确，仍然包含记录
                    filtered_records.append(record)
            records = filtered_records
    
    # 检查图像文件是否存在，如不存在则更新路径
    for record in records:
        if 'image_path' in record and not os.path.exists(record['image_path']):
            # 尝试在history_images目录中查找
            basename = os.path.basename(record['image_path'])
            potential_path = os.path.join(HISTORY_IMAGE_DIR, basename)
            if os.path.exists(potential_path):
                record['image_path'] = potential_path
            else:
                print(f"警告: 图像文件不存在: {record['image_path']}")
    
    # 按时间倒序排序（最新的在前）
    records.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return records

def delete_detection_record(record_id):
    """删除检测记录"""
    if not os.path.exists(HISTORY_FILE):
        print("历史记录文件不存在")
        return False
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            records = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError) as e:
        print(f"读取历史记录失败: {str(e)}")
        return False
    
    # 查找记录
    record_to_delete = None
    remaining_records = []
    
    for record in records:
        if record.get('id') == record_id:
            record_to_delete = record
        else:
            remaining_records.append(record)
    
    if not record_to_delete:
        print(f"未找到ID为{record_id}的记录")
        return False
    
    # 删除相关图像
    try:
        image_path = record_to_delete.get('image_path')
        if image_path and os.path.exists(image_path) and HISTORY_IMAGE_DIR in image_path:
            os.remove(image_path)
            print(f"已删除图像: {image_path}")
    except Exception as e:
        print(f"删除图像失败: {str(e)}")
        # 即使图像删除失败，继续尝试删除记录
    
    # 保存更新后的记录
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(remaining_records, f, ensure_ascii=False, indent=2)
        print(f"成功删除记录: ID={record_id}")
        return True
    except Exception as e:
        print(f"保存记录失败: {str(e)}")
        return False

def get_detection_statistics(period=None):
    """获取检测统计数据"""
    records = get_detection_records(period)
    
    # 初始化统计数据
    stats = {
        'total_count': len(records),
        'health_count': 0,
        'swine_fever_count': 0,
        'image_count': 0,
        'video_count': 0,
        'avg_confidence': 0
    }
    
    # 统计各类数据
    confidence_sum = 0
    
    for record in records:
        result = record.get('result', '')
        detection_type = record.get('type', '')
        confidence = record.get('confidence', 0)
        
        if result == 'health':
            stats['health_count'] += 1
        elif result == 'swine_fever':
            stats['swine_fever_count'] += 1
        
        if detection_type == 'image':
            stats['image_count'] += 1
        elif detection_type == 'video':
            stats['video_count'] += 1
            
        confidence_sum += confidence
    
    # 计算平均置信度
    if stats['total_count'] > 0:
        stats['avg_confidence'] = confidence_sum / stats['total_count']
        
    return stats 