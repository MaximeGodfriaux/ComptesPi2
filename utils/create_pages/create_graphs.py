import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def create_graph_page(new_data):
    """This function creates the graphs html page

    Args:
        new_data (dictionnary): dictionnary containing all the new sheets
    """
    pd.options.mode.chained_assignment = None

    with open("source_html/page.html", "r", encoding='utf-8') as f:
        page = f.read()

    page = page.replace('$1', 'Graphes')

    graphs = create_graphs(new_data)
    page = page.replace('$2', graphs)

    page_file = open("page_graphs.html", "w")
    page_file.write(page)
    page_file.close()


def create_graphs(new_data):
    """ This function create the html code for the graphs

    Args:
        new_data (dictionnary): dictionnary containing all the new sheets

    Returns:
        str: html code to print the graph
    """
    graphs = ''

    create_pie_charts(new_data)

    graphs = add_title(graphs, 'Entrées d\'argents')
    graphs = add_graph(graphs, 'images/pie_incomes.png')
    graphs = add_title(graphs, 'Sorties d\'argents')
    graphs = add_graph(graphs, 'images/pie_outcomes.png')

    return graphs


def create_pie_charts(new_data):
    """ This function crates two pie charts

    Args:
        new_data (dictionnary): dictionnary containing all the new sheets
    """
    clean_data = new_data['by_activity'][['Activité', 'Montant']].copy()
    clean_data['Montant'] = clean_data['Montant'].apply(lambda x: float(x[:-2]))
    
    incomes = clean_data[clean_data['Montant'] > 0]
    outcomes = clean_data[clean_data['Montant'] <= 0]

    create_pie_chart(incomes, 'incomes')
    create_pie_chart(outcomes, 'outcomes')


def create_pie_chart(df, name):
    """ This function create a pie chart in png format

    Args:
        df (pd.DataFrame): dataframe with libelles and values
        name (str): name of the graph
    """
    df = df.loc[df['Activité'] != 'Total']
    df['Montant'] = df['Montant'].apply(lambda x: np.abs(x))
    df.sort_values(by='Montant', inplace=True, ascending=False)
    
    plt.figure(figsize=(10,10))
    plt.pie(df['Montant'],
            labels=df['Activité'],
            autopct=make_autopct(df['Montant']),
            startangle=180,
            counterclock=False,
            textprops={'fontsize': 16, 'color': 'w'})
    plt.savefig(f'images/pie_{name}.png', transparent=True, pad_inches=0, bbox_inches='tight')


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        value = np.round(pct * total / 100)
        val_str = f'{value:.0f} €'
        if pct > 5:
            val_str += f'\n({pct:.1f} %)'
        return val_str
    return my_autopct


def add_title(html_str, title):
    """ This function add a title to HTML

    Args:
        html_str (str): HTML under string format
        title (str): string containing the title
    """
    html_str = html_str + '<h2>' + title + '</h2>\n'

    return html_str


def add_graph(html_str, dir_graph):
    """ This function add a graph to HTML

    Args:
        html_str (str): HTML under string format
        dir_graph (str): directory of the graph
    """
    html_str = html_str + '<p><img src=\'' + dir_graph + '\' class=\'graph\'></p>\n'

    return html_str