

def create_pages(new_data):
    """This function creates the sub pages

    Args:
        new_data (dictionnary): dictionnary containing all the new sheets
    """
    name_to_fr = {
        'compte': 'Compte',
        'cash': 'Cash',
        'materiel': 'Matériel',
        'by_activity': 'Tri par Activité',
        'total': 'Total'
    }

    dic_of_activity = get_activity(new_data['by_activity'])

    for name in new_data:
        with open("source_html/page.html", "r", encoding='utf-8') as f:
            page = f.read()

        page = page.replace('$1', name_to_fr[name])
        table = new_data[name].to_html(index=False)
        page = page.replace('$2', table)

        page = add_color_to_values(page)
        page = add_ref_to_activity(page, dic_of_activity)

        page_file = open(f"page_{name}.html", "w")
        page_file.write(page)
        page_file.close()


def get_activity(df):
    """Returns all the activities name into a dic

    Args:
        df (pandas.DataFrame): dataframe by activity

    Returns:
        dict: dictionnary of all the activites
    """
    dic_of_activity = {}

    for activity in df['Activité'].iteritems():
        dic_of_activity[activity[1]] = activity[0]

    if 'Total' in dic_of_activity:
        del dic_of_activity['Total']

    return dic_of_activity


def add_color_to_values(page):
    """This function add colors to values in subpages

    Args:
        page (str): HTML page in str format

    Returns:
        str: modified HTML page
    """
    new_page = ''

    for line in page.splitlines():

        if '€</td>' in line:

            if '-' in line:
                color = '#FA413B'  # Red

            else:
                color = '#34FF27'  # Greend

            line = line.replace('<td>', f'<td style="color:{color}"">')

        new_page += line + '\n'

    return new_page


def add_ref_to_activity(page, dic_of_activity):
    """This function add links to activities pages

    Args:
        page (str): HTML page in str format

    Returns:
        str: modified HTML page
    """
    new_page = ''

    for line in page.splitlines():

        text = line.replace('</td>', '<td>')
        text = text.split('<td>')

        if len(text) == 3 and text[1] in dic_of_activity:

            key = text[1]
            index = dic_of_activity[key]
            line = line.replace(key, f'<a href="subpage_{index}.html">{key}</a>')

        new_page += line + '\n'

    return new_page
