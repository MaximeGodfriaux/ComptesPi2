import numpy as np
import pandas as pd
from apply_change_data import values_to_string
from create_pages.create_pages import add_color_to_values, get_activity


def create_subpages(data, new_data):
    """Create the sub pages of activities

    Args:
        data (dictionnary): : dictionnary containing all the sheets
        new_data (dictionnary): dictionnary containing all the new sheets
    """
    sub_tables = get_sub_tables(data)

    sort_by_dates_and_values(sub_tables)
    add_sum_lines(sub_tables)
    values_to_string(sub_tables)

    dic_of_activity = get_activity(new_data['by_activity'])

    for name in sub_tables:
        with open("source_html/page.html", "r", encoding='utf-8') as f:
            page = f.read()

        page = page.replace('$1', name)
        table = sub_tables[name].to_html(index=False)
        page = page.replace('$2', table)

        page = add_color_to_values(page)

        index = dic_of_activity[name]
        page_file = open(f"subpage_{index}.html", "w")
        page_file.write(page)
        page_file.close()


def get_sub_tables(data):
    """This function will outputs a table by activities

    Args:
        data (dictionnary): : dictionnary containing all the sheets

    Returns:
        dict: dictionnary of all the activites
    """
    all_expenses = pd.concat([data['cash'], data['compte'], data['materiel']])

    all_expenses['Date'] = pd.to_datetime(all_expenses['Date'], format='%d-%m-%Y')

    list_tables = [x for _, x in all_expenses.groupby('Activité')]
    sub_tables = {}

    for table in list_tables:
        activity = table.iloc[0]['Activité']
        sub_tables[activity] = table.drop('Activité', axis=1)
    
    return sub_tables


def sort_by_dates_and_values(sub_tables):
    """Sort the gain by dates and signs

    Args:
        sub_tables ([type]): [description]
    """
    for name_dataframe in sub_tables:
        df = sub_tables[name_dataframe]
        df['sign'] = df['Montant'] < 0
        df.sort_values(by=['sign','Date'], inplace=True)
        df.drop('sign', axis=1, inplace=True)


def add_sum_lines(sub_tables):
    """This function add a line with the totale to each sheet

    Args:
        sub_tables (dictionnary): dictionnary containing all the new sheets
    """
    for name_dataframe in sub_tables:

        df = sub_tables[name_dataframe]

        df_plus = df[df['Montant'] >= 0]
        data_plus_line = [['', 'Recettes Totales', sum_montant_df(df_plus)]]
        plus_line = pd.DataFrame(data_plus_line, columns=df_plus.columns)

        df_minus = df[df['Montant'] < 0]
        data_minus_line = [['', 'Dépenses Totales', sum_montant_df(df_minus)]]
        minus_line = pd.DataFrame(data_minus_line, columns=df_minus.columns)

        data_total_line = [['', 'Total', sum_montant_df(df)]]
        total_line = pd.DataFrame(data_total_line, columns=df.columns)

        sub_tables[name_dataframe] = pd.concat([df_plus, plus_line, df_minus, minus_line, total_line])


def sum_montant_df(df):
    """Returns the sum of the Montant in the df

    Args:
        df (pd.DataFrame): DataFrame
    """
    sum_montant = 0

    if len(df) > 0:
        sum_montant = np.sum(df['Montant'])
    
    return sum_montant