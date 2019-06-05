
import scrapy

class MySpider(scrapy.Spider):

    name = 'IMDB_spider'
    main_site_url = 'https://www.imdb.com'
    cnt = 0

    def start_requests(self):

        base_url = 'https://www.imdb.com/search/title?genres=g&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres'

        myurl = base_url[:41] + self.category + base_url[42:]
        urls = []
        urls.append(myurl)
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)
    
    def parse(self, response):

        boxes = response.css("div.lister-item-content")
        for box in boxes:
            det_url = self.main_site_url + box.css("h3.lister-item-header a::attr(href)").get()
            name = box.css("h3.lister-item-header a::text").get()
            year = box.css("h3.lister-item-header span.lister-item-year.text-muted.unbold::text").get()[1:5]
            certificate = box.css("p.text-muted span.certificate::text").get()
            runtime = box.css("p.text-muted span.runtime::text").get()
            x = box.css("p.text-muted span.genre::text").get().split(',')
            genres = list(map(lambda y: y.strip(), x))
            
            rating = box.css("div.ratings-bar strong::text").get()
            #desc = box.css("p.text-muted::text").get()
            #votes = box.css("p.sort-num_votes-visible::text").get()
            #Collection = box.css("p.sort-num_votes-visible::text").get()
            #Director = box.css("p a::text").get()
            #Stars = box.css("p a::text").get()

            yield {
                "name":name,
                "year":year,
                "certificate":certificate,
                "runtime": runtime,
                "genres": genres,
                "rating": rating
            }
            
        self.cnt = self.cnt + 1
        self.log(self.cnt)

        pages = response.css("a.lister-page-next.next-page::attr(href)").get()
        next_page_id = self.main_site_url + pages

        if self.cnt < 5:
            if next_page_id is not None:
                next_page = response.urljoin(next_page_id)
                self.log(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
            

    # def parse(self, response):

    #     boxes = response.css("div._1UoZlX")
    #     for box in boxes:
    #         mobile_name = box.css("div._3wU53n::text").get()
    #         mobile_price = box.css("div._1vC4OE._2rQ-NK::text").get()[1:]
    #         mobile_rating = box.css("div.hGSR34::text").get()

    #         yield {
    #             "name":mobile_name,
    #             "price":mobile_price,
    #             "rating":mobile_rating,
    #         }
            
    #     self.cnt = self.cnt + 1
    #     self.log(self.cnt)

    #     pages = response.css("a._3fVaIS::attr(href)").getall()
    #     next_page_id = pages[0]
    #     if len(pages) > 1:
    #         next_page_id = pages[1]
    #         self.log(next_page_id)

    #     if self.cnt < 5:
    #         if next_page_id is not None:
    #             next_page = response.urljoin(next_page_id)
    #             self.log(next_page)
    #             yield scrapy.Request(next_page, callback=self.parse)
