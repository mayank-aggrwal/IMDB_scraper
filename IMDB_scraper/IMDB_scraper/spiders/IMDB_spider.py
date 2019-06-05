
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
            votes = box.css("p.sort-num_votes-visible span:nth-child(2)::text").get()
            collection = box.css("p.sort-num_votes-visible span:nth-child(5)::text").get()

            Directors = []
            i = 1
            selector = 'div.lister-item-content p:nth-child(5) a:nth-child(%i)::text'%i
            x = box.css(selector).get()
            while x is not None:
                Directors.append(x)
                i = i + 1
                selector = 'div.lister-item-content p:nth-child(5) a:nth-child(%i)::text'%i
                x = box.css(selector).get()
            
            i = i + 1
            Stars = []
            selector = 'div.lister-item-content p:nth-child(5) a:nth-child(%i)::text'%i
            x = box.css(selector).get()
            while x is not None:
                Stars.append(x)
                i = i + 1
                selector = 'div.lister-item-content p:nth-child(5) a:nth-child(%i)::text'%i
                x = box.css(selector).get()

            yield {
                "name":name,
                "year":year,
                "certificate":certificate,
                "runtime": runtime,
                "genres": genres,
                "rating": rating,
                "directors": Directors,
                "stars": Stars,
                "votes": votes,
                "collection": collection
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
            

            #  yield scrapy.Request(next_page, callback=self.parse)
