---------------------------------------------------------Team ChipsMORE!------------------------------------------------------------
Team Member : Trinh Tuan Dung 
              Dinh Khoat Hoang Anh
              Nguyen Ngoc Khanh
              Fransiscus Xaverius Wilbert
              Stella Marcella Lie
Bot Name : eatNTU (@eat_NTUbot)
     
Description of files :

- Canteen Restaurant List .xlsx : A Excel file that contains various sheets . Each sheet is about a single canteen in NTU  :
     + Column C contains the names of each stalls in the canteen. 
     + Column B contains the types of stalls.
     + Column D contains the names of the dishes in the stalls.
     + Column E contains the prices of the dishes.
     + Column F indicates whether a dish is healthier or not.
 Our eatNTU bot can access this Excel file to give out the names of canteens , or information about the stalls and the prices of dishes , as well as an addtional indication whether a dish is healthy . 

- PlaceID.xlsx : A Excel file that indicates the locations of NTU canteens :
     + Column A contains the names of canteens.
     + Column B indicates the place ID of canteens.
     + Column C indicates the addresses of canteens.
     + Column D and column E respectively indicates the latitudes and longtitudes of canteens. 
 To save the number of API calls ( because it is limited ) we make it an offline database . And this will make the locations more standardized and error - free .
 
Main Python file to run : MainK.py


                                
