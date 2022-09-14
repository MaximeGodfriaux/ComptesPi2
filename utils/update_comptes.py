from apply_change_data import apply_change_data
from create_pages.create_main_page import create_main_page
from create_pages.create_pages import create_pages
from create_pages.create_subpages import create_subpages
from create_pages.create_graphs import create_graph_page
from load_data import load_data


def main():
    data = load_data()
    new_data = apply_change_data(data)
    create_main_page(new_data)
    create_pages(new_data)
    create_subpages(data, new_data)
    create_graph_page(new_data)


if __name__ == '__main__':
    main()
