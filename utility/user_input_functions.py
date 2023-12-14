from typing import List


def get_clean_user_input_paths(user_input: str) -> List[str]:
    """
    Clean the user data and strip unnecessary information from each item in the list.
    Please note that the function assumes that the user input is separated by comma.
    :param user_input: user input separated by comma, example: "C:\Documents\, D:\Receipts\sample.pdf"
    :return: list <str>, example: ["C:\Documents\", "D:\Receipts\sample.pdf"]
    """
    user_input = user_input.strip().split(",")  # user input separated by comma

    cleaned_user_input = []
    for user_item in user_input:
        # Strip leading/trailing whitespace and remove any unwanted characters
        cleaned_user_item = user_item.strip().replace("\n", "").replace("\r", "")
        if cleaned_user_item:
            cleaned_user_input.append(cleaned_user_item)

    # Use the cleaned list of user input for further processing
    # cleaned_user_input contains the user input with unnecessary info stripped
    return cleaned_user_input


def get_clean_user_output_path(user_input: str):
    """
    Clean user's provided directory / file path. Don't trust user, change it to format
    you want it to be once execution is in your relam. Don't assume anything.
    :parameter user_input: 'C:/Users/MK/Downloads/experiment_output'
    :return: 'C:/Users/MK/Downloads/experiment_output'
    """
    dest_dir = user_input.strip().replace("\n", "").replace("\r", "")
    return dest_dir
