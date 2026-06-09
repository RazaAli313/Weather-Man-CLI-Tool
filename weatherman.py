import sys
from weatherman.loader import load_file
from time import sleep

#Three whitelines after imports skipped to fulfill PEP 8 standard
# User Command-Line Argument->Loader->Parser->Data Structure->Calculation->Report (Output)
def main()->None:

    """
    Main Entry Point Function to call loaders to load the concerned data
    of the user as per passed user's command line arguments
    """
    if len(sys.argv)<2:
        print("No command line arguments passed...")

    print(sys.argv)
    try: 
        load_file(sys.argv[1])
    except:
        print("Error loading file,either file not exists or invalid argument")

if __name__=="__main__":
    for i in range(14):
        print("-",end="",flush=True)
        sleep(0.06)
    
    welcome_sentence="Welcome to Weather Man CLI Tool"
    for word in welcome_sentence:
        print(word,end="",flush=True)
        sleep(0.06)
    
    for i in range(14):
        print("-",end="",flush=True)
        sleep(0.06)
    
    print("\n\n")
    sleep(1)

    main()
    print("--------------------------------------\n\n")

"""
User Request Format
weatherman.py /path/to/files-dir -c 2011/3
"""
