import json
import os
from pathlib import Path
from urllib.parse import quote

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


def get_browserstack_driver(scenario_name):
    username = os.getenv('BROWSERSTACK_USERNAME')
    access_key = os.getenv('BROWSERSTACK_ACCESS_KEY')
    if not username or not access_key:
        raise ValueError('Set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY in .env')

    options = webdriver.ChromeOptions()
    options.set_capability('browserName', os.getenv('BROWSERSTACK_BROWSER', 'Chrome'))
    options.set_capability('browserVersion', os.getenv('BROWSERSTACK_BROWSER_VERSION', 'latest'))
    options.set_capability('bstack:options', {
        'os': os.getenv('BROWSERSTACK_OS', 'Windows'),
        'osVersion': os.getenv('BROWSERSTACK_OS_VERSION', '11'),
        'projectName': os.getenv('BROWSERSTACK_PROJECT', 'Reelly Automation'),
        'buildName': os.getenv('BROWSERSTACK_BUILD', 'Task 4 BrowserStack'),
        'sessionName': scenario_name,
    })

    url = f"https://{quote(username)}:{quote(access_key)}@hub-cloud.browserstack.com/wd/hub"
    return webdriver.Remote(command_executor=url, options=options)


def browser_init(context, scenario):
    load_local_env()
    if os.getenv('RUN_ON_BROWSERSTACK', 'false').lower() == 'true':
        context.driver = get_browserstack_driver(scenario.name)
        context.app = Application(context.driver)
        return

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
    browser_init(context, scenario)


def before_step(context, step):
    print('\nStarted step: ', step)


def after_step(context, step):
    if step.status == 'failed':
        print('\nStep failed: ', step)


def after_scenario(context, scenario):
    if os.getenv('RUN_ON_BROWSERSTACK', 'false').lower() == 'true':
        status = 'passed' if scenario.status.name == 'passed' else 'failed'
        reason = 'Scenario passed' if status == 'passed' else f'Scenario {scenario.status.name}'
        context.driver.execute_script(
            'browserstack_executor: {}'.format(json.dumps({
                'action': 'setSessionStatus',
                'arguments': {
                    'status': status,
                    'reason': reason,
                }
            }))
        )

    context.driver.delete_all_cookies()
    context.driver.quit()
