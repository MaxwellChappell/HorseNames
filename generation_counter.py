import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import pprint
import re
from dataclasses import dataclass
from typing import List
import pandas as pd
import os

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
    """
    Adds to names dictionary every horse in the horse specified ancestry
    
    horse: a name of a horse as the end of of a pedigree query link ex. "/grand+fappy"
    names: a dictionary of all the names processed
    gen_start: the current generation of the horse

    """
    global count
    count += 1
    expand_names = dict()

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
                empty = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

                names[slash] = HorseBit(small.string, empty)
            names[slash].total_appeared += 1
            names[slash].generations[gen_start+generation] += 1
    return  expand_names

def save_simple(horse_list):
    """
    Creates a simple txt with horse information
    
    horse: expecting the same pedigree link format, becomes name of .txt
    horse_list: the whole horse dictionary
    """
    file = open("simple.txt", "w+")
    for horse in horse_list:
        file.write(horse)
        file.write('\n')
        file.write(str(horse_list[horse]))
        file.write('\n')
    file.close()

def save_names_only(horse_list):
    """
    Creates a simple txt with horse names
    
    horse: expecting the same pedigree link format, becomes name of .txt
    horse_list: the whole horse dictionary
    """
    file = open("names.txt", "w+")
    for horse in horse_list:
        file.write(horse)
        file.write(': ')
        file.write(str(horse_list[horse].name))
        file.write('\n')
    file.close()

def save_complex_data(horse_list):
    """
    Creates a csv and txt with differnt generation data
    
    horse: expecting the same pedigree link format, becomes name of .txt
    horse_list: the whole horse dictionary
    """
    data = []
    for item in horse_list:
        indiv = [item, horse_list[item].name, horse_list[item].total_appeared]
        for gen in horse_list[item].generations:
            indiv.append(gen)
        data.append(indiv)

    df = pd.DataFrame(data)
    df.columns = ["Link","Name","Apeared","1st Generation", "2nd Generation", "2rd Generation","4th Generation","5","6","7","8","9","10","11",'12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45']
    df.to_csv("sheet.csv")

    gen_data= {}
    for i in range(46):
            gen_data[i] = []

    for item in data:
            for i in range(3,len(item)-4):
                    if item[i] > 0:
                            gen_count = item[i]
                            gen_percent = item[i] / (2**(i-3))
                            gen_data[i-3].append([item[0],gen_count, gen_percent])

    file = open("generations.txt", "w+")
    for i in gen_data:
            file.write(str(i) +":\n")
            for horse in gen_data[i]:
                    file.write(horse[0] + ': ' + str(horse[1])+'\n')
                    file.write(str(horse[2])+'\n')
                    file.write('\n')
    file.close()


def start(horse_link, horse_name, horse_list):
    horse_list[horse_link] = HorseBit(horse_name, [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],1)
    new_names = {horse_link: 0}
    while len(new_names) != 0:
        print("Total: " + str(len(horse_list)))
        print("To Do: " + str(len(new_names)))
        print("Done: " + str(count))
        print()
        horse = list(new_names.keys())[0]
        gen = new_names[horse]
        new_names.pop(horse)
        new_names |= horse_set_creator(horse, horse_list, gen)


def main():
    link = '/grand+fappy'
    name = 'GRAND FAPPY'

    if os.path.isdir(link[1:]) == False:
        os.mkdir(link[1:])
    os.chdir(link[1:])
    horse_set = {}
    start(link, name, horse_set)
    save_simple(horse_set)
    save_names_only(horse_set)
    save_complex_data(horse_set)

if __name__ == "__main__":
    main()
