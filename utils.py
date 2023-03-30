# ================================================================================================ #
# read or save csv as UTF8 encoding and index=False
from pandas import DataFrame

def read_csv(filepath : str) : 
    """Read csv file as UTF8 encoding.

    Args:
        filepath (str) : directory of csv file.

    Returns:
        pd.read_csv(filepath, sep=",", encoding="UTF8")
    """
    import pandas as pd
    return pd.read_csv(filepath, sep=",", encoding="UTF8")
def save_csv(Data : DataFrame, filepath : str) : 
    """Save csv file as UTF8 encoding.

    Args:
        Data (DataFrame) : data build by DataFrame.
        filepath (str) : directory of csv file.

    Returns:
        Data.to_csv(filepath, sep=",", encoding="UTF8", index=False)
    """
    return Data.to_csv(filepath, sep=",", encoding="UTF8", index=False)

# ================================================================================================ #
# return [Data - Game_package_data - Game_name] directory
def return_data_dir(Game_name : str) -> str: 
    """Returns [Game_name]'s data directory.
    
    - Data 
        - Game_package_data 
            - Game_name

    Args:
        Game_name (str) : name of game.

    Returns:
        pd.read_csv("Data/Game_list.txt", sep=",", encoding="UTF8")[Game_name].values[0] 
            --> Data - Game_package_data - Game_name
    """
    import pandas as pd
    return pd.read_csv("Data/Game_list.txt", sep=",", encoding="UTF8")[Game_name].values[0]

# ================================================================================================ #
# creates [ ./Data/Game_package_data/Game_name ] : creates only one directory
def add_game_data_dir(Data_dir : str, Game_name : str) -> None: 
    """Only creates new game directory and saves to Game_list.txt
    
    If some game's package data directory is already exist, function do nothing.

    Directory that function creates : 
    - Current directory
        - Data
            - Game_package_data
                - Game_name
    
    Args:
        Data_dir (str) : [ ./Data ]
        Game_name (str) : name of game.
    """
    import os
    import pandas as pd
    
    dir_package_data = Data_dir + "/Game_package_data"
    
    game_list = read_csv(Data_dir + "/Game_list.txt")
    
    if Game_name in os.listdir(dir_package_data) : 
        print(f"[{Game_name}]'s data looks like already exist at {dir_package_data}")
        print(os.listdir(dir_package_data))
        return
    
    dir_game = dir_package_data + "/" + Game_name
    os.mkdir(dir_game)
    
    if Game_name in game_list.keys() : 
        game_list = game_list.drop([Game_name], axis=1)
    
    game_list = pd.concat([game_list, 
                           pd.Series(data=dir_game, name=Game_name)
                           ], axis=1)
    
    save_csv(Data=game_list, filepath=Data_dir + "/Game_list.txt")
    print(f"[{Game_name}] data directory has been created.")

# ================================================================================================ #
# creates [ ./Data/Game_list.txt ] with input Game_name_list
def create_game_list(Game_name_list : list) -> None: 
    """creates [ ./Data/Game_list.txt ] with input Game_name_list

    Args:
        Game_name_list (list): list of game names
    """
    import os
    import pandas as pd

    gmae_list_dir = "Data/Game_list.txt"

    if os.path.isfile(gmae_list_dir) : 
        print("Game_list.txt already exist.")
    
    else : 
        data_dir_list = [0]
        game_name_list = ["Null"]
        for name in Game_name_list : 
            data_dir_list.append("Data/Game_package_data/" + name)
            game_name_list.append(name)
        
        save_csv(Data=pd.DataFrame(data=[data_dir_list], columns=game_name_list), filepath=gmae_list_dir)
        print(f"Game_list.txt has been created. --> [ ./Data/Game_list.txt ] : {Game_name_list}")

# add input DataFrame in [ ./Data/Game_list.txt ]
from pandas import DataFrame

def add_game_list(Data : DataFrame) -> None: 
    """Add input DataFrame with [ ./Data/Game_list.txt ]

    If there's same data in [ /Game_list.txt ] and Data, function will overwrite [ /Game_list.txt ] as Data
    
    [ /Game_list.txt ] must be stored by columns=[list of games] --> shape=(1,N)
    
    Therefore, input DataFrame must be shape=(1,N)
    
    Args:
        Data (DataFrame) : input data
    """
    import pandas as pd
    
    if type(Data) != type(pd.DataFrame()) : 
        print(f"Args Data must be dataframe. --> [ Data : {type(Data)} ]")
        return
    
    prev = read_csv("Data/Game_list.txt")
    
    for game in Data.keys() : 
        if game in prev.keys() : 
            prev = prev.drop([game], axis=1)
    
    current = pd.concat([prev, Data], axis=1)
    save_csv(current, "Data/Game_list.txt")

# Deletes specific data, [Game_name] in [ ./Data/Game_list.txt ]
def delete_game_list(Game_name : str, Force=False) -> None: 
    """Deletes specific data, [Game_name] in [ ./Data/Game_list.txt ]

    If Force=True, deletes all data and creates new one
    """
    import os
    import pandas as pd
    
    game_list_dir = "Data/Game_list.txt"
    
    if not os.path.isfile(game_list_dir) : 
        print("Game_list.txt doesn't exist.")
    
    else : 
        if Force : 
            os.remove(game_list_dir)
            save_csv(pd.DataFrame(data=[0], columns=["Null"]), game_list_dir)
            print("Game_list.txt has been deleted and created.")
        
        else : 
            data = read_csv(game_list_dir)
            if not (Game_name in data.keys()) : 
                print(f"[{Game_name}] doesn't exist in Game_list.txt")
            else : 
                data = data.drop([Game_name], axis=1)
                save_csv(data, game_list_dir)
                print(f"{[Game_name]} has been deleted in Game_list.txt.")

# ================================================================================================ #
# save input DataFrame to [ ./Data/Game_package_data/Game_name/Calculation_Game_name.txt ]
def save_calculation(Calc_dataframe : DataFrame, Game_name : str, Force=False) -> bool: 
    """Save pacakge's calculation
    
    Directory that data stored : 
    - Data
        - Game_package_data
            - Game_name
                - Calculation_Game_name.txt

    Args:
        Calc_dataframe (DataFrame) : calculated DataFrame.
        Game_name (str) : name of game.
        Force (bool) : force to save data though already exist.
    
    Returns:
        bool : True if calculation was saved.
    """
    import os
    
    game_dir = return_data_dir(Game_name)
    
    if type(Calc_dataframe) != type(DataFrame()) : 
        print(f"Args Calc_dataframe must be dataframe. --> [ Calc_dataframe : {type(Calc_dataframe)} ]")
        return False
    
    game_dir = game_dir + "/Calculation_" + Game_name + ".txt"
    
    if os.path.isfile(game_dir) : 
        print(f"[{Game_name}]'s data looks like already exist at {game_dir}")
        if not Force :
            return False
        print("Forcing to save data...")
    
    save_csv(Data=Calc_dataframe, filepath=game_dir)
    print(f"[{Game_name}] calculation data has been saved.")
    return True

# deltes [ ./Data/Game_package_data/Game_name/Calculation_Game_name.txt ]
def delete_calculation(Game_name : str) -> None: 
    """Deletes [ ./Data/Game_package_data/Game_name/Calculation_Game_name.txt ]
    - the calculation data of Game_name

    Args:
        Game_name (str): name of game.
    """
    import os

    game_dir = return_data_dir(Game_name=Game_name)
    calc_dir = game_dir + "/Calculation_" + Game_name + ".txt"
    
    os.remove(calc_dir)
    print(f"[{Game_name}]'s calculation data has been deleted.")

# ================================================================================================ #
# save input DataFrame to [ ./Data/Game_package_data/Game_name/Package_data_Game_name.txt ]
def save_package_data(Package_dataframe : DataFrame, Game_name : str, Force=False) -> None: 
    """Save package data.

    Package data must be sotred with two columns : --> ["Package_name", "Value", "Price"]
    
    Therefore your input DataFrame should be shape=(N,3).
    
    Args:
        Package_dataframe (DataFrame) : package data with shape=(N,3).
        Game_name (str) : name of game.
        Force (bool, optional) : force to save data though already exist. Defaults to False.
    """
    import os
    
    game_dir = return_data_dir(Game_name=Game_name)
    
    if type(Package_dataframe) != type(DataFrame()) : 
        print(f"Args Package_dataframe must be dataframe. --> [ Package_dataframe : {type(Package_dataframe)} ]")
        return
    
    game_dir = game_dir + "/Package_data_" + Game_name + ".txt"
    
    if os.path.isfile(game_dir) : 
        print(f"[{Game_name}]'s data looks like already exist at [ /{game_dir} ]")
        if not Force :
            return
        print("Forcing to save data...")
    
    save_csv(Data=Package_dataframe, filepath=game_dir)
    print(f"[{Game_name}] package data has been saved.")

# ================================================================================================ #
# add input DataFrame with [ ./Data/Game_package_data/Game_name/Package_data_Game_name.txt ]
def add_package_dataframe(Package_dataframe : DataFrame, Game_name : str) -> None: 
    """Add package data.

    Package data are stored with two columns : --> ["Package_name", "Value", "Price"]
    
    Therefore your input DataFrame should be shpae=(N,3)
    
    Args:
        Package_dataframe (DataFrame) : package data with sahpe=(N,3).
        Game_name (str) : name of game.
    """
    import os
    import numpy as np
    import pandas as pd
    
    game_dir = return_data_dir(Game_name=Game_name)
    
    package_dir = game_dir + "/Package_data_" + Game_name + ".txt"
    
    prev_data = read_csv(package_dir).values
    new_data = Package_dataframe.values
    
    data_stack = np.vstack((prev_data, new_data))
    current_data = pd.DataFrame(data=data_stack, columns=Package_dataframe.keys())
    
    save_csv(current_data, package_dir)
    print(f"[{Game_name}] package data has been updated.")

# ================================================================================================ #
# delete input package data in [ ./Data/Game_package_data/Game_name/Package_data_Game_name.txt ]
def delete_package(Game_name : str, Package_name : str, Force=False) -> None: 
    """Delete specific package.

    Args:
        Game_name (str) : name of game.
        Package_name (str) : name of package.
        Force (bool, optional) : force to delete every data. Defaults to False.
    """
    game_dir = return_data_dir(Game_name=Game_name)
    
    package_dir = game_dir + "/Package_data_" + Game_name + ".txt"
    
    package_data = read_csv(package_dir)
    
    del_index = package_data.index[package_data['Package_name'] == Package_name]
    
    if len(del_index) > 1 : 
        print(f"There are multiple packages that named [ {Package_name} ] in data.")
        if not Force : 
            return
        print("Forcing to delete data...")
    
    del_index = sorted(del_index, reverse=True)
    
    for index in del_index : 
        package_data = package_data.drop(index=index)
    
    save_csv(package_data, package_dir)
    print(f"[{Game_name}] package data [{Package_name}] has been deleted.")
    print()

# ================================================================================================ #
# creates every essential game directories
# if there is something in Game_name_list, creates directory including it.
# if Game_name_list is None, creates directories by [ ./Data/Game_list.txt ]
# if Force=True, deletes every directories and make new one
def create_data_dir(Force=False, Game_name_list=False) -> None: 
    """Creates every essential directories like : [ ./Data, ./Data/Game_list.txt, ./Data/Game_package_data, ... ]

    1\. If Force=True, function deletes stored data and create new one. If not, function only creates directories that missing.
    - [ ./Data ]
    - [ ./Data/Game_list.txt ] 
    - [ ./Data/Game_package_data ]
    
    2\. If Game_name_list=False, function doesn't create sub directories like : 
    - [ /Game_package_data/Calculation_Game_name.txt ]
    - [ /Game_package_data/Package_data_Game_name.txt ]
    
    3\. If Game_name_list iterable, function will add Game_name_list to [ ./Data/Game_list.txt ] and create sub directories :
    - add new game list to [ /Game_list.txt ]
    - [ /Game_package_data/Calculation_Game_name.txt ]
    - [ /Game_package_data/Package_data_Game_name.txt ]
    
    4\. If Game_name_list=None, function only creates sub directories that already exist in [ ./Data/Game_list.txt ] : 
    - [ /Game_package_data/Calculation_Game_name.txt ]
    - [ /Game_package_data/Package_data_Game_name.txt ]
    
    Args:
        Force (bool, optional) : force to delete stored data and creates new one. Defaults to False.
        Game_name_list (bool, optional) : list of games to create directories. Defaults to False.
    """
    import os
    import pandas as pd
    
    game_list = True

    if Force : 
        if not Game_name_list : 
            print("Game_name_list must be considered when forcing to make directory")
            print(f"Please input iterable object likewise List --> [ Gmae_name_list : {type(Game_name_list)}]")
            return
        
        import shutil
        print("Forcing to make new directories...")
        print("--> [ ./Data, ./Data/Game_list.txt, ./Data/Game_package_data ]")
        
        shutil.rmtree("Data")
        os.makedirs("Data", exist_ok=True)
        print("[./Data] directory has been made.")

        game_dir_list = ["Data/Game_package_data/" + name for name in Game_name_list]
        save_csv(Data=pd.concat([
            pd.DataFrame(data=[0], columns=["Null"]), 
            pd.DataFrame(data=[game_dir_list], columns=Game_name_list)], 
            axis=1
            ),
            filepath="Data/Game_list.txt"
        )
        print("[./Data/Game_list.txt] directory has been made.")

        os.makedirs("Data/Game_package_data", exist_ok=True)
        print("[./Data/Game_package_data] directory has been made.")

        print()
        for name in Game_name_list : 
            add_game_data_dir("Data", name)
            save_calculation(pd.DataFrame(), Game_name=name)
            save_package_data(pd.DataFrame(), Game_name=name)
            print()
        return
    
    else : 
        if not os.path.isdir("Data") : 
            print("Directory [ ./Data ] doesn't exist. Create new one.")
            os.mkdir("Data")
        else : 
            print("[./Data] directory already exist.")
        
        if not os.path.isfile("Data/Game_list.txt") : 
            print("Directory [ ./Data/Game_list.txt ] doesn't exist. Create new one.")
            save_csv(pd.DataFrame(data=[0], columns=["Null"]), "Data/Game_list.txt")
            game_list = False
        else : 
            print("[./Data/Game_list.txt] directory already exist.")
        
        if not os.path.isdir("Data/Game_package_data") : 
            print("Directory [ ./Data/Game_package_data ] doesn't exist. Create new one.")
            os.mkdir("Data/Game_package_data")
        else : 
            print("[./Data/Game_package_data] directory already exist.")

        if (not Game_name_list) and (Game_name_list is not None) : 
            return
    
    if Game_name_list is not None : 
        game_dir_list = ["Data/Game_package_data/" + name for name in Game_name_list]
        add_game_list(
            pd.DataFrame(data=[game_dir_list], columns=Game_name_list)
        )
    
    dir_game_package_data = "Data/Game_package_data"

    game_list = read_csv("Data/Game_list.txt").drop(["Null"], axis=1)

    print()
    for name in game_list.keys() : 
        dir_game = dir_game_package_data + "/" + name
        if not os.path.isdir(dir_game) : 
            add_game_data_dir("Data", Game_name=name)
            save_calculation(pd.DataFrame(), Game_name=name)
            save_package_data(pd.DataFrame(), Game_name=name)
            print()

# ================================================================================================ #
# load the package data at [ /Game_pacakge_data/Game_name/Package_data_Game_name.txt ]
# and calculate package efficiency (value per price),
# saved to [ /Game_pacakge_data/Game_name/Calculation_Game_name.txt ]
def calc_package_eff(Game_name : str, Game_data_dir : str, Force=True) -> None: 
    """Calculate efficiency by [ /Game_name/Package_data_Game_name.txt ] and save to [ /Game_name/Calculation_Game_name.txt ]
    
    Load data from : 
    - [ /Game_package_data ]
        - [ /Game_name ]
            - [ /Package_data_Game_name.txt ]
    
    Save data to : 
    - [ /Game_package_data ]
        - [ /Game_name ]
            - [ /Calculation_Game_name.txt ]

    Args:
        Game_name (str) : name of game.
        Game_data_dir (str) : [ ./Data/Game_package_data/Game_name ]
        Force (bool, optional) : force to save data [ /Calculation_Game_name.txt ] though already exist. Defaults to True.
    """
    import os
    import pandas as pd
    
    data_list = os.listdir(Game_data_dir)
    
    if len(data_list) < 2 : 
        print("In [ ./Data/Game_package_data/Game_name ], [ /Package_data_.txt ] must be exist.")
        print(f"It seems like something's missing --> [ /{Game_data_dir} : {data_list} ]")
        return
        
    if "Package" not in data_list[0] and "Package" not in data_list[1] : 
        print("In [ ./Data/Game_package_data/Game_name ], [ /Package_data_.txt ] must be exist.")
        print(f"It seems like it's missing --> [ /{Game_data_dir} : {data_list} ]")
        return
    
    print("Calculating...")
    package_data = read_csv(Game_data_dir + "/Package_data_" + Game_name + ".txt")
    
    package_name_list = [name for name in package_data["Package_name"]]
    package_value_list = [value for value in package_data["Value"]]
    package_price_list = [price for price in package_data["Price"]]
    
    eff_list = []
    for index in range(len(package_data)) : 
        eff = package_value_list[index] / package_price_list[index]
        eff_list.append(eff)
    
    calc_dataframe = pd.DataFrame(
        data=[package_name_list, eff_list],
        index=["Package_name", "value_per_price"]
        ).transpose()
    
    if save_calculation(calc_dataframe, Game_name=Game_name, Force=Force) : 
        print(f"[{Game_name}]'s data was calculated and saved at [ /{Game_data_dir}/Calculation_{Game_name}.txt ]")

# ================================================================================================ #
# plots [ /Calculation_Game_name.txt ] using matplotlib.pyplot
from pandas import DataFrame
from numpy import ndarray

def plot_eff(Game_name : str, values=False) -> list and DataFrame and ndarray: 
    """Plots package efficency of [ Game_name ], using matplotlib.pyplot
    - plots [ /Game_pacakge_data/Game_name/Calculation_Game_name.txt ]

    This function returns 2 or 3 objects --> list, pd.DataFrame, np.ndarray

    Args:
        Game_name (str): name of game.
        values (bool, optional): True to return ndarray of efficency values [use .values method]. Defaults to False.

    Returns:
        list : max efficency [package name, package index]
        DataFrame : pd.DataFrame [ /Game_name/Calculation_Game_name.txt ]
        ndarray : values of [ /Game_name/Calculation_Game_name.txt ]
    """
    import os
    import matplotlib.pyplot as plt
    
    gamd_data_dir = return_data_dir(Game_name=Game_name)
    calc_data_dir = gamd_data_dir + "/Calculation_" + Game_name + ".txt"
    if not os.path.isfile(calc_data_dir) : 
        print(f"[{Game_name}]'s calculation data doesn't exist. Use create_data_dir or save calculation etc...")
        return
    
    calc_data = read_csv(calc_data_dir)
    
    max_eff = calc_data["value_per_price"].argmax()
    
    plt.bar(range(len(calc_data)), calc_data["value_per_price"], alpha=0.85, width=0.5)
    plt.plot(calc_data["value_per_price"], 'o', color='g')
    plt.plot(calc_data["value_per_price"], color='g')
    plt.xticks(range(len(calc_data)), labels=calc_data['Package_name'])
    plt.plot([max_eff], calc_data["value_per_price"][max_eff], 'o', color='r',
             label="Max_eff : {} --> {}".format(calc_data["Package_name"][max_eff], calc_data["value_per_price"][max_eff]))
    
    plt.title("Value per price of [ {} ]".format(Game_name))
    plt.legend(prop={'size':12}).set_alpha(1)
    plt.tight_layout()
    plt.show()

    if values : 
        return [calc_data["Package_name"][max_eff], max_eff], calc_data, calc_data.values
    else : 
        return [calc_data["Package_name"][max_eff], max_eff], calc_data

# ================================================================================================ #
# check the game list in [ ./Data/Game_list.txt ]
def check_game_list() -> list: 
    """Check the game list in [ ./Data/Game_list.txt ] and return as a list.

    Returns:
        list : list of game names in [ ./Data/Game_list.txt ]
    """
    try : 
        game_list = read_csv("Data/Game_list.txt")
    except : 
        print("There is no game in directory.")
        return
    
    game_list = game_list.drop(["Null"], axis=1)
    print(f"Currently, there are {len(game_list.keys())} game in directory")
    print("------------------------------------------------------------------")

    game_name_list = []
    for index in range(0, len(game_list.keys())) : 
        game_name_list.append(game_list.keys()[index])
        print(f"\t--> {game_list.keys()[index]}")
    
    print("------------------------------------------------------------------")
    print()

    return game_name_list

# ================================================================================================ #
# print the status of [ ./Data/Game_list.txt ] 
def serach_game() -> bool and list and list: 
    """Print the status of [ ./Data/Game_list.txt ]

    Returns:
        bool : whether the directories or file is valid.
        list_1 : list of unvalid game names, which doesn't exist in [ ./Data/Game_list.txt ].
        list_2 : list of unvalid data directories, which exist in [ ./Data/Game_package_data/Game_name ].
    """
    import os
    
    print("==================================================================")
    print("Searching...")
    valid = True

    game_dataframe = read_csv("Data/Game_list.txt")
    game_dataframe = game_dataframe.drop(["Null"], axis=1)

    num_game = len(game_dataframe.keys())                   # number of games in Game_list.txt
    game_name_list = list(game_dataframe.keys())            # name of gmaes in Game_list.txt
    game_dir_list = game_dataframe.values.ravel().tolist()  # directories in Game_list.txt

    print("------------------------------------------------------------------")
    print(f"Number of games in [ ./Data/Game_list.txt ] --> {num_game}")
    print("------------------------------------------------------------------")
    print("List of game directories in [ ./Data/Game_list.txt ]")

    for index, name in enumerate(game_name_list) : 
        print(f"[{name}]")
        print(f"\t--> [ ./{game_dataframe.values[0][index]} ]")
        print()
    print("------------------------------------------------------------------")
    
    pacakge_data_dir = "Data/Game_package_data"

    dir_unvalid_list = []
    file_unvalid_list = []

    print("Direcotires in [ ./Data/Game_package_data ]")
    print("------------------------------------------------------------------")
    for name in os.listdir(pacakge_data_dir) : 
        print(f"[{name}]", end=" ")
        
        if name not in game_name_list : 
            print("==> NOTE : [Dosen't exist in [ ./Data/Game_list.txt ]]", end="")
            valid = False
            dir_unvalid_list.append(name)
        print()

        data_dir = pacakge_data_dir + "/" + name

        if not len(os.listdir(data_dir)) : 
            print("\t==> NOTE : [Data doesn't exist properly. Data is missing]")
            valid = False
            file_unvalid_list.append(data_dir)
        
        else : 
            for file in os.listdir(data_dir) : 
                
                if ("Calculation" not in file and "Package_data" not in file) or len(os.listdir(data_dir)) != 2 : 
                    print("\t==> NOTE : [Data doesn't exist properly]")
                    valid = False
                    file_unvalid_list.append(data_dir)
                
                print(f"\t--> [{file}]")
        
        print()
    print("------------------------------------------------------------------")
    
    if not valid : 
        
        if dir_unvalid_list : 
            print("There's mismatch between [ ./Data/Game_list.txt ] and data directories.")
            print("In [ ./Data/Game_list.txt ], there's no game named as...")
            for name in dir_unvalid_list : 
                print(f"\t--> [{name}]")
            print()

        if file_unvalid_list : 
            print("In data directory, data is somewhere missing.")
            print("In [ ./Data/Game_package_data/[Game_name] ] directories, there should be file named as... \n[ Calculation_Game_name.txt, Package_data_Game_name.txt ]")
            print()

            for data_dir in file_unvalid_list : 
                print(f"\t==> In [ ./{data_dir} ] ...")
                
                if not len(os.listdir(data_dir)) : 
                    print("\t\t--> There's no data in directory.")
                
                else : 
                    for data in os.listdir(data_dir) : 
                        print(f"\t\t--> [ {data} ] exist.")
                
                print()
        
        print("------------------------------------------------------------------")

        return valid, dir_unvalid_list, file_unvalid_list

    return valid, None, None

# ================================================================================================ #
# search data directories via recursion and print if .txt file has chosen
def recursive_search(Current_dir : str, Depth : int, Parent_dir=None) -> None: 
    """Search [ ./Data ] and its sub directories.

    If you choose .txt file like [ Game_list.txt, Calculation_Game_name.txt etc... ], it will print the string inside of it.

    If it's empty, prints nothing.

    If Parent_dir=None and choose [0] : [/Exit],
    function will return you to menu.
    
    Args:
        Current_dir (str): directory that currently in use.
        Depth (int): Depth of current directory relative to root.
        Parent_dir (str, optional): parent directory of Current_dir. Defaults to None.
    """
    import os
    
    print("------------------------------------------------------------------")
    print(f"==> Current directory : {Current_dir}")

    is_file = [None]
    sub_dir_list = [None]
    sub_dir_name_list = [None]
    index_count = 0

    print("\t"*Depth, f"--> [0] : [/Exit]")
    for sub_dir in os.listdir(Current_dir) : 
        index_count += 1
        
        if ".txt" in sub_dir : 
            is_file.append(True)
        else : 
            is_file.append(None)
        
        sub_dir_name_list.append(sub_dir)
        sub_dir_list.append(
            os.path.join(Current_dir, sub_dir)
        )
        print("\t"*Depth, f"--> [{index_count}] : {sub_dir}")

    print()
    print("Waiting user input : ", end="")
    try : 
        user_input = input()
        user_input = int(user_input)
        print(user_input)
        print()
    
    except : 
        print(f"Your input is incompatible to {type(int())}. --> [{user_input}]")
        print("Please check your input.")
        print()
        return recursive_search(Current_dir=Current_dir, Parent_dir=Parent_dir, Depth=Depth)


    if not (user_input in list(range(0, index_count + 1))) : 
        print(f"You put wrong input. Please check the number you choosed. --> [{user_input}]")
        print()
        return recursive_search(Current_dir=Current_dir, Parent_dir=Parent_dir, Depth=Depth)
    
    elif user_input == 0 : 
        print("------------------------------------------------------------------")
        print("Going back to parent directory...")
        if Parent_dir == None : 
            print("Return to menu...")
        return
    
    else : 
        if is_file[user_input] is not None: 
            import pandas as pd
            try : 
                leaf_file = read_csv(sub_dir_list[user_input])
                print(leaf_file)
                print()
            except : 
                print("Data file is empty.")
                print("Use options like...")
                print("\t--> [2] : Manage data")
                print()

        else : 
            print("------------------------------------------------------------------")
            print("Moving to sub directory...")
            recursive_search(Current_dir=sub_dir_list[user_input], Parent_dir=Current_dir, Depth=Depth + 1)

        return recursive_search(Current_dir=Current_dir, Parent_dir=Parent_dir, Depth=Depth)

# ================================================================================================ #
# add data to [File_path] file
def add_data(File_path : str, File_type : int) -> None: 
    """Add data to [File_path] file

    Args:
        File_path (str): directory of file
        File_type (int): type of [File_path] file. More details at check_file_type(File_path : str) function.
    """
    import pandas as pd

    is_empty = False
    try : 
        data = read_csv(File_path)
    except : 
        is_empty = True
    
    if File_type == 1 :             # Game_list.txt
        print("Type name of the game : ", end="")
        game_name = str(input())
        print(game_name)
        
        if is_empty : 
            create_game_list(Game_name_list=[game_name])
        else : 
            game_data_dir = "Data/Game_package_data/" + game_name
            game_data = pd.DataFrame(data=[[game_data_dir]], columns=[game_name])
            add_game_list(Data=game_data)
        
        print(f"[{game_name}] has been updated in [ ./Data/Game_list.txt ]", end="\n\n")
        create_data_dir(Force=False, Game_name_list=None)
    
    elif File_type == 2 :           # Package_data_Game_name.txt
        if is_empty : 
            pass
        game_name = File_path.split("/")[2]
        
        print("Type package name to add : ", end="")
        package_name = str(input())
        print(package_name)
        
        try : 
            print(f"Type [{package_name}] price : ", end="")
            package_price = input()
            print(package_price)
            print(f"Type [{package_name}] value : ", end="")
            package_value = input()
            print(package_value)

            package_price = float(package_price)
            package_value = float(package_value)

        except : 
            print(f"Your input is incompatible to {type(float())}.")
            print(f"\t--> package_price : [{package_price}]")
            print(f"\t--> package_price : [{package_value}]")
            print("Please check your input.")
            print()
            return
        
        data_add = pd.DataFrame(data=[[package_name, package_price, package_value]], columns=["Package_name", "Price", "Value"])
        print()
        print("Saving package data...")
        if is_empty : 
            save_package_data(Package_dataframe=data_add, Game_name=game_name, Force=True)
        else : 
            add_package_dataframe(Package_dataframe=data_add, Game_name=game_name)
        
        gamd_data_dir = "Data/Game_package_data/" + game_name
        calc_package_eff(Game_name=game_name, Game_data_dir=gamd_data_dir, Force=True)

    else :                          # UNSUPPORTED
        print(f"[ ./{File_path} ] is not supported to operate.")
        print("Use options like...")
        print("\t--> [1] : Initialize data")
        print("\t--> [5] : Check data status")
        print()
        return

# delete data at [File_path] file
def delete_data(File_path : str, File_type : int) -> None: 
    """Delete data at [File_path] file

    Args:
        File_path (str): File_path (str): directory of file
        File_type (int): type of [File_path] file. More details at check_file_type(File_path : str) function.
    """
    import pandas as pd

    if File_type == 1 :             # Game_list.txt
        data = read_csv(File_path)
        print("Type correct game name to delete data : ", end="")
        game_name = str(input())
        print(game_name, end="\n\n")

        if not (game_name in data.keys()) : 
            print(f"There is no game named : [{game_name}]")
            print("Currently, there are games like...")
            for game in data.keys() : 
                print(f"\t--> [{game}]")
            print()
            print("Please type exact game name.", end="\n\n")
            return
        
        game_dir = return_data_dir(Game_name=game_name)
        delete_game_list(Game_name=game_name)

        import shutil
        shutil.rmtree(game_dir)

        print(f"[ ./{game_dir} ] has been deleted.")
    
    elif File_type == 2 :           # Package_data_Game_name.txt
        data = read_csv(File_path)
        game_name = File_path.split("/")[2]
        
        print("Type correct package name to delete data : ", end="")
        package_name = str(input())
        print(package_name, end="\n\n")

        if not (package_name in data["Package_name"].values) : 
            print(f"There is no package data named : [{package_name}]")
            print("Currently, there are packages named...")
            for package in data["Package_name"].values : 
                print(f"\t--> [{package}]")
            print()
            print("Please type exact package name.", end="\n\n")
            return
        
        delete_package(Game_name=game_name, Package_name=package_name)
        gamd_data_dir = "Data/Game_package_data/" + game_name
        calc_package_eff(Game_name=game_name, Game_data_dir=gamd_data_dir, Force=True)

    else :                          # UNSUPPORTED
        print(f"[ ./{File_path} ] is not supported to operate.")
        print("Use options like...")
        print("\t--> [1] : Initialize data")
        print("\t--> [5] : Check data status")
        print()
        return

# ================================================================================================ #
# check file type of [File_path]
def check_file_type(File_path : str) : 
    """Check the type of [File_path], Game_list.txt, Calculation_Game_name.txt, Package_data_Game_name.txt

    Args:
        File_path (str): directory of file

    Returns:
        - 1, 2, False
        - Gmae_list.txt
        - Package_data_Game_name.txt
        - UNSUPPORTED
    """
    if "Game_list.txt" in File_path : 
        return 1
    elif "Package_data" in File_path : 
        return 2
    return False

# ================================================================================================ #
# excute specific operation to [File_path] file
def manage_data(File_path : str) : 
    """Excute specific operation to [File_path] file

    Args:
        File_path (str): directory of file

    """
    is_empty = False
    try : 
        data = read_csv(File_path)
        print("Revealing data in file...")
        print("------------------------------------------------------------------")
    except : 
        is_empty = True

    if not is_empty : 
        if "Null" in data.keys() : 
            for game in data.drop(["Null"], axis=1).keys() : 
                print(game, end=" ")
                print(f"--> [ ./{data[game][0]} ]")
        else : 
            print(data)
    else : 
        print("Data file is empty.")

    print("------------------------------------------------------------------")
    print("Choose operation")
    print("[0] : Cancle")
    print("[1] : Add new data")
    print("[2] : Delete some data", end="\n\n")

    if is_empty : 
        print("==> Since data file is empty, you can use only option [0] and [1]", end="\n\n")
    
    print("Operation input : ", end="")
    oper_input = input()
    print(oper_input)
    print("------------------------------------------------------------------")

    try : 
        oper_input = int(oper_input)
        if not (oper_input in [0, 1, 2]) : 
            raise IndexError
        if is_empty and (not (oper_input in [0, 1])) : 
            raise IndexError
    except IndexError : 
        print(f"You put wrong input. Please check the number you choosed. --> [{oper_input}]")
        print()
        return 
    except : 
        print(f"Your input is incompatible to {type(int())}. --> [{oper_input}]")
        print("Please check your input.")
        print()
        return 
    
    if oper_input == 0 : 
        print("Canceling operation...")
        return

    print(f"Current file is [ ./{File_path} ]")
    file_type = check_file_type(File_path=File_path)
    if is_empty : 
        add_data(File_path=File_path, File_type=file_type)
    
    else : 
        if oper_input == 1 : 
            add_data(File_path=File_path, File_type=file_type)

        elif oper_input == 2 : 
            delete_data(File_path=File_path, File_type=file_type)

    return

# ================================================================================================ #
# search data directories via recursion and modify if .txt file has chosen
def recursive_modify(Current_dir : str, Depth : int, Parent_dir=None) -> None: 
    """Search [ ./Data ] and its sub directories.

    If you choose .txt file like [ Game_list.txt, Calculation_Game_name.txt etc... ], it will excute manage_data(File_path : str) function to modify data.

    If Parent_dir=None and choose [0] : [/Exit],
    function will return you to menu.
    
    Args:
        Current_dir (str): directory that currently in use.
        Depth (int): Depth of current directory relative to root.
        Parent_dir (str, optional): parent directory of Current_dir. Defaults to None.
    """
    import os
    
    print("------------------------------------------------------------------")
    print(f"==> Current directory : {Current_dir}")

    is_file = [None]
    sub_dir_list = [None]
    sub_dir_name_list = [None]
    index_count = 0

    print("\t"*Depth, f"--> [0] : [/Exit]")
    for sub_dir in os.listdir(Current_dir) : 
        index_count += 1
        
        if ".txt" in sub_dir : 
            is_file.append(True)
        else : 
            is_file.append(None)
        
        sub_dir_name_list.append(sub_dir)
        sub_dir_list.append(
            os.path.join(Current_dir, sub_dir)
        )
        print("\t"*Depth, f"--> [{index_count}] : {sub_dir}")

    print()
    print("Waiting user input : ", end="")
    try : 
        user_input = input()
        print(user_input)
        user_input = int(user_input)
        print()
    
    except : 
        print(f"Your input is incompatible to {type(int())}. --> [{user_input}]")
        print("Please check your input.")
        print()
        return recursive_modify(Current_dir=Current_dir, Parent_dir=Parent_dir, Depth=Depth)


    if not (user_input in list(range(0, index_count + 1))) : 
        print(f"You put wrong input. Please check the number you choosed. --> [{user_input}]")
        print()
        return recursive_modify(Current_dir=Current_dir, Parent_dir=Parent_dir, Depth=Depth)
    
    elif user_input == 0 : 
        print("------------------------------------------------------------------")
        print("Going back to parent directory...")
        if Parent_dir == None : 
            print("Return to menu...")
        return
    
    else : 
        if is_file[user_input] is not None: 
            print("------------------------------------------------------------------")
            print("Managing data...")
            manage_data(File_path=sub_dir_list[user_input])

        else : 
            print("------------------------------------------------------------------")
            print("Moving to sub directory...")
            recursive_modify(Current_dir=sub_dir_list[user_input], Parent_dir=Current_dir, Depth=Depth + 1)

        return recursive_modify(Current_dir=Current_dir, Parent_dir=Parent_dir, Depth=Depth)

# ================================================================================================ #
