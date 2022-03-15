import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# added following reviewer feedback
def check_data_entry(prompt, valid_entries):
    """
    Asks user to type some input and verify if the entry typed is valid.
    Since we have 3 inputs to ask the user in get_filters(), it is easier to write a function.
    Args:
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted
    Returns:
        (str) user_input - the user's valid input
    """
    try:
        user_input = str(input(prompt)).lower()

        while user_input not in valid_entries :
            print('Sorry... it seems like you\'re not typing a correct entry.')
            print('Let\'s try again!')
            user_input = str(input(prompt)).lower()

        print('Great! the chosen entry is: {}\n'.format(user_input))
        return user_input

    except:
        print('Seems like there is an issue with your input')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_cities = CITY_DATA.keys()
    prompt_cities = 'Please choose one of the 3 cities (chicago, new york city, washington): '
    city = check_data_entry(prompt_cities, valid_cities)

    # get user input for month (all, january, february, ... , june)
        # get user input for month (all, january, february, ... , june)
    valid_months = ['all','january','february','march','april','may','june']
    prompt_month = 'Please choose a month (all, january, february, ... , june): '
    month = check_data_entry(prompt_month, valid_months)

    # get user input for day of week (all, monday, tuesday, ... sunday)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
    prompt_day = 'Please choose a day (all, monday, tuesday, ... sunday): '
    day = check_data_entry(prompt_day, valid_days)

    print('-'*40)
    return city, month, day

def load_data(city,month,day_of_week):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #read in city data based on user input
    df = pd.read_csv(CITY_DATA[city])


    #extract month and day from Start time column
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['start_hour'] = df['Start Time'].dt.hour

    # Filter on month and day inputs
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

     # filter by day of week if applicable
    if day_of_week != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day_of_week.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month, common dow & common start hour
    popular_month = df['month'].mode()[0]
    popular_dow = df['day_of_week'].mode()[0]
    popular_start_hour = df['start_hour'].mode()[0]

    print('Most Popular Month:', popular_month)
    print('Most Popular Day of Week:', popular_dow)
    print('Most Popular start hour:', popular_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station=df.groupby('Start Station').size().reset_index(name='trip_counts').sort_values('trip_counts',ascending=False)['Start Station'].iloc[0]
    print('The most commonly used start station: {}'.format(pop_start_station))

    # display most commonly used end station
    pop_end_station=df.groupby('End Station').size().reset_index(name='trip_counts').sort_values('trip_counts',ascending=False)['End Station'].iloc[0]
    print('The most commonly used end station: {}'.format(pop_end_station))

    # display most frequent combination of start station and end station trip
    df['station_combo']=df['Start Station'] +" & " + df['End Station']
    pop_station_combo=df.groupby('station_combo').size().reset_index(name='trip_counts').sort_values('trip_counts',ascending=False)['station_combo'].iloc[0]
    print('The most common station combination: {}'.format(pop_station_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time_sum = round(df['Trip Duration'].sum()/3600,2)
    print('The total time travelled was {} hours'.format(travel_time_sum))

    # display mean travel time
    travel_time_mean = round(df['Trip Duration'].mean()/3600,2)
    print('The average trip duration was {} hours'.format(travel_time_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df.groupby('User Type').size().reset_index(name='trip_counts').sort_values('trip_counts',ascending=False)
    print('\nNumber of trips by each User Type:\n')
    print(user_type_counts)

    # Display counts of gender & Birth year for cities where data available
    if city in ['new york city','chicago']:
        gender_counts = df.groupby('Gender').size().reset_index(name='trip_counts').sort_values('trip_counts',ascending=False)
        print('\nNumber of trips by each Gender:\n')
        print(gender_counts)

        #calculate yob data
        latest_yob = int(df['Birth Year'].sort_values(ascending = False).iloc[0])
        earliest_yob = int(df['Birth Year'].sort_values(ascending = True).iloc[0])
        common_yob = int(df.groupby('Birth Year').size().reset_index(name='yob_counts').sort_values('yob_counts',ascending=False)['Birth Year'].iloc[0])

        print('\nThe most recent birth year: {}'.format(latest_yob))
        print('The earliest birth year: {}'.format(earliest_yob))
        print('The most common birth year: {}'.format(common_yob))

    else:
        print('\nNo gender or birth year data available for {}'.format(city.title()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw table data at user request"""

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()

def main():
    while True:
        city, month, day_of_week = get_filters()
        print('\nFilters received!\n')

        df = load_data(city, month, day_of_week)
        print('\nDataframe Loaded and Filtered!\n')

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
