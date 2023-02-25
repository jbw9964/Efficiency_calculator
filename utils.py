
import os
import pandas as pd
import numpy as np
from pandas import DataFrame

# ================================================================================================ #
# read or save csv as UTF8 encoding and index=False
def read_csv(filepath : str) : 
    """Read csv file as UTF8 encoding.

    Args:
        filepath (str) : directory of csv file.

    Returns:
        pd.read_csv(filepath, sep=",", encoding="UTF8")
    """
    return pd.read_csv(filepath, sep=",", encoding="UTF8")
def save_csv(Data : DataFrame, filepath : str) : 
    """Save csv file as UTF8 encoding.

    Args:
        Data (DataFrame) : data build by DataFrame
        filepath (str) : directory of csv file

    Returns:
        Data.to_csv(filepath, sep=",", encoding="UTF8", index=False)
    """
    return Data.to_csv(filepath, sep=",", encoding="UTF8", index=False)

# ================================================================================================ #
# return [Data - Game_package_data - Game_name] directory
def return_data_dir(Game_name : str) -> str: 
    """Returns [Game_name]'s data directory.
    
    - Data - Game_package_data - Game_name

    Args:
        Game_name (str) : name of game

    Returns:
        pd.read_csv("Data/Game_list.txt", sep=",", encoding="UTF8")[Game_name].values[0] 
            --> Data - Game_package_data - Game_name
    """
    return pd.read_csv("Data/Game_list.txt", sep=",", encoding="UTF8")[Game_name].values[0]

# ================================================================================================ #
# creates [ /Data/Game_package_data/Game_name ] : creates only one directory
def add_game_data_dir(Data_dir : str, Game_name : str) -> None: 
    """Only creates new game directory and saves to Game_list.txt
    
    If some game's package data directory is already exist, function do nothing.

    Creates : 
    - Current directory
        - Data
            - Game_package_data
                - Game_name
    
    Args:
        Data_dir (str) : [ /Data ]
        Game_name (str) : name of game
    """
    
    dir_package_data = Data_dir + "/Game_package_data"
    
    game_list = read_csv(Data_dir + "/Game_list.txt")
    
    if Game_name in os.listdir(dir_package_data) : 
        print(f"{Game_name}'s data looks like already exist at {dir_package_data}")
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
# save input DataFrame to [ /Data/Game_package_data/Game_name/Calculation_Game_name.txt ]
def save_calculation(Calc_dataframe : DataFrame, Game_name : str, Force=False) -> None: 
    """Save pacakge's calculation
    
    Directory : 
    - Data
        - Game_package_data
            - Game_name
                - Calculation_Game_name.txt

    Args:
        Calc_dataframe (DataFrame) : calculated DataFrame
        Game_name (str) : name of game
        Force (bool) : force to save data though already exist
    """
    
    game_dir = return_data_dir(Game_name)
    
    if type(Calc_dataframe) != type(DataFrame()) : 
        print(f"Args Calc_dataframe must be dataframe. --> [ Calc_dataframe : {type(Calc_dataframe)} ]")
        return
    
    game_dir = game_dir + "/Calculation_" + Game_name + ".txt"
    
    if os.path.isfile(game_dir) : 
        print(f"{Game_name}'s data looks like already exist at {game_dir}")
        if not Force :
            return
        print("Forcing to save data...")
    
    save_csv(Data=Calc_dataframe, filepath=game_dir)
    print(f"[{Game_name}] calculation data has been saved.")

# ================================================================================================ #
# save input DataFrame to [ /Data/Game_package_data/Game_name/Package_data.txt ]
def save_package_data(Package_dataframe : DataFrame, Game_name : str, Force=False) -> None: 
    """Save package data.

    Args:
        Package_dataframe (DataFrame) : package data.
        Game_name (str) : name of game.
        Force (bool, optional) : force to save data though already exist. Defaults to False.
    """
    
    game_dir = return_data_dir(Game_name=Game_name)
    
    if type(Package_dataframe) != type(DataFrame()) : 
        print(f"Args Package_dataframe must be dataframe. --> [ Package_dataframe : {type(Package_dataframe)} ]")
        return
    
    game_dir = game_dir + "/Package_data.txt"
    
    if os.path.isfile(game_dir) : 
        print(f"{Game_name}'s data looks like already exist at {game_dir}")
        if not Force :
            return
        print("Forcing to save data...")
    
    save_csv(Data=Package_dataframe, filepath=game_dir)
    print(f"[{Game_name}] package data has been saved.")

# ================================================================================================ #
# add input DataFrame with [ /Data/Game_package_data/Game_name/Package_data.txt ]
def add_package_dataframe(Package_dataframe : DataFrame, Game_name : str) -> None: 
    """Add package data.

    Args:
        Package_dataframe (DataFrame): package data.
        Game_name (str): name of game.
    """
    
    game_dir = return_data_dir(Game_name=Game_name)
    
    package_dir = game_dir + "/Package_data.txt"
    
    prev_data = read_csv(package_dir).values
    new_data = Package_dataframe.values
    
    data_stack = np.vstack((prev_data, new_data))
    current_data = pd.DataFrame(data=data_stack, columns=Package_dataframe.keys())
    
    save_csv(current_data, package_dir)
    print(f"[{Game_name}] package data has been created.")

# ================================================================================================ #
# delete input package data in [ /Data/Game_package_data/Game_name/Package_data.txt ]
def delete_package(Game_name : str, Package_name : str, Force=False) : 
    """Delete specific package.

    Args:
        Game_name (str): name of game.
        Package_name (str): name of package.
        Force (bool, optional): force to delete every data. Defaults to False.
    """
    game_dir = return_data_dir(Game_name=Game_name)
    
    package_dir = game_dir + "/Package_data.txt"
    
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
# need to add docstring

# add input DataFrame in [ /Data/Game_list.txt ]
def add_game_list(Data : DataFrame) -> None: 
    
    if type(Data) != type(pd.DataFrame()) : 
        print(f"Args Data must be dataframe. --> [ Data : {type(Data)} ]")
        return
    
    prev = read_csv("Data/Game_list.txt")
    current = pd.concat([prev, Data], axis=1)
    save_csv(current, "Data/Game_list.txt")

# ================================================================================================ #
# need to add docstring

# creates every essential game directories
# if there is something in Game_name_list, creates directory including it.
# if Game_name_list is None, creates directories by [ /Data/Game_list.txt ]
# if Force=True, deletes every directories and make new one
def create_data_dir(Force=False, Game_name_list=False) -> None: 
    
    game_list = True

    if Force : 
        if not Game_name_list : 
            print("Game_name_list must be considered when forcing to make directory")
            print(f"Please input iterable object likewise List --> [ Gmae_name_list : {type(Game_name_list)}]")
            return
        
        import shutil
        print("Forcing to make new directories...")
        print("--> [ /Data, /Data/Game_list.txt, /Data/Game_package_data ]")
        
        shutil.rmtree("Data")
        os.makedirs("Data", exist_ok=True)
        print("[/Data] directory has been made.")

        game_dir_list = ["Data/Game_package_data/" + name for name in Game_name_list]
        save_csv(Data=pd.concat([
            pd.DataFrame(data=[0], columns=["Null"]), 
            pd.DataFrame(data=[game_dir_list], columns=Game_name_list)], 
            axis=1
            ),
            filepath="Data/Game_list.txt"
        )
        print("[/Data/Game_list.txt] directory has been made.")

        os.makedirs("Data/Game_package_data", exist_ok=True)
        print("[/Data/Game_package_data] directory has been made.")

        print()
        for name in Game_name_list : 
            add_game_data_dir("Data", name)
            save_calculation(pd.DataFrame(), Game_name=name)
            save_package_data(pd.DataFrame(), Game_name=name)
            print()
        return
    
    else : 
        if not os.path.isdir("Data") : 
            print("Directory [ /Data ] doesn't exist. Create new one.")
            os.mkdir("Data")
        else : 
            print("[/Data] directory already exist.")
        
        if not os.path.isfile("Data/Game_list.txt") : 
            print("Directory [ /Data/Game_list.txt ] doesn't exist. Create new one.")
            save_csv(pd.DataFrame(data=[0], columns=["Null"]), "Data/Game_list.txt")
            game_list = False
        else : 
            print("[/Data/Game_list.txt] directory already exist.")
        
        if not os.path.isdir("Data/Game_package_data") : 
            print("Directory [ /Data/Game_package_data ] doesn't exist. Create new one.")
            os.mkdir("Data/Game_package_data")
        else : 
            print("[/Data/Game_package_data] directory already exist.")

        if not Game_name_list : 
            return
    
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


# ================================================================================================ #


# ================================================================================================ #


# ================================================================================================ #


# ================================================================================================ #


# ================================================================================================ #


# ================================================================================================ #