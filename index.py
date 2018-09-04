from bs4 import BeautifulSoup
import requests, pandas, os

keywords = ['Seperate Entrance', 'Side Door', 'Entrance']
bool_ = False


print ("Welcome to smartRealtor!")
budget = str(raw_input("Please provide max price."+os.linesep))
maxBedRooms = str(raw_input("Please specify the minimum number of Bedrooms."+os.linesep))
minBathRooms = str(raw_input("Please specify the minimum number of Bathrooms."+os.linesep))
city = str(raw_input("Please provide a city."+os.linesep))

req = requests.get("https://www.century21.ca/search/PropType-RES/0-"+budget+"/Beds-"+maxBedRooms+"/Baths-"+minBathRooms+"/Q-"+city)
content = req.content

soup = BeautifulSoup(content, "html.parser")
listings = soup.find_all("span", {"class": ["mls-id", "property-id"]}) #all the listings

if soup.find("ol", {"class": "pagination"}) != null:
    pages = soup.find("ol", {"class": "pagination"}).findChildren()

print ("Gathering Data! Please wait.")
for i in range(2, int(pages[-3].text) + 1):
    req = requests.get("https://www.century21.ca/search/PropType-RES/0-700000/Beds-3/Baths-2/Q-brampton/page" + str(i))    
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

print ("Filertering listings.")
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
            
            dic["Price"] = new_soup.find("h4").text
            
            dic["Bedrooms"] = new_soup.find("div", {"class": "details"}).findChildren()[0].text.split()[0]
            
            dic["Bathrooms"] = new_soup.find("div", {"class": "details"}).findChildren()[0].text.split()[2]
            lst.append(dic)
            
            dic["Listing"] = "https://www.century21.ca/" + str(item)
        else:
            pass
    else:
        pass

print ("Please check the src folder for 'Possibilities.csv'.")
new_lst = pandas.DataFrame(lst)
new_lst.to_csv("Possibles.csv")
