#!/usr/bin/python
# -*- encoding: UTF-8 -*-
# Author:SHI Zhongping
# 13/10/2016

import urllib2
from bs4 import BeautifulSoup


class Scraper(object):
    def __init__(self):
        self.soup = None
        self.list_raw = []
        self.dic_final = {}

    def get_BOC_exchange_rates(self, url):
        # html = urllib2.urlopen(url,context).read()
        self.soup = BeautifulSoup(urllib2.urlopen(url).read())

        for i in self.soup.findAll("table")[0]:
            try:
                for j in i.findAll("td"):
                    self.list_raw.append(j.get_text().replace("	", "").replace("\n", "").encode("utf-8"))
            except AttributeError:
                continue

        # print self.list_raw
        for k in range(0, len(self.list_raw), 3):
            self.dic_final[self.list_raw[k]] = (self.list_raw[k + 1], self.list_raw[k + 2])

        return self.dic_final

    def get_BOC_exchange_rates_against_HKD(self):
        return self.get_BOC_exchange_rates("https://www.bochk.com/whk/rates/exchangeRatesHKD/exchangeRatesHKD-input.action?lang=en")

    def get_BOC_exchange_rates_against_USD(self):
        return self.get_BOC_exchange_rates("https://www.bochk.com/whk/rates/exchangeRatesUSD/exchangeRatesUSD-input.action?lang=en")

    def get_BOC_precious_metal_trading_prices(self):
        html = urllib2.urlopen("https://www.bochk.com/whk/rates/preciousMetal/preciousMetalTradingPrices-enquiry.action?lang=en").read()
        self.soup = BeautifulSoup(html)

        for i in self.soup.findAll("table")[0]:
            try:
                for j in i.findAll("td"):
                    self.list_raw.append(j.get_text().replace("	", "").replace("\n", "").encode("utf-8"))
            except AttributeError:
                continue

        for k in range(1, len(self.list_raw), 4):
            self.dic_final[self.list_raw[k]] = (self.list_raw[k + 1], self.list_raw[k + 2], self.list_raw[k + 3])

        return self.dic_final


from Tkinter import *
import sys
import tkFont


class ScraperGUI(Scraper):
    def __init__(self, tkroot):
        self.list_raw = []
        self.dict_final = []
        Scraper.__init__(self)
        tkroot.configure(background='white')
        tkroot.minsize(width=758, height=400)
        tkroot.maxsize(width=758, height=400)
        tkroot.title("Scraper")

        self.labelFont = tkFont.Font(family="Helvetica", size=16)
        self.entryFont = tkFont.Font(family="Helvetica", size=16)
        self.buttonFont = tkFont.Font(family="Helvetica", size=18)

        self.label_frame_1 = Frame(tkroot)
        self.label_frame_1.configure(background="white")
        self.label_ini = Label(self.label_frame_1, text="Target currency name:", font=self.labelFont,
                               background='white')
        self.label_ini.grid(row=0, column=0, sticky=E, padx=50)
        self.currencyname = StringVar()
        self.entry_currencyname = Entry(self.label_frame_1, textvariable=self.currencyname, font=self.entryFont,
                                        width=23, relief=FLAT,
                                        disabledforeground="#BAC4CA", disabledbackground="white")
        self.entry_currencyname.grid(row=0, column=1, sticky=W, padx=50, pady=50)
        self.label_frame_1.grid(row=0, sticky=W, column=0)

        self.label_frame_2 = Frame(tkroot)

        self.label_frame_2.configure(background='white')
        self.label_CER = Label(self.label_frame_2, text="Currency Exchange Rates against HKD", font=self.labelFont,
                               background='white')
        self.label_CER.grid(row=0, column=0, sticky=W, padx=50, pady=0)

        self.label_buy = Label(self.label_frame_2, text="Buy", font=self.labelFont, background='white')
        self.label_buy.grid(row=1, column=0, sticky=W, padx=150, pady=20)

        self.label_sell = Label(self.label_frame_2, text="Sell", font=self.labelFont, background='white')
        self.label_sell.grid(row=2, column=0, sticky=W, padx=150, pady=0)

        self.button_getRate = Button(self.label_frame_2, text="Get it", width=9, height=1, command=self.getExchangeRate,
                                     fg='white', font=self.buttonFont, relief=GROOVE, bg="#14b294",
                                     activebackground='#2addba',
                                     activeforeground="white")
        self.button_getRate.grid(row=3, column=0, sticky=W, padx=310, pady=50)

        self.label_frame_2.grid(row=1, column=0, sticky=W)

    def getExchangeRate(self):
        price = scraper.get_BOC_exchange_rates_against_HKD().get(self.entry_currencyname.get().strip().upper())
        if price:
            self.label_CER["text"] = "Currency Exchange Rates against HKD"
            self.label_buy["text"] = "Buy: " + price[0]
            self.label_sell["text"] = "Sell: " + price[1]
            root.update_idletasks()
        else:
            self.label_CER["text"] = "Info not found"
            root.update_idletasks()

    def on_closingWindow(self):
        sys.exit()


if __name__ == '__main__':
    root = Tk()
    scraper = ScraperGUI(root)
    root.protocol("WM_DELETE_WINDOW", scraper.on_closingWindow)
    root.mainloop()
