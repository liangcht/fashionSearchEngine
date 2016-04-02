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
    				"T-Shirt": "http://www.amazon.com/gp/search/ref=sr_ex_n_5?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045624&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459626155&lo=none",
    				"Polo Shirt": "http://www.amazon.com/s/ref=sr_ex_n_7?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045640&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459626073&lo=none", 
    				"Buttom-Down Shirt": "http://www.amazon.com/s/ref=sr_ex_n_9?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045630&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459626251&lo=none", 
    				"Fashion Hoody": "http://www.amazon.com/s/ref=sr_ex_n_12?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1258644011&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459626264&lo=none",
    				"Pullover Sweater": "http://www.amazon.com/s/ref=sr_ex_n_7?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1044442%2Cn%3A2476516011&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459626535&lo=none",
    				"Vest Sweater": "http://www.amazon.com/s/ref=sr_ex_n_10?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1044442%2Cn%3A1045662&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459626580&lo=none",
    				"Active Jacket": "http://www.amazon.com/s/ref=sr_ex_n_8?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1045830%2Cn%3A2476494011&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459627781&lo=none",
    				"Down Jacket": "http://www.amazon.com/gp/search/ref=sr_ex_n_13?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1045830%2Cn%3A2476602011&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459627773&lo=none",
    				"Leather Jacket": "http://www.amazon.com/s/ref=sr_ex_n_11?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1045830%2Cn%3A2476603011&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459627847&lo=none",
    				"Lightweight Jacket": "http://www.amazon.com/s/ref=sr_ex_n_12?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1045830%2Cn%3A2528780011&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459627859&lo=none",
    				"Vest Jacket": "http://www.amazon.com/s/ref=sr_ex_n_14?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1045830%2Cn%3A2562597011&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459627939&lo=none",
    				"Wool Jacket": "http://www.amazon.com/s/ref=sr_ex_n_15?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A1045830%2Cn%3A2476613011&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459627939&lo=none"
    			}, 
    		 "Women":{
    				"Dress": "http://www.amazon.com/s/ref=lp_1040660_ex_n_4?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1045024&bbn=10445813011&ie=UTF8&qid=1459628163", 
    				"Blouses": "http://www.amazon.com/s/ref=lp_2368343011_ex_n_6?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A2368343011%2Cn%3A2368365011&bbn=10445813011&ie=UTF8&qid=1459628404",
    				"Tee": "http://www.amazon.com/s/ref=lp_5418124011_ex_n_8?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A2368343011%2Cn%3A1044544&bbn=10445813011&ie=UTF8&qid=1459628527",
    				"Polo": "http://www.amazon.com/s/ref=lp_1044544_ex_n_9?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A2368343011%2Cn%3A1044548&bbn=10445813011&ie=UTF8&qid=1459628542",
    				"Tank": "http://www.amazon.com/s/ref=lp_1044548_ex_n_10?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A2368343011%2Cn%3A2368344011&bbn=10445813011&ie=UTF8&qid=1459628584",
    				"Cardigan Sweater": "http://www.amazon.com/s/ref=lp_2368384011_ex_n_7?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1044456%2Cn%3A1044612&bbn=10445813011&ie=UTF8&qid=1459628732",
    				"Pullover Sweater": "http://www.amazon.com/s/ref=lp_1044612_ex_n_8?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1044456%2Cn%3A2368384011&bbn=10445813011&ie=UTF8&qid=1459628737",
    				"Down Jacket": "http://www.amazon.com/s/ref=lp_1044646_ex_n_18?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1044646%2Cn%3A12643250011&bbn=10445813011&ie=UTF8&qid=1459628963",
    				"Wool Jacket": "http://www.amazon.com/s/ref=sr_ex_n_21?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1044646%2Cn%3A12643255011&bbn=10445813011&ie=UTF8&qid=1459628980",
    				"Trench Coat": "http://www.amazon.com/gp/search/ref=sr_ex_n_20?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1044646%2Cn%3A2348895011&bbn=10445813011&ie=UTF8&qid=1459629011",
    				"Casual Jacket": "http://www.amazon.com/s/ref=lp_2348896011_ex_n_22?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A1044646%2Cn%3A12643253011&bbn=10445813011&ie=UTF8&qid=1459629291",
    				"Suit Set": "http://www.amazon.com/s/ref=lp_9522932011_ex_n_21?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147440011%2Cn%3A1040660%2Cn%3A9522932011%2Cn%3A10344911011&bbn=10445813011&ie=UTF8&qid=1459629335"
    		  }
    		}

    def start_requests(self):
        #yield scrapy.Request("http://www.amazon.com/s/ref=sr_ex_n_3?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A9479199011%2Cn%3A360832011&bbn=10445813011&ie=UTF8&qid=1442910853&ajr=0",self.parse)
        
        #yield scrapy.Request("http://www.amazon.com/gp/search/ref=sr_il_to_fashion-brands?rh=n%3A7141123011%2Cn%3A10445813011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Cn%3A1045624&bbn=10445813011&sort=featured-rank&ie=UTF8&qid=1459620840&lo=none",self.parse)
        
        for gender in self.table:
            for type in self.table[gender]: 
                for i in range(1, 15): 
                    request = scrapy.Request(self.table[gender][type]+ "&page="+str(i)+"",self.parse)
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
        #namelist = response.xpath('//a[@class="a-link-normal s-access-detail-page  a-text-normal"]/@title').extract()
        #htmllist = response.xpath('//a[@class="a-link-normal s-access-detail-page  a-text-normal"]/@href').extract()
        #imglist = response.xpath('//a[@class="a-link-normal a-text-normal"]/img/@src').extract()
        namelist = response.xpath('//a[@class="a-link-normal s-access-detail-page s-overflow-ellipsis a-text-normal"]/@title').extract()
        htmllist = response.xpath('//a[@class="a-link-normal s-access-detail-page s-overflow-ellipsis a-text-normal"]/@href').extract()
        imglist = response.xpath('//img[@class="s-access-image cfMarker"]/@src').extract()
        listlength = len(namelist)
        
        pwd = os.getcwd()+'/'

        if not os.path.isdir(pwd+'crawlImages/'):
            os.mkdir(pwd+'crawlImages/')

        for i in range(0,listlength):
            item = AmazonItem()
            item['Name'] = namelist[i]
            item['Source'] = htmllist[i]
            item["Type"] = response.meta["Type"]
            item["Gender"] = response.meta["Gender"]
        
            urllib.urlretrieve(imglist[i],pwd+"crawlImages/"+str(amazonSpider.imgcount)+".jpg")
            item['Path'] = pwd+"crawlImages/"+str(amazonSpider.imgcount)+".jpg"
            amazonSpider.imgcount = amazonSpider.imgcount + 1
            yield item