import json
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from os import system as CMD
from pathlib import Path
import os
import time


def get_config():
    exists = os.path.exists("./config.txt")
    if not exists:
        config_json = {
            "URL": "twitch URL here",
            "Headless (Y/N)": "N"
        }
        print("Couldn't find config file... generating one")
        with open("config.txt", 'w') as config_file:
            config_file.write(json.dumps(
                config_json, indent=4, separators=(',', ': ')
            ))
        return False
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
        windows_useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
        options.add_argument(f'user-agent={windows_useragent}')
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
        print("Inputting URL...")
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
        print("Downloading clip...")
        self.driver.execute_script("""
        document.querySelectorAll(".flex.items-center.space-x-4")[1].children[2].children[0].click();
        """)

    def quit(self):
        self.driver.quit()


def main():
    data = get_config()
    if not data:
        return
    url, headless = data
    headless = headless.lower()
    headless = True if headless == "y" else False
    scraper = ClipScraper(headless)
    scraper.download_clip(url)
    CMD("pause")
    scraper.quit()


if __name__ == '__main__':
    main()
