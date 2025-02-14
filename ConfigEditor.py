import os
import sys
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


class ConfigEditor(wx.Dialog):
    # def __init__(self, parent, title):
    #     super(ConfigEditor, self).__init__(parent, title=title, size=(600, 400))
    #     self.config_path = 'config2.json'
    #     self.init_ui()
    #     self.load_config()  # 自动加载配置文件
    #     self.Show()
    def __init__(self, parent, title):
        super(ConfigEditor, self).__init__(parent, title=title, size=(600, 400))
        # 动态获取配置文件路径
        if getattr(sys, 'frozen', False):
            # 打包后的路径
            bundle_dir = sys._MEIPASS
        else:
            # 开发环境下的路径
            bundle_dir = os.path.dirname(os.path.abspath(__file__))

        self.config_path = os.path.join(bundle_dir, 'config.json')
        self.init_ui()
        self.load_config()  # 自动加载配置文件
        self.DisableIME()  # 禁用输入法
        self.Show()

    def DisableIME(self):
        """Disable the Input Method Editor (IME) for this dialog."""
        if hasattr(self.text_ctrl, "SetDefaultIMEMode"):
            self.text_ctrl.SetDefaultIMEMode(wx.IME_MODE_OFF)
    # def init_ui(self):
    #     main_sizer = wx.BoxSizer(wx.VERTICAL)
    #
    #     # 创建文本编辑器
    #     self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_RICH2)
    #     main_sizer.Add(self.text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
    #
    #     # 创建按钮面板
    #     button_sizer = wx.BoxSizer(wx.HORIZONTAL)
    #     # 添加保存按钮
    #     save_button = wx.Button(self, label="保存")
    #     save_button.Bind(wx.EVT_BUTTON, self.on_save)
    #     button_sizer.Add(save_button, 0, wx.ALL | wx.CENTER, 5)
    #
    #     main_sizer.Add(button_sizer, 0, wx.ALL | wx.CENTER, 5)
    #
    #     self.SetSizer(main_sizer)
    def init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 创建文本编辑器，并确保其使用 UTF-8 编码和合适字体
        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_RICH2)
        font = wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, u'Consolas')
        self.text_ctrl.SetFont(font)
        main_sizer.Add(self.text_ctrl, 1, wx.ALL | wx.EXPAND, 5)

        # 创建按钮面板
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # 添加保存按钮
        save_button = wx.Button(self, label="保存")
        save_button.Bind(wx.EVT_BUTTON, self.on_save)
        button_sizer.Add(save_button, 0, wx.ALL | wx.CENTER, 5)

        main_sizer.Add(button_sizer, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(main_sizer)

        # # 创建工具栏
        # toolbar = self.CreateToolBar()
        # # open_tool = toolbar.AddTool(wx.ID_ANY, 'Open', wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN))
        # save_tool = toolbar.AddTool(wx.ID_ANY, 'Save', wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE))
        # toolbar.Realize()
        #
        # # 绑定工具栏事件
        # # self.Bind(wx.EVT_TOOL, self.on_open, open_tool)
        # self.Bind(wx.EVT_TOOL, self.on_save, save_tool)
        #
        # self.SetSizer(main_sizer)

    def load_config(self):
        try:
            with open(self.config_path, 'r') as file:
                content = file.read()
                self.text_ctrl.SetValue(content)
        except FileNotFoundError:
            print(f"File {self.config_path} not found. Creating a new one.")
            self.text_ctrl.SetValue("{}")  # 设置一个空的 JSON 对象
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.config_path}. Creating a new one.")
            self.text_ctrl.SetValue("{}")  # 设置一个空的 JSON 对象

    def on_open(self, event):
        with wx.FileDialog(self, "Open JSON file", wildcard="JSON files (*.json)|*.json", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r',encoding='utf-8') as file:
                    content = file.read()
                    self.text_ctrl.SetValue(content)
                    self.config_path = pathname
            except IOError:
                wx.LogError(f"Cannot open file '{pathname}'.")

    def on_save(self, event):
        try:
            content = self.text_ctrl.GetValue()
            try:
                json.loads(content)  # 检查 JSON 格式是否正确
                with open(self.config_path, 'w') as file:
                    file.write(content)
                wx.MessageBox("File saved successfully!", "Success", wx.OK | wx.ICON_INFORMATION)
            except json.JSONDecodeError:
                wx.LogError("Invalid JSON format. Please check your JSON syntax.")
        except IOError:
            wx.LogError(f"Cannot save current data in file '{self.config_path}'.")
