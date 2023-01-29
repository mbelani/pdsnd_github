import time
import datetime
import pandas as pd
from tabulate import tabulate

from Prompter import Prompter
import Utilities
from StatsUtil import StatsUtil

# Simple associative array for cities and corresponding data files.
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Lists that will be used for prompting and validation.
MONTHS = [ 'january', 'february', 'march', 'april', 'may', 'june' ]
DAYS = [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', \
        'saturday', 'sunday' ]

# Used to prompt user for additional filters
MONTH_DAY_FILTERS = [ 'month', 'day', 'both', 'none' ]

# Holds the number of DataFrame rows to display at a time
NUM_DATA_ROWS_TO_SHOW = 5

def prompt_user_for_city():
    """
    Asks user for a city name. Note that city must be one there is data for.
    
    Returns
    -------
    city - string, containing the name of the city

    """
    
    # Use a generic prompter to get the city
    c = Prompter("city", "cities "
                          , CITY_DATA.keys(), False)
    city = c.getinput()
    
    return city

def prompt_user_for_addl_filters():
    """
    Asks user if they want to filter by month or day.
    
    Returns
    -------
    string - indicating what the user wants to filter by (month, day, both
                or none).

    """

    # Use generic prompter for any additional filters the user wants
    md = Prompter("filter", "data filters ", MONTH_DAY_FILTERS
                           , True)
    md_filters = md.getinput()
    
    return md_filters

def prompt_user_for_month():
    """
    Asks user for a month to filter the data by.
    
    Returns
    -------
    month - string, the month that the user wants to filter the data for,
    or 'all', if no month-based filtering is desired.

    """
    
    mp = Prompter("month", "months ", MONTHS, True)
    month = mp.getinput()
    
    return month

def prompt_user_for_day():
    """
    Asks user for a day to filter the data by.
    
    Returns
    -------
    day - string, the day (of week) that the user wants to filter the data for,
    or 'all', if no day-based filtering is desired.

    """
    
    dp = Prompter("day", "days ", DAYS, True)
    day = dp.getinput()
    
    return day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply 
                        no month filter
        (str) day - name of the day of week to filter by, or "all" to apply 
                        no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    #HINT: Use a while loop to handle invalid inputs
    city = prompt_user_for_city()

    # Default the month and day filters to be all (i.e., no filters)    
    month = 'all'
    day = 'all'
    
    md_filters = prompt_user_for_addl_filters()
    
    # 'none' indicates no filtering
    if md_filters != 'none':
        if md_filters in ['month', 'both']:
            month = prompt_user_for_month()
            
        if md_filters in ['day', 'both']:
            day = prompt_user_for_day()

    print('=' * 80)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month & day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply 
                        no month filter
        (str) day - name of the day of week to filter by, or "all" to apply 
                        no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
             None, if there was an error trying to load data
    """

    try:
        df = pd.read_csv(CITY_DATA[city])
    except IOError as e:
        print("IOError: {}".format(e))
        
        return None
    
    # Save the original list of columns, as we plan to add some columns to
    # the dataset. The raw data will be shown using the original columns in
    # the dataset.
    df_orig_col_list = df.columns
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    # df['day_of_week'] = df['Start Time'].dt.day_of_week
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == DAYS.index(day)]
 
    # Get the start_hour from the time
    df['start_hour'] = df['Start Time'].dt.hour
    
    # Determine user age; note that the Birth Year is NOT present in all the
    # data files; hence the check
    if 'Birth Year' in df:
        df['age'] = datetime.date.today().year - df['Birth Year']
    
    # Get station start and end combo
    df['station_end_points'] = df['Start Station'] + ' => ' + df['End Station']

    # Retrun the data as well as the (original) column list.
    return df, df_orig_col_list


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\n***Calculating The Most Frequent Times of Travel (numbers '
          'inside parens indicate volume)...\n')
    su = StatsUtil()
    
    # display the most common month
    freq_month = df['month'].mode()[0]
    freq_month_occs = (df['month'] == freq_month).sum()

    # display the most common day of week
    freq_day = df['day_of_week'].mode()[0]
    freq_day_occs = (df['day_of_week'] == freq_day).sum()

    # display the most common start hour
    freq_st_hour = df['start_hour'].mode()[0]
    freq_st_hour_occs = (df['start_hour'] == freq_st_hour).sum()

    print("Popular month: {} ({}), popular day: {} ({})"
          ", popular hour: {} ({})."
          .format(freq_month, freq_month_occs, freq_day, freq_day_occs
                  , freq_st_hour, freq_st_hour_occs))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n***Calculating The Most Popular Stations and Trip (numbers '
          'inside parens indicate volume)...\n')
    su = StatsUtil()

    # display most commonly used start station
    freq_start_st = df['Start Station'].mode()[0]
    freq_start_st_occs = (df['Start Station'] == freq_start_st).sum()

    # display most commonly used end station
    freq_end_st = df['End Station'].mode()[0]
    freq_end_st_occs = (df['End Station'] == freq_end_st).sum()


    # display most frequent combination of start station and end station trip
    freq_end_points = df['station_end_points'].mode()[0]
    freq_end_points_occs = (df['station_end_points'] == freq_end_points).sum()

    print("Popular start stn: {} ({}) \nPopular end stn: {} ({}) \n"
          "Popular end points: {} ({})."
          .format(freq_start_st, freq_start_st_occs, freq_end_st
                  , freq_end_st_occs, freq_end_points, freq_end_points_occs))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n***Calculating Trip Duration...\n')
    su = StatsUtil()

    # display total travel time
    tot_travel_time = Utilities.Utilities.format_seconds(
        df['Trip Duration'].sum())

    # display mean travel time
    avg_travel_time = Utilities.Utilities.format_seconds(
        df['Trip Duration'].mean())

    print("Total travel time: {}, average travel time: {}."
          .format(tot_travel_time, avg_travel_time))


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n***Calculating User Stats (numbers '
          'inside parens indicate volume)...\n')
    su = StatsUtil()

    # Display counts of user types
    for user_type in df['User Type'].dropna().unique():
        print("Count of user type {}: {}"
              .format(user_type, (df['User Type'] == user_type).sum()))

    # Display counts of gender, only if Gender is part of the data set
    if 'Gender' in df:
        for gender in df['Gender'].dropna().unique():
            print("Count of gender {}: {}"
                  .format(gender, (df['Gender'] == gender).sum()))

    if 'Birth Year' in df:
        # Display earliest, most recent, and most common year of birth
        print("Earliest year of birth: {} \nLatest year of birth: {} \n"
              "Most frequent year of birth: {}"
              .format(int(df['Birth Year'].min()), int(df['Birth Year'].max()), 
                      int(df['Birth Year'].mode()[0])))
        
        # Show number of rides based on age groups/bands.
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 100, 125]
        grouped = df.groupby(pd.cut(df['age'], bins = bins)).size()
        print("Data grouped by age groups:")
        print(grouped)
    

def get_df_data_in_parts(df):
    """
    Gets dataframe data in part (i.e., a few rows at a time), and yields
    this data in a pretty/tabulated format.
    
    Parameters
    ----------
    df : DataFrame - the DataFrame that contains the data we want to show.
            Note that this returns a few rows at a time (using yield).

    Returns
    -------
    Yields a few rows at a time (using yield)

    """
    done = False
    i = 0
    
    while not done:
        if (i >= df.shape[0]):
            done = True
            
        else:
            yield(tabulate(df[i:i+NUM_DATA_ROWS_TO_SHOW], headers=df.keys()
                           , tablefmt='psql'))
            i += NUM_DATA_ROWS_TO_SHOW

def show_df_data(df):
    """
    Shows dataframe data in parts (few rows at a time), prompting the user
    after every time.
    
    Parameters
    ----------
    df : DataFrame - the DataFrame that contains the data we want to show.

    Returns
    -------
    None
    
    """
    
    sd = Prompter('raw data', 'to see raw data '
                           , ['yes', 'no'], False)
    inputval = sd.getinput()
    
    if (inputval == "yes"):        
        for i in get_df_data_in_parts(df):
            print(i)
            inp = input("Show more rows? ")
            if (inp.title() == "No"):
                break

def main():
    while True:
        city, month, day = get_filters()
        df, df_orig_col_list = load_data(city, month, day)

        if df is None:
            print("Error loading data! Exiting!")

            break

        print("City: {}, month: {}, day: {}.".format(city, month, day))

        # Get (and print) data statistics.
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_df_data(df[df_orig_col_list])

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
