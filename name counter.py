import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import pprint

http = httplib2.Http()

count = 0

def name_formater(name):
    format_name = name
    format_name = format_name.replace('\'', '').replace(' ','+')
    return format_name

def horse_set_creator(name, names):
    global count
    count += 1
    expand_names = dict()
    new_names = dict()

    status, response = http.request('https://www.pedigreequery.com/' + name)
    
    box = BeautifulSoup(response, parse_only=SoupStrainer("td",{'data-g':5}))
    for thing in box.find_all('a',{'class':'horseName'}):
        if thing.string != None:
            expand_names[thing["href"]] = 0
   
    for link in BeautifulSoup(response, parse_only=SoupStrainer('a',{'class':'horseName'})):
        if link.string != None:
            if link["href"] not in names:
                names[link["href"]] = 1
            else:
                names[link["href"]] += 1
    return expand_names



horse_set = {'/grand+fappy' : 1}
new_set = {'/grand+fappy': 1}

while len(new_set) != 0:
    print("Total: " + str(len(horse_set)))
    print("To Do: " + str(len(new_set)))
    print("Done: " + str(count))
    print()
    horse = list(new_set.keys())[0]
    new_set.pop(horse)
    new_set |= horse_set_creator(horse, horse_set)
    

file = open("names2.txt", "w+")
file.write(str(horse_set).replace(',','\n').replace('{',' ').replace('}',' ').replace('\'','').replace('"',''))
file.close()
