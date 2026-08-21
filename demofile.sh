
mkdir templates 
python3 scaffold.py user username email password phone country_id:references
python3 scaffold.py gem_quest place_name lat lon
python3 scaffold.py seasonal_sport name season
python3 scaffold.py place_visit gem_quest_id:references user_id:references seasonal_sport_id:references
python3 scaffold.py panomaric_view description gem_quest_id:references
python3 scaffold.py job_offer name description user_id:references
python3 scaffold.py myscore mymusic:staff pic user_id:references time_signature key_signature time_signature
