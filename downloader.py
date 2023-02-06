import json
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from os import system as CMD
import os
import time


def get_config():
    with open("config.txt") as config_file:
        unpacked = json.loads(config_file.read())
        return unpacked["URL"], unpacked["Headless (Y/N)"]


class ClipScraper:
    def __init__(self, headless):
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        download_path = os.getcwd() + "\\downloads"
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        prefs = {"download.default_directory": download_path}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)

    def download_clip(self, link):
        clipr_url = r"https://clipr.xyz/"
        self.driver.get(clipr_url)
        # Grab the element to input the clip URL
        clip_input = self.driver.execute_script("""
        let inputs = document.querySelectorAll("input");
        let urlInput;
        for (let input of inputs) {
            if (input.placeholder == "https://clips.twitch.tv/MoistTenuousSandwichRickroll-gIFD6ceHnz7_JHuO") {
                urlInput = input;
                break;
            }
        }
        return urlInput;
        """)
        # Input the URL
        clip_input.send_keys(link)
        # For some reason, the first time the button is clicked it does nothing
        for i in range(2):
            # Click the download now button after inputting URL
            self.driver.execute_script("""
            let buttons = document.querySelectorAll("button");
            let downloadButton;
            for (let button of buttons) {
                if (button.textContent.includes("Download now")) {
                    downloadButton = button;
                    break;
                }
            }
            downloadButton.click();
            """)
            time.sleep(2)
        time.sleep(2)
        self.driver.execute_script("""
        document.querySelectorAll(".flex.items-center.space-x-4")[1].children[2].children[0].click();
        """)

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    url, headless = get_config()
    headless = headless.lower()
    headless = True if headless == "y" else False
    scraper = ClipScraper(headless)
    scraper.download_clip(url)
    CMD("pause")
    scraper.quit()
