from utils import *

# main function
def main() : 
    
    import os
    
    print("======================================================================================================")
    print("Welcome to Efficiency calculator")
    print("This program calculates efficency of mobile game packages and store the results.")
    print("To see details of source code, visit my github repository.")
    print("https://github.com/jbw9964/Efficiency_calculator.git")
    print("======================================================================================================")

    if not ("Data" in os.listdir(os.getcwd())) : 
        print("It seems like no data exist.")
        print("Forcing to create data directories.")
        print("Type the name of games seperated by ', ' : ", end="")
        game_list = list(str(input()).split(", "))
        for game in game_list : 
            print(game, end=" ")
        print()
        print()
        create_data_dir(Force=False, Game_name_list=game_list)
        print()
        print("======================================================================================================")
    
    while True : 
        print()
        print("Options : [ 0 ~ 5 ]")
        print("[0] : Exist program")
        print("[1] : Initialize data")
        print("[2] : Manage data")          # Game_list.txt, Calculation_Game_name.txt, Package_data_Game_name.txt
        print("[3] : Read data")            # Game_list.txt, Calculation_Game_name.txt, Package_data_Game_name.txt
        print("[4] : Plot efficency")
        print("[5] : Check data status")
        print()

        # [2] : create, add, delete
        
        print("user input --> ", end="")
        user_input = str(input())
        print(user_input)
        print("------------------------------------------------------------------")
        
        # Done
        if user_input == '1' :      # [1] : Initialize data
            print()
            print("To initialize your data (directories), we need the lists of the game.")
            check_game_list()
            print("Are you sure to initialize data? [y/n] : ", end="")
            temp_input = str(input())
            print(temp_input)

            if temp_input == 'y' : 
                print()
                print("Type the name of games seperated by ', ' : ")
                game_list = list(str(input()).split(", "))
                create_data_dir(Force=True, Game_name_list=game_list)
            
            elif temp_input == 'n' : 
                print("======================================================================================================")
                continue
            
            else : 
                print("You put wrong input. Please try again.")
                print("======================================================================================================")
                continue
            
            print("Directories has been initialized.")
            print("======================================================================================================")
            print()

        elif user_input == '2' :    # [2] : Manage data
            print("Manage data active")
            current_dir = "Data"
            depth = 0

            recursive_modify(Current_dir=current_dir, Parent_dir=None, Depth=depth)
            print("------------------------------------------------------------------")

        # Done
        elif user_input == '3' :    # [3] : Read data
            print("Read data active")

            current_dir = "Data"
            depth = 0

            recursive_search(Current_dir=current_dir, Parent_dir=None, Depth=depth)
            print("------------------------------------------------------------------")

        # Done
        elif user_input == '4' :    # [4] : Plot efficency
            game_name_list = check_game_list()
            print("Which game do you want to plot? Type the exact game name : ", end="")

            game_name_input = str(input())
            print(game_name_input)
            print()

            if game_name_input not in game_name_list : 
                print(f"There's no game as named [{game_name_input}]. Please type properly.")
                print("\t--> In [ ./Data/Game_list.txt ] ...")
                for name in game_name_list : 
                    print(f"\t\t--> [{name}]")
                print()
                print("======================================================================================================")
                continue
            
            try : 
                calculation_data_dir = "Data/Game_package_data/" + game_name_input + "/Calculation_"  + game_name_input + ".txt"
                calculation_dataframe = read_csv(calculation_data_dir)
            except : 
                print(f"There's no saved calculation in [ ./{calculation_data_dir} ].")
                print("Please use options before to plot calculation.")
                print()
                print("Use options like...")
                print("\t--> [2] : Manage data")
                print()
                print("======================================================================================================")
                continue
            
            [max_eff_name, max_eff_index], package_dataframe = plot_eff(game_name_input)

            print(f"-->In [{game_name_input}], [{max_eff_name}] is most efficient.")
            print("\t==> [{}] is [{}] valuable per price.".format(
                max_eff_name, package_dataframe["value_per_price"][max_eff_index]
            ))
            print()

        # Done
        elif user_input == '5' :    # [5] : Check data status
            print()
            
            valid, dir_unvalid_list, file_unvalid_list = serach_game()

            if not valid : 

                if dir_unvalid_list is not None : 
                    print("There's mismatch between [ ./Data/Game_list.txt ] and data.")
                    print("Please check the directories of...")

                    for name in dir_unvalid_list : 
                        print(f"\t--> [ {name} ]")
                    print()
                
                if file_unvalid_list is not None : 
                    print("There's some error in data directories.")
                    print("Please check the data of...")

                    for name in file_unvalid_list : 
                        print(f"\t--> [ ./{name} ]")

                        for data in os.listdir(name) : 
                            print(f"\t\t--> [ {data} ]")

                print()
                print("Please use options like...")
                print("\t--> [1] : Initialize data")
                print("\t--> [2] : Manage data")
                print("======================================================================================================")
                print()
            
            else : 
                print("==> All data exists properly.")
                print()

        # Done
        elif user_input == '0' :    # [0] : Exist program
            print()
            print("Exist program.")
            print("Good bye and thank you for using this program.")
            print("======================================================================================================")
            break
        
        # Done
        else : 
            print()
            print("You put wrong input. Please try again.")
            print()
            continue
        
        print("======================================================================================================")


if __name__ == "__main__" : 
    main()