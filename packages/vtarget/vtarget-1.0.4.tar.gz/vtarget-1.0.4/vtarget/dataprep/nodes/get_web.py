import json
import os
import time

import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class GetWeb:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# Get Web")

        # field
        field: list = settings["field"] if "field" in settings and settings["field"] else []
        split: bool = settings["split"] if "split" in settings and settings["split"] else False
        library: str = settings["library"] if "library" in settings and settings["library"] else None
        timeout: str = settings["timeout"] if "timeout" in settings and settings["timeout"] else None

        if not field:
            msg = app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_node_log(flow_id, node_key, msg, console_level="error")

        try:
            if library == "requests":
                df["html"] = df.apply(
                    self.process_web_requests,
                    axis=1,
                    args=(
                        split,
                        field,
                    ),
                )
                df = df.explode("html", ignore_index=True)

            elif library == "selenium":
                df["html"] = df.apply(self.process_web_selenium, axis=1, args=(split, field, timeout))
                df = df.explode("html", ignore_index=True)

            else:
                # ! Enviar error
                pass

        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_node_log(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(map(str, e.args))})")

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"Out": df}

    def process_web_requests(self, row, split, field):
        url = row[field]
        response = requests.get(url)

        content_type = response.headers.get("Content-Type", "")
        if "text/html" in content_type:
            html_text = response.content.decode("utf-8", errors="ignore")  # Intentar decodificar
        else:
            html_text = response.content

        return html_text.split("\n") if split else [html_text]

    def process_web_selenium(self, row, split, field, timeout):
        url = row[field]

        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-direct-composition")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-direct-composition")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

        service = Service(self.get_driver_path())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(url)
        try:
            # WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, "promo-card-container")))

            WebDriverWait(driver, timeout).until(lambda d: d.execute_script("return document.readyState") == "complete")
            time.sleep(timeout)
            print("Página lista según document.readyState")

        except Exception as e:
            print(f"No se pudo procesar la url: {url}\nError: {e}")

        # time.sleep(5)
        html_text = driver.page_source
        driver.quit()

        return html_text.split("\n") if split else [html_text]

    def get_driver_path(self):
        driver_path = ""
        if os.name == "nt":
            driver_path = os.path.join("scrapping_driver", "windriver", "chromedriver.exe")
        elif os.name == "posix":
            driver_path = os.path.join("scrapping_driver", "posixdriver", "")
        else:
            driver_path = ""

        return driver_path
