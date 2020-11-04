from DataLoader.BostonDataLoader import BostonDataLoader
from DataLoader.NewYorkCityDataLoader import NewYorkCityDataLoader
from Dataset.Dataset import Dataset
from PropertyAnalyzer.PropertyAnalyzer import PropertyAnalyzer
from ReportCreator.ReportCreator import ReportCreator


def main():
    dataset = Dataset("sql_credentials.json")

    print("====== Airbnb Ideal Property Finder ======")
    print("Welcome to the Airbnb Ideal Property Finder! by Robert Ciborowski")
    print("This program will find the characteristics of the ideal real estate")
    print("property to purchase and use for Airbnb renting!")
    print("To begin, let's select some cities.")

    selectedAnyDataset = False

    while True:
        print("Would you like to consider purchasing in New York City, NY? [Y/n]")
        answer = input()

        if answer.lower() == "y":
            print("Loading New York City, NY data...")
            selectedAnyDataset = True
            newYorkCityLoader = NewYorkCityDataLoader()
            newYorkCityLoader.load("data/new_york_city", dataset)
            break
        elif answer.lower() == "n":
            print("Skipping New York City, NY.")
            break
        else:
            print("That is not a valid answer.")

    while True:
        print(
            "Would you like to consider purchasing in Boston, MA? [Y/n]")
        answer = input()

        if answer.lower() == "y":
            print("Loading Boston, MA data...")
            selectedAnyDataset = True
            bostonLoader = BostonDataLoader()
            bostonLoader.load("data/boston", dataset)
            break
        elif answer.lower() == "n":
            print("Skipping Boston, MA.")
            break
        else:
            print("That is not a valid answer.")

    if not selectedAnyDataset:
        print("You have decided not to consider property in any city.")
        print("Goodbye!")
        return 1

    print("We have now selected some cities to consider.")
    numberOfDaysRented = 1

    while True:
        print("How many days out of the year would you like to rent out")
        print("your property? [0-365]")
        answer = 0

        try:
            answer = int(input())
        except:
            print("Invalid input.")
            continue

        if answer == 0:
            print("If you do not want to rent out your property for even one")
            print("day, there is no point in running this program. Please")
            print("submit a valid answer.")
            continue

        if answer < 0 or answer > 365:
            print("That is an invalid number.")
            continue

        numberOfDaysRented = answer
        break

    print("You have decided to rent out your property for "
          + str(numberOfDaysRented) + " days.")
    print("We will now analyze our data.")
    print("Analyzing data...")

    analyzer = PropertyAnalyzer()
    best_listing, best_listing_profit, listing_stats, best_neighbourhood = analyzer.getHighestYearlyProfitProperties(dataset, numberOfDaysRented)
    print("Results obtained!")
    print("Best listing:")
    print(best_listing)
    print("Best listing's annual profit if rented for " + str(numberOfDaysRented) + " days: " + str(best_listing_profit))
    print("Neighbourhood statistics can be viewed in the report.")
    print("Best neighbourhood:")
    print(best_neighbourhood)

    reportCreator = ReportCreator()
    reportCreator.createReport(numberOfDaysRented, best_listing, best_listing_profit, listing_stats, best_neighbourhood)

    print("Your report has been created. Please check report.pdf.")
    print("Thank you and goodbye.")
    return 0


if __name__ == "__main__":
    main()
