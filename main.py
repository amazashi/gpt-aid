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

from demo08.gptaid_v1.MyApp import MyApp
if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()