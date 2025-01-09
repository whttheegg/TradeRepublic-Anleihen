from datetime import datetime
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests


anleihen = []
name = []
isin = []
coupon = []
jahrlrendide = []
falligkeit = []
restlaufzeit = []
ask_preis = []
ytm = []
anleihen_array = []
heutigesdatum = datetime(datetime.today().year, datetime.today().month, datetime.today().day)

###### öffnen von TradeRepublic

driver = webdriver.Firefox()
driver.get("https://app.traderepublic.com/browse/bond?time_to_maturity=one_to_two_years,two_to_four_years")
sleep(2)
accept_btn = driver.find_elements(By.CLASS_NAME, 'buttonBase__title')
accept_btn[7].click()


###### Screen scrollen, gleichzeitig den HTML Code in Array anleihen speichern, scrollt bis zum Ende der Seite

screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    sleep(1)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    content = driver.find_element(By.XPATH, "/html/body").text
    for line in content[553:].split('\n'):
        anleihen.append(line)
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break

sleep(1)
driver.quit()


###### Löscht unvollständigen Datensatz. Ein Datensatz besteht aus
###### Name der Anleige, ISIN + Unternehmensname, järtliche Rendite, Coupon, Fälligkeit im Datum
def delf():
    for index, bond in enumerate(anleihen):
        if 'Bond' in bond:
            if anleihen[index + 4][2] != '/':
                anleihen.pop(index)
                anleihen.pop(index)
                return delf()
delf()


##### Löscht doppelte Datensätze
def clear_dbl():
    for index, element in enumerate(anleihen):
        if 'Bond' in element:
            isinfound = anleihen[index + 1][0:12]
            #print(index + 1, ' ', isinfound)

            for subindex, subelement in enumerate(anleihen):
                if isinfound in subelement and index + 1 != subindex:
                    #print(f'gefunden {subindex} {subelement}')
                    anleihen.pop(subindex)
                    anleihen.pop(subindex)
                    anleihen.pop(subindex)
                    anleihen.pop(subindex)
                    anleihen.pop(subindex-1)

clear_dbl()


###### Anleihen ohne Coupon kommen mit einem minus an. Wird zum rechnen hier umformatiert
for index, x in enumerate(anleihen):
    if '—' in x:
        anleihen[index] = '0.00 %'
    #print(f'{index} {anleihen[index]}')


###### Einzelne Bestandteile werden in einzelne Arrays hinzugefügt
for i in range(0, len(anleihen), 5):
    if i + 4 < len(anleihen):  # Stelle sicher, dass noch 7 Zeilen vorhanden sind
        # Aus jeder Zeile die entsprechende Information extrahieren
        name.append(anleihen[i + 1][13:].strip())  # 3. Zeile: Jährliche Rendite
        isin.append(anleihen[i + 1][0:12].strip())  # 3. Zeile: Jährliche Rendite
        jahrlrendide.append(anleihen[i + 2].strip())
        coupon.append(anleihen[i + 3].strip())  # 5. Zeile: Coupon
        falligkeit.append(anleihen[i + 4].strip())  # 7. Zeile: RLZ
    else:
        print("Unvollständiger Eintrag gefunden und übersprungen.")


##### Berechnung der RLZ in dezimal, herunterladen vom aktuellen Ask-Preis bei Lang und Schwarz je ISIN
i = 0
while i < len(falligkeit):
    tage = datetime(int(falligkeit[i][6:10]), int(falligkeit[i][3:5]), int(falligkeit[i][0:2])) - heutigesdatum
    tage = tage.days
    rlz_jahre = tage/365
    restlaufzeit.append(round(rlz_jahre, 2))

    url = f"https://www.ls-tc.de/de/anleihe/{isin[i]}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    ask = soup.find('span', attrs={'field': 'ask'}).text
    ask = ask.replace(',','.')
    ask_preis.append(ask)

    i = i + 1

#### Berechnung für Yielt to Maturity (YTM)
i=0
while i < len(coupon):
    durchschnnitspreis = (float(ask_preis[i]) + 100) / 2
    kommaindex = coupon[i].index('.')
    gewinn_falligkeit = (float(coupon[i][0:kommaindex + 2]) + (((100 - float(ask_preis[i])) / restlaufzeit[i]))) / durchschnnitspreis
    ytm.append(str(gewinn_falligkeit*100)[0:5])
    i = i + 1


print(name)
print(isin)
print(coupon)
print(falligkeit)
print(restlaufzeit)
print(ask_preis)
print(ytm)

###### einzelne Elemente der Anleihe in den einzelnen Arrays werden in einen gemeinsamen Array hinzugefügt
x = 0
while x < len(name):
    einzelanleihe=[]
    einzelanleihe.append(falligkeit[x])
    einzelanleihe.append(isin[x])
    einzelanleihe.append(coupon[x])
    einzelanleihe.append(str(restlaufzeit[x]))
    einzelanleihe.append(jahrlrendide[x])
    einzelanleihe.append(ytm[x])
    einzelanleihe.append(name[x])

    anleihen_array.append(einzelanleihe)
    x = x + 1

#Umformatierung des Datumformats
i = 0
while i < len(falligkeit):
    falligkeitCache = []
    falligkeitCache.append(falligkeit[i][6:10])
    falligkeitCache.append(falligkeit[i][3:5])
    falligkeitCache.append(falligkeit[i][0:2])
    join = '-'.join(falligkeitCache)
    anleihen_array[i][0] = join

    i = i + 1


##### Output im Form einer einfachen txt Datei. Sortiert nach YTM, RLZ, Coupon
##### Eigener Ordnerpfad gewählt

def output_erstellen(sort, index):
    anleihen_array.sort(reverse=True, key=lambda x:x[index])
    header = ['Falligkeit', '        ISIN', ' Coupon', 'RLZ','jäh.Rndte', 'YTM', ' Name']

    #schreibe die sortierte Liste in eine .txt
    output = open(f'C:/Users/Jakob/Desktop/Anleihe Ymt Archiv/{datetime.today().year}-{datetime.today().month}-{datetime.today().day} bond_data_output_{sort}Sort.txt', 'w')

    i = 0
    u = 0
    x = 0

    while x < len(header):
        output.write(header[x])
        output.write('     ')
        x = x + 1
    output.write('\n')
    output.write('3------------------------------------------------------------------------------------------------------------------')
    output.write('\n')

    while u < len(anleihen_array):
        while i < len(anleihen_array[0]):
            output.write(anleihen_array[u][i])
            output.write('     ')
            i = i + 1
        output.write('\n')
        i = 0
        u = u + 1

    output.write('\n')
    output.write('Anzahl Bonds: ')
    output.write(str(len(name)))
    output.write('\n')
    output.write('Anzahl Coupon: ')
    output.write(str(len(coupon)))
    output.write('\n')
    output.write('Anzahl RLZ: ')
    output.write(str(len(restlaufzeit)))
    output.write('\n')
    output.write('Anzahl ISIN: ')
    output.write(str(len(isin)))
    output.write('\n')
    output.write('Anzahl Ask: ')
    output.write(str(len(ask_preis)))

    output.close()


output_erstellen('ymt', 5)
output_erstellen('Coupon', 2)
output_erstellen('rlz', 3)
output_erstellen('jäh. Rednite', 4)
