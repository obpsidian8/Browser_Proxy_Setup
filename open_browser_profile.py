from pywinauto.application import Application
import json
import time
import pyautogui
import re
import os
import sys



def open_browser_profile_NO_proxy(profile_name):
    print(f"Opening browser for {profile_name} with NO PROXY ")
    cmd_command = f"\"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe\" --user-data-dir=\"C:\chromepurchase\chromeprofiles_purchase_{profile_name}\" --profile-directory=\"{profile_name}\""
    print(cmd_command)
    app = Application(backend='uia').start(cmd_command, timeout=7)
    app.window(title_re="Chrome")
    time.sleep(4)
    app.window().type_keys('{F6}')
    app.window().type_keys('{ESC}')
    app.window().type_keys('https://www.ultratools.com/tools/yourIPResult')
    app.window().type_keys('{ENTER}')


def run_broswer_profile_with_proxy(profile_name, PROXY_setting):
    cmd_command = f"\"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe\" --user-data-dir=\"C:\chromepurchase\chromeprofiles_purchase_{profile_name}\" --profile-directory=\"{profile_name}\" --proxy-server=\"{PROXY_setting}\""
    print(cmd_command)
    app = Application(backend='uia').start(cmd_command, timeout=7)
    app.window(title_re="Chrome")
    time.sleep(3)
    app.window().type_keys('{F6}')
    app.window().type_keys('{ESC}')
    app.window().type_keys('https://www.ultratools.com/tools/yourIPResult')
    app.window().type_keys('{ENTER}')


def process_account_options_for_vendor(vendor_working_on, users_list):
    proxies_file_name = 'proxies.json'


    proxy_list = json.load(open(proxies_file_name))
    PROXY_setting = None


    options_dict = dict()
    index = 0
    for user in users_list:

        account_str = (f"{user['Account']}").ljust(30, ' ')
        email_str = (f"{user['Username']}").ljust(10, ' ')

        combined_dict_str = f"  {account_str}:{email_str}"

        index += 1

        options_dict.update({str(index): combined_dict_str})


    print(f"\nWhat account are you working on for {vendor_working_on},")


    alert_content = (json.dumps(options_dict, indent=4))

    account_index_number = pyautogui.prompt(text=str(alert_content), title="Enter number corresponding to account and hit OK")

    account_index_number = str(account_index_number)
    account_working_on = options_dict[account_index_number]

    print(f"Account chosen is: {account_working_on}")
    account_working_on_regex = re.compile(r"(.+):")
    account_working_on = account_working_on_regex.search(account_working_on).group(1).strip()

    pyautogui.confirm(text=f"You chose {account_working_on}", title="Chrome Profile Window Manager")
    pyautogui.confirm(text=f"Ok! Opening browser profile for {vendor_working_on}, user {account_working_on}", title="Chrome Profile Window Manager")

    print(f"Ok! Opening browser profile for {vendor_working_on}, user {account_working_on}")

    proxy_id_for_user = None
    for user in users_list:
        if account_working_on == user['Account']:
            proxy_id_for_user = user['proxy_id_assigned']
            break

    proxy_found = False
    print(f"Searching for proxy settings for this user {account_working_on}")
    for proxy_entry in proxy_list:
        if proxy_id_for_user is not None and proxy_id_for_user == proxy_entry['proxy_id']:
            proxyIP = proxy_entry['proxy_address']
            proxyPort = proxy_entry['port']
            PROXY_setting = proxyIP + ":" + proxyPort  # IP:PORT or HOST:PORT
            print("Proxy settings for sepcified proxy id ", PROXY_setting)
            proxy_found = True
            break
        else:
            print("Searching")

    if proxy_found == True:
        run_broswer_profile_with_proxy(account_working_on, PROXY_setting)
    else:
        msg = f"No proxy settings exist for {account_working_on}.\n Opening profile with NO PROXY"
        print(msg)
        pyautogui.confirm(text=msg, title="Chrome Profile Window Manager")
        open_browser_profile_NO_proxy(account_working_on)


def main_process():

    vendor_working_on = pyautogui.confirm("What vendor are you working on", "Choose and option", ['Bestbuy', 'Amazon', 'Newegg', 'NeweggBusiness', 'Dell', 'Walmart', 'No Vendor Yet'])
    print("What vendor are you working on?")

    account_working_on = None
    print(vendor_working_on)

    if vendor_working_on == "Bestbuy":
        users_list = json.load(open('BestbuyAccounts.json'))
        vendor_working_on = "Bestbuy"
        process_account_options_for_vendor(vendor_working_on, users_list)

    if vendor_working_on == "Newegg":
        users_list = json.load(open('NeweggAccounts.json'))
        vendor_working_on = "Newegg"
        process_account_options_for_vendor(vendor_working_on, users_list)

    if vendor_working_on == "Amazon":
        amazon_accounts_file_name = 'AmazonAccounts.json'

        users_list = json.load(open(amazon_accounts_file_name))
        vendor_working_on = "Amazon"
        process_account_options_for_vendor(vendor_working_on, users_list)

    if vendor_working_on == "NeweggBusiness":
        users_list = json.load(open('NeweggBusinessAccounts.json'))
        vendor_working_on = "NeweggBusiness"
        process_account_options_for_vendor(vendor_working_on, users_list)

    if vendor_working_on == "Dell":
        users_list = json.load(open('DellAccounts.json'))
        vendor_working_on = "Dell"
        process_account_options_for_vendor(vendor_working_on, users_list)

    if vendor_working_on == "Walmart":
        users_list = json.load(open('WalmartAccounts.json'))
        vendor_working_on = "Walmart"
        process_account_options_for_vendor(vendor_working_on, users_list)

    if vendor_working_on == "No Vendor Yet":
        users_list = json.load(open('NoVendorAcoount.json'))
        vendor_working_on = "No Vendor Yet"
        process_account_options_for_vendor(vendor_working_on, users_list)

    pyautogui.confirm(text="Profile set. You may access accounts", title="Chrome Profile Window Manager")



if __name__ == '__main__':
    main_process()

