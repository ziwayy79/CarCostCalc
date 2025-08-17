import requests
import xmltodict #converts xml files to JSON
import os

original_cars = {"1": ("48495", "Toyota", "Corolla", "$23,520"),
            "2": ("48016", "Honda", "Civic", "$24,250"),
            "3": ("48020","Hyundai", "Elantra", "$23,370"),
            "4": ("48500", "Nissan", "Sentra", "$22,730")}
cars = original_cars.copy()
ListLength = len(cars)

numlist = []
def main():


    while True:
        try:
            global cars, numlist #modifies the global variables back to default values
            cars = original_cars.copy()
            numlist = []
            print(
                "Welcome, from the following list, please select a car model you would like to view by typing their respective number:\n"
                f"    1: {cars['1'][1]} {cars['1'][2]}\n"
                f"    2: {cars['2'][1]} {cars['2'][2]}\n"
                f"    3: {cars['3'][1]} {cars['3'][2]}\n"
                f"    4: {cars['4'][1]} {cars['4'][2]}\n"
            )

            i = input()
            getCar(i)
            flag = True #flag variable learned from CS50 Duck
            while flag:
                choose = input("\nHere are your next choices (Please Type the Number): \n"
                "1: Analyse the Saved Vehicle(s)\n" \
                "2: Reset List\n" \
                "3: Continue Selecting\n").strip()
                if choose == "3":
                    x = track(numlist)
                    if x is None:
                        print("There are no more models left")
                    elif x == "0":
                        pass
                    else:
                        getCar(x)
                elif choose == "2":
                    removeCarfile(numlist)
                    flag = False
                elif choose == "1":
                    comparefiles(numlist)
                    flag = False


        except TypeError:
            print("Please enter a valid number")
            pass

def track(numlist): #Communicates the avaliable choices to the user to avoid double picking models
    if ListLength == len(numlist):
        return None
    else:
        print("Here are the remaining models, Please Select One")
    for _ in cars:
        if not(_ in numlist):
            print(f"{_}: {cars[_][1]} {cars[_][2]}")
    user = input("Type '0' to Go Back\n")
    return user

def getCar(i):
    if i not in cars:
        raise TypeError()
    else:
        print(f"You picked a {cars[i][1]} {cars[i][2]}")
        response = requests.get("https://www.fueleconomy.gov/ws/rest/vehicle/" + cars[i][0])
        data = xmltodict.parse(response.text) #code from CS50 Duck Debugger
        print(
            "Here are the stats: \n"
            f"MSRP (USD): {cars[i][3]} \n"
            f"Mileage (L/100 km): {round(235.215 / int(data['vehicle']['comb08']), 2)} \n"
            f"Mileage (MPG): {data['vehicle']['comb08U']} \n"
        )
    while True:
        try:
            ask = input("Would you like to save this vehicle as a potential option? (Yes/No)\n").lower().strip()
            if ask != "yes" and ask != "no":
                raise TypeError()
            elif ask == "yes":
                createCarfile(i)
                print(f"Vehicle stats have been saved into {data['vehicle']['baseModel']}.txt")
                numlist.append(i)
                del cars[i]
            else:
                return 0
            break
        except TypeError:
            print("Invalid Response")
def removeCarfile(numlist): #removes created files once the user decides to reset their list
    for _ in numlist:
        os.remove(f"{original_cars[_][2]}.txt")
def createCarfile(i):
    response = requests.get("https://www.fueleconomy.gov/ws/rest/vehicle/" + cars[i][0])
    data = xmltodict.parse(response.text)
    file = open(f"{data['vehicle']['baseModel']}.txt", "w")
    file.write(
        f"Car: {cars[i][1]} {cars[i][2]}\n"
        f"MSRP (USD): {cars[i][3]}\n"
        f"Mileage (MPG): {data['vehicle']['comb08']}\n"
        f"Mileage (L/100 km): {round(235.215 / int(data['vehicle']['comb08']), 2)}"
    )

def comparefiles(numlist):
    response = requests.get("https://www.fueleconomy.gov/ws/rest/vehicle/" + original_cars[numlist[0]][0]) #Used as a placeholder for the car with the lowest mileage
    data = xmltodict.parse(response.text)

    while True:
        try:
            user = input("How much do you plan on traveling per week with a new vehicle? (Enter in miles or kilometers)\n").lower()
            km = ""
            if ("miles" or "mile") in user or ("kilometer" or "kilometers") in user:
                for _ in user:
                    if _.isdigit():
                        km += _
                km = int(km)
                if ("miles" or "mile") in user :
                    km = km * 1.60934
            else:
                raise KeyError()
            break
        except KeyError:
            return("Please enter a distance in kilometers or miles")

    while True:
        try:
            useryears = input("How long do you plan on owning a new vehicle? Enter in years, decimals required (Ex. 4.5 years)\n").lower().replace(" ", "")
            years = ""
            count = 0
            if "years" in useryears or "year" in useryears:
                for _ in useryears:
                    if _.isdigit():
                        years += _
                    elif _ == "." and count == 0:
                        years += _
                        count += 1
                    elif _.isalpha():
                        continue
                    else:
                        raise ValueError()
            else:
                raise ValueError()
            break
        except ValueError:
            return("Please enter a valid period")

    print("The data of your selected vehicles have been saved into 'summary.txt'")
    cheapestMSRP = original_cars[numlist[0]][3]
    cheapestCar = f"{original_cars[numlist[0]][1]} {original_cars[numlist[0]][2]}"
    highestMPG = float(data["vehicle"]["comb08"])
    highestMPGCar = f"{original_cars[numlist[0]][1]} {original_cars[numlist[0]][2]}"
    highestMPGCarMSRP = original_cars[numlist[0]][3]
    for _ in numlist: #Determines the model with the cheapestMSRP
        if original_cars[_][3] < cheapestMSRP:
            cheapestMSRP = original_cars[_][3]
            cheapestCar = f"{original_cars[_][1]} {original_cars[_][2]}"

    for _ in numlist: #Determines the model with the highest mpg (Best gas mileage)
        response1 = requests.get("https://www.fueleconomy.gov/ws/rest/vehicle/" + original_cars[_][0])
        data1 = xmltodict.parse(response1.text)
        if float(data1["vehicle"]["comb08"]) > highestMPG:
            highestMPG = float(data1["vehicle"]["comb08"])
            highestMPGCar = f"{original_cars[_][1]} {original_cars[_][2]}"
            highestMPGCarMSRP = original_cars[numlist[_]][3]

    fileSum = open("summary.txt", "w")
    fileSum.write("Model(s) Selected: \n")
    for _ in numlist:
        fileSum.write(f"   {original_cars[_][1]} {original_cars[_][2]} \n")
    fileSum.write(f"\nThe cheapest vehicle to buy is the {cheapestCar}, priced at {cheapestMSRP}\n\n")

    gasprice = 1.33 #Formatted in Canadian dollars per litre (price data from En-Pro).
    USD = requests.get("https://api.frankfurter.app/latest?from=USD&to=CAD") #API from https://frankfurter.dev/ (documentation)
    data = USD.json()
    multi = float(data['rates']['CAD'])



    totaldistance = km * 52 * float(years)
    L_per_100km = 235.215/highestMPG
    totalL = totaldistance * (L_per_100km / 100)
    CADprice = (totalL * gasprice)
    USDprice = CADprice / multi
    #Math above calculates the price of ownership over the user's inputted years, using today's gas price in Canadian Doller/Litre

    fileSum.write(f"The vehicle that will cost you the least to own over the next {years} year(s) of ownership is the {highestMPGCar}\n")
    fileSum.write(f"Cost over {years} year(s) if you drive {(km/1.60934):.2f} miles ({km:.2f} km) every week:\n ${USDprice:.2f} USD, ${CADprice:.2f} CAD (Assuming that gas prices are always constant at {gasprice}/L in the Canadian Dollar)\n")
    fileSum.write(f"MSRP of the {highestMPGCar}: {highestMPGCarMSRP}")



if __name__ == "__main__":
    main()
