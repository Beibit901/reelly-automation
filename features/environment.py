import os
from pathlib import Path

from selenium import webdriver

from app.application import Application


def load_local_env():
    env_path = Path(__file__).resolve().parent.parent / '.env'
    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def browser_init(context):
    load_local_env()
    browser = os.getenv('BROWSER', 'chrome').lower()
    headless = os.getenv('HEADLESS', 'true').lower() != 'false'

    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless=new')
        options.add_argument('--window-size=1440,1200')
        context.driver = webdriver.Chrome(options=options)
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('-headless')
        options.add_argument('--width=1440')
        options.add_argument('--height=1200')
        options.set_preference(
            'general.useragent.override',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
        )
        context.driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f'Unsupported browser: {browser}')

    context.driver.implicitly_wait(4)
    context.app = Application(context.driver)


def before_scenario(context, scenario):
    print('\nStarted scenario: ', scenario.name)
    browser_init(context)


def before_step(context, step):
    print('\nStarted step: ', step)


def after_step(context, step):
    if step.status == 'failed':
        print('\nStep failed: ', step)


def after_scenario(context, feature):
    context.driver.delete_all_cookies()
    context.driver.quit()
