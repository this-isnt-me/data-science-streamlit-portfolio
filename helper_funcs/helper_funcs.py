def filter_countries(input_dataframe,
                     filter_column,
                     year=None):
    input_dataframe = input_dataframe[input_dataframe['year'].isin(year)]
    return sorted(list(set(list(input_dataframe[filter_column]))))
