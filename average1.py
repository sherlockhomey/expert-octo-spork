# log_analyzer.py

def analyze_log_file(file_path, min_threshold=0):
    """
    Analyzes a log file to find all numbers after "sent:",
    calculates their sum, and finds the average for numbers
    above a certain threshold.

    Args:
        file_path (str): The path to the log file.
        min_threshold (int): The minimum value to include in the calculation.
                               Numbers below or equal to this will be ignored.
    """
    # A list to hold the numbers we find
    sent_numbers = []
    
    try:
        # Open the file and read it line by line
        with open(file_path, 'r') as f:
            for line in f:
                # Split the line into individual words
                words = line.split()
                # Go through each word to find the one we need
                for word in words:
                    # Check if a word starts with "sent:"
                    if word.startswith("sent:"):
                        try:
                            # Split the word "sent:117" into "sent" and "117"
                            parts = word.split(':')
                            # The number is the second part
                            number = int(parts[1])
                            
                            # NEW: Only include numbers greater than the threshold
                            if number > min_threshold:
                                sent_numbers.append(number)
                                
                            # Found it, no need to check other words in this line
                            break
                        except (ValueError, IndexError):
                            # This will skip any lines where "sent:" isn't followed by a valid number
                            pass

        # Make sure we actually found some numbers
        if sent_numbers:
            # Calculate the sum
            total_sum = sum(sent_numbers)
            # Calculate the average
            average = total_sum / len(sent_numbers)
            
            # Print out the final results
            print(f"Found {len(sent_numbers)} instances of 'sent:' above the threshold of {min_threshold}.")
            print(f"The sum of all 'sent' numbers is: {total_sum}")
            print(f"The average of all 'sent' numbers is: {average:.2f}")
        else:
            print(f"Could not find any instances of 'sent:' above the threshold of {min_threshold} in the log file.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Name of the log file to analyze.
    # Make sure this file is in the same directory as the script,
    # or provide the full path to the file.
    log_file = "messages.txt"
    
    # Set a minimum value. Numbers below or equal to this will be ignored.
    # To ignore all the '0' values, set this to 0.
    # To ignore values 10 and under, set this to 10.
    minimum_threshold = 89
    
    analyze_log_file(log_file, minimum_threshold)