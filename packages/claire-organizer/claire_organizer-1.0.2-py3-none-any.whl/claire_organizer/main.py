from sys import platform
from os import system, path, makedirs, listdir, walk
from typing import Union
import tkinter, tkinter.filedialog, json, shutil

def check_config(config_path: str, def_config: dict) -> None:
    """
    Check if config is valid or not, reset the config to default if the config file is not valid, create a new config file if missing
    """
    try:
        with open(config_path) as temp:
            temp.read()
    except FileNotFoundError:
        with open(config_path, "w") as temp:
            json.dump(def_config, temp, ensure_ascii = False, indent = 4)

    with open(config_path) as temp:
        return json.load(temp)

def write_config_to_file(config_path: str, config: dict, def_config: dict) -> None:
    """
    Self-explanatory
    """
    try:
        with open(config_path, "w") as temp:
            json.dump(config, temp, ensure_ascii = False, indent = 4)
    except FileNotFoundError:
        try: makedirs(path.expanduser("~") + r"\claire_config")
        except:...
        check_config(config_path, def_config)
        write_config_to_file(config_path, config)

def check(arg1: str, arg2: str) -> bool:
    """
    Check if any of arg1's element exist in arg2, use to determine if a file name is illegal or not
    """
    for k in arg1:
        if k in arg2:
            return True
    return False

def check_extension(extension: str, config: dict):
    """
    Check if a certain extension is already in config
    """
    for k in config.keys():
        if extension in config[k]:
            return True
    return False

def clear() -> None:
    """
    Clear the terminal
    """
    if platform == "win32":
        system("cls")
    else:
        system("clear")

def menu(config: Union[dict, list]) -> str:
    """
    Generate the option in a menu
    """
    if isinstance(config, dict):
        temp = [x for x in config.keys()]
    else:
        temp = config
    output = ""
    for i in range(1, len(config) + 1):
        output += f"{i}. {temp[i - 1]}."
        if i < len(config):
            output += "\n"
    return output

def file_sorter(folder_path: str, config: dict):
    """
    Generate folders and sort files
    """
    for folder_name in config.keys():
        try: makedirs(fr"{folder_path}\{folder_name}")
        except:...
    try: makedirs(fr"{folder_path}\Others")
    except:...

    for root, dirs, files in walk(folder_path):
        if not dirs:
            break
        for name in dirs:
            for x in listdir(fr"{folder_path}\{name}"):
                try: shutil.move(fr"{folder_path}\{name}\{x}", folder_path)
                except:...
    
    for root, dirs, files in walk(folder_path):
        if not files:
            break
        for name in files:
            temp = ""
            for i in reversed(name):
                temp += i
                if i == ".":
                    temp = temp[::-1]
                    break
            for i in config.keys():
                if temp in config[i]:
                    try: shutil.move(fr"{folder_path}\{name}", fr"{folder_path}\{i}")
                    except:...
                    break
    
    for root, dirs, files in walk(folder_path):
        if not files:
            break
        for i in files:
            try: shutil.move(fr"{folder_path}\{i}", fr"{folder_path}\Others")
            except:...

def main() -> None:
    """
    The main function
    """
    try: makedirs(path.expanduser("~") + r"\claire_config")
    except:...
    config_path = path.expanduser("~") + r"\claire_config\config.json"
    def_config = {
        "Images": [".png", ".jpg", ".jpeg", ".webp", ".gif"],
        "Videos": [".mp4", ".avi", ".webm", ".mkv", ".flv"],
        "Documents": [".doc", ".docx", ".pdf", ".txt"],
        "Sounds": [".mp3", ".wav", ".m4a"],
        "Archives": [".zip", ".rar"],
        "Executables": [".exe"]
    }
    config = check_config(config_path, def_config)

    root = tkinter.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    clear()
    while True:
        cmd = input("1. Choose a folder to organize. \n2. Options. \n3. Exit. \nYour input: ").strip()
        clear()
        if cmd == "3":
            root.destroy()
            exit(0)
        elif not cmd:
            print("Invalid input: Empty input.  \n")
        elif cmd not in [*"12"]:
            print("Invalid input: Command does not exist. \n")
        
        while cmd == "1":
            target = tkinter.filedialog.askdirectory(title="Choose your output folder. Cancel to go back")
            if not target:
                break
            file_sorter(target, config)
            print("Sucessful. \n")
            break

        while cmd == "2":
            temp = [x for x in config.keys()]
            conf = [str(x) for x in range(1, len(temp) + 4)]

            toggle = input(f"""Configure file types in each category. 
{menu(config)}
{len(temp) + 1}. Add/Remove file category.
{len(temp) + 2}. Go back. 
{len(temp) + 3}. Reset setting to default.
Your input: """).strip()
            
            clear()
            if not toggle:
                print("Invalid input: Empty input.  \n")
                continue
            elif toggle not in conf:
                print("Invalid input: Option does not exist. \n")
                continue
            elif toggle == str(len(temp) + 2):
                break
            elif toggle == str(len(temp) + 3):
                while True:
                    confirm = input("Do you want to reset the setting to default? [Y/N]: ").strip().upper()

                    clear()
                    if confirm == "N":
                        break
                    elif confirm not in [*"YN"]:
                        print("Invalid input: Option does not exist. \n")
                        continue
                    elif not confirm:
                        print("Invalid input: Empty input. \n")
                        continue
                    with open(config_path, "w") as temp:
                        json.dump(def_config, temp, ensure_ascii = False, indent = 4)
                    config = def_config
                    break

                continue
            elif toggle == str(len(temp) + 1):
                while True:
                    mode = input("1. Add. \n2. Remove. \n3. Back. \nYour input: ").strip()

                    clear()
                    if mode == "3":
                        break
                    while mode == "1":
                        category = input(f"{menu(config)} \nYour input (Type / to go back) (Category name cannot contains \"\\/:*?\"<>|\"): ").strip()
                        
                        clear()
                        if category == "/":
                            break
                        elif check(category, [*'\\/:*?"<>|']):
                            print("Invalid input: Illegal category name (Category name cannot contains \"\\/:*?\"<>|\"). \n")
                            continue
                        elif not category:
                            print("Invalid input: Empty input.  \n")
                            continue
                        config.setdefault(category, [])
                        conf = [str(x) for x in range(1, len(temp) + 1)]
                        temp = [x for x in config.keys()]
                        write_config_to_file(config_path, config, def_config)
                    
                    while mode == "2":
                        category = input(f"Type the category you want to remove: \n{menu(config)} \n{len(temp) + 1}. Exit. \nYour input: ").strip()

                        clear()
                        if category == str(len(temp) + 1):
                            break
                        elif category not in conf:
                            print("Invalid input: Option does not exist. \n")
                            continue
                        elif not category:
                            print("Invalid input: Empty input. \n")
                            continue
                        del config[temp[int(category) - 1]]
                        conf = [str(x) for x in range(1, len(temp) + 1)]
                        temp = [x for x in config.keys()]
                        write_config_to_file(config_path, config, def_config)

                continue
            
            while True:
                index = int(toggle) - 1
                mode = input(f"""Configure file extension for {temp[index]}:
1. Append mode. 
2. Remove mode.
3. Back
Your input: """).strip()
                
                clear()
                if mode == "3":
                    break
                elif not mode:
                    print("Invalid input: Empty input.  \n")
                    continue
                elif mode not in [*"12"]:
                    print("Invalid input: Option does not exist. \n")
                    continue

                while mode == "1":
                    option = config[temp[index]]
                    if len(option) > 0:
                        opt = input(f"""Type the file extension you want to add to the \"{temp[index]}\" list of extension:
{menu(option)}
Your input (Preceed the extension with a ".") (Type / to go back): """).strip()
                    else:
                        opt = input(f"""Type the file extension you want to add to the \"{temp[index]}\" list of extension:
Your input (Preceed the extension with a ".") (Type / to go back): """).strip()
                        
                    clear()
                    if len(opt) > 1 and opt[0] == "." and not check_extension(opt, config):
                        option.append(opt)
                        write_config_to_file(config_path, config, def_config)
                    elif opt == "/":
                        break
                    elif check_extension(opt, config):
                        print("Invalid input: Extension already exist in other category. \n")
                    elif not opt:
                        print("Invalid input: Empty input. \n")
                    else:
                        print("Invalid input: Not a valid extension. \n")
                
                while mode == "2":
                    temp2 = [str(x) for x in range(1, len(option) + 1)]
                    if len(option) > 0:
                        opt = input(f"""Type the extension you want to remove from the \"{temp[index]}\" list of extension:
{menu(option)}
{len(option) + 1}. Go back.
Your input: """).strip()
                    else:
                        opt = input(f"""Type the extension you want to remove from the \"{temp[index]}\" list of extension:
{len(option) + 1}. Go back.
Your input: """).strip()

                    clear()
                    if int(opt) == len(option) + 1:
                        break
                    elif not opt:
                        print("Invalid input: Empty input. \n")
                        continue
                    elif opt not in temp2:
                        print("Invalid input: Not a valid extension. \n")
                        continue
                    del option[int(opt) - 1]
                    write_config_to_file(config_path, config, def_config)

if __name__ == "__main__":
    main()