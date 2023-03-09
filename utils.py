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
        Data (DataFrame) : _description_
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

# Deletes [ ./Data/Game_list.txt ] and creates new one
def delete_game_list() -> None: 
    """Deletes [ ./Data/Game_list.txt ] and creates new one.
    """
    import os
    import pandas as pd
    
    game_list_dir = "Data/Game_list.txt"
    
    if not os.path.isfile(game_list_dir) : 
        print("Game_list.txt doesn't exist.")
    
    else : 
        os.remove(game_list_dir)
        save_csv(pd.DataFrame(data=[0], columns=["Null"]), game_list_dir)
        print("Game_list.txt has been deleted and created.")

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
    print(f"[{Game_name}] package data has been created.")

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
    
    del_index = package_data.index[package_data['name'] == Package_name]
    
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

        if not Game_name_list and Game_name_list is not None: 
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
        return calc_data["Package_name"][max_eff], calc_data

# ================================================================================================ #
# check the game list in [ ./Data/Game_list.txt ]
def check_game_list() -> None: 
    """Check the game list in [ ./Data/Game_list.txt ]
    """
    game_list = read_csv("Data/Game_list.txt")
    game_list = game_list.drop(["Null"], axis=1)
    print()
    print(f"Currently, there are {len(game_list.keys())} game in directory --> ")
    print("---------------------------------")
    for index in range(0, len(game_list.keys())) : 
        print(game_list.keys()[index])
    print("---------------------------------")
    print()

# ================================================================================================ #
# print the status of [ ./Data/Game_list.txt ] 
def serach_game() -> int and list and list: 
    """Print the status of [ ./Data/Game_list.txt ]

    Returns:
        int : number of games in [ ./Data/Game_list.txt ]
        list_1 : list of game names in [ ./Data/Game_list.txt ]
        list_2 : list of game directory in [ ./Data/Game_list.txt ]
    """
    import os

    print("------------------------------------------------------------------")
    print("Searching...")
    
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

    print("Direcotires in [ ./Data/Game_package_data ]")
    print("------------------------------------------------------------------")
    for name in os.listdir(pacakge_data_dir) : 
        print(f"[{name}]")
        data_dir = pacakge_data_dir + "/" + name
        for file in os.listdir(data_dir) : 
            print(f"\t--> [{file}]")
        print()
    print("------------------------------------------------------------------")

    return num_game, game_name_list, game_dir_list

# ================================================================================================ #


# ================================================================================================ #


# ================================================================================================ #