import scrapy
import urllib
from amazon.items import AmazonItem
import os


class amazonSpider(scrapy.Spider):
    imgcount = 1
    name = "amazon"
    allowed_domains = ["amazon.com"]
    '''
    start_urls = ["http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=backpack",
                  "http://www.amazon.com/s/ref=sr_pg_2?rh=i%3Aaps%2Ck%3Abackpack&page=2&keywords=backpack&ie=UTF8&qid=1442907452&spIA=B00YCRMZXW,B010HWLMMA"
                  ]
    '''
    table = {"Men":{
                    "T-Shirt": [30, "http://www.amazon.com/gp/search/ref=sr_ex_n_5?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045624&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459626155"],
                    "Tank": [15, "http://www.amazon.com/s/ref=sr_ex_n_6?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A2476518011&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1461522822"],
                    "Polo Shirt": [15, "http://www.amazon.com/gp/search/ref=sr_ex_n_7?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045640&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1461522848"], 
                    "Buttom-Down Shirt": [50, "http://www.amazon.com/s/ref=sr_ex_n_9?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045630&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459626251"], 
                    "Fashion Hoody": [20, "http://www.amazon.com/s/ref=sr_ex_n_12?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1258644011&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459626264"],
                    "Pullover Sweater": [20, "http://www.amazon.com/s/ref=sr_ex_n_7?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1044442%2Cn%3A2476516011&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1461523053"],
                    "Cardigan Sweater": [15, "http://www.amazon.com/s/ref=sr_ex_n_8?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1044442%2Cn%3A1045658&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1461523517"],
                    "Shell Jacket": [15, "http://www.amazon.com/s/ref=sr_ex_n_12?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1045830%2Cn%3A2476494011%2Cn%3A7132367011&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1461523911"],
                    "Down Jacket": [15, "http://www.amazon.com/s/ref=sr_ex_n_9?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1045830%2Cn%3A2476602011&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1461523594"],
                    "Leather Jacket": [10, "http://www.amazon.com/s/ref=sr_ex_n_11?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1045830%2Cn%3A2476603011&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459627847"],
                    "Wool Jacket": [15, "http://www.amazon.com/s/ref=sr_ex_n_15?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1045830%2Cn%3A2476613011&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459627939"],
                    "Suit": [20, "http://www.amazon.com/s/ref=sr_ex_n_14?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1045684%2Cn%3A1045686&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1461524243"],
                    "Blazer": [30, "http://www.amazon.com/s/ref=sr_ex_n_16?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1045684%2Cn%3A1045694&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1461524250"]
                }, 
            "Women":{
                    "Casual Dress": [30, "http://www.amazon.com/s/ref=sr_ex_n_5?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1045024%2Cn%3A2346727011&bbn=10445813011&ie=UTF8&qid=1461520202"], 
                    "Work Dress": [30, "http://www.amazon.com/s/ref=lp_2346727011_ex_n_6?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1045024%2Cn%3A2346728011&bbn=10445813011&ie=UTF8&qid=1461520648"],
                    "Formal Dress": [30, "http://www.amazon.com/s/ref=lp_2346728011_ex_n_8?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1045024%2Cn%3A11006704011&bbn=10445813011&ie=UTF8&qid=1461520897"],
                    "Blouse": [30, "http://www.amazon.com/s/ref=lp_2368343011_ex_n_6?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A2368343011%2Cn%3A2368365011&bbn=10445813011&ie=UTF8&qid=1461520968"],
                    "Henley": [8, "http://www.amazon.com/s/ref=sr_ex_n_7?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A2368343011%2Cn%3A5418124011&bbn=10445813011&ie=UTF8&qid=1461521314&ajr=2"],
                    "Polo": [15, "http://www.amazon.com/s/ref=lp_1044544_ex_n_9?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A2368343011%2Cn%3A1044548&bbn=10445813011&ie=UTF8&qid=1459628542"],
                    "Tank": [30, "http://www.amazon.com/s/ref=lp_1044548_ex_n_10?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A2368343011%2Cn%3A2368344011&bbn=10445813011&ie=UTF8&qid=1459628584"],
                    "Cardigan Sweater": [20, "http://www.amazon.com/s/ref=lp_2368384011_ex_n_7?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1044456%2Cn%3A1044612&bbn=10445813011&ie=UTF8&qid=1459628732"],
                    "Pullover Sweater": [30, "http://www.amazon.com/s/ref=lp_1044456_ex_n_8?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1044456%2Cn%3A2368384011&bbn=10445813011&ie=UTF8&qid=1461522045"],
                    "Hoody": [15, "http://www.amazon.com/s/ref=sr_ex_n_7?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1258603011&bbn=10445813011&ie=UTF8&qid=1461521671&ajr=2"],
                    "Down & Parkas": [15, "http://www.amazon.com/s/ref=sr_ex_n_18?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1044646%2Cn%3A12643250011&bbn=10445813011&ie=UTF8&qid=1461521987"],
                    "Wool Jacket": [15, "http://www.amazon.com/s/ref=sr_ex_n_19?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1044646%2Cn%3A12643255011&bbn=10445813011&ie=UTF8&qid=1461521955"],
                    "Trench Coat": [8, "http://www.amazon.com/s/ref=lp_2348895011_ex_n_23?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1044646%2Cn%3A2348895011%2Cn%3A7132360011&bbn=10445813011&ie=UTF8&qid=1461522120"],
                    "Casual Jacket": [10, "http://www.amazon.com/s/ref=lp_7132357011_ex_n_22?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1044646%2Cn%3A12643253011&bbn=10445813011&ie=UTF8&qid=1461522168"],
                    "Leather Jacket": [10, "http://www.amazon.com/s/ref=lp_2348892011_pg_2?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1044646%2Cn%3A2348892011&bbn=10445813011&ie=UTF8&qid=1461522419"],
                    "Blazer": [15, "http://www.amazon.com/s/ref=lp_9522932011_ex_n_19?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A9522932011%2Cn%3A1045112&bbn=10445813011&ie=UTF8&qid=1461522625"],
                    "Suit": [15, "http://www.amazon.com/s/ref=sr_ex_n_21?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A9522932011%2Cn%3A10344911011&bbn=10445813011&ie=UTF8&qid=1461522686"]
              }
            }

    def start_requests(self):
        #yield scrapy.Request("http://www.amazon.com/s/ref=sr_ex_n_3?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A9479199011%2Cn%3A360832011&bbn=10445813011&ie=UTF8&qid=1442910853&ajr=0",self.parse)
        
        #yield scrapy.Request("http://www.amazon.com/gp/search/ref=sr_il_to_fashion-brands?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045624&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459620840&lo=none",self.parse)
        
        for gender in ["Women", "Men"]:
            for type in self.table[gender]: 
                for i in range(1, self.table[gender][type][0]+1): 
                    request = scrapy.Request(self.table[gender][type][1]+ "&page="+str(i)+"",self.parse)
                    request.meta['Type'] = type
                    request.meta['Gender'] = gender
                    yield request

        # for i in range(1,3):
        #     request = scrapy.Request("http://www.amazon.com/gp/search/ref=sr_il_to_fashion-brands?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045624&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459620840&lo=none" + "&page="+str(i)+"",self.parse)
        #     request.meta['Type'] = "T-Shirt"
        #     request.meta['Gender'] = "Men"
        #     yield request
            #yield scrapy.Request("http://www.amazon.com/gp/search/ref=sr_il_to_fashion-brands?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045624&page="+str(i)+"&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459620840&lo=none",self.parse)

    def parse(self,response):
        namelist = response.xpath('//a[@class="a-link-normal s-access-detail-page  a-text-normal"]/@title').extract()
        htmllist = response.xpath('//a[@class="a-link-normal s-access-detail-page  a-text-normal"]/@href').extract()
        #imglist = response.xpath('//a[@class="a-link-normal a-text-normal"]/img/@src').extract()
        # namelist = response.xpath('//a[@class="a-link-normal s-access-detail-page s-overflow-ellipsis a-text-normal"]/@title').extract()
        # htmllist = response.xpath('//a[@class="a-link-normal s-access-detail-page s-overflow-ellipsis a-text-normal"]/@href').extract()
        imglist = response.xpath('//img[@class="s-access-image cfMarker"]/@src').extract()
        listlength = len(namelist)
        
        pwd = os.getcwd()+'/'

        if not os.path.isdir(pwd+'crawlImages_large/'):
            os.mkdir(pwd+'crawlImages_large/')

        for i in range(0,listlength):
            item = AmazonItem()
            item['Name'] = namelist[i]
            item['Source'] = htmllist[i]
            item["Type"] = response.meta["Type"]
            item["Gender"] = response.meta["Gender"]
        
            urllib.urlretrieve(imglist[i].split('._')[0]+ ".jpg",pwd+"crawlImages_large/"+str(amazonSpider.imgcount)+".jpg")
            item['Path'] = pwd+"crawlImages_large/"+str(amazonSpider.imgcount)+".jpg"
            amazonSpider.imgcount = amazonSpider.imgcount + 1
            yield item