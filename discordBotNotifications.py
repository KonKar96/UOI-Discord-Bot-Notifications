from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time
import datetime
import requests
import discord
import textwrap
import sys
import asyncio
import os


def sleep(x):
    # print(
    #     "------------------------------------------------------- \n                    sleeping for"
    # )
    for i in range(x, 0, -1):
        # sys.stdout.write(str(i) + " ")
        # sys.stdout.flush()
        time.sleep(1)
    # print(
    #     "\n------------------------------------------------------- \n                    waking up"
    # )


def find(driver, xpath):
    tries = 0
    while True:
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element.location_once_scrolled_into_view
            return element
        except (
            exceptions.StaleElementReferenceException,
            exceptions.ElementClickInterceptedException,
            exceptions.ElementNotInteractableException,
            exceptions.TimeoutException,
            AttributeError,
            UnboundLocalError,
        ):
            tries += 1
            if tries > 5:
                return None
            pass


def telegram_bot_sendtext(bot_message):
    bot_token = os.environ.get("BOT_TOKEN")
    bot_chatID = os.environ.get("BOT_CHAT_ID")
    send_text = (
        "https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage?chat_id="
        + bot_chatID
        + "&parse_mode=Markdown&text="
        + bot_message
    )
    response = requests.get(send_text)
    return response.json()


def compare_arrays(course_name, array, announcements):
    if array[0] == ["0"]:
        print(f"First Page Scrape For {course_name}")
        array[0] = []
        print(f"Found {len(announcements)} Announcements")
        for announcement in announcements:
            array[0].append(announcement)
        array[1] = array[0]
        return array
    print(f"Page Scrape For {course_name}")
    str = ""
    array[1] = []
    for announcement in announcements:
        array[1].append(announcement)
    if array[0] != array[1]:
        print("Change Detected With Different New Array")
        for item in array[1]:
            if item not in array[0]:
                str += item + "\n"
        print(str)
    else:
        str = "0"
    array[2] = str
    array[0] = array[1]
    return array


def theoria_ypologismou(driver, array, course_name):
    driver.get("http://www.cse.uoi.gr/~palios/automata/")
    sleep(2)
    driver.refresh()
    if find(driver, "//h2[@style='color:red']") == None:
        print("NOT LOADED")
        return array
    announcements = driver.find_elements(By.XPATH, "//body/ul[2]/li")
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def diktya_1(driver, array, course_name):
    driver.get("http://www.cse.uoi.gr/~epap/MYY703/")
    sleep(2)
    driver.refresh()
    if find(driver, "//div[@class='customh1'][.='Ανακοινώσεις']") == None:
        return array
    announcements = driver.find_elements(By.XPATH, "//div[@class='announcement']")
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def texniti_nohmosynh(driver, array, course_name):
    driver.get("https://www.cse.uoi.gr/~arly/courses/ai/ai.html")
    sleep(2)
    driver.refresh()
    if find(driver, "//h2[7]") == None:
        return array
    announcements = driver.find_elements(
        By.XPATH,
        "//body/div/child::*[preceding::h2[.='Ανακοινώσεις'] and following::span[.='Περιγραφή Μαθήματος']]",
    )
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def ypologistiki_nohmosynh(driver, array, course_name):
    driver.get("https://www.cse.uoi.gr/~arly/courses/nn/nn.html")
    sleep(2)
    driver.refresh()
    if find(driver, "//h2[7]") == None:
        return array
    announcements = driver.find_elements(
        By.XPATH, "//body/div/child::*[preceding::h2[.='Ανακοινώσεις']]"
    )
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def leitourgika_systimata(driver, array, course_name):
    driver.get("http://www.cse.uoi.gr/~stergios/teaching/myy601/")
    sleep(2)
    driver.refresh()
    if find(driver, "//frameset") == None:
        return array
    driver.switch_to.frame(1)
    announcements = driver.find_elements(By.XPATH, "//p[not(.//b)]")
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def anaktisi_pliroforias(driver, array, course_name):
    driver.get("http://www.cs.uoi.gr/~pitoura/courses/ap/ap22/")
    sleep(2)
    driver.refresh()
    body = find(driver, "//body").text.split("\n")
    announcements = []
    for i in range((body.index("Ανακοινώσεις") + 1), body.index("Βιβλία")):
        announcements.append(body[i])
    return compare_arrays(course_name, array, announcements)


def baseis_dedomenwn(driver, array, course_name):
    driver.get("https://www.cs.uoi.gr/~pitoura/courses/db/db21/index.html")
    sleep(2)
    driver.refresh()
    body = find(driver, "//body").text.split("\n")
    announcements = []
    for i in range((body.index("Ανακοινώσεις") + 1), body.index("Διδακτικό Βιβλίο")):
        announcements.append(body[i])
    return compare_arrays(course_name, array, announcements)


def texnologia_logismikou(driver, array, course_name):
    driver.get("https://www.cse.uoi.gr/~zarras/se.htm")
    sleep(2)
    driver.refresh()
    if find(driver, "//h3[normalize-space()='Announcements']") == None:
        return array
    announcements = driver.find_elements(
        By.XPATH,
        "//td/*[preceding::h3[normalize-space()='Announcements'] and following::h3[normalize-space()='Useful Links']]",
    )
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def programmatismos_systimatwn(driver, array, course_name):
    driver.get("http://www.cse.uoi.gr/~dimako/teaching/fall20.html")
    sleep(2)
    driver.refresh()
    if find(driver, "//h4[contains(text(),'Ανακοινωσεις / Announcements')]") == None:
        return array
    announcements = driver.find_elements(
        By.XPATH, "//ul[@class='twocolor-list']/child::li"
    )
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def arxes_glwsswn(driver, array, course_name):
    driver.get("http://www.cse.uoi.gr/~cnomikos/courses/pl/pl-main.htm")
    sleep(2)
    driver.refresh()

    if find(driver, "//ul[1]//span/parent::li") == None:
        return array
    announcements = driver.find_elements(By.XPATH, "//ul[1]//span/parent::li")
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def diakrita2(driver, array, course_name):
    driver.get("http://www.cse.uoi.gr/~kontog/courses/Discrete-Math-2/")
    sleep(2)
    driver.refresh()
    if find(driver, "//a[@name='announcements']") == None:
        return array
    announcements = driver.find_elements(
        By.XPATH, "//ul[preceding::a[@name='announcements']]/li"
    )
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def anaptixi_logismikou(driver, array, course_name):
    driver.get("http://www.cs.uoi.gr/~pvassil/courses/sw_dev/intro.html")
    sleep(2)
    driver.refresh()
    if find(driver, "//h1[contains(text(),'Νέα')]") == None:
        return array
    announcements = driver.find_elements(By.XPATH, "//section[@id='news']/ul/child::li")
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def prox_themata_texnologias(driver, array, course_name):
    driver.get("https://www.cse.uoi.gr/~pvassil/courses/db_III/info.html")
    sleep(2)
    driver.refresh()
    if find(driver, "//h1[contains(text(),'Ανακοινώσεις')]") == None:
        return array
    announcements = driver.find_elements(By.XPATH, "//section[@id='news']/ul/child::li")
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def asyrmata_diktia(driver, array, course_name):
    driver.get("https://www.cs.uoi.gr/~epap/MYE006/")
    sleep(2)
    driver.refresh()
    if find(driver, "//div[@class='customh1'][.='Ανακοινώσεις']") == None:
        return array
    announcements = driver.find_elements(By.XPATH, "//div[@class='announcement']")
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def anaptixi_logismikou_2(driver, array, course_name):
    driver.get("https://www.cse.uoi.gr/~zarras/soft-devII.htm")
    sleep(2)
    driver.refresh()
    if find(driver, "//h3[normalize-space()='Announcements']") == None:
        return array
    announcements = driver.find_elements(
        By.XPATH,
        "//td/*[preceding::h3[normalize-space()='Announcements'] and following::h3[normalize-space()='Useful Links']]",
    )
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def parallila_systimata(driver, array, course_name):
    driver.get("https://www.cse.uoi.gr/~dimako/teaching/spring22.html")
    sleep(2)
    driver.refresh()
    if find(driver, "//h4[contains(text(),'Ανακοινωσεις')]") == None:
        return array
    announcements = driver.find_elements(
        By.XPATH,
        "//ul[@class='twocolor-list']/li",
    )
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def ypolistiki_poliplokotita(driver, array, course_name):
    driver.get("https://www.cse.uoi.gr/~cnomikos/courses/cc/cc-main.htm")
    sleep(2)
    driver.refresh()
    if find(driver, "//body/p[1]") == None:
        return array
    announcements = driver.find_elements(
        By.XPATH,
        "//font[@size='4' and preceding::font[contains(text(),'ΑΝΑΚΟΙΝΩΣΗ')] and following::font[contains(.,'ΕΚΠΑΙΔΕΥΤΙΚΟ ΥΛΙΚΟ')]]",
    )
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def ilektroniki(driver, array, course_name):
    driver.get("https://www.cs.uoi.gr/~tsiatouhas/MYY404-ELEC.htm")
    sleep(2)
    driver.refresh()
    if find(driver, "//*[.='Ανακοινώσεις']") == None:
        return array
    announcements = driver.find_elements(
        By.XPATH,
        "//tr[preceding::*[.='Ανακοινώσεις'] and following::*[.='Γενικές Ανακοινώσεις']]",
    )
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def vasikes_arxes_kiklomatwn(driver, array, course_name):
    driver.get("https://www.cs.uoi.gr/~tsiatouhas/MYY203.htm")
    sleep(2)
    driver.refresh()
    if find(driver, "//*[.='Ανακοινώσεις']") == None:
        return array
    announcements = driver.find_elements(
        By.XPATH,
        "//tr[preceding::*[.='Ανακοινώσεις'] and following::*[.='Γενικές Ανακοινώσεις']]",
    )
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def vlsi(driver, array, course_name):
    driver.get("https://www.cs.uoi.gr/~tsiatouhas/MYE018-VLSI.htm")
    sleep(2)
    driver.refresh()
    if find(driver, "//*[.='Ανακοινώσεις Μαθήματος']") == None:
        return array
    announcements = driver.find_elements(
        By.XPATH,
        "//tr[preceding::*[.='Ανακοινώσεις Μαθήματος'] and following::*[.='Γενικές Ανακοινώσεις']]",
    )
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def eksoriksi_dedomenwn(driver, array, course_name):
    driver.get("https://www.cs.uoi.gr/~tsap/teaching/cse012/index-gr.html")
    sleep(2)
    driver.refresh()
    if find(driver, "//span[contains(text(),'ακοινώσεις')]") == None:
        return array
    announcements = driver.find_elements(
        By.XPATH,
        "//ul[preceding::*[.='Ανακοινώσεις']]",
    )
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def asyrmates_zefkseis(driver, array, course_name):
    driver.get(
        "https://users.cse.uoi.gr/~cliaskos/?Courses___MYE048___MYE048_%2F_2021-22"
    )
    sleep(2)
    driver.refresh()
    if find(driver, "//strong[normalize-space()='Announcements']") == None:
        return array
    announcements = driver.find_elements(
        By.XPATH,
        "//body/div[@id='tplge_main']/div[@id='tplge_mainin']/div[@id='tplge_content']/div[@id='tplge_contentin']/ul[1]/li",
    )
    for i in range(0, len(announcements)):
        announcements[i] = announcements[i].text
    return compare_arrays(course_name, array, announcements)


def main(driver):
    channels = {
        theoria_ypologismou: 695387115332173897,
        diktya_1: 695387944302805033,
        texniti_nohmosynh: 695387649015414885,
        ypologistiki_nohmosynh: 695390129182736425,
        leitourgika_systimata: 695387546330333184,
        anaktisi_pliroforias: 695388768894451713,
        baseis_dedomenwn: 695387847502463006,
        texnologia_logismikou: 695388195176710224,
        programmatismos_systimatwn: 695387172114792469,
        arxes_glwsswn: 695386600930017312,
        diakrita2: 695386294619996281,
        anaptixi_logismikou: 695386250449780785,
        prox_themata_texnologias: 695390128771694643,
        asyrmata_diktia: 695389110440951838,
        anaptixi_logismikou_2: 695388843431690320,
        parallila_systimata: 695389820935077958,
        ypolistiki_poliplokotita: 695390656293765160,
        ilektroniki: 695386762511515668,
        vasikes_arxes_kiklomatwn: 695385596276768808,
        vlsi: 695389624570478712,
        eksoriksi_dedomenwn: 695389386094805062,
        asyrmates_zefkseis: 695391258704871485,
    }

    course_names = [
        "ΜΥΥ501 Θεωρία Υπολογισμού",
        "ΜΥΥ703 Δίκτυα Υπολογιστών Ι",
        "ΜΥΥ602 Τεχνητή Νοημοσύνη",
        "ΜΥΕ035 Υπολογιστική Νοημοσύνη",
        "ΜΥΥ601 Λειτουργικά Συστήματα",
        "ΜΥΕ003 Ανάκτηση Πληροφορίας",
        "ΜΥΥ701 Βάσεις Δεδομένων",
        "ΜΥΥ803 Τεχνολογία Λογισμικού",
        "ΜΥΥ502 Προγραμματισμός Συστημάτων",
        "ΜΥΥ401 Αρχές Γλωσσών Προγραμματισμού",
        "ΜΥΥ302 Διακριτά Μαθηματικά ΙΙ",
        "ΜΥΥ301 Ανάπτυξη Λογισμικού",
        "ΜΥΕ030 Προχωρημένα Θέματα Τεχνολογίας και Εφαρμογών Βάσεων Δεδομένων",
        "ΜΥΕ006 Ασύρματα Δίκτυα",
        "ΜΥΕ004 Ανάπτυξη Λογισμικού ΙΙ",
        "ΜΥΕ023 Παράλληλα Συστήματα και Προγραμματισμός",
        "ΜΥΕ036 Υπολογιστική Πολυπλοκότητα",
        "ΜΥΥ203 Βασικές Αρχές Κυκλωμάτων",
        "ΜΥΥ404 Ηλεκτρονική",
        "MYE018 Κυκλώματα VLSI",
        "ΜΥΕ012 Εξόρυξη Δεδομένων",
        "ΜΥΕ048 Ασύρματες Ζεύξεις",
    ]

    links = [
        "https://www.cse.uoi.gr/~palios/automata/",
        "https://www.cse.uoi.gr/~epap/MYY703/",
        "https://www.cse.uoi.gr/~arly/courses/ai/ai.html",
        "https://www.cse.uoi.gr/~arly/courses/nn/nn.html",
        "https://www.cse.uoi.gr/~stergios/teaching/myy601/",
        "https://www.cs.uoi.gr/~pitoura/courses/ap/ap21/",
        "https://www.cs.uoi.gr/~pitoura/courses/db/db21/index.html",
        "https://www.cse.uoi.gr/~zarras/se.htm",
        "https://www.cse.uoi.gr/~dimako/teaching/fall20.html",
        "https://www.cse.uoi.gr/~cnomikos/courses/pl/pl-main.htm",
        "https://www.cse.uoi.gr/~kontog/courses/Discrete-Math-2/",
        "https://www.cs.uoi.gr/~pvassil/courses/sw_dev/intro.html",
        "https://www.cse.uoi.gr/~pvassil/courses/db_III/info.html",
        "https://www.cs.uoi.gr/~epap/MYE006/",
        "https://www.cse.uoi.gr/~zarras/soft-devII.htm",
        "https://www.cse.uoi.gr/~dimako/teaching/spring21.html",
        "https://www.cse.uoi.gr/~cnomikos/courses/cc/cc-main.htm",
        "https://www.cs.uoi.gr/~tsiatouhas/MYY404-ELEC.htm",
        "https://www.cs.uoi.gr/~tsiatouhas/MYY203.htm",
        "https://www.cs.uoi.gr/~tsiatouhas/MYE018-VLSI.htm",
        "https://www.cs.uoi.gr/~tsap/teaching/cse012/index-gr.html",
        "https://users.cse.uoi.gr/~cliaskos/?Courses___MYE048___MYE048_%2F_2021-22",
    ]

    notifications = [
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
        [["0"], [], "0"],
    ]

    TOKEN = os.environ.get("DISCORD_TOKEN")
    client = discord.Client()

    @client.event
    async def on_connect():
        print("Bot connected")

    @client.event
    async def on_ready():
        print("Bot ready")
        while True:
            i = 0
            try:
                for key, value in channels.items():
                    channel = client.get_channel(value)
                    alive_channel = client.get_channel(879312665263099934)
                    await alive_channel.send(
                        f"{i} : still running channel {str(datetime.datetime.now())} at {str(key)}"
                    )
                    notifications[i] = key(driver, notifications[i], course_names[i])
                    if notifications[i][2] != "0":
                        print(telegram_bot_sendtext(f"New announcement at: {i}"))

                        embed = discord.Embed(
                            title=f"<{links[i]}>",
                            description=notifications[i][2],
                            color=discord.Colour.dark_blue(),
                        )
                        embed.set_author(name=course_names[i])
                        await channel.send(embed=embed)
                        notifications[i][2] = "0"
                    i += 1

                await asyncio.sleep(1800)
                alive_channel = client.get_channel(879312665263099934)
                await alive_channel.send(
                    f"-----------------------------------------------------------"
                )
            except Exception as e:
                alive_channel = client.get_channel(879312665263099934)
                await alive_channel.send(
                    f"crash at {str(datetime.datetime.now())} with {e}"
                )
                telegram_bot_sendtext(
                    f"crash at {str(datetime.datetime.now())} with {e}"
                )
                if "session id" in str(e):
                    print("Session ID Expired")
                    telegram_bot_sendtext("Session ID Expired")
                    return

    client.run(TOKEN)


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--window-size=1020,720")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-sh-usage")
    options.add_argument("--headless")


    while True:
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
        main(driver)
        driver.close()
        driver.quit()
        print("Restarting Driver")
        telegram_bot_sendtext("Restarting Driver")
        time.sleep(5)
