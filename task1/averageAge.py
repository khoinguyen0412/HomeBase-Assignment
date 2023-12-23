import pandas as pd 

def calculate_avg_age(df):
    try:
        average_age = df["Age"].mean()
        print(f"Average age is '{average_age}' ")

    except KeyError:
        print("Column Age is not found")



if __name__ == '__main__':
    df = None
    while df is None:
        file_name = input('Please enter your file name: ')
        csv_file_path = f'./data/{file_name}'

        try:
            df = pd.read_csv(csv_file_path)

        except pd.errors.EmptyDataError:
            print(f"File '{file_name}' is not a valid CSV file. Please enter a valid CSV file.")
            df = None
        except FileNotFoundError:
            print(f"File '{file_name}' not found. Please enter a valid file name.")

    calculate_avg_age(df)