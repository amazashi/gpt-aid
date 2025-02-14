import os
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
from demo08.gptaid_v1.MyFrame import MyFrame





# config = load_config('config.json')
# spark_config = config['spark-stt-v1']
# # 接口配置
# app_id = spark_config['app_id']
# api_key = spark_config['api_key']
# # 录音配置
# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 16000
# device_index = 0
#
# base_url = spark_config['url']
# ts = str(int(time.time()))
# tt = (app_id + ts).encode('utf-8')
# md5 = hashlib.md5()
# md5.update(tt)
# baseString = md5.hexdigest()
# baseString = bytes(baseString, encoding='utf-8')
#
# apiKey = api_key.encode('utf-8')
# signa = hmac.new(apiKey, baseString, hashlib.sha1).digest()
# signa = base64.b64encode(signa)
# signa = str(signa, 'utf-8')




class MyApp(wx.App):
    def __init__(self):
        super().__init__()
        self.is_recording = None
        self.thread = None
        self.recording_thread = None
        # self.ui_updated = None
        # self.model = None
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.rec = None
        self.config = self.load_config('config.json')
        self.spark_config = self.config['spark-stt-v1']
        print(self.spark_config)

        # 接口配置
        self.app_id = self.spark_config['app_id']
        self.api_key = self.spark_config['api_key']

        # 录音配置
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.device_index = 0

        self.base_url = self.spark_config['url']
        self.ts = str(int(time.time()))
        self.tt = (self.app_id + self.ts).encode('utf-8')
        self.md5 = hashlib.md5()
        self.md5.update(self.tt)
        self.baseString = self.md5.hexdigest()
        self.baseString = bytes(self.baseString, encoding='utf-8')

        self.apiKey = self.api_key.encode('utf-8')
        self.signa = hmac.new(self.apiKey, self.baseString, hashlib.sha1).digest()
        self.signa = base64.b64encode(self.signa)
        self.signa = str(self.signa, 'utf-8')

        self.end_tag = "{\"end\": true}"
        self.ws = create_connection(self.base_url + "?appid=" + self.app_id + "&ts=" + self.ts + "&signa=" + quote(self.signa))
        self.trecv = threading.Thread(target=self.recv)
        self.trecv.start()

    def OnInit(self):
        self.frame = MyFrame(None, self, title="GPT桌面助手", size=(800, 600))
        self.frame.Show()
        # self.ui_updated = False  # 标志变量，初始为False

        # 绑定关闭事件
        # self.frame.Bind(wx.EVT_CLOSE, self.frame.on_close)
        return True

    def initialize_websocket(self):
        try:
            self.ts = str(int(time.time()))
            self.tt = (self.app_id + self.ts).encode('utf-8')
            self.md5 = hashlib.md5()
            self.md5.update(self.tt)
            self.baseString = self.md5.hexdigest()
            self.baseString = bytes(self.baseString, encoding='utf-8')

            self.apiKey = self.api_key.encode('utf-8')
            self.signa = hmac.new(self.apiKey, self.baseString, hashlib.sha1).digest()
            self.signa = base64.b64encode(self.signa)
            self.signa = str(self.signa, 'utf-8')

            self.ws = create_connection(
                self.base_url + "?appid=" + self.app_id + "&ts=" + self.ts + "&signa=" + quote(self.signa))
            self.trecv = threading.Thread(target=self.recv)
            self.trecv.daemon = True
            self.trecv.start()
            print("WebSocket 连接成功")
        except Exception as e:
            print(f"初始化 WebSocket 时发生错误: {e}")
            wx.CallAfter(self.frame.left_panel.update_left_ui, f"初始化 WebSocket 时发生错误: {e}")
            self.is_recording = False
            if self.ws is not None:
                self.ws.close()
                self.ws = None

    def load_config(self, config_path):
        # 使用相对路径读取配置文件
        config_path = os.path.join(os.path.dirname(__file__), config_path)
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    # def start_recording(self):
    #     # 开始录音并进行实时识别
    #     print("开始实时语音识别")
    #     wx.CallAfter(self.frame.left_panel.update_left_ui, "开始录音")  # 更新UI
    #     self.stream = self.p.open(format=pyaudio.paInt16,
    #                               channels=1,
    #                               rate=16000,
    #                               input=True,
    #                               frames_per_buffer=1024)
    #     self.is_recording = True
    #     self.recording_thread = threading.Thread(target=self.send)
    #     self.recording_thread.daemon = True
    #     self.recording_thread.start()
    #     self.end_tag = "{\"end\": true}"
    #     # self.ws = create_connection(base_url + "?appid=" + app_id + "&ts=" + ts + "&signa=" + quote(signa))
    #     # self.trecv = threading.Thread(target=self.recv)
    #     # self.trecv.start()
    def start_recording(self):
        # 开始录音并进行实时识别
        print("开始实时语音识别")

        try:
            self.stream = self.p.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      frames_per_buffer=self.CHUNK)
            self.is_recording = True
            self.recording_thread = threading.Thread(target=self.send)
            self.recording_thread.daemon = True
            self.recording_thread.start()
            self.end_tag = "{\"end\": true}"
            wx.CallAfter(self.frame.left_panel.update_left_ui, "开始实时语音识别")
        except Exception as e:
            print(f"启动录音时发生错误: {e}")
            wx.CallAfter(self.frame.left_panel.update_left_ui, f"启动录音时发生错误: {e}")
            self.is_recording = False
            if self.stream is not None:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None

    def stop_recording(self):
        # 停止录音
        print("停止录音")
        self.is_recording = False  # 设置为False
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        # self.rec = None
        wx.CallAfter(self.frame.left_panel.update_left_ui, "停止录音了")  # 更新UI

    def send(self):
        while self.is_recording:
            p = pyaudio.PyAudio()  # 初始化pyaudio，进行录音
            self.stream = p.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            input_device_index=self.device_index,
                            frames_per_buffer=self.CHUNK)
            try:
                index = 1
                while True:
                    chunk = self.stream.read(1280)
                    if not chunk:
                        break
                    self.ws.send(chunk)

                    index += 1
                    time.sleep(0.04)
            finally:
                self.stream.stop_stream()

            self.ws.send(bytes(self.end_tag.encode('utf-8')))
            print("send end tag success")

    # def recv(self):
    #     try:
    #         while self.ws.connected:  # 当ws连接状态为True，则一直循环接收数据
    #             result = str(self.ws.recv())
    #             if len(result) == 0:
    #                 print("receive result end")
    #                 break
    #             result_dict = json.loads(result)
    #             # 解析结果
    #             if result_dict["action"] == "started":
    #                 print("handshake success, result: " + result)
    #
    #             if result_dict["action"] == "result":
    #                 # 解析并提取文本
    #                 text = self.extract_text(result_dict)
    #                 print("rtasr result: " + text)
    #                 wx.CallAfter(self.frame.left_panel.update_left_ui, text)
    #             if result_dict["action"] == "error":
    #                 if not self.is_recording:#状态不对才关闭，否则继续等待接受
    #                     print("rtasr error: " + result)
    #                     print("未接受到数据")
    #                     self.ws.close()
    #                 return
    #     except websocket.WebSocketConnectionClosedException:
    #         print("receive result end")
    #     except json.JSONDecodeError as e:
    #         print(f"JSONDecodeError: {e}")
    #     except Exception as e:
    #         print(f"Exception: {e}")
    def recv(self):
        try:
            last_ping_time = time.time()
            PING_INTERVAL = 5  # 心跳间隔时间，单位为秒

            while self.ws.connected:  # 当ws连接状态为True，则一直循环接收数据
                result = self.ws.recv()
                if not result:
                    print("receive result end")
                    break

                result = str(result)
                if len(result) == 0:
                    print("receive result end")
                    break

                try:
                    result_dict = json.loads(result)
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e}")
                    continue

                # 解析结果
                if result_dict["action"] == "started":
                    print("handshake success, result: " + result)

                if result_dict["action"] == "result":
                    # 解析并提取文本
                    text = self.extract_text(result_dict)
                    print("rtasr result: " + text)
                    wx.CallAfter(self.frame.left_panel.update_left_ui, text)

                if result_dict["action"] == "error":
                    if not self.is_recording:  # 状态不对才关闭，否则继续等待接受
                        print("rtasr error: " + result)
                        print("未接受到数据")
                        # self.ws.close()
                    return

                # 更新最后收到消息的时间
                last_ping_time = time.time()

                # 发送心跳包
                if time.time() - last_ping_time > PING_INTERVAL:
                    try:
                        self.ws.send(json.dumps({"action": "ping"}))
                        print("Sent ping")
                        last_ping_time = time.time()
                    except Exception as e:
                        print(f"Error sending ping: {e}")
                        break

        except websocket.WebSocketConnectionClosedException:
            print("WebSocket connection closed")
        except Exception as e:
            print(f"Exception: {e}")

    def extract_text(self, result_dict):
        try:
            data = result_dict["data"]
            if isinstance(data, str):
                data = json.loads(data)
            text = ""
            for rt in data["cn"]["st"]["rt"]:
                for ws in rt["ws"]:
                    for cw in ws["cw"]:
                        text += cw["w"]
            return text
        except KeyError as e:
            print(f"KeyError: {e}")
            return ""
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            return ""
        except Exception as e:
            print(f"Exception: {e}")
            return ""

    def close(self):
        self.ws.close()
        print("connection closed")
    # def on_exit(self):
    #     if self.stream:
    #         self.stream.stop_stream()
    #         self.stream.close()
    #     self.p.terminate()
    #     print("退出程序")