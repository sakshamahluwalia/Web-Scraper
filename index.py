from bs4 import BeautifulSoup
import requests, pandas

keywords = ['Seperate Entrance', 'Side Door', 'Entrance']
bool_ = False

req = requests.get("https://www.century21.ca/search/PropType-RES/0-700000/Beds-3/Baths-2/Q-brampton")
content = req.content
soup = BeautifulSoup(content, "html.parser")
listings = soup.find_all("span", {"class": ["mls-id", "property-id"]}) #all the listings
pages = soup.find("ol", {"class": "pagination"}).findChildren()
for i in range(2, int(pages[-3].text) + 1):
    req = requests.get("https://www.century21.ca/search/PropType-RES/0-700000/Beds-3/Baths-2/Q-brampton/page" + str(i))
    print(i)
    content = req.content
    soup = BeautifulSoup(content, "html.parser")
    listings += soup.find_all("span", {"class": ["mls-id", "property-id"]})

ids = []
for i in range(len(listings)):
    id_ = ''
    for ch in listings[i].text:
        if ch.isdigit() or ch == 'W':
            id_ += ch
    ids.append(id_)

lst = []
for item in ids:
    dic = {}
    req = requests.get("https://www.century21.ca/" + str(item))
    if req:
        content = req.content
        new_soup = BeautifulSoup(content, "html.parser")
        for word in keywords:
            if word in new_soup.find("section", {"class": "property-description"}).text.strip():
                bool_ = True
        if bool_:
            dic["Address"] = (new_soup.find("div",{"class" : 
                "main-details-section"}).findChildren()[1].text + " " + new_soup.find("div", 
                {"class" : "main-details-section"}).findChildren()[3].text)
            print(dic["Address"])
            
            dic["Price"] = new_soup.find("h4").text
            
            dic["Bedrooms"] = new_soup.find("div", {"class": "details"}).findChildren()[0].text.split()[0]
            
            dic["Bathrooms"] = new_soup.find("div", {"class": "details"}).findChildren()[0].text.split()[2]
            lst.append(dic)
            
            dic["Listing"] = "https://www.century21.ca/" + str(item)
        else:
            pass
    else:
        pass

new_lst = pandas.DataFrame(lst)
new_lst.to_csv("Possibles.csv")
