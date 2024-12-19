from selenium import webdriver
import time

from selenium.webdriver.chrome.service import Service

# starts the browser
driver = webdriver.Chrome()  # for firefox for exmple just change to driver.FireFox.
# Open google
driver.get("https://www.google.com")
# Other way to open the browser if by directly executing an executable
# serive_obj = Service("Path/to/executer")
# driv_2 = webdriver.Chrome(service=serive_obj)
driver.maximize_window()  # After the windows has been opened this maximaze the window
print(f"Title {driver.title}")  # print browser title
print(f"Title {driver.current_url}")  # print browser url

time.sleep(5)
