from energy_factors.buildings import get_df
from visualize.data_reducer import do_reducing
from visualize.calc_best import get_stuff

def run():
    df = get_df()

    # Export data to csv file
    print("Debug: started writing data-frame to csv file")
    df.to_csv("generated_data/bremen_test.csv")
    print("Debug: finished writing data-frame to csv file")
    print("Debug: Make squares")
    do_reducing()
    print("Debug: Make squares")
    print("Debug: Get top 100")
    get_stuff()
    print("Debug: Get top 100")

if __name__ == '__main__':
    run()
