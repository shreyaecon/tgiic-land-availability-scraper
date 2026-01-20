# Assignment-1 
# land availability task
# Assignment start date: 24/04/2025
# Assignment end date: 28/04/2025
# Author: Shreya


import scrapy

# defining the spider class
class TelanganaSpider(scrapy.Spider):
    name = "telangana" # name of the spider
    allowed_domains = ["www.tgiic.telangana.gov.in"] # domain to restrict the spider
    start_urls = ["https://www.tgiic.telangana.gov.in/PMVacantPlots"] # first page to scrape

    def parse(self, response):
        # print(response.text)
         # Parsing the list of zones from the main vacant plots page
        zones = response.xpath("//tr[@id='dataBody']") # extracting all zone rows
        if response.url:
            for zone in zones:
                #for each zone, following the link to its detail page with relevant metadata

                yield scrapy.Request(
                    url="https://www.tgiic.telangana.gov.in/" + zone.xpath(".//a/@href").get(), # specifies full URL to zone page 
                    meta = {"Serial_Number": zone.xpath("./td[@class='formField'][1]/text()").get(),
                            "Zone": zone.xpath(".//a/font/text()").get(),
                            "Zone_href": zone.xpath(".//a/@href").get(),
                            "No_of_Plots": zone.xpath("./td[@class='formField'][3]/text()").get(),
                            "No_of_Sheds": zone.xpath("./td[@class='formField'][4]/text()").get(),
                            "Plotted_Area": zone.xpath("./td[@class='formField'][5]/text()").get()},
                    callback=self.parseZone # callback to parse each zone 
                )

    def parseZone(self, response):
        # Parsing the list of districts under the current zone
        districts = response.xpath("//tr[@id='dataBody']")
        Zones_meta = response.meta # Getting metadata passed from previous level (zone)
        # print(Zones_meta)

        if response.url:
            for district in districts:
                # For each district, following the link to its detail page with relevant metadata

                yield scrapy.Request(
                    url = "https://www.tgiic.telangana.gov.in/" +  district.xpath(".//a/@href").get(),
                    meta = {"disctrict_name": district.xpath(".//a/font/text()").get(),
                            "district_href": district.xpath(".//a/@href").get(),
                            "disctrict_no_of_plots":district.xpath(".//td[@class='formField'][3]/text()").get(),
                            "disctrict_no_of_sheds":district.xpath(".//td[@class='formField'][4]/text()").get(),
                            "disctrict_plotted_area": district.xpath(".//td[@class='formField'][5]/text()").get(),
                            "Zones_data": Zones_meta}, # Passing zone metadata along
                    callback=self.parseDistrict # Callback to parse each district
                )

    def parseDistrict(self, response):
        # Parsing the list of Industrial Parks (IPs) in the district
        district_meta_data = response.meta # Metadata from zone and district level
        IP_names = response.xpath("//tr[@id='dataBody']")

        for IP_name in IP_names:
            # For each IP, following the link to its vacant plots page with relevant metadata

            yield scrapy.Request(
                url = "https://www.tgiic.telangana.gov.in/" + IP_name.xpath(".//a/@href").get(),

                meta = {"IP_name": IP_name.xpath(".//a/font/text()").get(),
                        "IP_name_href": IP_name.xpath(".//a/@href").get(),
                        "IP_No_of_plots" : IP_name.xpath(".//td[@class='formField'][3]/text()").get(),
                        "IP_No_of_Sheds" : IP_name.xpath(".//td[@class='formField'][4]/text()").get(),
                        "IP_Area_sq_mt" :  IP_name.xpath(".//td[@class='formField'][5]/text()").get(),
                        "IP_Land_rate_in_Rupee_sq_mt" :  IP_name.xpath(".//td[@class='formField'][6]/text()").get(),
                        "IP_remarks" : IP_name.xpath(".//td[@class='formField'][7]/text()").get(),
                        "IP_purpose_of_industrial_park" : IP_name.xpath(".//td[@class='formField'][8]/text()").get(),
                        "IP_layout_href" : IP_name.xpath(".//td[@class='formField'][9]/a/@href").get(),
                        "IP_meta_data" : district_meta_data }, # Passing district and zone metadata along

                callback = self.parseIP # Callback to parse each IP’s vacant plots
            )

    def parseIP(self, response):
        # Parse the final level: the list of vacant plots in a given Industrial Park
        meta_data = response.meta  # All previous metadata: zone, district, IP
        vacant_names = response.xpath("//tr[@id='dataBody']") # Each row is a plot

        for vacant_name in vacant_names:
            # Yielding final data item containing all levels of metadata + plot info

            yield {
                'Serial_Number' : meta_data.get('IP_meta_data').get("Zones_data").get('Serial_Number'),
                "Zone": meta_data.get('IP_meta_data').get("Zones_data").get('Zone'),
                "Zone_href":meta_data.get('IP_meta_data').get("Zones_data").get('Zone_href'),
                "No_of_Plots":meta_data.get('IP_meta_data').get("Zones_data").get("No_of_Plots"),
                "No_of_Sheds":meta_data.get('IP_meta_data').get("Zones_data").get("No_of_Sheds"),
                "Plotted_Area": meta_data.get('IP_meta_data').get("Zones_data").get("Plotted_Area"),

                "disctrict_name": meta_data.get('IP_meta_data').get("disctrict_name"),
                "district_href": meta_data.get('IP_meta_data').get("district_href"),
                "disctrict_no_of_plots": meta_data.get('IP_meta_data').get("disctrict_no_of_plots"),
                "disctrict_no_of_sheds": meta_data.get('IP_meta_data').get("disctrict_no_of_sheds"),
                "disctrict_plotted_area": meta_data.get('IP_meta_data').get("disctrict_plotted_area"),

                "IP_name": meta_data.get('IP_name'),
                "IP_name_href": meta_data.get('IP_name_href'),
                "IP_No_of_plots" : meta_data.get('IP_No_of_plots'),
                "IP_No_of_Sheds" : meta_data.get('IP_No_of_Sheds'),
                "IP_Area_sq_mt" :  meta_data.get('IP_Area_sq_mt'),
                "IP_Land_rate_in_Rupee_sq_mt" : meta_data.get('IP_Land_rate_in_Rupee_sq_mt'),
                "IP_remarks" : meta_data.get('IP_remarks'),
                "IP_purpose_of_industrial_park" : meta_data.get('IP_purpose_of_industrial_park'),
                "IP_layout_href" : meta_data.get('IP_layout_href'),

                "Vacant_S_no": vacant_name.xpath(".//td[@class='formField'][1]/text()").get(),
                "Vacant_IP_name" : vacant_name.xpath(".//td[@class='formField'][2]/text()").get(),
                "Vacant_Plot_No" : vacant_name.xpath(".//td[@class='formField'][3]/text()").get(),
                "Vacant_Property_type": vacant_name.xpath(".//td[@class='formField'][4]/text()").get(),
                "Vacant_Plot_area_sq_mt" : vacant_name.xpath(".//td[@class='formField'][5]/text()").get(),
                "Vacant_Land_rate_in_rupee_per_sq_mt" : vacant_name.xpath(".//td[@class='formField'][6]/text()").get(),
                "Vacant_remarks" : vacant_name.xpath(".//td[@class='formField'][7]/text()").get(),
                "Vacant_Purpose_of_industrial_park" : vacant_name.xpath(".//td[@class='formField'][8]/text()").get(),

            }





