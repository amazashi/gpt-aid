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



class LeftPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, size=(300, -1), style=wx.SIMPLE_BORDER)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # 添加控件到界面1
        self.label1 = wx.StaticText(self, label="识别语音")
        self.sizer.Add(self.label1, 0, wx.ALL | wx.CENTER, 5)
        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.sizer.Add(self.text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(self.sizer)

    def update_left_ui(self, str):
        self.text_ctrl.AppendText(str + "\n")  # 每次写入后添加换行符
