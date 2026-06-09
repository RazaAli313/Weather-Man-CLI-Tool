import sys
from weatherman.loader import load_directory
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

    directory_path=sys.argv[1]
    argument_types=[]
    timelines=[]

    if(len(sys.argv)<4):
        print("Minimum Required arguments' length is 4")
        print("Valid Request Format Example: weatherman.py /path/to/files-dir -c 2011/3")    
    else:
        for i in range(2,len(sys.argv)):
            if i%2==0:
                argument_types.append(sys.argv[i])
            else:
                timelines.append(sys.argv[i])

    try: 
        load_directory(directory_path, argument_types, timelines)
    except Exception as e:
        print("Error loading file,either file not exists or invalid argument: ",e)
        print("Valid Request Format Example: weatherman.py /path/to/files-dir -c 2011/3",e)


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
