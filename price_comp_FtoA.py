from tkinter import *
from bs4 import BeautifulSoup
import requests
import random
import webbrowser
from collections import defaultdict
from difflib import  get_close_matches

root =Tk()
root.geometry("320x150")

class price_compare:
    def __init__(self,master):
        
        self.var=StringVar()
        self.var_flipkart=StringVar()
        self.var_amzn=StringVar()
        
        label=Label(master,text="Enter the product name:")
        label.grid(row=0,column=0,padx=(30,10),pady=30)
        
        entry=Entry(master, textvariable=self.var)
        entry.grid(row=0,column=1,sticky=W,pady=8)
        
        button_find = Button(master,text="find",bd=4,command=self.find)
        button_find.grid(row=1,column=1,sticky=W,pady=8)
        
    def find(self):
        self.product=self.var.get()
        self.product_arr=self.product.split()
        self.n=1
        self.key=""
        self.title_flip_var=StringVar()
        self.title_amzn_var=StringVar()
        self.variable_amzn=StringVar()
        self.variable_flip=StringVar()
        
        for word in self.product_arr:
            if self.n==1:
                self.key=self.key + str(word)
                self.n = self.n+ 1
            else:
                self.key= self.key + "+" + str(word)
        self.window=Toplevel(root)
        self.window.title("Comparison Of Prices")
        
        label_title_flip = Label(self.window, text="Flipkart Title:")
        label_title_flip.grid(row=0, column=0, sticky=W)
        
        label_flipkart = Label(self.window, text="Flipkart Price(Rs):")
        label_flipkart.grid(row=1,column=0,sticky=W)
        
        entry_flipkart = Entry(self.window, textvariable=self.var_flipkart)
        entry_flipkart.grid(row=1, column=1,sticky=W)
        
        label_title_amzn = Label(self.window, text="Amazon Title:")
        label_title_amzn.grid(row=3, column=0, sticky=W)
        
        label_amzn = Label(self.window, text="Amazon Price(Rs):")
        label_amzn.grid(row=4,column=0,sticky=W)
        
        entry_amzn = Entry(self.window, textvariable=self.var_amzn)
        entry_amzn.grid(row=4, column=1,sticky=W)
        
        self.price_flipkart(self.key)
        self.price_amzn(self.key)
        
        try:
            self.variable_amzn.set(self.matches_amzn[0])
        except:
            self.variable_amzn.set("Product not available")
        
        try:
            self.variable_flip.set(self.matches_flip[0])
        except:
            self.variable_flip.set("Product not available")
        
        option_amzn=OptionMenu(self.window,self.variable_amzn, *self.matches_amzn)
        option_amzn.grid(row=3,column=2,sticky=W)
        
        lab_amzn=Label(self.window,text="Not this? Try out suggestions by clicking on title")
        lab_amzn.grid(row=3,column=1,padx=4)
        
        option_flip=OptionMenu(self.window,self.variable_flip,*self.matches_flip)
        option_flip.grid(row=0,column=2,sticky=W)
        
        lab_flip=Label(self.window,text="Not this? Try out suggestions by clicking on title")
        lab_flip.grid(row=0,column=1,padx=4)
        
        button_search=Button(self.window,text='search',command=self.search,bd=4)
        button_search.grid(row=2, column=2, sticky=E, padx=10, pady=4)
        
        button_search_amzn=Button(self.window,text='Visit Site',command=self.visit_amzn,bd=4)
        button_search_amzn.grid(row=4, column=2, sticky=W)
        
        button_search_flip=Button(self.window,text='Visit Site',command=self.visit_flip,bd=4)
        button_search_flip.grid(row=1, column=2, sticky=W)
        
        
        
    def price_flipkart(self,key):
        url_flip="https://www.flipkart.com/search?q=" +str(key)+ "&marketplace=FLIPKART&as-show=on&as=off"
        map = defaultdict(list)
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        source_code=requests.get(url_flip, headers=self.headers)
        soup=BeautifulSoup(source_code.text,"html.parser")
        self.opt_title_flip=StringVar()
        home="https://www.flipkart.com"
        
        for block in soup.find_all('div',{'class':'_2kHMtA'}):
            title,price,link=None,"Currently Unavailable",None
            for heading in block.find_all('div',{'class':'_4rR01T'}):
                title=heading.text
            for p in block.find_all('div',{'class':'_30jeq3 _1_WHN1'}):
                price=p.text[1:]
            for l in block.find_all('a',{'class':'_1fQZEK'}):
                link=home+l.get('href')
            map[title]=[price,link]
        user_input= self.var.get().title()
        self.matches_flip=get_close_matches(user_input, list(map.keys()),20,0.1)
        self.looktable_flip={}
        
        for title in self.matches_flip:
            self.looktable_flip[title]=map[title]
        
        try:
            self.opt_title_flip.set(self.matches_flip[0])
            self.var_flipkart.set(self.looktable_flip[self.matches_flip[0]][0]+'.00')
            self.link_flip=self.looktable_flip[self.matches_flip[0]][1]
        except IndexError:
            self.opt_title_flip.set("Product Not found")
    
    def price_amzn(self,key):
        url_amzn="https://www.amazon.in/s?k=" + str(key) +"&ref=nb_sb_noss_2"
        map=defaultdict(list)
        headers = {
            'authority': 'www.amazon.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        source_code=requests.get(url_amzn, headers=headers)
        soup=BeautifulSoup(source_code.text,"html.parser")
        self.opt_title_amzn=StringVar()
        home="https://www.amazon.in"
        
        for block1 in soup.find_all('div',{'class':'sg-col-inner'}):
            title,price,link=None,'Currently Unavailable',None
            for heading in block1.find_all('span',{'class':'a-size-medium a-color-base a-text-normal'}):
                title=heading.text
            for p in block1.find_all('span',{'class':'a-price-whole'}):
                price=p.text
            for l in block1.find_all('a',{'class':'a-link-normal a-text-normal'}):
                link=home + l.get('href')
            if title and link:
                map[title]=[price,link]
            
            
            
        user_input= self.var.get().title()
        self.matches_amzn=get_close_matches(user_input, list(map.keys()),20,0.01)
        self.looktable_amzn={}
        
        for title in self.matches_amzn:
            self.looktable_amzn[title]=map[title]
        
        try:
            self.opt_title_amzn.set(self.matches_amzn[0])
            self.var_amzn.set(self.looktable_amzn[self.matches_amzn[0]][0]+'.00')
            self.link_amzn=self.looktable_amzn[self.matches_amzn[0]][1]
        except IndexError:
            self.opt_title_amzn.set("Product Not found")
            
    
    
    def search(self):
        amzn_get=self.variable_amzn.get()
        self.opt_title_amzn.set(amzn_get)
        product=self.opt_title_amzn.get()
        price,self.link_amzn=self.looktable_amzn[product][0],self.looktable_amzn[product][1]
        self.var_amzn.set(price+'.00')
        
        flip_get=self.variable_flip.get()
        self.opt_title_flip.set(flip_get)
        prod=self.opt_title_flip.get()
        flip_price,self.link_flip=self.looktable_flip[prod][0],self.looktable_flip[prod][1]
        self.var_flipkart.set(flip_price+'.00')
        
    def visit_amzn(self):
        webbrowser.open(self.link_amzn)
    
    def visit_flip(self):
        print(self.link_flip)
        webbrowser.open(self.link_flip)


if __name__=="__main__":
    c=price_compare(root)
    root.title("Price Comparision Engine")
    root.mainloop()
    
    
        