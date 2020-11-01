from DataLoader.NewYorkCityDataLoader import NewYorkCityDataLoader


def main():
    newYorkCityLoader = NewYorkCityDataLoader()
    newYorkCityDf = newYorkCityLoader.load("data/new_york_city/AB_NYC_2019.csv")
    print(newYorkCityDf)

    bostonLoader = BostonDataLoader()
    newYorkCityDf = bostonLoader.load("data/new_york_city/AB_NYC_2019.csv")
    print(newYorkCityDf)

if __name__ == "__main__":
    main()
