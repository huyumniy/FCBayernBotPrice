from selenium.webdriver.common.by import By
import time
import platform
from random import choice
import undetected_chromedriver as webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyshadow.main import Shadow
import sounddevice as sd
import soundfile as sf
import sys, os
import eel
import socket
import shutil
import tempfile
import datetime

WAITX = 30
MAXMIN=True
P_BLOCKS=list(range(101,107))+list(range(119,125))+list(range(229,233))
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
    current_datetime = datetime.datetime.now()
    date_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    with open(file_name, "a") as file:
        file.write(f"{date_str} - block_row_seat: {array1}\n")
        file.write(f"{date_str} - accepted: {array2}\n")


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



@eel.expose
def main(proxy, USR, PWD, maxprc, minprc, radio, near, preferred_block, fifth_category):
    
    print(proxy, USR, PWD, maxprc, minprc, radio, near, preferred_block)
    maxprc = float(maxprc)
    minprc = float(minprc)
    
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
    proxy_extension = ProxyExtension(*(proxy.split(':')))
    # options.add_argument(f"--load-extension={proxy_extension.directory},D:\\projects\\rugby-bot-resale\\NopeCHA")
    options.add_argument(f"--load-extension={proxy_extension.directory}")
    current_directory = os.getcwd()
    is_windows = platform.system() == "Windows"
    chromedriver_filename = "chromedriver.exe" if is_windows else "chromedriver"
    chromedriver_path = os.path.join(current_directory, chromedriver_filename)
    print(chromedriver_path)
    # Create the WebDriver with the configured ChromeOptions
    driver = webdriver.Chrome(
        driver_executable_path=chromedriver_path,
        options=options,
        enable_cdp_events=True,
    )
    screen_width, screen_height = driver.execute_script(
        "return [window.screen.width, window.screen.height];")
    
    desired_width = int(screen_width /2)
    desired_height = int(screen_height)
    driver.set_window_position(0, 0)
    driver.set_window_size(desired_width, screen_height)

    #, driver_executable_path='./chromedriver'
    shadow = Shadow(driver)

    while True:
        driver.execute_script("location.href='Logout.aspx';")
        print('making logout')
        driver.delete_all_cookies()
        driver.get(
            'https://tickets.fcbayern.com/internetverkaufzweitmarkt/EventList.aspx')
        
        login(driver, shadow, USR, PWD)
        print('pass login')
        
        num_seats = int(radio)
       
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
        while not selected:
            time.sleep(3)
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
                    time.sleep(1)
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

        rw_sel = '//*[@id="ctl00_ContentMiddle_TicketList1_GridView1"]//tr[.//*[contains(text(),"Add")]]/td[.//*[contains(text(),"€")]]'
        gut = True
        while True:
            remhed(driver)
            if category:
                try:
                    ensure_check_elem(driver, '//*[@title="Show all tickets"]', click=True)
                    ensure_check_elem(driver, 
                        f'//li[contains(text(),"e {category}")]',tmt=3, click=True)
                    time.sleep(1)
                    ensure_check_elem(driver, 
                        '//*[@class="modalPopup"][contains(@style,"display: none;")]', tmt=600)
                except:
                    time.sleep(WAITX)
                    driver.refresh()
                    continue
            try:
                ensure_check_elem(driver, rw_sel).text
            except:
                print('No available tickets')
                time.sleep(WAITX)#delay 1
                driver.refresh()
                continue
            
            block_row_seat = []
            for row in driver.find_elements(By.XPATH, rw_sel):
                rwdt=row.text.split('\n')
                print(rwdt)
                rwdt[3] = float(rwdt[3].replace(',',".").split(' ')[0])
                if MAXMIN and rwdt[3] > minprc and maxprc > rwdt[3] and not preferred_block:
                    block_row_seat.append(rwdt[:4])
                else:
                    try:
                        nrow=row.text.split('\n')[:3]
                        if nrow[0] in P_BLOCKS and not MAXMIN:
                            block_row_seat.append(nrow)
                    except:pass
            if near:
                block_row = [brs[:2] for brs in block_row_seat]
                if fifth_category:
                    accepted = [[inc for inc in brs if inc]
                            for brs 
                            in block_row_seat if block_row.count(brs[:2]) >= num_seats or brs[3] < 20]
                else:
                    accepted = [[inc for inc in brs if inc]
                            for brs 
                            in block_row_seat if block_row.count(brs[:2]) >= num_seats]
                append_arrays_to_file(block_row_seat, accepted, 'logs.txt')

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
                    if len(ky_accepted) >= num_seats:
                        last_accepted.append(ky_accepted)
                try:
                    selected_s = last_accepted[-1]
                except:
                    try:
                        if MAXMIN and maxprc>25:
                            ensure_check_elem(driver, '//*[contains(@id,"btnNextPag")]',tmt=1,click=True)
                        elif MAXMIN and 25>=maxprc:
                            ensure_check_elem(driver, '//*[contains(@id,"btnLastPag")]',tmt=1,click=True)
                        else:
                            ensure_check_elem(driver, '//*[contains(@id,"btnNextPag")]',tmt=1,click=True)
                        ensure_check_elem(driver, 
                                '//*[@class="modalPopup"][contains(@style,"display: none;")]', tmt=30)
                    except:
                        time.sleep(WAITX)
                        driver.refresh()
                        remhed(driver)
                    continue
            else:
                try:
                    selected_s = [[brs for brs in choice(block_row_seat)]
                    for __ in range(num_seats)]
                except:
                    try:
                        if MAXMIN and maxprc>25:
                            ensure_check_elem(driver, '//*[contains(@id,"btnNextPag")]',tmt=1,click=True)
                        elif MAXMIN and 25>=maxprc:
                            ensure_check_elem(driver, '//*[contains(@id,"btnLastPag")]',tmt=1,click=True)
                        else:
                            ensure_check_elem(driver, '//*[contains(@id,"btnNextPag")]',tmt=1,click=True)
                        ensure_check_elem(driver, 
                                '//*[@class="modalPopup"][contains(@style,"display: none;")]', tmt=30)
                    except:
                        time.sleep(WAITX)
                        driver.refresh()
                        remhed(driver)
                    continue
            
            for s in selected_s[:num_seats]:
                try:
                    if int(driver.find_element(By.XPATH, '//b[contains(text(),"position")]').text.split(' ')[0]) >= num_seats:# and near is False
                        break
                except:
                    pass

                while True:

                    try:
                        seat_sel = f'//td[.//p//span[1]//*[text()="{s[0]}"]][.//p//span[2]//*[text()="{s[1]}"]][.//p//span[3]//*[text()="{s[2]}"]]//a'
                        ckckc = driver.find_element(By.XPATH, seat_sel)
                        driver.execute_script(
                            "arguments[0].scrollIntoView()", ckckc)
                        ensure_check_elem(driver, seat_sel, click=True)
                        time.sleep(.5)

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
                time.sleep(WAITX)
                continue
            try:
                driver.execute_script('window.scrollTo(0,0);')
                ensure_check_elem(driver, 
                    '//td//*[@href="showcart.aspx"]', tmt=5, click=True)
            except:
                pass
            break
        data, fs = sf.read('noti.wav', dtype='float32')  
        sd.play(data, fs)
        status = sd.wait()
        lastcom = input('q: to quit or ENTER to start selecting again: ').lower()
        if lastcom.strip() == 'q':
            driver.quit()
            exit()



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

def print_value(n):
    print(n)

if __name__ == "__main__":
  eel.init('web')
  port = 8000
  while True:
    try:
      if not is_port_open('localhost', port):
        eel.start('main.html', size=(600, 800), port=port)
        # eel.spawn(eel.continue_function()(print_value))
        break
      else: port+=1
    except OSError as e:
      print(e)