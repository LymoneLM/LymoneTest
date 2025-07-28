import requests
import json
import os
import base64
import config.key as key

class BaiduVoice:
    def __init__(self):
        self.API_KEY = key.baidu_api_key
        self.SECRET_KEY = key.baidu_secret_key
        self.TTS_URL = "https://tsn.baidu.com/text2audio"
        self.ASR_URL = "https://vop.baidu.com/server_api"
        self.TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
        self.token = None
        
    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        params = {
            "grant_type": "client_credentials", 
            "client_id": self.API_KEY, 
            "client_secret": self.SECRET_KEY
        }
        try:
            response = requests.post(self.TOKEN_URL, params=params)
            return response.json().get("access_token")
        except Exception as e:
            print(f"获取access_token失败: {e}")
            return None
    
    def text2audio(self, text, output_file=None, lan='zh', spd=5, pit=5, vol=5, per=1, aue=6):
        """
        将文字转换为音频文件（语音合成）
        
        Args:
            text (str): 要转换的文字
            output_file (str): 输出文件名，如果不指定则使用默认名称
            lan (str): 语言，默认为中文'zh'
            spd (int): 语速，取值0-9，默认为5中等语速
            pit (int): 音调，取值0-9，默认为5中等音调
            vol (int): 音量，取值0-15，默认为5中等音量
            per (int): 发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为1
            aue (int): 3为mp3格式； 4为pcm-16k；5为pcm-8k；6为wav（内容同pcm-16k），默认为6
            
        Returns:
            bool: 转换是否成功
        """
        # 获取token
        if not self.token:
            self.token = self.get_access_token()
            if not self.token:
                print("获取token失败")
                return False
        
        # 构建payload
        payload = f'tok={self.token}&cuid=wtyiQt5jxuCAgcFwFw7zgZpPmSKvqKun&ctp=1&lan={lan}&spd={spd}&pit={pit}&vol={vol}&per={per}&aue={aue}&tex={text}'
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*'
        }
        
        try:
            response = requests.post(self.TTS_URL, headers=headers, data=payload.encode("utf-8"))
            
            # 检查响应状态
            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                print(f"错误信息: {response.text}")
                return False
            
            # 检查是否为音频文件
            content_type = response.headers.get('content-type', '')
            if 'audio/' not in content_type:
                print(f"返回的不是音频文件，content-type: {content_type}")
                print(f"错误信息: {response.text}")
                return False
            
            # 确定输出文件名
            if not output_file:
                # 使用文本前10个字符作为文件名，避免特殊字符
                safe_text = "".join(c for c in text[:10] if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_text = safe_text.replace(' ', '_')
                output_file = f"{safe_text}.wav"
            
            # 确保输出路径在device目录下
            if not os.path.isabs(output_file):
                # 获取当前文件所在目录的上级目录（device目录）
                current_dir = os.path.dirname(os.path.abspath(__file__))
                device_dir = os.path.dirname(current_dir)
                output_file = os.path.join(device_dir, output_file)
            
            # 保存音频文件
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            print(f"音频文件已保存: {output_file}")
            return True
            
        except Exception as e:
            print(f"语音合成失败: {e}")
            return False
    
    def audio2text(self, audio_file, format='pcm', rate=16000, channel=1, dev_pid=1537):
        """
        将音频文件转换为文字（语音识别）
        
        Args:
            audio_file (str): 音频文件路径
            format (str): 音频格式，支持pcm/wav/amr/m4a，默认为pcm
            rate (int): 采样率，16000或8000，默认为16000
            channel (int): 声道数，仅支持单声道，默认为1
            dev_pid (int): 语言模型，1537为普通话，其他值见百度文档
            
        Returns:
            str: 识别结果文字，失败返回None
        """
        # 获取token
        if not self.token:
            self.token = self.get_access_token()
            if not self.token:
                print("获取token失败")
                return None
        
        # 检查音频文件是否存在
        if not os.path.exists(audio_file):
            print(f"音频文件不存在: {audio_file}")
            return None
        
        try:
            # 读取音频文件
            with open(audio_file, 'rb') as f:
                audio_data = f.read()
            
            # 对音频数据进行base64编码
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            # 构建请求数据
            payload = {
                "format": format,
                "rate": rate,
                "channel": channel,
                "cuid": "4m48cWyLk4sSqmMOm8BqwCLgftlQKjn7",
                "token": self.token,
                "dev_pid": dev_pid,
                "speech": audio_base64,
                "len": len(audio_data)
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            # 发送请求
            response = requests.post(self.ASR_URL, headers=headers, data=json.dumps(payload, ensure_ascii=False))
            
            # 检查响应状态
            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                print(f"错误信息: {response.text}")
                return None
            
            # 解析响应结果
            result = response.json()
            
            if result.get('err_no') == 0:
                # 识别成功
                recognized_text = result.get('result', [''])[0]
                print(f"语音识别成功: {recognized_text}")
                return recognized_text
            else:
                # 识别失败
                error_msg = result.get('err_msg', '未知错误')
                print(f"语音识别失败: {error_msg}")
                return None
                
        except Exception as e:
            print(f"语音识别失败: {e}")
            return None


# 创建全局实例
baidu_voice = BaiduVoice()


def text2audio(text, output_file=None, lan='zh', spd=5, pit=5, vol=5, per=1, aue=6):
    """
    便捷函数：将文字转换为音频文件（语音合成）
    
    Args:
        text (str): 要转换的文字
        output_file (str): 输出文件名，如果不指定则使用默认名称
        lan (str): 语言，默认为中文'zh'
        spd (int): 语速，取值0-9，默认为5中等语速
        pit (int): 音调，取值0-9，默认为5中等音调
        vol (int): 音量，取值0-15，默认为5中等音量
        per (int): 发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为1
        aue (int): 3为mp3格式； 4为pcm-16k；5为pcm-8k；6为wav（内容同pcm-16k），默认为6
        
    Returns:
        bool: 转换是否成功
    """
    return baidu_voice.text2audio(text, output_file, lan, spd, pit, vol, per, aue)


def audio2text(audio_file, format='wav', rate=16000, channel=1, dev_pid=1537):
    """
    便捷函数：将音频文件转换为文字（语音识别）
    
    Args:
        audio_file (str): 音频文件路径
        format (str): 音频格式，支持pcm/wav/amr/m4a，默认为pcm
        rate (int): 采样率，16000或8000，默认为16000
        channel (int): 声道数，仅支持单声道，默认为1
        dev_pid (int): 语言模型，1537为普通话，其他值见百度文档
        
    Returns:
        str: 识别结果文字，失败返回None
    """
    return baidu_voice.audio2text(audio_file, format, rate, channel, dev_pid)


if __name__ == '__main__':
    # 测试语音合成
    print("=== 测试语音合成 ===")
    test_text = "百度语音合成测试"
    success = text2audio(test_text, "test_output.wav")
    if success:
        print("语音合成测试成功")
    else:
        print("语音合成测试失败")
    
    # 测试语音识别（如果有音频文件的话）
    print("\n=== 测试语音识别 ===")
    # 这里可以测试语音识别，需要提供音频文件路径
    # result = audio2text("test_audio.wav")
    # if result:
    #     print(f"语音识别结果: {result}")
    # else:
    #     print("语音识别失败")