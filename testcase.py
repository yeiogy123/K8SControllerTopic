from tkinter import BROWSE
from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.keys import Keys


class selenium_grid (unittest.TestCase):
     def setUp(self):
          self.driver = webdriver.Remote(
               command_executor='http://localhost:49991',
               desired_capabilities={
                    "browserName": "chrome",
                    "platformName": "LINUX"
                    }
          )

     def tearDown(self):
          self.driver.quit()
     
     def test(self):
          driver = self.driver
          driver.get("https://www.google.com/")
          time.sleep(5)
          search_box = driver.find_element("name", "q")
          search_box.send_keys("NCKU CSIE")
          search_box.send_keys(Keys.RETURN)
          time.sleep(5)
          self.assertEqual("NCKU CSIE - Google 搜尋", driver.title, "webpage title is not the expected")

if __name__ == "__main__":
     unittest.main()
