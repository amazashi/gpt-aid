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

from demo08.gptaid_v1.ButtonPanel import ButtonPanel

from demo08.gptaid_v1.LeftPanel import LeftPanel

from demo08.gptaid_v1.RightPanel import RightPanel
# 语音和大模型使用API版本
class MyFrame(wx.Frame):
    def __init__(self, parent, app, *args, **kw):
        super(MyFrame, self).__init__(parent, *args, **kw)
        self.app = app  # 将 MyApp 的实例传递给 MyFrame
        self.panel = wx.Panel(self)
        self.SetTransparent(255)  # 128表示半透明
        # 创建一个水平的BoxSizer来管理三部分
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_panel = ButtonPanel(self.panel, self.app)  # 将 MyApp 实例传递给 ButtonPanel
        main_sizer.Add(self.button_panel, 0, wx.EXPAND)
        # 第二部分是实时语音部分
        self.left_panel = LeftPanel(self.panel)
        main_sizer.Add(self.left_panel, 1, wx.EXPAND)
        # 第三部分是GPT结果部分
        self.right_panel = RightPanel(self.panel)
        main_sizer.Add(self.right_panel, 1, wx.EXPAND)
        self.panel.SetSizer(main_sizer)
        self.Show()

    def on_close(self, event):
        self.Destroy()

