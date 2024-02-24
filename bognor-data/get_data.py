import requests
from bs4 import BeautifulSoup
from datetime import datetime


def filter_tide_data(data):
    filtered_data = []
    current_time = datetime.now().time()
    prevTide = None
    nextTide = None

    # Convert the string to a datetime.time object
    for i in data['times']:
        time_obj = datetime.strptime(i[1], '%H:%M').time()
        if time_obj >= current_time:
            filtered_data.append(i)
            if nextTide is None:
                nextTide = i
            else:
                if datetime.strptime(i[1], '%H:%M').time() < datetime.strptime(nextTide[1], '%H:%M').time():
                    nextTide = i
        else:
            if prevTide is None:
                prevTide = i
            else:
                if datetime.strptime(i[1], '%H:%M').time() > datetime.strptime(prevTide[1], '%H:%M').time():
                    prevTide = i

    if prevTide is None:
        prevTide = data['times'][1]
    if nextTide is None:
        nextTide = data['times'][-2]

    if nextTide[2] > prevTide[2]:
        perc = (data['currentHeight'] - prevTide[2]) / (nextTide[2] - prevTide[2])
        perc = round(perc * 100, 2)
    else:
        perc = (data['currentHeight'] - nextTide[2]) / (prevTide[2] - nextTide[2])
        perc = round(perc * 100, 2)

    return {
        "times": filtered_data,
        "currentHeight": data['currentHeight'],
        "heightPercentage": perc,
        "sunrise": data['sunrise'],
        "sunset": data['sunset']
    }


def get_tide_data():
    url = "https://www.tidetimes.org.uk/pagham-tide-times"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Replace 'your_class_name_here' with the actual class name
    elements = soup.find_all(class_='vis2')
    times = []
    for i in elements:
        tal = i.find(class_='tal').text
        tac = i.find(class_='tac').text
        tar = i.find(class_='tar').text
        if tal != "Hi/Lo":
            times.append([tal, tac, float(tar.replace('m', ''))])

    testElement = soup.find(id='left-col')
    testElements = testElement.find('p')
    element_text = []
    for i in testElements:
        element_text.append(i.text)

    heightRaw = element_text[-1].strip()
    height = float(heightRaw[heightRaw.find('approx') + 14:heightRaw.rfind('m')])

    sunriseLoc = response.text.find('Sunrise :')
    sunsetLoc = response.text.find('Sunset  :')

    sunriseTime = response.text[sunriseLoc + 15:sunriseLoc + 20]
    sunsetTime = response.text[sunsetLoc + 15:sunsetLoc + 20]

    return {
        "times": times,
        "currentHeight": height,
        "sunrise": sunriseTime,
        "sunset": sunsetTime
    }
