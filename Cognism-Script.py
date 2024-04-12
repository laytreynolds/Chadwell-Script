from playwright.sync_api import Playwright, sync_playwright, expect
import time
from playwright_stealth import stealth_sync
import logging

# Logging output to a file called "Cognism.log". This will log the user, start and end pages and the time ran. 
# Helpful when you forget which page you ended at.
logging.basicConfig(filename='./Cognism.log', filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


def logs():
    user = input("User: ")
    start_page = int(input('Start Page: '))
    end_page = start_page + 19
    logging.info(f'Script ran as {user}\n Start Page: {start_page}\n End Page: {end_page}')

SBR_WS_CDP = "http://127.0.0.1:9666/"
PARTIAL_LIST_NAME = "Newslet"
LIST_NAME = "Newsletter"
SEARCH_LIST = 'Call Centre Accounting'
CONTACTS_PER_C0 = '2'


def run(playwright: Playwright) -> None:

    print('connecting to browser')
    browser = playwright.chromium.connect_over_cdp(SBR_WS_CDP)
    default_context = browser.contexts[0]
    page = default_context.pages[0]
    stealth_sync(page)

    print('navigating')
    page.get_by_role("columnheader", name="").get_by_role("button").click()
    page.locator("label").filter(has_text="Select Page25").click()
    expect(page.locator("lib-items-selector")).to_contain_text("25")
    page.get_by_role("button", name=" Save to List").click()
    page.get_by_text("Enter Name or Create New List").click()
    page.locator("nz-form-control").get_by_role("textbox").fill(PARTIAL_LIST_NAME)
    page.get_by_text(LIST_NAME).click()
    expect(page.locator("nz-form-control")).to_contain_text(LIST_NAME)
    expect(page.get_by_text("Cancel Save")).to_be_visible()
    expect(page.get_by_role("banner")).to_contain_text("Saving 25 contacts in a List")
    page.locator("[id^='cdk-overlay']").get_by_role("button", name="Save").click()

    for _ in range(20):
        print(f"Starting Loop {_}")
        page.query_selector('a[data-cognism="paginate-next-a"]').click()
        time.sleep(1.5)
        page.get_by_role("columnheader", name="").get_by_role("button").click()
        page.locator("label").filter(has_text="Select Page25").click()
        page.get_by_role("button", name=" Save to List").click()
        page.get_by_text("Enter Name or Create New List").click()
        time.sleep(1)
        page.locator("nz-form-control").get_by_role("textbox").fill(PARTIAL_LIST_NAME)
        time.sleep(1.2)
        page.get_by_text(LIST_NAME).click()
        expect(page.locator("nz-form-control")).to_contain_text(
            LIST_NAME
        )
        page.get_by_placeholder("Enter the number of contacts").click()
        page.get_by_placeholder("Enter the number of contacts").fill("2")
        expect(page.get_by_text("Cancel Save")).to_be_visible()
        expect(page.get_by_role("banner")).to_contain_text(
            "Saving 25 contacts in a List"
        )
        page.locator("[id^='cdk-overlay']").get_by_role("button", name="Save").click()
    
        
        
        # ---------------------
    page.click('button[data-cognism="user-menu-button"]')
    page.get_by_text("Log Out").click()
    default_context.close()

logs()

with sync_playwright() as playwright:
    run(playwright)
