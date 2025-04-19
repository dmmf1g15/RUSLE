import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd
import datetime
import numpy as np



def get_weather(start_date,end_date,lat,long): #function to get weather data from Open Meteo API
    #start_date and end_date should be strings of format YYYY-MM-DD
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    
    
    end_date_dt=datetime.datetime.strptime(end_date,'%Y-%m-%d') #doesn't work
    if end_date_dt<datetime.datetime.today(): #Its histroic weather
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {"latitude": lat,
            "longitude": long,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "precipitation_sum", #or rain_sum (whats the difference)
            "timezone": "GMT"}
    else: #Future Weather
        url = "https://climate-api.open-meteo.com/v1/climate"
        params = {
            "latitude": lat,
            "longitude": long,
            "start_date": start_date,
            "end_date": end_date,
            "models": "HiRAM_SIT_HR", #Chose the climate model you want here!
            "timezone": "GMT",
            "daily": "precipitation_sum" #or rain_sum 
                }
        
    responses = openmeteo.weather_api(url, params=params) #This downloads the weather data as a json
    #Now we unpack the data so its in a nicer format.
    daily=responses[0].Daily()
    daily_precipitation_sum = daily.Variables(0).ValuesAsNumpy() #extract rainfall data
    daily_data = {"date": pd.date_range( #make dates
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left")}
    daily_data["precipitation_sum"] = daily_precipitation_sum
    return daily_data


def calc_rain_day_10(month_precip): #function to calculate the number of days in a month with rainfall greater than 10mm and the total rainfall on those days
    #month_precip is a months worth of rainfall data at daily resolution
    greater_10= month_precip>=10
    day_10=np.count_nonzero(greater_10) # number of days in the month with rain greater than 10mm
    rain_10=np.sum(month_precip[greater_10]) #summed rainfall in those days
    return rain_10,day_10

def calc_R(start_date,end_date,lat,long):
    #A period of 20–25 yr. is recommended for computing the average R
    #Get data. NEEDS INERNET CONNECTION TO RUN
    daily_data=get_weather(start_date,end_date,lat,long)
    years=list(set(daily_data['date'].year)) #A list of all the years
    months=np.arange(1,13) #a list of all the months
    month_R={}#np.zeros(len(years)) #to save the months R value in
    for im,m in enumerate(months):
        month_indxs=daily_data['date'].month==m #pick out indexes in the month m
        dates_month=daily_data['date'][month_indxs] #the dates in the month m
        precip_month=daily_data['precipitation_sum'][month_indxs] # the precipitation data in this month only
        years_R=[] #to save the months R value in
        for iy,y in enumerate(years):
            year_indxs=dates_month.year==y #pick out indexes in the month and year
            precip_month_year=precip_month[year_indxs] #the precipitaiton in this month and year
            rain_10,day_10=calc_rain_day_10(precip_month_year) #call function to get rain_10 and day_10
            result=7.05*rain_10-88.92*day_10 #use the formula
            if result<=0: #Catch those with negatative values
                years_R.append(0)
            else:
                years_R.append(result)  # a list of EI30 value for month m for each year
        month_R[m]=years_R  #{month:[list of yearly EI30s for this month in each year]}
    return [np.mean(v) for v in month_R.values()]

def calc_K(pH,Sa,Cl,Si,OM):
    #pH - pH of soil
    #Sa - percent Sand of soil
    #Cl - percent Clay of soil
    #Si - percent Silt of soil
    #OM - OM percent of soil
    #output units are th/MJ/mm
    Cl_ratio=Cl/(Sa+Si)
    Si_ratio = Si/100
    return (0.043*pH+0.62/OM+0.0082*Sa-0.0062*Cl_ratio)*Si_ratio*0.1317 #convert to SI


def calc_LS(s,l): #slope and length factor

    return (l/22)**0.5*(0.065+0.045*s+0.0065*s**2)


def calc_Amonthly(start_date,end_date,lat,long,pH,Sa,Cl,Si,OM,s,l,C,P):
    monthly_mean_Rs=calc_R(start_date,end_date,lat,long)
    R=np.array(monthly_mean_Rs)
    K=calc_K(pH,Sa,Cl,Si,OM)
    LS=calc_LS(s,l) ###MAKE SURE YOU FINISH THE EXERCISE TO COMPLETE THIS FUNCTION
    return R*K*LS*C*P #t/ha/year/

def calc_A(start_date,end_date,lat,long,pH,Sa,Cl,Si,OM,s,l,C,P):
    monthly_mean_Rs=calc_R(start_date,end_date,lat,long)
    R=np.nansum(monthly_mean_Rs)
    K=calc_K(pH,Sa,Cl,Si,OM)
    LS=calc_LS(s,l) ###MAKE SURE YOU FINISH THE EXERCISE TO COMPLETE THIS FUNCTION
    return R*K*LS*C*P #t/ha/year/

if __name__ == "__main__":
    #test get_weather
    daily_data=get_weather("2024-01-01","2024-12-31",37.212281,-8.119963)

    #test calc_rain_day_10
    #Test the function
    rain_10,day_10=calc_rain_day_10(daily_data['precipitation_sum'][0:30])
    print('The number of days with rainfall greater than 10mm in the first 30 days was {} and those days rainfall summed to {:.1f}'.format(day_10,rain_10))
    print('The rainfall in this month looked like:')
    print(daily_data['precipitation_sum'][0:30])

    #test calc_R
    monthly_mean_Rs=calc_R("1970-01-01","1997-12-31",37.310764, -8.826724) #Aljezur
    print('The yearly R value from 1970-1997 in Aljezur is {} MJmm/ha/h/year'.format(monthly_mean_Rs))


    #test calc_K
    pH=5.5
    OM=2.4
    Sa=75
    Si=6
    Cl=19
    K=calc_K(pH,Sa,Cl,Si,OM)
    print(K)

    #test calc_LS
    print(calc_LS(9,22))

    ##Test the function
    #R params
    start_date='2010-01-01'
    end_date='2022-12-31'
    lat=37.2
    long=-7.516667
    #Soil K params - to measure in field
    pH=5.5
    OM=2.4
    Sa=75
    Si=6
    Cl=19
    #Slope LS params - to measure in field
    l=22
    s=9
    ##C and P factors
    C=0.005 #Forest, is this valid for eucalyptus?!
    P=1 #No conservation starts
    A=calc_Amonthly(start_date,end_date,lat,long,pH,Sa,Cl,Si,OM,s,l,C,P) ##Call the function