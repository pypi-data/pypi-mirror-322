import argparse
from pathlib import Path


def virvar(path: str, **kwargs: str) -> None:
    """virvar.

    Mofifies the `activate` script of a virtual environment to add environment variables.

    Args:
        path (str): The path to the virtual environment directory.
        kwargs (dict): Arbitrary keyword arguments representig the 
                    environment variables to add.

    Returns:
        None:

    Description:
        This function takes the path to a virtual environment (created with `venv`) and a list of
         environment variables as key-value pairs. It adds these variables to the `activate` script
         of the virtual environment, so they are set when the environment is activated and unset
         when the environment is deactivated.

    Usage:
        >>> virvar("venv", DEBUG="TRUE", COEF=2.56, INT=5)
        Environment validated: Unix-like virtual environment detected, and environment variables successfully configured.

        This adds the following lines to the `activate` script:
        # Self destruct!
        unset DEBUG
        unset COEF
        unset INT

        # set environment variables
        export DEBUG="TRUE"
        export COEF=2.56
        export INT=5
    """

    # Unset variables after this
    start_unset = "# Self destruct!"
    
    # build the path
    # Path for POSIX-compliant systems (e.g., Linux, macOS, BSD)
    bin_path_unix = Path(path) / "bin" / "activate"
    #  Path for WINDOWS-compliant systems 
    bin_path_windows = Path(path) / "Scripts" / "activate"

    if bin_path_unix.exists():
        bin_path = bin_path_unix
        print("Environment validated: Unix-like virtual environment detected, and environment variables successfully configured.")
    elif bin_path_windows.exists():
        bin_path = bin_path_windows
        print("Environment validated: Windows-like virtual environment detected, and environment variables successfully configured.")
    else:
        print("Error: Virtual environment not found. Unable to configure environment variables. Please ensure the specified path is correct.")
        raise FileNotFoundError("No such file or directory")


    # Build the export and the unset variables list
    export = "\n#set environment variables\n"
    unset = "\n        #unset environment variable\n"
    for key, value in kwargs.items():
        if isinstance(value, str):
            export += f'export {key.upper()}="{value}"\n'
        else:
            export += f'export {key.upper()}={value}\n'

        unset += f"        unset {key.upper()}\n"

    with bin_path.open("r") as file:
        lines = file.readlines()

    with bin_path.open("w") as file:
        for line in lines:
            file.write(line)
            if start_unset in line:
                file.write(unset + "\n")
                break
        remaining_lines = lines[lines.index(line) + 1:]
        file.writelines(remaining_lines)
        file.write(export)


def main():
    # Create parser
    parser = argparse.ArgumentParser()

    # Add arguments to the parser
    parser.add_argument(
        "path",
        help="Path to the virtual environment created with venv python command",
    )
    parser.add_argument(
            "env_var",
            nargs="+", # Accepts one or more pairs key = "value"
            help='Environment variables in the format KEY="value"'
            )

    #Parse the arguments
    args = parser.parse_args()

    # Transforms pairs key=value into a dictionary
    env_var = dict(arg.split("=", 1) for arg in args.env_var)

    virvar(args.path, **env_var)


if __name__=="__main__":
    main()
