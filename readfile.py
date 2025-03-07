def read_file_content(filename):
    """
    Reads and returns the content of a file specified by filename.

    Args:
    filename (str): The path to the file to be read.

    Returns:
    str: The content of the file.
    """
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"

""" # Example usage
file_path = "gencode.log"  # Replace 'example.txt' with your actual file path
content = read_file_content(file_path)
print(print(repr(content)) ) """
