import pandas as pd

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(100 * df['education'].isin(['Bachelors']).sum() / len(df), 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    lower_education = df[~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]

    # percentage with salary >50K
    higher_education_rich = round(100 * len(higher_education[higher_education['salary'] == '>50K']) / len(higher_education), 1)
    lower_education_rich = round(100 * len(lower_education[lower_education['salary'] == '>50K']) / len(lower_education), 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    min_hrs = df[df['hours-per-week'] == df['hours-per-week'].min()]

    rich_percentage = round(100 * len(min_hrs[min_hrs['salary'] == '>50K'])  / len(min_hrs), 1)

    # What country has the highest percentage of people that earn >50K?
    countries_salaries = df[['native-country', 'salary']].value_counts().reset_index(name='count')

    countries_salaries = countries_salaries \
        .pivot(index='native-country', columns='salary', values='count') \
        .reset_index() \
        .rename_axis(None, axis=1)

    countries_salaries['salary_pc_over_50k'] = round(
        100 * countries_salaries['>50K'] / (countries_salaries['>50K'] + countries_salaries['<=50K']), 1
    )
    
    highest_earning_country = countries_salaries.sort_values('salary_pc_over_50k', ascending=False).iloc[0]['native-country']
    highest_earning_country_percentage = countries_salaries.sort_values('salary_pc_over_50k', ascending=False).iloc[0]['salary_pc_over_50k']

    # Identify the most popular occupation for those who earn >50K in India.
    df_india = df[df['native-country'] == 'India']

    top_IN_occupation = df_india[df_india['salary'] == '>50K']['occupation'].value_counts().keys()[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }