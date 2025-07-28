import requests
import json
import config.key as key

class DeepseekChat:
    def __init__(self):
        self.API_KEY = key.deepseek_key
        self.URL = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.API_KEY}",
            "Content-Type": "application/json"
        }
        self.system_prompt = "你是一个AI助手"
        
    def set_system_prompt(self, prompt):
        """
        设置系统提示词
        
        Args:
            prompt (str): 系统提示词
        """
        self.system_prompt = prompt
        
    def chat(self, user_message, temperature=0.7, max_tokens=2000, model="deepseek-chat"):
        """
        与Deepseek AI进行对话
        
        Args:
            user_message (str): 用户消息
            temperature (float): 随机性控制（0~1），默认为0.7
            max_tokens (int): 最大生成长度，默认为2000
            model (str): 模型名称，默认为deepseek-chat
            
        Returns:
            str: AI回复内容，失败返回None
        """
        try:
            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            response = requests.post(self.URL, json=data, headers=self.headers)
            
            # 检查响应状态
            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                print(f"错误信息: {response.text}")
                return None
            
            # 解析响应结果
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                reply = result['choices'][0]['message']['content']
                print(f"AI 回复：{reply}")
                return reply
            else:
                print("响应格式错误")
                return None
                
        except Exception as e:
            print(f"对话失败: {e}")
            return None


# 创建全局实例
deepseek_chat = DeepseekChat()


def chat_with_ai(user_message, system_prompt=None, temperature=0.7, max_tokens=2000, model="deepseek-chat"):
    """
    便捷函数：与Deepseek AI进行对话
    
    Args:
        user_message (str): 用户消息
        system_prompt (str): 系统提示词，如果不指定则使用默认提示词
        temperature (float): 随机性控制（0~1），默认为0.7
        max_tokens (int): 最大生成长度，默认为2000
        model (str): 模型名称，默认为deepseek-chat
        
    Returns:
        str: AI回复内容，失败返回None
    """
    if system_prompt:
        deepseek_chat.set_system_prompt(system_prompt)
    
    return deepseek_chat.chat(user_message, temperature, max_tokens, model)


if __name__ == '__main__':
    # 测试基本对话
    print("=== 测试基本对话 ===")
    test_message = "你好！请介绍一下你自己"
    reply = chat_with_ai(test_message)
    if reply:
        print("✓ 基本对话测试成功")
    else:
        print("✗ 基本对话测试失败")