import pull_data as gcp
import json
import os
import evaplib
import time
import scipy
from scipy import integrate

def yeet(error):
    raise Exception(error)

class metric_calculator:
    def __init__(self, field_name, date):
        self.name = field_name
        self.date = date
        self.forecast = self.download_forecast()
        self.history = self.download_history()

    def download_forecast(self):
        filename = self.name+','+self.date+','+'forecast.json'
        location = self.name+'/'+self.date +'/'+filename
        destination = 'data/'+self.name+'-forecast.json'

        # check to see if file is already downloaded
        exists = os.path.isfile(destination)
        if not exists:
            # download forecast information from correct bucket
            gcp.download('vspectral-weather-bucket-1',location,destination)
        
        data = []
        with open(destination) as f:
            data = json.load(f)
        #REVIEW os.remove(destination)
        return data

    def download_history(self):
        # download forecast information from correct bucket
        filename = self.name+','+self.date+','+'history.json'
        location = self.name+'/'+self.date +'/'+filename
        destination = 'data/'+self.name+'-history.json'

        # check to see if file is already downloaded
        exists = os.path.isfile(destination)
        if not exists:
            # download forecast information from correct bucket
            gcp.download('vspectral-weather-bucket-1',location,destination)
        
        data = []
        with open(destination) as f:
            data = json.load(f)
        # REVIEW os.remove(destination)
        return data

    def check_errors(self):
        # check for common errors
        if self.forecast == []:
            return 'Error: forecast empty'
        elif self.history == []:
            return 'Error: history empty'
        else:
            return 0

#################################################
#              Metric functions                 #
#################################################
# growth metrics
    def calculate_gdd(self, high=30, low=10):
        history = self.history
        forecast = self.forecast
        day_metric = {}
        for data_hour in history: # same day of data, history is taken at 7am
            str_day = time.strftime("%m-%d-%Y",time.gmtime(data_hour['epoch']))
            # calculate metric here
            num_metric = max(0,min(data_hour['air temperature']-low,high-low)) / 24
            # done calculating metric
            try: 
                day_metric[str_day] = day_metric[str_day] + num_metric # additive hourly metric
            except:
                day_metric[str_day] = num_metric

        # this needs to be calculated after history to correctly overwrite overlaps
        for data_day in forecast:
            str_day = time.strftime("%m-%d-%Y",time.gmtime(data_day['epoch']))
            # using single sin fitting method
            amplitude = data_day['max air temperature'] - data_day['min air temperature']
            baseline = data_day['min air temperature']
            num_samples = 24
            samples = [i/(num_samples-1)*scipy.pi for i in range(num_samples)]
            day_sin = [amplitude*scipy.sin(x) + baseline for x in samples]
            day_sin_thresholded_zero = [max(min(x,high-low),0) for x in day_sin]
            integrated_sin = integrate.trapz(day_sin_thresholded_zero)
            day_metric[str_day] = integrated_sin / num_samples
        return day_metric

    def calculate_gtr(self):
        yeet('metric not yet implemented')

        return 4

# water balance metrics
    def calculate_cwsi(self):
        yeet('metric not yet implemented')

        # calculates cwsi using thermal image and weather
        # not implemented in v1
        return 4

    def calculate_spei(self):
        yeet('metric not yet implemented')

        return 4

    def calculate_et_makkink_daily(self):
        yeet('metric not yet implemented')
        history = self.history
        forecast = self.forecast
        str_previous_day = ''
        day_metric = {}
        for data_hour in history: # same day of data, history is taken at 7am
            str_previous_day = str_day
            str_day = time.strftime("%m-%d-%Y",time.gmtime(data_hour['epoch']))
            # calculate metric here
            Rs = 666 #radiation solar, solar radiation is in W/m^s, converted to J/m^s/day

            #TODO check units
            # done calculating metric
            try:
                # calculate units using daily average
                day_metric[str_day] = day_metric[str_day] + num_metric # average units
                num_metric = evaplib.Em() # Makkink evaporation mm/day
                data_hour['air temperature'], data_hour['relative humidity'], #C, %
                data_hour['atmospheric pressure'], # hPa
                Rs # J / m^2 / day)
            except:
                day_metric[str_day] = num_metric

        # this needs to be calculated after history to correctly overwrite overlaps
        for data_day in forecast:
            str_day = time.strftime("%m-%d-%Y",time.gmtime(data_day['epoch']))
            # using single sin fitting method
            amplitude = data_day['max air temperature'] - data_day['min air temperature']
            baseline = data_day['min air temperature']
            num_samples = 24
            samples = [i/(num_samples-1)*scipy.pi for i in range(num_samples)]
            day_sin = [amplitude*scipy.sin(x) + baseline for x in samples]
            day_sin_thresholded_zero = 666#[max(min(x,high-low),0) for x in day_sin]
            integrated_sin = integrate.trapz(day_sin_thresholded_zero)
            day_metric[str_day] = integrated_sin / num_samples
        return day_metric

    def calculate_et_makkink(self):
        '''
        NOTE: makkink equation given in evaplib is ment to be a daily metric
        it was assumed that the input units could be changed to /hr instead of 
        /day and that would changed the output units accordingly to calculate
        a daily sum using hourly data. However, there may be an intrinsic unit
        or assumption with the calculation that may invalidate it.
        This should be tested or investigated further.
        '''
        history = self.history
        forecast = self.forecast
        day_metric = {}
        for data_hour in history: # same day of data, history is taken at 7am
            str_day = time.strftime("%m-%d-%Y",time.gmtime(data_hour['epoch']))
            # calculate metric here
            avg_tmp = data_hour['air temperature']
            rh = data_hour['relative humidity']
            airpress = data_hour['atmospheric pressure']
            solar_radiation = data_hour['solar radiation']*86400 #convert from W/m^2 to J/M^2/hr
            num_metric = evaplib.Em(
                avg_tmp, rh, airpress, solar_radiation
            )
            try:
                day_metric[str_day] = day_metric[str_day] + num_metric # addative hourly metric
            except:
                day_metric[str_day] = num_metric

        # this needs to be calculated after history to correctly overwrite overlaps
        for data_day in forecast:
            str_day = time.strftime("%m-%d-%Y",time.gmtime(data_day['epoch']))
            # using single sin fitting method
            avg_tmp = (data_day['max air temperature'] + data_day['min air temperature'])/2
            rh = data_day['relative humidity']
            airpress = data_day['atmospheric pressure']
            solar_radiation = data_day['solar radiation']*86400 #convert from W/m^2 to J/M^2/day
            num_metric = evaplib.Em(
                avg_tmp, rh, airpress, solar_radiation
            )
            day_metric[str_day] = num_metric
        return day_metric

    def calculate_et0pm(self): #daily Penman Monteith reference evaporation estimates
        history = self.history
        forecast = self.forecast
        day_metric = {}
        for data_hour in history: # same day of data, history is taken at 7am
            str_day = time.strftime("%m-%d-%Y",time.gmtime(data_hour['epoch']))
            # calculate metric here
            ra = evaplib.ra(6,0.5,4,data_hour['wind speed']) # aerodynamic resistance TODO if hops z=, if potato z=
            Rn = 150 # net radioation input over time #ANCHOR assumption
            G = 0 #soil heat flux input over time, ignored http://www.fao.org/3/x0490e/x0490e07.htm 
            Rext = 59443200 # TODO estimate for Incoming shortwave radiation at the top of the atmosphere [J m-2 day-1].
            Rs = 41610240 # TODO estimate for total incoming shortwave radiation
            elevation = 1835 # Elevation of Elk mountian farms [m]
            num_metric = evaplib.ET0pm( # desired units in comments
                data_hour['air temperature'], data_hour['relative humidity'], #C, %
                data_hour['atmospheric pressure'], Rext, Rs,
                data_hour['wind speed'], elevation
            ) #TODO check units
            # done calculating metric
            num_metric = num_metric/24 # day to hour
            num_metric = num_metric*0.0393701 # mm to inch
            try:
                day_metric[str_day] = day_metric[str_day] + num_metric # additive hourly metric
            except:
                day_metric[str_day] = num_metric
        return day_metric

    def calculate_e0(self):
        history = self.history
        forecast = self.forecast
        day_metric = {}
        for data_hour in history: # same day of data, history is taken at 7am
            str_day = time.strftime("%m-%d-%Y",time.gmtime(data_hour['epoch']))
            # calculate metric here
            ra = evaplib.ra() # aerodynamic resistance TODO if hops z=, if potato z=
            Rn = 666 # net radioation input over time TODO
            G = 666#soil heat flux input over time TODO
            ra= 666#surface resistance TODO
            num_metric = evaplib.Epm( # desired units in comments
                data_hour['air temperature'], data_hour['relative humidity'], #C, %
                data_hour['atmospheric pressure'], #Rext, Gsoil, # hPa, J/t, J/t
                    # raerodynamic, rsurface # s/m, s/m 
            ) #TODO check units
            # done calculating metric
            try:
                day_metric[str_day] = day_metric[str_day] + num_metric # additive hourly metric
            except:
                day_metric[str_day] = num_metric

        # this needs to be calculated after history to correctly overwrite overlaps
        for data_day in forecast:
            num_metric = 666
            day_metric[str_day] = num_metric
            yeet('metric not implemented yet')
        return day_metric

# disease metrics
    #helper function
    def __continuous_hours_greater_than(self, temp_list, up_threshold=200, continuous_threshold=6,
                                    low_threshold=-10):
        #  helper function used to calculate how many continuous hours of a value there are
        #  withing a given range
        continuous_hours = 0
        for temp in temp_list:
            if low_threshold <= float(temp) <= up_threshold:
                continuous_hours = continuous_hours + 1
            if continuous_hours > continuous_threshold:
                return True
        return False

    # potato specific
    def calculate_lateblight(self):
        # infection potential index, source: http://ipm.ucanr.edu/DISEASE/DATABASE/tomatolateblight.html 
        return 4

    # hop specific
    def __calculate_new_PM_index(self, day_info, pm_index, i_prev_day):
        #  calculate PM index change for that day
        #  private function
        #  (i) If there are greater than six continuous hours above 30°C, then subtract 20 points.
        if self.__continuous_hours_greater_than(day_info['temperature'],
                                        low_threshold=30):
            return pm_index - 20, True
        #  (ii) If there are greater than 2.5 mm rainfall, then subtract 10 points.
        elif day_info['rain'] > 2.5:
            return pm_index - 10, False
        #  (iii) If there are greater than six continuous hours above 30°C on the previous day, then no change
        if i_prev_day:
            return pm_index, False
        #  (iv) If there are at least six continuous hours of temperatures between 16 and 27°C, then add 20 points.
        elif self.__continuous_hours_greater_than(day_info['temperature'],
                                            up_threshold=27, low_threshold=16):
            return pm_index + 20, False
        #  (v) If none of the above rules apply, then subtract 10 points.
        return pm_index - 10, False

    def __calculate_new_PM_index_forecast(self, day_info, pm_index, i_prev_day):
        #  calculate PM index change for that day
        #  private function
        #  (i) If there are more than six continuous hours above 30°C, then subtract 20 points.
        if day_info['max air temperature'] > 33: #assuming that if a day has a max temperature of 33 then powdery mildew damager occurs
            return  -20, True
        #  (ii) If there is greater than 2.5 mm rainfall, then subtract 10 points.
        elif day_info['precipitation'] >= 2.5:
            return  -10, False
        #  (iii) If there are more than six continuous hours above 30°C on the previous day, then no change
        if i_prev_day:
            return 0, False
        #  (iv) If there are at least six continuous hours of temperatures between 16 and 27°C, then add 20 points.
        elif day_info['max air temperature'] < 30 and day_info['min air temperature'] > 13: 
                        #assuming that if max/min temperatures are >13 and <30 (resp.) then this is true
            return  20, False
        #  (v) If none of the above rules apply, then subtract 10 points.
        return pm_index - 10, False

    def calculate_powderymildew(self):
        # gent index, source https://www.plantmanagementnetwork.org/pub/php/review/2003/hpm/
        history = self.history
        forecast = self.forecast
        day_info = {
            'temperature':[],
            'rain': 0
        }
        day_metric = {}
        i_rule_prev = False # rule i of gent's model carries over to next day
        last_str_day = time.strftime("%m-%d-%Y",time.gmtime(history[0]['epoch']))
        for data_hour in history: # same day of data, history is taken at 7am
            str_day = time.strftime("%m-%d-%Y",time.gmtime(data_hour['epoch']))
            if last_str_day != str_day: # same day
                day_metric[last_str_day],i_rule_prev = self.__calculate_new_PM_index(day_info,0,i_rule_prev)
                day_info = { #reset day_metric for new day
                    'temperature':[],
                    'rain': 0
                }
                last_str_day = str_day
            # build day datastructure needed for *PM_index(*) method
            day_info['temperature'].append(data_hour['air temperature'])
            day_info['rain'] = day_info['rain']+ data_hour['precipitation']
            
        # this needs to be calculated after history to correctly overwrite overlaps
        for data_day in forecast:
            str_day = time.strftime("%m-%d-%Y",time.gmtime(data_day['epoch']))
            day_metric[str_day], i_rule_prev = self.__calculate_new_PM_index_forecast(data_day,0,i_rule_prev)
        return day_metric
        return 4


    def calculate_spidermites(self):
        # source: http://ipm.ucanr.edu/PHENOLOGY/ma-2spotted_spider_mite.html 
        return self.calculate_gdd(high=32, low=11.7)

