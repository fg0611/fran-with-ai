import scrapy


class GooglemapsSpider(scrapy.Spider):
    name = "maps"
    # allowed_domains = ["maps.googlemaps.api"]
    # start_urls = ["https://maps.googlemaps.api"]

    def start_requests(self):
        query = "cafeterías en Córdoba Argentina"
        gmaps_url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}/"

        yield scrapy.Request(
            url=gmaps_url,
            callback=self.parse,
            meta={
                "zyte_api_automap": True, # tranparent mode
                "zyte_api_browser": True,
                "zyte_api": {
                    "browserHtml": True,
                    "httpResponseBody": True,
                    "httpResponseHeaders": True,
                },
            },
        )

    def parse(self, response):
        # EXTRAER DATOS — aún no es fácil, necesita investigación con devtools
        # Por ahora mostramos el HTML para inspeccionar
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        self.log("HTML guardado como debug.html")
