import pandas as pd
import numpy as np

# Question 1.1

def extract_hour(time):
    """
    Extracts hour information from military time.
    
    Args: 
        time (float64): array of time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
    
    Returns:
        array (float64): array of input dimension with hour information.  
          Should only take on integer values in 0-23
    """
    
    # extract the first 2 digits as hour
    time = time.apply(lambda x: np.nan if pd.isnull(x) else 1.0*int(x/100))
    time = time.apply(lambda x: np.nan if pd.isnull(x) 
                      or x < 0 or x > 23 else x)
    return time
    
def extract_mins(time):
    """
    Extracts minute information from military time
    
    Args: 
        time (float64): array of time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
    
    Returns:
        array (float64): array of input dimension with hour information.  
          Should only take on integer values in 0-59
    """
    # cut off decimal part and return
    # the last 2 digits as minutes
    time = time.apply(lambda x: np.nan if pd.isnull(x) == True 
                       else 1.0*int(x)%100)
    time = time.apply(lambda x: np.nan if pd.isnull(x) 
                      or x < 0 or x > 59 else x)
    return time

# Question 1.2

def convert_to_minofday(time):
    """
    Converts military time to minute of day
    
    Args:
        time (float64): array of time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
    
    Returns:
        array (float64): array of input dimension with minute of day
    
    Example: 1:03pm is converted to 783.0
    >>> convert_to_minofday(1303.0)
    783.0
    """
#     sr = pd.Series()
#     for val in time:
#         if pd.notnull(val) and val >= 0 and val <= 2359.0:
#             sr.append(extract_hour(val)*60.0 + extract_mins(val))
#         else:
#             sr.append(val)
    #time = time.map(lambda x: x if pd.isnull(x) == True else extract_hour(x)*60.0 + extract_mins(x))
    hour = extract_hour(time)
    minutes = extract_mins(time)
    hour = hour.apply(lambda x: x*60.0)
    return hour.add(minutes)
    
    
def calc_time_diff(x, y):
    """
    Calculates delay times y - x
    
    Args:
        x (float64): array of scheduled time given in military format.  
          Takes on values in 0.0-2359.0 due to float64 representation.
        y (float64): array of same dimensions giving actual time
    
    Returns:
        array (float64): array of input dimension with delay time
    """
    
    scheduled = convert_to_minofday(x)
    actual = convert_to_minofday(y)
    
    return actual.subtract(scheduled)