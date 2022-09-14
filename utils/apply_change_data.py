from loguru import logger
import numpy as np
import pandas as pd


def add_by_activity(data, new_data):
    """This function add the sheet by activity

    Args:
        data (dictionnary): : dictionnary containing all the sheets
        new_data (dictionnary): dictionnary containing all the new sheets
    """
    all_expenses = pd.concat([data['cash'], data['compte'], data['materiel']])
    all_expenses.drop('Libellé', axis=1, inplace=True)

    all_expenses['Date'] = pd.to_datetime(all_expenses['Date'], format='%d-%m-%Y')

    by_activity = all_expenses.groupby('Activité').agg({'Date': 'min', 'Montant': 'sum'})

    by_activity.reset_index(inplace=True)
    by_activity = by_activity[['Date', 'Activité', 'Montant']]
    
    new_data['by_activity'] = by_activity


def add_compte(data, new_data):
    """This function add the sheet compte

    Args:
        data (dictionnary): : dictionnary containing all the sheets
        new_data (dictionnary): dictionnary containing all the new sheets
    """
    compte = pd.concat([data['compte'], data['transfer_cash'], data['transfer_materiel']])
    compte.fillna(value='', inplace=True)

    new_data['compte'] = compte


def add_cash(data, new_data):
    """This function add the sheet cash

    Args:
        data (dictionnary): : dictionnary containing all the sheets
        new_data (dictionnary): dictionnary containing all the new sheets
    """
    data['transfer_cash']['Montant'] = - data['transfer_cash']['Montant']
    
    cash = pd.concat([data['cash'], data['transfer_cash']])
    cash.fillna(value='', inplace=True)

    new_data['cash'] = cash


def add_materiel(data, new_data):
    """This function add the sheet materiel

    Args:
        data (dictionnary): : dictionnary containing all the sheets
        new_data (dictionnary): dictionnary containing all the new sheets
    """
    data['transfer_materiel']['Montant'] = - data['transfer_materiel']['Montant']
    
    materiel = pd.concat([data['materiel'], data['transfer_materiel']])
    materiel.fillna(value='', inplace=True)

    new_data['materiel'] = materiel


def add_total(data, new_data):
    """This function add the sheet total

    Args:
        data (dictionnary): : dictionnary containing all the sheets
        new_data (dictionnary): dictionnary containing all the new sheets
    """
    total = data['total']
    total.fillna(value='', inplace=True)

    new_data['total'] = total


def sort_by_dates(new_data):
    """This function sort the elements by date

    Args:
        new_data (dictionnary): dictionnary containing all the new sheets
    """
    for name_dataframe in new_data:

        if name_dataframe is not 'by_activity':
            new_data[name_dataframe]['Date'] = pd.to_datetime(
                new_data[name_dataframe]['Date'], format='%d-%m-%Y'
            )

        new_data[name_dataframe].sort_values(by='Date', inplace=True)


def add_sum_line(new_data):
    """This function add a line with the totale to each sheet

    Args:
        new_data (dictionnary): dictionnary containing all the new sheets
    """
    for name_dataframe in new_data:

        sum_value = np.sum(new_data[name_dataframe]['Montant'])

        if name_dataframe is 'by_activity':
            data_total_line = [['', 'Total', sum_value]]
        else:
            data_total_line = [['', 'Total', '', sum_value]]

        total_line = pd.DataFrame(data_total_line, columns=new_data[name_dataframe].columns)
        new_data[name_dataframe] = pd.concat([new_data[name_dataframe], total_line])


def check_correctness(new_data):
    """This function checks if the sum of all sheets is consistent

    Args:
        new_data (dictionnary): dictionnary containing all the new sheets
    """
    check_sum = 0
    check_total = 0
    check_by_activity = 0

    for name_dataframe in new_data:

        if name_dataframe is 'by_activity':
            check_by_activity += new_data[name_dataframe].iloc[-1]['Montant']
        
        elif name_dataframe is 'total':
            check_total += new_data[name_dataframe].iloc[-1]['Montant']

        else:
            check_sum += new_data[name_dataframe].iloc[-1]['Montant']

    if np.abs(check_sum - check_total) < 0.01 and np.abs(check_sum - check_by_activity) < 0.01:
        logger.success('Correctness of the code')

    else:
        logger.error('Total and sum of by activity are differnt !!')


def values_to_string(new_data):
    for name_dataframe in new_data:
        new_data[name_dataframe]['Montant'] = \
            new_data[name_dataframe]['Montant'].apply(lambda x: f'{x:.2f} €')
        new_data[name_dataframe]['Date'] = \
            new_data[name_dataframe]['Date'].apply(lambda x: x.strftime('%d/%m/%Y') if type(x) is not str else '')


def apply_change_data(data):
    """This function add the transfer and compute the by activity sheet

    Args:
        data (dictionnary): : dictionnary containing all the sheets

    Returns:
        dictionnary: dictionnary containing all the new sheets
    """
    new_data = {}

    add_by_activity(data, new_data)
    add_compte(data, new_data)
    add_cash(data, new_data)
    add_materiel(data, new_data)
    add_total(data, new_data)

    sort_by_dates(new_data)
    add_sum_line(new_data)

    check_correctness(new_data)

    values_to_string(new_data)
    
    return new_data