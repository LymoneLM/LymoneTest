![title](assets/title.png)
# 哨兵Sentry

家庭智能安防综合解决方案

## 功能

除了最基本的摄像与存储，本项目有五大智能功能模块

### 人脸检测

基于SCRFD的人脸检测提供支持，哨兵可以检测摄制范围内的人脸目标，统计计数，并记录为事件。

同时哨兵也配有可开关的人脸跟随功能和哨卫模式人脸查找功能。

### 安全检测

依靠自有的安全检测数据集和高效的YOLOv5Nano框架，哨兵实现了对于常见安全敏感目标的实时检测。

对于管制刀具和枪械等目标，哨兵会记录报告事件；对于火灾目标，哨兵会触发火灾警报并立即发动全部告警功能提醒。

### 语音交互

有赖于百度智能云的ASR、TTS服务与DeepSeek开放平台的API服务，哨兵实现了一套高效、即时的语音交互系统，可以让用户无需启动后台，仅需语音交互就可以了解安防信息。

### 事件系统

由SQLite作为内部存储，支持MQTT订阅机制，哨兵内部有一套检测驱动的事件机制。可以很好的响应安全事件、记录工作期间的安防相关动态，确保安全无虞。

必要时，哨兵也可以作为MQTT Client，订阅其他传感器甚至其他哨兵的话题获取信息存入事件系统。

### 声音检测

凭借着YAMNet高效的声音分类功能，我们实现了伪即时的声音检测功能，可以实时处理当前的环境声音，分辨当前环境是否有安全事件，必要时会联动其他模块进行检测。

## 部署

### 快速开始

1. 克隆本项目/解压源代码，进入项目根目录

2. (推荐)新建Python3.10.12虚拟环境，安装所需库

   ```bash
   pip install -r requirments.txt -y
   ```

3. 在根目录新建`config/key.py`文件，添加如下四个秘钥值：

	```python
	# picovoice 用户AK秘钥
	picovoice_access_key = your_own_key
	# 百度智能云应用，需包含基础语音识别服务和短文本转语音服务
	# 云应用AK秘钥
	baidu_api_key = your_own_key
	# 云应用SK秘钥
	baidu_secret_key = your_own_key
	# DeepSeek开放平台AK
	deepseek_key = your_own_key
	```

4. 运行

	运行主程序：

	```bash
	python3 main.py
	```

	运行音频识别辅助程序（可选）：

	```bash
	python3 YAMNet_mic.py
	```

### 安装需求环境

硬件使用香橙派Zero3(H618)1.5G，配合专用控制板。

参考Python环境

> - Python==3.10.12
>
> - Machine Learning & AI 
>   `tensorflow==2.19.0`, `keras==3.10.0`, `torch==2.7.1`, `torchvision==0.22.1`, `scikit-learn==1.7.1`, `jax==0.6.2`, `jaxlib==0.6.2`
>
> - Computer Vision & Media 
>   `opencv-python==4.12.0.88`, `opencv-contrib-python==4.11.0.86`, `mediapipe==0.10.18`, `Pillow==9.0.1`
>
> - Audio Processing 
>   `librosa==0.11.0`, `sounddevice==0.5.2`, `soundfile==0.13.1`, `pvporcupine==3.0.5`, `pvrecorder==1.2.7`, `PyAudio==0.2.14`
>
> - Data Science & Math 
>   `numpy==1.26.4`, `pandas==2.3.1`, `scipy==1.15.3`
>
> - Utilities & Visualization 
>   `matplotlib==3.10.3`, `Flask==3.1.1`, `networkx==3.4.2`, `rich==14.1.0`
>
> - ONNX Runtime 
>   `onnx==1.18.0`, `onnxruntime==1.18.1`

详细需求请查看项目根目录requirments.txt

### 迁移部署

想要在自己的设备上部署哨兵Sentry，您可能需要修改根目录`utils`下若干程序以适配底层硬件。

> [!NOTE]
>
> 哨兵Sentry做了严格的项目分层管理。`utiles`中`mic.py`、`motor.py`、`speaker.py`、`temp_hum.py`作为底层设备的兼容层纯在。分别实现了麦克风录入功能、步进电机控制功能、扬声器播放功能、温湿度获取功能。

如果您的设备平台不具备设备或者没有相关功能设计，您可以通过修改这几份程序为定值返回来简单的避免错误。

同样的，您也可以通过类似的方式修改系统时间`utils/time.py`或者修改`utils/deepseek.py`和`utils/baidu.py`来替换使用的LLM、ASR和TTS为其他的API。

## 许可

哨兵Sentry程序遵循MIT许可开源

## 致谢

感谢百科荣创为本项目提供硬件和技术支持