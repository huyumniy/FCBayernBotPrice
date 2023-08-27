from selenium.webdriver.common.by import By
import time
import platform
from random import choice
import undetected_chromedriver as webdriver
from pyshadow.main import Shadow
import sounddevice as sd
import soundfile as sf
import sys, os



WAITX = 30
PROXY= True
MAXMIN=True
P_BLOCKS=list(range(101,107))+list(range(119,125))+list(range(229,233))
def ensure_check_elem(selector, methode=By.XPATH, tmt=20, click=False):
    global driver
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

if __name__=="__main__":
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
    
    desired_width = int(screen_width / 3)
    desired_height = int(screen_height / 3)
    driver.set_window_position(0, 0)
    driver.set_window_size(desired_width, screen_height)

    #, driver_executable_path='./chromedriver'
    shadow = Shadow(driver)


    USR=input('Username/Email: ')
    PWD=input('password: ')
    if PROXY:
        driver.get('chrome://extensions')
        input('start')
    def remhed():
        try:
            driver.execute_script("document.querySelector('#HeaderNav').remove();")
        except:
            pass
    def login():
        global ck_acc
        driver.get(
            'https://tickets.fcbayern.com/internetverkaufzweitmarkt/EventList.aspx')
        if not ck_acc:
            while True:
                try:
                    shadow.find_element(
                        '[data-testid="uc-accept-all-button"]').click()
                    ck_acc = True
                    break
                except:
                    time.sleep(.5)
        ensure_check_elem(
            '//*[@class="header-actions"]//a[.//*[contains(text(),"Login")]]', click=True)
        urlx = driver.current_url
        usrnm = ensure_check_elem('//*[@id="username"]', click=True)
        usrnm.clear()
        usrnm.send_keys(USR)
        passwd = ensure_check_elem('//*[@type="password"]', click=True)
        passwd.clear()
        passwd.send_keys(PWD+'\n')
        lgntmt=0
        while urlx == driver.current_url:
            if lgntmt>=20:
                login()
            time.sleep(.5)
            lgntmt+=.5
        return 1

    ck_acc = False
    while True:
        # driver.delete_all_cookies()
        driver.execute_script("location.href='Logout.aspx';")
        login()

        driver.get(
            'https://tickets.fcbayern.com/internetverkaufzweitmarkt/EventList.aspx')
        while True:
            try:
                num_seats = int(input('Number Of seats: '))
                break
            except:
                print('Please insert correct values')
        if MAXMIN:
            while True:
                try:
                    maxprc = int(input('Max Price: '))
                    break
                except:
                    print('Please insert correct values')
            while True:
                try:
                    minprc = int(input('Min Price: '))
                    break
                except:
                    print('Please insert correct values')
        while True:
            if MAXMIN:
                category=False
                break
            try:
                category = int(input('Category [number or 999 for all]: '))
                if category == 999:
                    category = False
                break
            except:
                print('Please insert correct values')

        near = input(
            'Near Each Other [Y:N] (default is N):').lower().strip() == "y"
        preferred_block = input(
            'Preferred Blocks Only [Y:N] (default is N):').lower().strip() == "y"
        nx_sel = '//table[.//*[contains(text()," from ")]]//*[@src="Images/Icons/next.png"]'
        pr_sel = '//table[.//*[contains(text()," from ")]]//*[@src="Images/Icons/prev.png"]'
        bx_sel = '//*[@class="side-box-container"][.//*[contains(text(),"buy online") or contains(text(),"Mem")]]'
        selected = False
        [driver.execute_script(x.get_attribute('href')) for x in driver.find_elements(
            By.XPATH, '//*[@class="card-container"]//a')]
        while not selected:
            time.sleep(3)
            try:
                ensure_check_elem(bx_sel, tmt=3)
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
                        '//*[@class="modalPopup"][contains(@style,"display: none;")]', tmt=60)
                    selected = True
                    break
                except:
                    pass
                if comd not in commands:
                    print('Please insert a correct command...')
                else:
                    if comd == 'next':
                        ensure_check_elem(nx_sel, click=True)
                        break
                    elif comd == 'prev':
                        ensure_check_elem(pr_sel, click=True)
                        break

        rw_sel = '//*[@id="ctl00_ContentMiddle_TicketList1_GridView1"]//tr[.//*[contains(text(),"Add")]]/td[.//*[contains(text(),"€")]]'
        gut = True
        while True:
            remhed()
            if category:
                try:
                    ensure_check_elem('//*[@title="Show all tickets"]', click=True)
                    ensure_check_elem(
                        f'//li[contains(text(),"e {category}")]',tmt=3, click=True)
                    time.sleep(1)
                    ensure_check_elem(
                        '//*[@class="modalPopup"][contains(@style,"display: none;")]', tmt=600)
                except:
                    time.sleep(WAITX)
                    driver.refresh()
                    continue
            try:
                ensure_check_elem(rw_sel).text
            except:
                print('No available tickets')
                time.sleep(WAITX)#delay 1
                driver.refresh()
                continue
            
            block_row_seat = []
            for row in driver.find_elements(By.XPATH, rw_sel):
                rwdt=row.text.split('\n')
                rwprc=float(rwdt[3].replace(',',".").split(' ')[0])
                if MAXMIN and rwprc > minprc and maxprc > rwprc and not preferred_block:
                    block_row_seat.append(rwdt[:3])
                else:
                    try:
                        nrow=row.text.split('\n')[:3]
                        if nrow[0] in P_BLOCKS and not MAXMIN:
                            block_row_seat.append(nrow)
                    except:pass
            if near:
                block_row = [brs[:2] for brs in block_row_seat]
                accepted = [[inc for inc in brs if inc]
                            for brs in block_row_seat if block_row.count(brs[:2]) >= num_seats]
                magic_accepted = {}

                for acc in accepted:
                    magic_accepted['-'.join([str(j) for j in acc[:2]])] = []
                last_accepted = []
                for ky in list(magic_accepted.keys()):
                    ky_accepted = []
                    for acc in accepted:
                        if [k for k in ky.split('-')] == acc[:2]:
                            if ky_accepted == [] or ky_accepted[-1][-1]-acc[-1] in [1, -1]:
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
                            ensure_check_elem('//*[contains(@id,"btnNextPag")]',tmt=1,click=True)
                        elif MAXMIN and 25>=maxprc:
                            ensure_check_elem('//*[contains(@id,"btnLastPag")]',tmt=1,click=True)
                        else:
                            ensure_check_elem('//*[contains(@id,"btnNextPag")]',tmt=1,click=True)
                        ensure_check_elem(
                                '//*[@class="modalPopup"][contains(@style,"display: none;")]', tmt=30)
                    except:
                        time.sleep(WAITX)
                        driver.refresh()
                        remhed()
                    continue
            else:
                try:
                    selected_s = [[brs for brs in choice(block_row_seat)]
                    for __ in range(num_seats)]
                except:
                    try:
                        if MAXMIN and maxprc>25:
                            ensure_check_elem('//*[contains(@id,"btnNextPag")]',tmt=1,click=True)
                        elif MAXMIN and 25>=maxprc:
                            ensure_check_elem('//*[contains(@id,"btnLastPag")]',tmt=1,click=True)
                        else:
                            ensure_check_elem('//*[contains(@id,"btnNextPag")]',tmt=1,click=True)
                        ensure_check_elem(
                                '//*[@class="modalPopup"][contains(@style,"display: none;")]', tmt=30)
                    except:
                        time.sleep(WAITX)
                        driver.refresh()
                        remhed()
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
                        ensure_check_elem(seat_sel, click=True)
                        time.sleep(.5)

                    except:
                        break
                    while True:
                        try:
                            ensure_check_elem(
                                '//*[@class="modalPopup"][contains(@style,"display: none;")]', tmt=1)
                            try:
                                ensure_check_elem(
                                    '//*[@value="Back"]', tmt=1, click=True)
                                remhed()
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
                ensure_check_elem(
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
