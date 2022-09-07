import sys
import zipfile
import os

def get_username(assignment: str) -> str:
    """
    Gets the student username from the assignment filename.
    :param assignment:
    :return:
    """
    username = ""

    # Get student username from auto-generated filename from BlackBoard
    try:
        username = assignment.split("_")[1]
    except:
        # We should still continue the routine
        print("> Could not simplify student's directory name.")

    return username


def unzip(argv) -> bool:
    """
    Unzips the global .zip file and structures all student deliverables.
    :param argv: is the command line arguments.
    :return: a boolean value indicating whether the unzipping was successful.
    """

    print(argv)
    # argv should only process 2 arguments
    if len(argv) != 2:
        print("> Invalid input. Please use the following format:")
        print(f'$ python3 unzip.py zipped-filename destination-directory')
        return False

    # Get command line arguments
    zipped = argv[0]
    destination = argv[1]

    # Only handle .zip files
    if zipped[-3:] != "zip":
        print(f"> {zipped} is not a zip file.")
        print()
        return False

    # Unzip assignment file
    try:
        with zipfile.ZipFile(zipped, 'r') as read:
            read.extractall(destination)
            print(f"> Unzipped {zipped}.")
    except:
        print(f"> Could not unzip {zipped}.")
    

    # Remove zipped assignment file
    # try:
    #     os.system(f"rm -rf *.zip")
    # except:
    #     # We should still continue the routine
    #     print("> Could not remove zipped assignment file.")

    # Navigate to the destination directory
    try:
        os.chdir(destination)
    except:
        print(f"> Could not navigate to /{destination}.")

    print(zipped[:-4])
    try:
        os.chdir(zipped[:-4])
    except:
        print(f"> Could not navigate to /{zipped[:-4]}.")

    # Make a feedback directory to store each student's feedback files
    if not os.path.exists('feedback'):
        os.mkdir("feedback")

    # Make a deliverables directory to store each student's deliverables files
    if not os.path.exists('deliverables'):
        os.mkdir("deliverables")

    # Remove redundant .txt files
    try:
        os.system("rm *.txt")
    except:
        # We should still continue the routine
        print("> Could not remove .txt files, or no .txt files was found.")



    # Keep track of how many files we can unzip.
    count = 0
    # Target is an integer determined by the number of .zip files in the destination directory.
    target = len([filename for filename in os.listdir() if filename[-3:] == "zip"])

    print(os.listdir())
    # For each zipped assignment in the destination directory
    for assignment in os.listdir():
        # Only handle .zip files
        if assignment[-3:] != "zip":
            continue

        username = get_username(assignment)

        # Unzip student file
        try:
            with zipfile.ZipFile(assignment, 'r') as read:
                read.extractall(f'deliverables/{username}')
                count += 1
                print(f"> Unzipped {username}'s deliverable. ({count} / {target})")
        except:
            print("> Could not unzip student's zipped assignment.")
            continue

    for assignment in os.listdir():
        username = get_username(assignment)

        # Navigate to the feedback directory
        # try:
        #     os.chdir("feedback")
        # except:
        #     print("> Could not navigate to the feedback directory.")

        with open(f'feedback/{username}.txt', 'w') as f:
            f.write(f"Tilbakemelding til {username} (__%)")

    # Remove zipped assignment file
    # try:
    #     os.system(f"rm -rf *.zip")
    # except:
    #     # We should still continue the routine
    #     print("> Could not remove zipped assignment file.")

    return True


if __name__ == '__main__':
    # Syntax: python3 unzip.py zipped destination
    succeeded = unzip(sys.argv[1:])

    print(
        "> Finished unzipping files!"
        if succeeded
        else "> An error occurred when trying to unzip files!"
    )
