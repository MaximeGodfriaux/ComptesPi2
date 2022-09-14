

def create_main_page(new_data):
    """This function creates the main html page

    Args:
        new_data (dictionnary): dictionnary containing all the new sheets
    """
    with open("source_html/index.html", "r", encoding='utf-8') as f:
        page = f.read()

    for name in ['compte', 'cash', 'materiel', 'by_activity']:
        total_value = new_data[name].iloc[-1]['Montant']
        page = page.replace(f'${name}', total_value)

    page_file = open("index.html", "w")
    page_file.write(page)
    page_file.close()
