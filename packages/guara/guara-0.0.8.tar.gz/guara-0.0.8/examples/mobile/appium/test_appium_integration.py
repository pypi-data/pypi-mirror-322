import pathlib
import random
import pytest
from appium import webdriver
from guara.transaction import Application
from guara import it
from setup import OpenAppiumApp, CloseAppiumApp
from home import SubmitTextAppium


@pytest.mark.skip(reason="Complex setup in CI environment")
class TestAppiumIntegration:
    def setup_method(self, method):
        file_path = pathlib.Path(__file__).parent.resolve()
        desired_caps = {
            "platformName": "Android",
            "deviceName": "emulator-5554",
            "browserName": "Chrome",
            "app": "/absolute/path/to/sample.apk",
            "automationName": "UiAutomator2",
            "noReset": True,
            "appWaitActivity": "*",
            "goog:chromeOptions": {"args": ["--headless"]},
        }
        self.driver = webdriver.Remote(
            "http://localhost:4723/wd/hub", desired_capabilities=desired_caps
        )
        self._app = Application(self.driver)
        self._app.at(OpenAppiumApp, url=f"file:///{file_path}/sample.html")

    def teardown_method(self, method):
        self._app.at(CloseAppiumApp)

    def test_local_page(self):
        text = ["cheese", "appium", "test", "bla", "foo"]
        text = text[random.randrange(len(text))]
        self._app.at(SubmitTextAppium, text=text).asserts(
            it.IsEqualTo, f"It works! {text}!"
        )
        self._app.at(SubmitTextAppium, text=text).asserts(it.IsNotEqualTo, "Any")
