from energy_factors.buildings import get_df

def run():
    df = get_df()

    # Export data to csv file
    print(df.to_csv("generated_data/test_bremen.csv"))

if __name__ == '__main__':
    run()
