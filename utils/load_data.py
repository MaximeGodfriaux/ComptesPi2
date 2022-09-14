import pandas as pd


def load_sheet(csv_path):
    """This function load sheet as pandas dataframe

    Args:
        csv_path (string): path of the csv sheet

    Returns:
        pd.DataFrame: sheet in pandas Dataframe
    """
    sheet = pd.read_csv(csv_path, header=None)
    sheet = sheet.rename(columns={0:'Date', 1:'Libellé', 2:'Activité', 3:'Montant'})

    return sheet


def load_transfer(csv_path):
    """This function load transfer sheet as pandas dataframe

    Args:
        csv_path (string): path of the csv transfer sheet

    Returns:
        pd.DataFrame: transfer sheet in pandas Dataframe
    """
    sheet = pd.read_csv(csv_path, header=None)
    sheet = sheet.rename(columns={0:'Date', 1:'Libellé', 2:'Montant'})

    return sheet


def create_total_sheet(data):
    """This function create the shet with all values

    Args:
        data (dictionnary): dictionnary containing all the sheets
    """
    data['total'] = pd.concat([data['cash'], data['compte'], data['materiel']])


def load_data():
    """This function loads all the sheets

    Returns:
        dictionnary: dictionnary containing all the sheets
    """
    data = {}
    data['cash'] =  load_sheet('csv_files/cash.csv')
    data['compte'] = load_sheet('csv_files/compte.csv')
    data['materiel'] = load_sheet('csv_files/materiel.csv')

    create_total_sheet(data)

    data['transfer_cash'] = load_transfer('csv_files/transfer_cash.csv')
    data['transfer_materiel'] = load_transfer('csv_files/transfer_materiel.csv')

    return data
