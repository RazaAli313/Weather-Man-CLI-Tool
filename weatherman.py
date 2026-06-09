import sys
from weatherman.loader import load_directory
from time import sleep


def main() -> None:
    """
    Main Entry Point Function to call loaders to load the concerned data
    of the user as per passed user's command line arguments.
    
    Usage: weatherman.py /path/to/files-dir -e 2002
           weatherman.py /path/to/files-dir -a 2005/6
           weatherman.py /path/to/files-dir -c 2011/3
           weatherman.py /path/to/files-dir -c 2011/03 -a 2011/3 -e 2011
    """
    if len(sys.argv) < 4:
        print("Error: Minimum required arguments length is 4")
        print("Valid Request Format Examples:")
        print("  weatherman.py /path/to/files-dir -e 2002")
        print("  weatherman.py /path/to/files-dir -a 2005/6")
        print("  weatherman.py /path/to/files-dir -c 2011/3")
        print("  weatherman.py /path/to/files-dir -c 2011/03 -a 2011/3 -e 2011")
        return

    directory_path = sys.argv[1]
    argument_types = []
    timelines = []

    # Parse command-line arguments in pairs: -flag value
    for i in range(2, len(sys.argv)):
        if sys.argv[i].startswith('-') and i % 2 == 0:
            argument_types.append(sys.argv[i])
            if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith('-'):
                timelines.append(sys.argv[i + 1])
            else:
                print(f"Error: Flag {sys.argv[i]} requires a value")
                return

    if len(argument_types) == 0 or len(timelines) == 0:
        print("Error: No valid flag-value pairs found")
        return

    try:
        load_directory(directory_path, argument_types, timelines)
    except Exception as e:
        print(f"Error loading files: {e}")
        print("Ensure the directory path is correct and readable.")


if __name__ == "__main__":
    # Welcome message with animation
    for i in range(14):
        print("-", end="", flush=True)
        sleep(0.06)

    welcome_sentence = "Welcome to Weather Man CLI Tool"
    for word in welcome_sentence:
        print(word, end="", flush=True)
        sleep(0.06)

    for i in range(14):
        print("-", end="", flush=True)
        sleep(0.06)

    print("\n\n")
    sleep(1)

    main()
    print("--------------------------------------\n\n")
