from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import win32gui, win32com.client
import os
import pyautogui


class Account_browser:
    def __init__(self, name):
        self.name = name
        with open(f'accounts_data/{name}.txt') as data_f:
            self.mail = data_f.readline()[:-1]
            self.password = data_f.readline()[:-1]
            self.chrome_user_path = data_f.readline()[:-1]
            self.ps_file = os.getcwd() + '\\photoshop_files\\' + name + '.psd'
        