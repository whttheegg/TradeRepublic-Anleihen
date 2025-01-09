


from bs4 import BeautifulSoup
import requests
from datetime import datetime


anleihen = ['Bond Jan 2028', 'XS2438616240 Volkswagen Financial Services', '-', '0.88 %', '31/01/2028', 'Bond Jan 2027', 'FR0013476090 RCI Banque', '2.94 %', '1.13 %', '15/01/2027', 'Bond Oct 2027', 'XS1972547696 Volkswagen Financial Services', '2.93 %', '2.25 %', '01/10/2027', 'Bond Oct 2027', 'XS1696445516 Hungary', 'Bond Mar 2026', 'XS2694872081 Volkswagen Leasing', 'Bond Jun 2026', 'XS2014291616 Volkswagen Leasing', 'Bond Feb 2027', 'XS2558594391 Hungary', 'Bond Feb 2027', 'XS2374595044 Volkswagen Financial Services', 'Bond Feb 2026', 'XS2178857285 Romania', 'Bond May 2026', 'XS2265369657 Lufthansa', 'Bond Oct 2026', 'XS2745344601 Volkswagen Leasing', 'Bond Sep 2028', 'XS2892988275 Lufthansa', 'Bond Oct 2026', 'XS1893631769 Volkswagen Financial Services', 'Bond May 2026', 'FR0013334695 RCI Banque', 'Bond Oct 2028', 'FR001400D0F9 Carrefour', 'Bond Sep 2026', 'XS2837886014 Volkswagen Financial Services', 'Bond Mar 2028', 'XS2324724645 Fraport', 'Bond Oct 2028', 'XS2745725155 Volkswagen Leasing', 'Bond Jul 2026', 'FR001400F0U6 RCI Banque', '3.04 %', '4.63 %', '13/07/2026', 'Bond Dec 2026', 'XS1934867547 Romania', '3.03 %', '2.00 %', '08/12/2026', 'Bond Jan 2028', 'XS2438616240 Volkswagen Financial Services', '2.97 %', '0.88 %', '31/01/2028', 'Bond Jan 2027', 'FR0013476090 RCI Banque', '2.94 %', '1.13 %', '15/01/2027']
name = []
isin = []
coupon = []
falligkeit = []
restlaufzeit = []
ask_preis = []
ytm = []
anleihen_array = []
heutigesdatum = datetime(datetime.today().year, datetime.today().month, datetime.today().day)


for index, a in enumerate(anleihen):
    print(f'{index} {a}')
print('1-----------------------------------------------------------------------------')

def delf():
    for index, bond in enumerate(anleihen):
        if 'Bond' in bond:
            #print(f'{index} {bond}')
            if anleihen[index + 4][2] != '/':
                anleihen.pop(index)
                anleihen.pop(index)
                return delf()

delf()
print('>Aufgeräumte Liste----------------------------------------------------------------------------------------')
for index, x in enumerate(anleihen):
    print(f'{index} {x}')
print('<Aufgeräumte Liste----------------------------------------------------------------------------------------')

print('>Liste der gefundenn ISINs----------------------------------------------------------------------------------------')
def clear_dbl():
    for index, element in enumerate(anleihen):
        if 'Bond' in element:
            isinfound = anleihen[index + 1][0:12]
            print(index + 1, ' ', isinfound)

            for subindex, subelement in enumerate(anleihen):
                if isinfound in subelement and index + 1 != subindex:
                    print(f'gefunden {subindex} {subelement}')
                    anleihen.pop(subindex)
                    anleihen.pop(subindex)
                    anleihen.pop(subindex)
                    anleihen.pop(subindex)
                    anleihen.pop(subindex - 1)

clear_dbl()
print('<Liste der gefundenn ISINs----------------------------------------------------------------------------------------')


print('----------------------------------------------------------------------------------------')

for index, x in enumerate(anleihen):
    if '-' in x:
        anleihen[index] = '0.00 %'
    print(f'{index} {anleihen[index]}')

for i in range(0, len(anleihen), 5):
    if i + 4 < len(anleihen):  # Stelle sicher, dass noch 7 Zeilen vorhanden sind
        # Aus jeder Zeile die entsprechende Information extrahieren
        name.append(anleihen[i + 1][13:].strip())  # 3. Zeile: Jährliche Rendite
        isin.append(anleihen[i + 1][0:12].strip())  # 3. Zeile: Jährliche Rendite
        coupon.append(anleihen[i + 3].strip())  # 5. Zeile: Coupon
        falligkeit.append(anleihen[i + 4].strip())  # 7. Zeile: RLZ
    else:
        print("Unvollständiger Eintrag gefunden und übersprungen.")

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

x = 0
while x < len(name):
    einzelanleihe=[]
    einzelanleihe.append(falligkeit[x])
    einzelanleihe.append(isin[x])
    einzelanleihe.append(coupon[x])
    einzelanleihe.append(str(restlaufzeit[x]))
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


def output_erstellen():
    anleihen_array.sort(reverse=True)
    header = ['Falligkeit','        ISIN',' Coupon','RLZ','YTM', ' Name']

    #schreibe die sortierte Liste in eine .txt
    output = open(f'C:/Users/Jakob/Desktop/Anleihe Ymt Archiv/{datetime.today().year}-{datetime.today().month}-{datetime.today().day} bond_data_output_ymtSort.txt', 'w')

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

output_erstellen()