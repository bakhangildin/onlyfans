from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pyautogui


import win32gui, win32com.client
# from PIL import ImageGrab
import os


def get_window_handler(window_title):
    """Returns window handler by name"""
    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    
    win32gui.EnumWindows(enum_cb, toplist)
    windows = [(hwnd, title) for hwnd, title in winlist if window_title in title.lower()]
    handler = windows[0][0]
    return handler
    
    
def set_foreground_window(handler):
    """Sets window foreground by window handler"""
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(handler)
    
    
def get_window(name):
    """Old version of taking screenshots"""
    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, toplist)

    firefox = [(hwnd, title) for hwnd, title in winlist if name in title.lower()]
    firefox = firefox[0]
    hwnd = firefox[0]

    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)
    sleep(0.1)


class Accaunt_browser:
    def __init__(self, name):
        self.name = name
        with open(f'accaunts_data/{name}.txt') as data_f:
            self.mail = data_f.readline()[:-1]
            self.password = data_f.readline()[:-1]
            self.chrome_user_path = data_f.readline()[:-1]
            self.ph_fname = os.getcwd() + '\\photoshop_files\\' + name + '.psd'
            
        with open('global_parameters.txt') as global_f:
            self.chrome_exe_path = global_f.readline()[:-1]
        
        self.open_browser()
        
        # Handler of new browser window
        self.window_handler = get_window_handler(self.driver.title)
        
        self.driver.get('https://onlyfans.com/')
        
        with open(f'last_followers/{name}.txt') as lf:
            self.last_follower = lf.readline()[:-1]
               
        raise NotImplementedError
        
    
    def open_browser(self):
        """
        Opens browser
        TODO: Add profile name as argument
        """
        
        argument = f'user-data-dir={self.chrome_user_path}'
        
        options = webdriver.ChromeOptions()
        options.add_argument(argument)
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        
        self.driver = webdriver.Chrome(
            executable_path=self.chrome_exe_path,
            chrome_options=options
        )
    
    # followers staff
        
    def scroll(self, amount):
        SCROLL_PAUSE_TIME = 1.5
        last_height = self.driver.execute_script("return document.body.scrollHeight")
    
        for i in range(amount):
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)
    
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
     
        
    
    def get_new_followers(self, notifications):
        usernames = []
        
        for notification in notifications:
            try:
                username = notification.find_element(By.CLASS_NAME, value=r"g-user-username")
                notif_message = notification.find_element(By.CLASS_NAME, value=r"b-notifications__list__item__text")
                if notif_message.text == 'subscribed to your profile!':
                    usernames.append(username.text[1:])
            except:
                continue
        return usernames
    
    
    def open_notifications(self):
        """
        Opens notifications. If notification page is loaded doesn't update it.
        """
        if self.driver.current_url == 'https://onlyfans.com/my/notifications/subscribed':
            return
            
        self.driver.get(r"https://onlyfans.com/my/notifications/subscribed")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, r"swiper-wrapper"))
            )
        except:
            raise RuntimeError("Notifications page not loaded")        
    
    
    def get_notifications(self, n_scrolls):
        self.open_notifications()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, r"swiper-wrapper"))
        )
        self.scroll(self.driver, n_scrolls)
        
        
        try:
            notifications = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, r'//*[@id="content"]/div[1]/div/div/div[3]'))
            )
            notifications = self.driver.find_elements(by=By.CLASS_NAME, value=r"b-notifications__list__item")
            usernames = self.get_new_followers(notifications)
            
        except:
            usernames = []
        
        try:
            last_id = usernames.index(self.last_follower)
        except:
            if n_scrolls > 3:
                raise RuntimeError('Can\'t find last follower')
            return self.get_notifications(self.driver, n_scrolls + 1)
            
        return usernames[:last_id]
    
    
    def screenshot(self, username):
        folder = f'screenshots/{self.name}/'
        if not os.path.exists(folder):
            os.mkdir(folder)
            
        url = r"https://onlyfans.com/" + username
        self.driver.get(url)
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, r"l-profile-page"))
        )
            
        # get_window('onlyfans')
        # pic_name = f"{username}.png"
        # pyautogui.screenshot(f'{folder}{pic_name}')
        # get_window('script - jupyter notebook - google chrome')
        
        # with open('log/log.txt', 'a') as f:
        #     f.write(username + "\n")
        
        """Screenshots update"""
        set_foreground_window(self.handler)
        pic_name = f"{username}.png"
        pyautogui.screenshot(f'{folder}{pic_name}')
        with open('log/log.txt', 'a') as f:
            f.write(username + "\n")
        
    
    def open_chat(self, username):
        self.driver.get(f'https://onlyfans.com/{username}')
        
        profile = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                r'//*[@id="content"]/div[1]/div[1]/div[2]/div/div[2]/div[1]'
            ))
        )
        
        message_button = profile.find_element(
            by=By.CSS_SELECTOR, 
            value=r'#content > div.l-wrapper > div.l-wrapper__content > div.l-profile-container > div > div.b-profile__header__user.g-sides-gaps > div.b-profile__user > div.b-group-profile-btns > a'
        )
        message_button.click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                r'//*[@id="attach_file_photo"]'
            ))
        )
            
    def attach_image(self, username):
    	"""
    
    
    	ВСТАВИТЬ ПРИВИЛЬНЫЙ ПУТЬ
    
    
    
    
    	"""
        folder = os.getcwd() + '\\screnshots\\{self.name}\\'
        image_name = f'{username}.png'
        image_path = f'{folder}{image_name}'
        if not os.path.exists(image_path):
            raise RuntimeError(f"Image \"{image_path}\" doesn't exist")
        
        attach_image = driver.find_element(
            by=By.XPATH,
            value=r'//*[@id="attach_file_photo"]'
        )
        
        attach_image.click()
        sleep(1)
        pyautogui.write(image_path)
        pyautogui.press('enter')
        
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, 
                r'//*[@id="make_post_form"]/div/div[2]/button[7]'))
        )
    
    
    def write_message(driver, message_text):
        message_field = driver.find_element(
            by=By.ID,
            value='new_post_text_input'
        )
        
        message_field.send_keys(message_text)
    
    
    def send_message(driver):
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, 
                r'//*[@id="make_post_form"]/div/div[2]/button[7]'))
        )
        send_button.click()
    
    
    def send_picture(driver, username, message_text):
        open_chat(driver, username)    
    
        attach_image(driver, username)
    
        if message_text:
            write_message(driver, message_text)
    
        send_message(driver)
