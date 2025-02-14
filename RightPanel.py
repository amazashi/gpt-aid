import threading

import wx

import time

import pyaudio

import wave
import json
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

import hashlib
import hmac
import base64
from socket import *
import json, time, threading
from websocket import create_connection
import websocket
from urllib.parse import quote
import logging
import pyaudio


class RightPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, size=(300, -1), style=wx.SIMPLE_BORDER)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # 添加控件到界面2
        self.label2 = wx.StaticText(self, label="GPT答案")
        self.sizer.Add(self.label2, 0, wx.ALL | wx.CENTER, 5)
        self.question_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.sizer.Add(self.question_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        # 添加发送按钮
        self.send_button = wx.Button(self, label="发送")
        self.sizer.Add(self.send_button, 0, wx.ALL | wx.CENTER, 5)
        self.send_button.Bind(wx.EVT_BUTTON, self.on_send_click)  # 绑定按钮点击事件

        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.sizer.Add(self.text_ctrl, 5, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(self.sizer)

    def update_right_ui(self, str):
        self.text_ctrl.AppendText(str + "\n")  # 每次写入后添加换行符

    def on_send_click(self, event):
        question = self.question_ctrl.GetValue()
        formatted_question = f"我:{question}"  # 拼接字符串
        print(f"发送的问题: {question}")
        wx.CallAfter(self.update_right_ui, formatted_question)
        # 创建一个新的线程来处理生成响应的操作
        threading.Thread(target=self.generate_response_in_thread, args=(question,), daemon=True).start()
        # generated_text, token_usage = self.generate_response(question)
        # formatted_generated_text = f"答:{generated_text}"
        # wx.CallAfter(self.update_right_ui, formatted_generated_text)
        # 在这里可以添加发送问题到GPT的逻辑
        # self.question_ctrl.Clear()  # 清空输入框

    def generate_response_in_thread(self, question):
        generated_text, token_usage = self.generate_response(question)
        formatted_generated_text = f"答:{generated_text}"
        wx.CallAfter(self.update_right_ui, formatted_generated_text)

    def load_config(self, config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        return config

    def generate_response(self, question):
        config = self.load_config('config.json')
        spark_config = config['sparkai-v4-chat']
        spark = ChatSparkLLM(
            spark_api_url=spark_config['url'],
            spark_app_id=spark_config['app_id'],
            spark_api_key=spark_config['api_key'],
            spark_api_secret=spark_config['api_secret'],
            spark_llm_domain=spark_config['domain'],
            streaming=False,
        )
        messages = [ChatMessage(
            role="user",
            content=question
        )]
        print("发出请求",question)
        start_time=time.time()
        handler = ChunkPrintHandler()
        response = spark.generate([messages], callbacks=[handler])
        end_time=time.time()
        print("请求耗时",end_time-start_time)
        # 提取生成的文本
        generated_text = ""
        if response.generations:
            generated_text = response.generations[0][0].text
        # 提取 token 使用情况
        token_usage = {}
        if response.llm_output and 'token_usage' in response.llm_output:
            token_usage = response.llm_output['token_usage']
        return generated_text, token_usage
