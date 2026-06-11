from behave import given, when, then


@given('Open Reelly main page')
def open_reelly_main_page(context):
    context.app.main_page.open_main_page()


@given('Log in to Reelly')
def log_in_to_reelly(context):
    context.app.sign_in_page.log_in()


@when('Click on settings option')
def click_settings_option(context):
    context.app.settings_page.open_settings()


@when('Click on Contact us option')
def click_contact_us_option(context):
    context.app.settings_page.open_contact_us()


@then('Verify Contact us page opens')
def verify_contact_us_page_opens(context):
    context.app.contact_us_page.verify_contact_us_page_opened()


@then('Verify at least 4 social media icons are shown')
def verify_social_media_icons(context):
    context.app.contact_us_page.verify_at_least_four_social_media_icons()


@then('Verify Connect the company button is available and clickable')
def verify_connect_company_button(context):
    context.app.contact_us_page.verify_connect_company_button_clickable()
