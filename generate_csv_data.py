from energy_factors.buildings import get_df

def run():
    df = get_df()

    # Export data to csv file
    print("Debug: started writing data-frame to csv file")
    df.to_csv("generated_data/germany.csv")
    print("Debug: finished writing data-frame to csv file")

if __name__ == '__main__':
    run()
