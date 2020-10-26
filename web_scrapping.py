from bs4 import BeautifulSoup
import requests

page = requests.get("http://web.kma.go.kr/home/index.tab.now-ten.jsp?gubun=1&myPointCode=&unit=M")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup)
# data1 = soup.find('div', {'class':'weather'})
# find_weather = data1.find_all('dl')

# for weather in find_weather:
#     print('위치: '+weather.get_text())

# page = requests.get("http://web.kma.go.kr/home/index.tab.now-ten.jsp?gubun=2&myPointCode=&unit=M")
# soup = BeautifulSoup(page.content, 'html.parser')

# data2 = soup.find('div', {'class':'rainfall'})
# find_rainfall = data2.find_all('dl')

# for rainfall in find_rainfall:
#     print('현재 위치: '+rainfall.get_text())


# page = requests.get("http://web.kma.go.kr/home/index.tab.now-ten.jsp?gubun=3&myPointCode=&unit=M")
# soup = BeautifulSoup(page.content, 'html.parser')

# data3 = soup.find('div', {'class':'wind'})
# find_wind = data3.find_all('dl')

# for wind in find_wind:
#     print('현재 위치: '+wind.get_text())


#links = soup.find_all(class_="an_txt")
#for link in links:
#    print(link.get_text())
