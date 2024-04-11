import shutil

def move_file_with_check(source, destination):
    try:
        shutil.move(source, destination)
    except shutil.Error as e:
        # Check if the error is a DestinationError
        for error in e.args[0]:
            if isinstance(error, (shutil.DestinationError, FileExistsError)):
                # Define your condition to determine whether to raise the error
                condition_met = True  # For example, you can set this based on some criteria
                if condition_met:
                    raise error
                else:
                    # Handle other shutil errors
                    print("An error occurred:", error)
            else:
                # Handle other shutil errors
                print("An error occurred:", error)