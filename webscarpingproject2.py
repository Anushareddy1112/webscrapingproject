import requests
from bs4 import BeautifulSoup
import pandas
import argparse
import connect

parser= argparse.ArgumentParser()
parser.add_argument("--page_num_max",help="enter the number of pages to parse",type =int)
parser.add_argument("--dbname",help="enter the number of pages to parse",type =int)
args=parser.parse_args()

oyo_url = 'https://wwww.oyorooms.com/hotels-in-bangalore/?pages='
page_num_MAx=args.page_num_max
scraped_info_list =[]
connect.connect(args.dbname)

for page_num in range(1, page_num_MAx):
    req=requests.get(oyo_url+str(page_num))
    content = req.content

    soup=BeautifulSoup(content,"html.parser")

    all_hotels = soup.find_all("div",{"class":"hotelcardListing"})

    for hotel in all_hotels:
        hotel_dict={}
        hotel_dict["name"]=hotel.find("h3",{"class":"listingHotelDescription_hotelName"}).text
        hotel_dict["address"]=hotel.find("span",{"itemprop":"streetAddress"}).text
        hotel_dict["price"]=hotel.find("span",{"class":"ListingPrice__finalPrice"}).text

        # try..... except

        try:
            hotel_dict["rating"]=hotel.find("span",{"class":"hotelRating__ratingSummary"}).text

        except AttributeError:
            pass

        parent_amenities_element = hotel.find("div",{"class" :"amenityWrapper"})

        amenities_list =[]
        for amenity in parent_amenities_element.findall("div",{"class" :"amenityWrapper__amenity"}):
            amenities_list.append(amenity.find("span",{"class":"d=body-sm"}).text.strip())

        hotel_dict["amenities"]=', '.join(amenities_list[:-1])

        scraped_info_list.append(hotel_dict)

        
        connect.insert_into_table(args.dbname,tuple(hotel_dict.values())
dataFrame=pandas.DataFrame(scraped_info_list)
dataFrame.to_csv("Oyo.csv")
connect.get_hotel_info(args.dbname)      
                                  
                                  
                                  


                          







        
