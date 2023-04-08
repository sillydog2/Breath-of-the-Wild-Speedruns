

import time
from termcolor import colored
import shutil




def get_previous_key(dictionary, specific_key):
    """
    Get the previous key in a dictionary given a specific key.
    
    Args:
        dictionary (dict): The input dictionary.
        specific_key (str): The specific key for which to find the previous key.
        
    Returns:
        str: The previous key in the dictionary, or None if the specific key is the first key in the dictionary.
    """
    # Convert dictionary keys to a list
    split_keys = list(dictionary.keys())

    # Find the index of the specific key in the list of keys
    index = split_keys.index(specific_key)

    # Check if the specific key is not the first key in the list
    if index > 0:
        # Access the previous key using list indexing
        previous_key = split_keys[index - 1]
        return previous_key
    else:
        # Return None if the specific key is the first key in the dictionary
        return None







# Define the split points for Great Plateau any% run
splits = {
    "Shrine of Resurrection + Stasis Clip": 0,
    "Stasis Shrine": 0,
    "Boulder Launch + Cryonis BTB and Clip": 0,
    "Cryonis Shrine": 0,
    "Magnesis BTB + Clip": 0,
    "Magnesis Shrine": 0,
    "Magnesis Launch + Bomb BTB": 0,
    "Bomb Shrine": 0,
    "Paraglider": 0
}



#holds splits from PB and gold splits from all runs
splits2 = {}
differences = {}


#gets PB splits, gold splits and total time from informtion stored in txt file
with open("botw_speedrun_splits.txt", "r") as file:
    # Read all lines from the file
    lines = file.readlines()
    # Extract the last line
    last_line = lines[-1].strip()
    # Split the line by colon
    split, time_and_gold = last_line.split(":", 1)
    time_str, gold = time_and_gold.split("$")
    # Split the time string by colon
    time_parts = time_str.strip().split(":")
    # Extract the minutes and seconds
    minutes = float(time_parts[0])
    seconds = float(time_parts[1])
    # Calculate the total time in seconds
    old_total_time = minutes * 60 + seconds
    for line in lines:  
        allsplit, alltime_and_gold = line.split(":", 1)
        alltime_str , allgold = alltime_and_gold.split("$")
        splits2[allsplit] = alltime_str
        differences[allsplit] = float(allgold) 
        
        



# Wait for user input to mark start of speedrun
input("Press Enter to start the speedrun...")

# Record start time
start_time = time.time()



gold_index = 0 #will be changed to 1 if a gold split is recorded

# Loop through the splits and record timestamps
for split in splits:
    # Wait for user input to mark split point
    input(f"\n{colored(split, 'blue', attrs=['bold'])}\nPress Enter to mark {split}...")

    # Record split time
    splits[split] = time.time() - start_time
    
    potential_gold = 0.0 #value to compare to gold splits in the differences dictionary
    if get_previous_key(splits, split) is None: 
        potential_gold = splits[split]
    else: 
        potential_gold = splits[split] - splits[get_previous_key(splits, split)]
    
    
    #Here we extract the splits from PB which are stored \using a specific format ("Split name": Minutes:seconds.1f$gold)
    time_parts_0 = splits2[split].strip().split(":")
    minutes2 = float(time_parts_0[0])
    seconds2 = float(time_parts_0[1])


    #case work: printing red, green or gold split
    if potential_gold <= differences[split]: 
        minutes = int(splits[split] // 60)
        seconds = round(splits[split] % 60, 1)
        print(f"{colored(split, 'yellow', attrs=['bold'])}: {minutes}:{seconds}") 
        differences[split] = round(potential_gold, 1)
        gold_index=1
    elif splits[split] > 60:
        minutes = int(splits[split] // 60)
        seconds = round(splits[split] % 60, 1)
        if minutes < minutes2: 
            print(f"{colored(split, 'green', attrs=['bold'])}: {minutes}:{seconds}")
        elif minutes == minutes2 and seconds <= seconds2: 
            print(f"{colored(split, 'green', attrs=['bold'])}: {minutes}:{seconds}")
        else:
            print(f"{colored(split, 'red', attrs=['bold'])}: {minutes}:{seconds}")
    else:
        seconds = round(splits[split] % 60, 1)
        if seconds <= seconds2: 
            print(f"{colored(split, 'green', attrs=['bold'])}: 0:{splits[split]:.1f}")
        else: 
            print(f"{colored(split, 'red', attrs=['bold'])}: 0:{splits[split]:.1f}")

#record end time
end_time = time.time()



# Print final split times
print("\nFinal split times:")
for split, time_elapsed in splits.items():
    # Check if split time is above 1 minute
    if time_elapsed > 60:
        minutes = int(time_elapsed // 60)
        seconds = round(time_elapsed % 60,1)
        print(f"{colored(split, 'blue', attrs=['bold'])}: {minutes}:{seconds}")
    else:
        print(f"{colored(split, 'blue', attrs=['bold'])}: 0:{time_elapsed:.1f}")




# Calculate total time of current speedrun
total_time = end_time - start_time


# Compare total times and save to file if current speedrun is faster, or if currend speedrun recorded gold times
if total_time < old_total_time or old_total_time == 0:
    # Specify the source file and backup file names
    source_file = "botw_speedrun_splits.txt"
    backup_file = "botw_speedrun_splits_backup.txt"

# Create a backup copy of the source file
    shutil.copy(source_file, backup_file)
    with open("botw_speedrun_splits.txt", "w") as file:
        for split, time_elapsed in splits.items():
            file.write(f"{split}: ")
            if time_elapsed > 60:
                minutes = int(time_elapsed // 60)
                seconds = round(time_elapsed % 60,1)
                diff = differences[split]
                file.write(f"{minutes}:{seconds}${diff}\n")
            else:
                diff = differences[split]
                file.write(f"0:{time_elapsed:.1f}${diff}\n")
elif gold_index == 1: 
    # Specify the source file and backup file names
    source_file = "botw_speedrun_splits.txt"
    backup_file = "botw_speedrun_splits_backup.txt"

    # Create a backup copy of the source file
    shutil.copy(source_file, backup_file)
    with open("botw_speedrun_splits.txt", "w") as file:
        for split, time_elapsed in splits2.items():
            file.write(f"{split}: ")
            diff = differences[split]
            file.write(f"{time_elapsed}${diff}\n")

minutes_final = int(splits["Paraglider"] // 60)
seconds_final = round(splits["Paraglider"] % 60,1)
print("\nSpeedrun complete!") 
print(f"Total time: {minutes_final}:{seconds_final}")

# Check if current speedrun is faster and update best time
if total_time < old_total_time or old_total_time == 0:
    print(colored("Congratulations! New best speedrun time! Backup of old PB was created. ", "yellow", attrs=["bold"]))
elif gold_index == 1: 
    print(colored("Back file was made for old PB due to new gold", "green", attrs=["bold"]))

print("Thank you for playing!")


