import re
import os

def analyze_log(file_path, search_string, min_value=None):
    """
    Analyzes a log file to find a specific string, extract all integers that
    immediately follow that string and meet a minimum value, and then calculates
    their average.

    Args:
        file_path (str): The full path to the log file.
        search_string (str): The string to search for in the log file. The script
                             will look for numbers that immediately follow this string.
        min_value (int, optional): The minimum value an integer must have to be
                                   included in the average. Defaults to None (no minimum).

    Returns:
        tuple: A tuple containing the average (float), the total count of numbers (int),
               and a list of all the numbers found (list of ints).
               Returns (0, 0, []) if no numbers are found or the file doesn't exist.
    """
    all_numbers = []

    # Check if the file exists before trying to open it
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return 0, 0, []

    try:
        # Open the log file for reading
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # Iterate over each line in the file
            for line in f:
                # UPDATED LOGIC: We now use a more specific regex with a word boundary (\b)
                # to ensure we are matching the exact search term as a whole word.
                
                # Construct a regex pattern to find numbers immediately following the search string.
                # \b ensures we match a whole word, preventing partial matches like "audioSent".
                # re.escape handles any special characters in the search_string.
                # \s* matches any whitespace (or no whitespace).
                # (-?\d+) is a capture group for the integer itself.
                pattern = r'\b' + re.escape(search_string) + r'\s*(-?\d+)'
                found_numbers = re.findall(pattern, line)

                # re.findall with a capture group returns a list of strings of the captured group,
                # so we can iterate through them directly.
                for num_str in found_numbers:
                    num = int(num_str)
                    # Only include the number if it meets the minimum value threshold
                    if min_value is None or num >= min_value:
                        all_numbers.append(num)

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return 0, 0, []

    # Calculate the average if numbers were found
    if all_numbers:
        total_sum = sum(all_numbers)
        count = len(all_numbers)
        average = total_sum / count
        return average, count, all_numbers
    else:
        # Return zero values if no numbers were found
        return 0, 0, []

# --- Main execution block ---
if __name__ == "__main__":
    # Define a dummy log file name for demonstration
    log_file_name = "messages.txt"

    # Create some dummy log content that matches the user's example
    log_content = """
    Aug 28 16:39:50 buildroot user.info root: ... decoded:120 scaled:120 sent:118 ...
    Aug 28 16:39:55 buildroot user.info root: ... decoded:120 scaled:120 sent:116 ...
    ERROR: A different error message.
    Aug 28 16:40:00 buildroot user.info root: ... decoded:120 scaled:120 sent:114 ...
    INFO: Some other process sent:9999 bytes which we should ignore.
    Aug 28 16:40:05 buildroot user.info root: ... audioSent:0 packet errors:0 sent:115 ...
    """

    # Write the dummy content to the log file
    try:
        with open(log_file_name, 'w') as f:
            f.write(log_content)
        print(f"Created a dummy log file: '{log_file_name}'")

        # --- Use the function with the user's example ---
        # Note: The search term should not have a space after it unless the log does.
        search_term = "sent:"
        # Define the minimum value threshold
        min_threshold = 89
        
        # Call the analysis function with the new minimum value argument
        avg, num_count, numbers_list = analyze_log(log_file_name, search_term, min_threshold)

        # Print the results in a user-friendly way
        print("-" * 30)
        if num_count > 0:
            print(f"Analysis for numbers following '{search_term}':")
            print(f"(Ignoring values less than {min_threshold})")
            print(f"Found {num_count} numbers: {numbers_list}")
            print(f"The average is: {avg:.2f}") # Format average to 2 decimal places
        else:
            print(f"No numbers found following '{search_term}' that met the threshold.")
        print("-" * 30)

    except Exception as e:
        print(f"An error occurred during the demonstration: {e}")
    finally:
        # Clean up by deleting the dummy log file
        if os.path.exists(log_file_name):
            os.remove(log_file_name)
            print(f"Cleaned up and removed '{log_file_name}'.")