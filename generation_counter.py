import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import pprint
import re
from dataclasses import dataclass
from typing import List
http = httplib2.Http()

@dataclass
class HorseBit:
    name: str
    generations: List[int]
    total_appeared: int = 0

    def __str__(self):
        pretty = "Name: " + self.name + '\n'
        pretty = pretty + "Generation Spread: "+str(self.generations) + '\n'
        pretty = pretty + "Count: " + str(self.total_appeared) + '\n'
        return pretty

count = 0

def horse_set_creator(name, names, gen_start):
    global count
    count += 1
    expand_names = dict()
    new_names = dict()

    status, response = http.request('https://www.pedigreequery.com/' + name)
    
    box = BeautifulSoup(response, parse_only=SoupStrainer("td",{'data-g':5}))
    for thing in box.find_all('a',{'class':'horseName'}):
        if thing.string != None:
            expand_names[thing["href"]] = gen_start + 5
   

    for link in BeautifulSoup(response, parse_only=SoupStrainer('td',{"class":["f","m"]})):
        gen_chunk = re.findall("data-g=\"[1-5]\"", str(link))
        if len(gen_chunk):
            generation = int(gen_chunk[0][8:9])
            small = link.find('a',{'class':'horseName'})
            slash = small['href']
            if slash not in names:
                empty = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                names[slash] = HorseBit(small.string, empty)
            names[slash].total_appeared += 1
            names[slash].generations[gen_start+generation] += 1
            
    return expand_names



horse_set = {'/grand+fappy' : HorseBit("GRAND FAPPY", [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],1)}
new_set = {'/grand+fappy': 1}

while len(new_set) != 0:
    print("Total: " + str(len(horse_set)))
    print("To Do: " + str(len(new_set)))
    print("Done: " + str(count))
    print()
    horse = list(new_set.keys())[0]
    gen = new_set[horse]
    new_set.pop(horse)
    new_set |= horse_set_creator(horse, horse_set, gen)
    
file = open("names3.txt", "w+")
for horse in horse_set:
    file.write(horse)
    file.write(horse_set[horse]+'\n')
file.close()
