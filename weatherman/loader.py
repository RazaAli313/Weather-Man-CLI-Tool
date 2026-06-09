from pathlib import Path


#Three whitelines after imports skipped to fulfill PEP 8 standard
# def load_directory(directory_path: str)->None:
#     """
#     This is the Function to load the weatherfiles 
#     directory in the memory.
#     """
#     directory_path=Path(directory_path)
#     count=1
#     for file in directory_path.iterdir():
#         print(f"File Count: {count}", file.name)
#         load_file(file)
#         count+=1

def load_file(file_path: str)->None:
    """
    This is the Function to load the weatherfiles 
    from the weatherfiles directory
    """

    with open(file_path, encoding="utf-8") as file:
        file_content=file.readlines()
        # print(file_content)
        parse_file(file_content)



# load_directory("weatherfiles")

""" 
File Data Format
PKT,Max TemperatureC,Mean TemperatureC,Min TemperatureC,Dew PointC,MeanDew PointC,Min DewpointC,Max Humidity, Mean Humidity, Min Humidity, Max Sea Level PressurehPa, Mean Sea Level PressurehPa, Min Sea Level PressurehPa, Max VisibilityKm, Mean VisibilityKm, Min VisibilitykM, Max Wind SpeedKm/h, Mean Wind SpeedKm/h, Max Gust SpeedKm/h,Precipitationmm, CloudCover, Events,WindDirDegrees
"""


        