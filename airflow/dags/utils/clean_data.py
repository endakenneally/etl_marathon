import pandas as pd


def return_event_type(athlete_performance):
    try:
        if 'k' in athlete_performance.lower():
            return "Time"
        elif 'h' in athlete_performance.lower():
            return "Distance"
    except:
        return None


def return_end_date(event_dates):
    if len(event_dates) == 10:
        return event_dates
    else:
        date_split = event_dates.split('-')
        return date_split[1]


def return_start_date(event_dates):
    match len(event_dates):
        case 10:
            return event_dates
        case 14:
            date_split = event_dates.split('-')
            second_split = date_split[1].split('.')
            return f'{date_split[0]}{second_split[1]}.{second_split[2]}'
        case 17:
            date_split = event_dates.split('-')
            second_split = date_split[1].split('.')
            return f'{date_split[0]}{second_split[2]}'
        case 21:
            return event_dates.split('-')[0]


def clean_csv_data(df):
    # Rename Columns
    df.rename(columns={"Year of event": "year_of_event",
                       "Event dates": "event_dates",
                       "Event name": "event_name",
                       "Event distance/length": "event_distance_length",
                       "Event number of finishers": "event_number_of_finishers",
                       "Athlete performance": "athlete_performance",
                       "Athlete club": "athlete_club",
                       "Athlete country": "athlete_country",
                       "Athlete year of birth": "athlete_year_of_birth",
                       "Athlete gender": "athlete_gender",
                       "Athlete age category": "athlete_age_category",
                       "Athlete average speed": "athlete_average_speed",
                       "Athlete ID": "athlete_id"
                       }, inplace=True)

    # Add the country column using last 5 chars of event name field
    df['event_country'] = df['event_name'].apply(
        lambda x: x[-5:].strip('()').upper())

    ioc = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_IOC_country_codes')[0]
    ioc = ioc.assign(Code=ioc['Code'].str[-3:]
                     ).set_index('Code')['National Olympic Committee']
    df['country_name'] = df['event_country'].map(ioc)

    df['event_type'] = df['athlete_performance'].apply(return_event_type)

    df['start_date'] = df['event_dates'].apply(return_start_date)

    df['end_date'] = df['event_dates'].apply(return_end_date)

    return df
