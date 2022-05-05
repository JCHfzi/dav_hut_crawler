# %%


from data_collection import *


def main():
    #print("Hello World")
    # Bevor die Suche ausgeführt wird, müssen die Funktionen untern einmal ausgeführt werden
    selected_date = "20.05.2022"
    lists_of_huts = range(1,3)

    meta_data_df, free_beds_data_df = collect_data(selected_date, lists_of_huts)
    meta_data_df.to_csv("collected_data/alle_huetten.csv")
    free_beds_data_df.to_csv("collected_data/free_beds_data_df.csv")

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()


# %%
