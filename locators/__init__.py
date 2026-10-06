# Every locator lives in this package: one module per page (login_locators.py,
# book_store_locators.py, ...), one class per module. Locators are built from the
# Playwright `page`, role-first:
#
# from playwright.sync_api import Page
#
#
# class LoginLocators:
#     def __init__(self, page: Page) -> None:
#         self.username = page.get_by_role("textbox", name="UserName")
#         self.login_button = page.get_by_role("button", name="Login", exact=True)
#
# Order of preference: get_by_role > get_by_label > get_by_placeholder > get_by_text
# > get_by_test_id > CSS. Use CSS only when the element has no accessible role or
# name, and leave a comment saying why.
