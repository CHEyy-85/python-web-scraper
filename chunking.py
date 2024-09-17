import re
import glob

def merge_files(file_paths):
    """
    Merge the content of multiple text files into a single string.

    Args:
        file_paths (list): A list of file paths to merge.

    Returns:
        str: The merged content of all files.
    """
    merged_content = ""
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as file:
            merged_content += file.read() + "\n"
    return merged_content


def split_text_into_chunks(text, max_length=750):
    """
    Splits the text into chunks of maximum specified length while keeping headers, paragraphs,
    and lists intact.

    Args:
        text (str): The input text to be split.
        max_length (int): The maximum character length of each chunk.

    Returns:
        list: A list of text chunks.
    """
    # Regular expression patterns to identify headers and list items
    header_pattern = r'^#.*'
    list_pattern = r'^[-*].*'

    # Split input text by lines
    lines = text.splitlines()

    chunks = []
    current_chunk = ""

    for i, line in enumerate(lines):
        # Check if the line is a header or part of a list
        is_header_or_list = re.match(header_pattern, line) or re.match(list_pattern, line)
        
        # If adding this line exceeds max length, save the current chunk
        if len(current_chunk) + len(line) + 1 > max_length and not is_header_or_list:
            chunks.append(current_chunk.strip())
            current_chunk = ""

        # Append the line to the current chunk
        if current_chunk:
            current_chunk += "\n" + line
        else:
            current_chunk = line

        # If the line is a header or a list item, start a new chunk
        if is_header_or_list:
            # Do not break mid-list
            if current_chunk and (i + 1 < len(lines) and not re.match(list_pattern, lines[i + 1])):
                chunks.append(current_chunk.strip())
                current_chunk = ""

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


if __name__ == "__main__":
    # Get all text files in the current directory (or specify your directory)
    file_paths = glob.glob("txt_files/*.txt")

    # Merge all text files into one string
    merged_content = merge_files(file_paths)

    # Split the merged content into chunks
    chunks = split_text_into_chunks(merged_content)

    # Print the array of chunks
    print(chunks)
    
