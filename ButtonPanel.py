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
from demo08.gptaid_v1.ConfigEditor import ConfigEditor

class ButtonPanel(wx.Panel):
    def __init__(self, parent, main_app):
        super().__init__(parent, size=(100, -1))
        self.click_counter = 0
        self.main_app = main_app  # 保存 MyApp 实例
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # 添加按钮到按钮栏
        self.button1 = wx.Button(self, label="录音")
        self.button2 = wx.Button(self, label="停止录音")
        self.button3 = wx.Button(self, label="设置")

        # 绑定事件
        self.button1.Bind(wx.EVT_BUTTON, self.on_button_click)
        self.button2.Bind(wx.EVT_BUTTON, self.on_button_click)
        self.button3.Bind(wx.EVT_BUTTON, self.on_button_click)

        self.sizer.Add(self.button1, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.button2, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.button3, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(self.sizer)

    def on_button_click(self, event):
        button = event.GetEventObject()
        button_label = button.GetLabel()
        print(f"按钮 {button.GetLabel()} 被点击了")
        if button_label == "录音":
            if self.click_counter == 0:
                self.click_counter += 1
                print("录音按钮已点击，计数器加1")
                self.main_app.start_recording()  # 调用 MyApp 的 start_recording 方法
            else:
                print("录音按钮已被点击，无法重复点击")
        elif button_label == "停止录音":
            if self.click_counter > 0:
                self.click_counter -= 1
                print("停止录音按钮已点击，计数器减1")
                self.main_app.stop_recording()  # 调用 MyApp 的 stop_recording 方法
            else:
                print("录音按钮未被点击，无法点击停止录音按钮")
        elif button_label == "设置":
            print("设置按钮被点击，计数器不受影响")
            self.show_config_editor()

    def show_config_editor(self):
        config_editor = ConfigEditor(self, "Config Editor")
        config_editor.ShowModal()
        config_editor.Destroy()
