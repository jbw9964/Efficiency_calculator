
import os
import pandas as pd
import numpy as np
from pandas import DataFrame

# ================================================================================================ #
def return_data_dir(Game_name) : 
    """Returns [Game_name]'s data directory.
    
    - Data - Game_package_data - Game_name

    Args:
        Game_name (str): name of game.

    Returns:
        str : Data - Game_package_data - Game_name
    """
    return pd.read_csv("Data\Game_list.txt", sep=",", encoding="UTF8")[Game_name].values[0]

# ================================================================================================ #
def add_newgame_dir(Data_dir, Game_name) : 
    """Only creates new game directory and saves to Game_list.txt
    
    If some game's package data directory is already exist, function do nothing.

    Creates : 
    - Current directory
        - Data
            - Game_package_data
                - Game_name
    
    Args:
        Data_dir (str): relative or absolute directory of "Data".
        Game_name (str): name of game.
    """
    game_path = Data_dir + "\Game_package_data"
    
    game_list = pd.read_csv(Data_dir + "\Game_list.txt", sep=",", encoding="UTF8")
    
    if Game_name in os.listdir(game_path) : 
        print(f"{Game_name}'s data looks like already exist at {game_path}")
        print(os.listdir(game_path))
        return
    
    game_dir = game_path + "\\" + Game_name
    os.mkdir(game_dir)
    
    if Game_name in game_list.keys() : 
        game_list = game_list.drop([Game_name], axis=1)
    
    game_list = pd.concat([game_list, 
                           pd.Series(data=game_dir, name=Game_name)
                           ], axis=1)
    
    game_list.to_csv(Data_dir + "\Game_list.txt", sep=",", encoding="UTF8", index=False)
    print(f"({Game_name}) data directory has been created.")

# ================================================================================================ #
def save_calculation(Calc_dataframe : DataFrame, Game_name, Force=False) : 
    """Save package's calculation
    
    Directory : 
    - Data
        - Game_package_data
            - Game_name
                - Calculation_Game_name.txt

    Args:
        Calc_dataframe (DataFrame): calculated DataFrame.
        Game_name (str): name of game.
        Force (bool, optional) : whether force to save data though already exist. Defaults to False.
    """
    
    game_dir = return_data_dir(Game_name)
    
    if type(Calc_dataframe) != type(DataFrame()) : 
        print(f"Args Calc_dataframe must be dataframe. --> [ Calc_dataframe : {type(Calc_dataframe)} ]")
        return
    
    game_dir = game_dir + "\Calculation_" + Game_name + ".txt"
    
    if os.path.isfile(game_dir) : 
        print(f"{Game_name}'s data looks like already exist at {game_dir}")
        if not Force :
            return
        print("Forcing save data...")
    
    Calc_dataframe.to_csv(game_dir, sep=",", encoding="UTF8", index=False)
    print(f"({Game_name}) data has been saved.")

# ================================================================================================ #
def save_package_data(Package_dataframe : DataFrame, Game_name, Force=False) : 
    """Save package data

    Args:
        Package_dataframe (DataFrame): package data.
        Game_name (str): name of game.
        Force (bool, optional):whether force to save data though already exist. Defaults to False.
    """
    game_dir = return_data_dir(Game_name=Game_name)
    
    if type(Package_dataframe) != type(DataFrame()) : 
        print(f"Args Package_dataframe must be dataframe. --> [ Package_dataframe : {type(Package_dataframe)} ]")
        return
    
    game_dir = game_dir + "\Package_data.txt"
    
    if os.path.isfile(game_dir) : 
        print(f"{Game_name}'s data looks like already exist at {game_dir}")
        if not Force :
            return
        print("Forcing save data...")
    
    Package_dataframe.to_csv(game_dir, sep=",", encoding="UTF8", index=False)
    print(f"({Game_name}) data has been saved.")

# ================================================================================================ #
def read_csv(filepath) : 
    return pd.read_csv(filepath, sep=",", encoding="UTF8")
def save_csv(filepath, Data : DataFrame) : 
    return Data.to_csv(filepath, sep=",", encoding="UTF8", index=False)




# ================================================================================================ #