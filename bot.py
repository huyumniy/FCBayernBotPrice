from concurrent.futures import thread
import threading
from selenium.webdriver.common.by import By
import time
import platform
from random import choice
import undetected_chromedriver as webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pyshadow.main import Shadow
import sounddevice as sd
import soundfile as sf
import sys, os
import eel
import socket
import shutil
import tempfile
from pprint import pprint
import asyncio
import random
import requests
import json
import datetime

WAITX = 30
MAXMIN=True
P_BLOCKS=list(range(101,107))+list(range(119,125))+list(range(229,233))

SPREADSHEET_ID = '1WMZaj7idACXKJO7ukdZcDhO807MhU2LoYP2DuJWJ5Wo'
SHEET_TITLE = 'main'


def ensure_check_elem(driver, selector, methode=By.XPATH, tmt=20, click=False):
    var = None
    tmt0 = 0
    while True:
        if tmt0 >= tmt:
            raise Exception('Not Found')
        try:
            var = driver.find_element(methode, selector)
            if click:
                var.click()
            break
        except:
            pass
        tmt0 += 0.5
        time.sleep(0.6)
    return var


def check_for_element(driver, selector, click=False, xpath=False, debug=False):
    try:
        if xpath:
            element = driver.find_element(By.XPATH, selector)
        else:
            element = driver.find_element(By.CSS_SELECTOR, selector)
        if click: 
            driver.execute_script("arguments[0].scrollIntoView();", element)
            # slow_mouse_move_to_element(driver, element)
            element.click()
        return element
    except Exception as e: 
        if debug: print("selector: ", selector, "\n", e)
        return False
    

def wait_for_element(driver, selector, timeout=10, xpath=False, debug=False):
    try:
        element = None
        while timeout > 0:
          try:
              if xpath:
                  element = driver.find_element(By.XPATH, selector)
              else:
                  element = driver.find_element(By.CSS_SELECTOR, selector)
              break
          except: 
              time.sleep(1)
              timeout-=1
        return element
    except Exception as e:
        if debug: print("selector: ", selector, "\n", e)
        return False



def check_for_elements(driver, selector, xpath=False, debug=False):
    try:
        if xpath:
            element = driver.find_elements(By.XPATH, selector)
        else:
            element = driver.find_elements(By.CSS_SELECTOR, selector)
        return element
    except Exception as e: 
        if debug: print("selector: ", selector, "\n", e)
        return False


def check():
    while True:
        a = input('>>')
        if a == "exit":
            break
        try:
            print(eval(a))
        except Exception as r:
            print(r)


class ProxyExtension:
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {"scripts": ["background.js"]},
        "minimum_chrome_version": "76.0.0"
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: %d
            },
            bypassList: ["localhost"]
        }
    };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        { urls: ["<all_urls>"] },
        ['blocking']
    );
    """

    def __init__(self, host, port, user, password):
        self._dir = os.path.normpath(tempfile.mkdtemp())

        manifest_file = os.path.join(self._dir, "manifest.json")
        with open(manifest_file, mode="w") as f:
            f.write(self.manifest_json)
        background_js = self.background_js % (host, int(port), user, password)
        background_file = os.path.join(self._dir, "background.js")
        with open(background_file, mode="w") as f:
            f.write(background_js)

    @property
    def directory(self):
        return self._dir

    def __del__(self):
        shutil.rmtree(self._dir)

ck_acc = False

def remhed(driver):
        try:
            driver.execute_script("document.querySelector('#HeaderNav').remove();")
        except:
            pass


def append_arrays_to_file(array1, array2, file_name):
    try:
        current_datetime = datetime.datetime.now()
        date_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        with open(file_name, "a") as file:
            file.write(f"{date_str} - block_row_seat: {array1}\n")
            file.write(f"{date_str} - accepted: {array2}\n")
    except:
        with open(file_name, "a") as file:
            file.write(f'{date_str} - cant write data')


def login(driver, shadow, USR, PWD):
    driver.get(
        'https://tickets.fcbayern.com/internetverkaufzweitmarkt/EventList.aspx')
    for _ in range(0, 10):
        try:
            shadow.find_element(
                '[data-testid="uc-accept-all-button"]').click()
            break
        except:
            time.sleep(1)
    ensure_check_elem(
        driver, '//*[@class="header-actions"]//a[.//*[contains(text(),"Login")]]', click=True)
    urlx = driver.current_url
    usrnm = ensure_check_elem(driver, '//*[@id="username"]', click=True)
    usrnm.clear()
    usrnm.send_keys(USR)
    passwd = ensure_check_elem(driver, '//*[@type="password"]', click=True)
    passwd.clear()
    passwd.send_keys(PWD+'\n')
    lgntmt=0
    while urlx == driver.current_url:
        if lgntmt>=20:
            login(driver, shadow, USR, PWD)
        time.sleep(.5)
        lgntmt+=.5
    return 1

data = {
    'proxy': '',
    'USR': '',
    'PWD': '',
    'maxprc': 999.0,
    'minprc': 0,
    'radio': [],
    'near': False,
    'preferred_block': False,
    'fifth_category': False
}

server_data = [
  
]

def change_proxy(driver, proxy):
    driver.get('chrome://extensions/')
    js_code = """
        const callback = arguments[0];
        chrome.management.getAll((extensions) => {
            callback(extensions);
        });
    """
    extensions = driver.execute_async_script(js_code)
    filtered_extensions = [extension for extension in extensions if 'Change your proxies with one click' in extension['description']]
    
    extension_id = [extension['id'] for extension in filtered_extensions if 'id' in extension][0]
    vpn_url = f'chrome-extension://{extension_id}/popup.html'
    print(vpn_url)
    driver.get(vpn_url)
    check_for_element(driver, '#editProxyList', click=True)
    text_area = wait_for_element(driver, '.linedtextarea > textarea')
    text_area.clear()
    text_area.send_keys(proxy)
    check_for_element(driver, '#addProxyOK', click=True)
    driver.refresh()
    # selectProxy = wait_for_element(driver, "//*[@id='proxySelectDiv']", xpath=True)
    # selectProxy.click()
    # wait_for_element(selectProxy, '')
    for _ in range(0, 3):
        try:
            selectProxy = wait_for_element(driver, "#selectProxy")
            drop = Select(selectProxy)
            time.sleep(2)
            drop.select_by_value(proxy)
            time.sleep(2)
            break
        except Exception as e: print(e)
    return True


def run(model='0', server_data_id=1, id=1):
    if model == '0':
        global data
    elif model == '1': 
        data = server_data[server_data_id]
    event = data.get('event')
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    #options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--lang=EN')
    prefs = {"credentials_enable_service": False,
        "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)
    if data['proxy']:
        cwd = os.getcwd()
        proxy_extension = ''
        if os.name == 'posix' and platform.system() == 'Darwin':
            proxy_extension = cwd + "/BP-Proxy-Switcher-CUSTOM"
        elif os.name == 'nt':
            proxy_extension = cwd + "\\BP-Proxy-Switcher-CUSTOM"
        options.add_argument(f"--load-extension={proxy_extension}")
    current_directory = os.getcwd()
    is_windows = platform.system() == "Windows"
    chromedriver_filename = "chromedriver.exe" if is_windows else "chromedriver"
    chromedriver_path = os.path.join(current_directory, chromedriver_filename)
    # Create the WebDriver with the configured ChromeOptions
    driver = webdriver.Chrome(
        options=options,
        enable_cdp_events=True,
    )
    screen_width, screen_height = driver.execute_script(
        "return [window.screen.width, window.screen.height];")
    
    desired_width = int(screen_width /2)
    desired_height = int(screen_height)
    driver.set_window_position(0, 0)
    driver.set_window_size(desired_width, screen_height)
    change_proxy(driver, data['proxy'])

    #, driver_executable_path='./chromedriver'
    # input('continue?')
    shadow = Shadow(driver)

    while True:
        if model == '1': 
            data = server_data[server_data_id]
        driver.execute_script("location.href='Logout.aspx';")
        print('making logout')
        driver.delete_all_cookies()
        driver.get(
            'https://tickets.fcbayern.com/internetverkaufzweitmarkt/EventList.aspx')
        proxy_input = wait_for_element(driver, '#proxyInput', timeout=5)
        print(proxy_input.get_attribute('value'))
        login(driver, shadow, data['USR'], data['PWD'])
        print('pass login')
        try:
            if ensure_check_elem(driver, '//*[contains(text(),"Oops! Something went wrong")]', tmt=3):
                data, fs = sf.read('proxy-error.mp3', dtype='float32')  
                sd.play(data, fs)
                status = sd.wait()
                post_request('http://localhost:40/book', {"message": f"Oops! Something went wrong ({data['USR']} {data['PWD']}). Номер рядка в таблиці {id}"})
                eel.sleep(WAITX)
                continue
        except: pass
        num_seats = data['radio'] if data['radio'] != [] else [0]
       
        if MAXMIN:
            category=False
        if category == 999:
            category = False

        nx_sel = '//table[.//*[contains(text()," from ")]]//*[@src="Images/Icons/next.png"]'
        pr_sel = '//table[.//*[contains(text()," from ")]]//*[@src="Images/Icons/prev.png"]'
        bx_sel = '//*[@class="side-box-container"][.//*[contains(text(),"buy online") or contains(text(),"Mem")]]'
        selected = False
        [driver.execute_script(x.get_attribute('href')) for x in driver.find_elements(
            By.XPATH, '//*[@class="card-container"]//a')]
        if not event:
          while not selected:
              eel.sleep(3)
              try:
                  ensure_check_elem(driver, bx_sel, tmt=3)
              except:
                  pass
              boxes = driver.find_elements(By.XPATH, bx_sel)
              mtc = []
              for i, box in enumerate(boxes):
                  mtc.append(box.find_element(
                      By.XPATH, '..//*[contains(text(),"buy online") or contains(text(),"Mem")]').get_attribute('href'))
                  print(i, '\t', box.find_element(
                      By.XPATH, '..//strong').text.strip())
              commands = []
              try:
                  driver.find_element(By.XPATH, nx_sel)
                  commands.append('next')
              except:
                  pass
              try:
                  driver.find_element(By.XPATH, pr_sel)
                  commands.append('prev')
              except:
                  pass

              while True:
                  print('In addition to match ID, You can use one of these commands to change page [', ' | '.join(
                      commands), ']')
                  comd = input('Match ID or page commands >> ').lower().strip()
                  try:
                      driver.execute_script(mtc[int(comd)])
                      eel.sleep(1)
                      ensure_check_elem(
                          driver, '//*[@class="modalPopup"][contains(@style,"display: none;")]', tmt=60)
                      selected = True
                      break
                  except:
                      pass
                  if comd not in commands:
                      print('Please insert a correct command...')
                  else:
                      if comd == 'next':
                          ensure_check_elem(driver, nx_sel, click=True)
                          break
                      elif comd == 'prev':
                          ensure_check_elem(driver, pr_sel, click=True)
                          break
        elif event:
          change_data = False
          success_data = False
          driver.execute_script("""
                      document.querySelector('div[style*="height:80px"]').style.display = 'none';
                  """)
          while not change_data and not success_data:
            try:
                is_member = ''
                for id, event_element in enumerate(check_for_elements(driver, '//*[@class="fcb-row-align-top"]', xpath=True)):
                    print('INDEX:', id)
                    event_ensure = check_for_element(event_element, f'.//div[2]/div[1]/strong/span[contains(text(), "{event}")]', xpath=True)
                    if event_ensure:
                        print(event_ensure.text)
                    if event_ensure:
                        is_member = wait_for_element(event_element, './/*[contains(text(),"buy online") or contains(text(),"Booking for Members only")]', xpath=True)
                        
                        if not is_member:
                            print(f"Не можливо придбати квитки на введеному аккаунті ({data['USR']} {data['PWD']}). Номер рядка в таблиці {id}")
                            post_request('http://localhost:40/book', {"message": f"Не можливо придбати квитки на введеному аккаунті ({data['USR']} {data['PWD']}). Номер рядка в таблиці {id}"})
                            time.sleep(300)
                            change_data = True
                            break  # Breaks from the for loop
                        
                        elif is_member:
                            # Click on 'is_member'
                            while True:
                                if check_for_elements(driver, '.fcb-row-align-top'):
                                    is_member.click()
                                    time.sleep(5)
                                else:
                                    break
                            
                            success_data = True
                            print("Member booking success!")
                            break  # Breaks from the for loop

                # Exit the loop if booking was successful
                if success_data: break
                if is_member == None or is_member == False: continue

                # Check for the next page
                next_page = check_for_element(driver, nx_sel, click=True, xpath=True)

                # Wait for the page to load
                while not check_for_element(driver, "//div[@id='ctl00_PleaseWaitMessagePanel' and contains(@style, 'display: none')]", xpath=True):
                    time.sleep(1)

                # If there is no next page, handle the error and break
                if not next_page:
                    print(f'Введеної події {event} не існує, перевірте правильність написання')
                    post_request('http://localhost:40/book', {"message": f"Введеної події {event} не існує, перевірте правильність написання. Номер рядка в таблиці {id}"})
                    time.sleep(300)
                    change_data = True
                    break
            except Exception as e:
                print("Exception in loop", e)


            # Ensure that the outer while loop continues only if `change_data` is set
            if change_data:
                continue


                
        rw_sel = '//*[@id="ctl00_ContentMiddle_TicketList1_GridView1"]//tr[.//*[contains(text(),"Add")]]/td[.//*[contains(text(),"€")]]'
        gut = True
        temp_data = ''
        temp_url = driver.current_url
        if model == '1': 
            temp_data = data
        restart_credentials = False

        while True:
            print(temp_data['proxy'], server_data[server_data_id]['proxy'])
            if not check_for_element(driver, '#ctl00_ContentMiddle_TicketList1_GridView1'): 
                restart_credentials = True
                break
            if model == '1':
                print(temp_data['proxy'], server_data[server_data_id]['proxy'])
                if temp_data['proxy'] != server_data[server_data_id]['proxy']:
                    change_proxy(driver, server_data[server_data_id]['proxy'])
                    restart_credentials = True
                    break
                if temp_data['USR'] != server_data[server_data_id]['USR'] or temp_data['PWD'] != server_data[server_data_id]['PWD'] or \
                temp_data['event'] != server_data[server_data_id]['event']:
                    print('User credentials have changed. Exiting loop.')
                    restart_credentials = True
                    break
            remhed(driver)
            if category:
                try:
                    ensure_check_elem(driver, '//*[@title="Show all tickets"]', click=True)
                    ensure_check_elem(driver, 
                        f'//li[contains(text(),"e {category}")]',tmt=3, click=True)
                    eel.sleep(1)
                    ensure_check_elem(driver, 
                        '//*[@class="modalPopup"][contains(@style,"display: none;")]', tmt=600)
                except:
                    eel.sleep(WAITX)
                    driver.refresh()
                    continue
            try:
                ensure_check_elem(driver, rw_sel).text
            except:
                print('No available tickets')
                eel.sleep(WAITX)#delay 1
                driver.refresh()
                continue
            
            block_row_seat = []
            block_row_seat_price = []
            for row in driver.find_elements(By.XPATH, rw_sel):
                rwdt=row.text.split('\n')
                rwprc = float(rwdt[3].replace(',',".").split(' ')[0])
                if MAXMIN and rwprc > data['minprc'] and data['maxprc'] > rwprc and not data['preferred_block']:
                    block_row_seat.append(rwdt[:3])
                    block_row_seat_price.append(rwdt[:3] + [rwprc])
                else:
                    try:
                        nrow=row.text.split('\n')[:3]
                        if nrow[0] in P_BLOCKS and not MAXMIN:
                            block_row_seat.append(nrow)
                            block_row_seat_price.append(nrow + [rwprc])
                    except:pass
            if data['near']:
                block_row = [brs[:2] for brs in block_row_seat]
                accepted = []
                if data['fifth_category']:
                    for index, brs in enumerate(block_row_seat):
                        if block_row.count(brs[:2]) >= min(num_seats) and block_row.count(brs[:2]) <= max(num_seats) or block_row_seat_price[index][3] < 20:
                            inc_list = []
                            for inc in brs:
                                if inc:
                                    inc_list.append(inc)
                            accepted.append((inc_list))
                else:
                    accepted = [[inc for inc in brs if inc]
                            for brs 
                            in block_row_seat if block_row.count(brs[:2]) >= min(num_seats) and block_row.count(brs[:2]) <= max(num_seats)]
                append_arrays_to_file(block_row_seat_price, accepted, 'logs.txt')

                magic_accepted = {}

                for acc in accepted:
                    magic_accepted['-'.join([str(j) for j in acc[:2]])] = []
                last_accepted = []
                for ky in list(magic_accepted.keys()):
                    ky_accepted = []
                    for acc in accepted:
                        if [k for k in ky.split('-')] == acc[:2]:
                            if ky_accepted == [] or int(ky_accepted[-1][-1]) - int(acc[-1]) in [1, -1]:
                                ky_accepted.append(acc)
                            else:
                                ky_accepted = []
                    if len(ky_accepted) >= min(num_seats) and len(ky_accepted) <= max(num_seats):
                        last_accepted.append(ky_accepted)
                try:
                    print(last_accepted)
                    selected_s = last_accepted[-1]
                except:
                    try:
                        if MAXMIN and data['maxprc']>25:
                            ensure_check_elem(driver, '//*[contains(@id,"btnNextPag")]',tmt=1,click=True)
                        elif MAXMIN and 25>=data['maxprc']:
                            ensure_check_elem(driver, '//*[contains(@id,"btnLastPag")]',tmt=1,click=True)
                        else:
                            ensure_check_elem(driver, '//*[contains(@id,"btnNextPag")]',tmt=1,click=True)
                        ensure_check_elem(driver, 
                                '//*[@class="modalPopup"][contains(@style,"display: none;")]', tmt=30)
                    except:
                        eel.sleep(WAITX)
                        driver.refresh()
                        remhed(driver)
                    continue
            else:
                try:
                    selected_s = [[brs for brs in choice(block_row_seat)]
                    for __ in range(max(num_seats))]
                except:
                    try:
                        if MAXMIN and data['maxprc']>25:
                            ensure_check_elem(driver, '//*[contains(@id,"btnNextPag")]',tmt=1,click=True)
                        elif MAXMIN and 25>=data['maxprc']:
                            ensure_check_elem(driver, '//*[contains(@id,"btnLastPag")]',tmt=1,click=True)
                        else:
                            ensure_check_elem(driver, '//*[contains(@id,"btnNextPag")]',tmt=1,click=True)
                        ensure_check_elem(driver, 
                                '//*[@class="modalPopup"][contains(@style,"display: none;")]', tmt=30)
                    except:
                        eel.sleep(WAITX)
                        driver.refresh()
                        remhed(driver)
                    continue
            print(selected_s[:max(num_seats)])
            print(data)
            for s in selected_s[:max(num_seats)]:
                try:
                    position = int(driver.find_element(By.XPATH, '//b[contains(text(),"position")]').text.split(' ')[0])
                    if position >= min(num_seats) and position <= max(num_seats):# and near is False
                        print('position: ', position)
                        break
                except:
                    pass
                try_to_purchase = 0
                while True:

                    try:
                        print(try_to_purchase)
                        if try_to_purchase == 1: break
                        seat_sel = f'//td[.//p//span[1]//*[text()="{s[0]}"]][.//p//span[2]//*[text()="{s[1]}"]][.//p//span[3]//*[text()="{s[2]}"]]//a'
                        ckckc = driver.find_element(By.XPATH, seat_sel)
                        driver.execute_script(
                            "arguments[0].scrollIntoView()", ckckc)
                        ensure_check_elem(driver, seat_sel, click=True)
                        eel.sleep(.5)
                        try_to_purchase += 1
                    except:
                        break
                    while True:
                        try:
                            ensure_check_elem(driver,
                                '//*[@class="modalPopup"][contains(@style,"display: none;")]', tmt=1)
                            try:
                                ensure_check_elem(driver, 
                                    '//*[@value="Back"]', tmt=1, click=True)
                                remhed(driver)
                                gut = False
                                break
                            except:
                                pass
                            break
                        except:
                            pass
            if gut == False:
                eel.sleep(WAITX)
                continue
            cart_check_value = cart_check(driver, num_seats)
            if not cart_check_value: 
                print('in cart_check', cart_check_value)
                eel.sleep(WAITX)
                driver.refresh()
                continue 
            try:
                driver.execute_script('window.scrollTo(0,0);')
                ensure_check_elem(driver, 
                    '//td//*[@href="showcart.aspx"]', tmt=5, click=True)
            except:
                pass
            break
        if restart_credentials: continue
        sound_data, fs = sf.read('noti.wav', dtype='float32')  
        sd.play(sound_data, fs)
        status = sd.wait()

        card_containers = check_for_elements(driver, 'td > .card-container')
        data_to_send = f'*Усього квитків:* {len(card_containers)}\n'
        for number, card_container in enumerate(card_containers):
          event_info = check_for_elements(card_container, 'p > span > span')
          event_name = event_info[1].text
          seat_information = event_info[2].text
          event_category = event_info[3].text
          proxy_input = wait_for_element(driver, '#proxyInput', timeout=5)
          print(proxy_input.get_attribute('value'))
          price = check_for_element(card_container, 'div > div > span')
          if price: price = price.text
          data_to_send += f'*Квиток {number+1}:*\n*Event:* {event_name}\n*Seat Info:* {seat_information}\n*Category:* {event_category}\n*Price:* {price}\n\n'
        data_to_send += f'*Url:* {driver.current_url}'
        post_request('http://localhost:40/cookie', {"data": data_to_send, "cookie": driver.get_cookies(),\
        'ua': driver.execute_script('return navigator.userAgent'), 'proxy': proxy_input.get_attribute('value')})
        
        
        time.sleep(600)

def cart_check(driver, num_seats):
    try:
        position = int(driver.find_element(By.XPATH, '//b[contains(text(),"position")]').text.split(' ')[0])
        return position >= min(num_seats) and position <= max(num_seats)
    except: return False

@eel.expose
def main(proxy, USR, PWD, maxprc, minprc, radio, near, preferred_block, fifth_category):
    global data
    data.update({
        'proxy': proxy,
        'USR': USR,
        'PWD': PWD,
        'maxprc': float(maxprc),
        'minprc': float(minprc),
        'radio': radio,
        'near': near,
        'preferred_block': preferred_block,
        'fifth_category': fifth_category
    })
    eel.spawn(run)


@eel.expose
def restart_main(proxy, USR, PWD, maxprc, minprc, radio, near, preferred_block, fifth_category):
    print("Restarting the process...")
    global data
    data.update({
        'proxy': proxy,
        'USR': USR,
        'PWD': PWD,
        'maxprc': float(maxprc),
        'minprc': float(minprc),
        'radio': radio,
        'near': near,
        'preferred_block': preferred_block,
        'fifth_category': fifth_category
    })
    print("Process restarted.")


def parse_json_from_response(rep):
    # Extract the substring starting from the 47th character to the second-to-last character
    json_string = rep[47:-2]
    
    # Parse the JSON string
    try:
        parsed_data = json.loads(json_string)
        return parsed_data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None


def get_request(url):
    try:
        print(url)
        headers = {'Accept': 'application/json'}
        response = requests.get(f"{url}", headers=headers)
        return response.text
    except Exception as e:
        print("get_request Exception", e)
    # Check the response status code
    if response.status_code == 200:
        print("GET request successful!")
    else:
        print("GET request failed.")


def post_request(url, data=None):
    try:
        print(url)
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        response = requests.post(f"{url}", headers=headers, json=data)
        return response.text
    except Exception as e:
        print("post_request Exception", e)
    # Check the response status code
    if response.status_code == 200:
        print("POST request successful!")
    else:
        print("POST request failed.")

  
def receive_sheet_data(sheet_raw):
    return sheet_raw.get('v') if isinstance(sheet_raw, dict) else None




def get_data_from_google_sheets():
    global server_data
    try:
        sheet_range = "A1:K"
        api_url = f'https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?sheet={SHEET_TITLE}&range={sheet_range}'
        response = get_request(api_url)
        sheet_data = parse_json_from_response(response)
        data = []
        if sheet_data['status'] == 'ok':
          sheet_rows = sheet_data['table']['rows']
          for sheet_row in sheet_rows:
            email = receive_sheet_data(sheet_row['c'][0])
            password = receive_sheet_data(sheet_row['c'][1])
            proxy = receive_sheet_data(sheet_row['c'][2])
            event = receive_sheet_data(sheet_row['c'][3])
            amount_range = receive_sheet_data(sheet_row['c'][4])
            min_price = receive_sheet_data(sheet_row['c'][5])
            max_price = receive_sheet_data(sheet_row['c'][6])
            category_5th = receive_sheet_data(sheet_row['c'][7])
            near = receive_sheet_data(sheet_row['c'][8])
            blocks = receive_sheet_data(sheet_row['c'][9])
            data.append({
                'proxy': proxy,
                'USR': email,
                'PWD': password,
                'event': event,
                'maxprc': max_price,
                'minprc': min_price,
                'radio': [int(amount) for amount in amount_range.split(' ')] if isinstance(amount_range, str) else int(amount_range),
                'near': near,
                'preferred_block': blocks,
                'fifth_category': category_5th,
                })
          server_data = data

    except Exception as e:
        print(f"An error occurred in get_data_from_google_sheets: {e}")
        return None
    

def is_port_open(host, port):
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    sock.connect((host, port))
    return True
  except (socket.timeout, ConnectionRefusedError):
    return False
  finally:
    sock.close()


def check_model():
  while True:
    model = input("Choose model:\n0  Client Model [DEFAULT]\n1  Server Model\n--> ")
    
    if model == '0' or model == '1' or model == '':
      # If empty string, set model to '0'
      if model == '':
        model = '0'
      return model
    else:
        print("Invalid input. Please enter '0', '1', or leave it blank for default (0).")

def periodic_google_sheet_check():
    while True:
        time.sleep(120)
        print('Checking for googlesheet data...')
        get_data_from_google_sheets()
        print("Google Sheets data refreshed.")


if __name__ == "__main__":
    selected_model = check_model()
    if selected_model == '0':
        eel.init('web')

        port = 8000
        while True:
            try:
                if not is_port_open('localhost', port):
                    eel.start('main.html', size=(600, 800), port=port)
                    break
                else:
                    port += 1
            except OSError as e:
                print(e)
    elif selected_model == '1':
        # Start a thread for checking Google Sheets every 5 minutes
        google_sheet_thread = threading.Thread(target=periodic_google_sheet_check)
        google_sheet_thread.daemon = True  # Ensures thread exits when main program exits
        google_sheet_thread.start()

        get_data_from_google_sheets()  # Initial call to get the data

        threads = []
        for id, row in enumerate(server_data):
            print(row)
            thread = threading.Thread(target=run, args=('1', id, id + 2))
            thread.start()
            threads.append(thread)

            delay = random.uniform(5, 10)
            time.sleep(delay)

        for thread in threads:
            thread.join()