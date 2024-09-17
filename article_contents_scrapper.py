import requests
from bs4 import BeautifulSoup

def scrape_article_content(article_url):
    """
    Scrape the content from a given article page.

    Args:
        article_url (str): The URL of the article.

    Returns:
        str: The formatted core content of the article, preserving the structure.
    """
    print(f"Scraping content from article: {article_url}")
    article_page = requests.get(article_url)
    article_soup = BeautifulSoup(article_page.text, 'lxml')

    # Initialize list to hold the content in order
    content = []

    # Extract the main title (if exists)
    title = article_soup.find('h1')
    if title:
        title_text = title.get_text(strip=True)
    content.append(f"# {title_text}\n")


    # More specific search for relevant content containers
    # content_containers = article_soup.find_all(['div', 'section', 'article'], class_=lambda x: x and ('content' in x or 'rich-text' in x))
    content_containers = article_soup.find_all(['div', 'header'], class_=lambda x: x and ('helpArticle' in x or 'contentfulRichText' in x or 'help-article-header' in x or 'mediaWithCaption_media__TLfag' in x or 'animation--running appear-instantly' in x or 'faqDrawers_questionText__CBY_y' in x))
    # Process each content container
    for container in content_containers:
        for element in container.find_all(['h2', 'h3', 'h4', 'p', 'ul', 'ol', 'img', 'video'], recursive=False):
            # print(element.name)
            # Create a more robust unique identifier using the element type, text, and position in the document
            element_text = element.get_text(strip=True)
            unique_id = f"{element.name}_{element_text}_{container.name}_{container.get('class')}"

            # Process headers
            if element.name in ['h2', 'h3', 'h4']:
                header_level = '#' * (int(element.name[1]) + 1)
                content.append(f"{header_level} {element.get_text(strip=True)}\n")

            # # Process lists (handle lists first to avoid double processing)
            # elif element.name in ['ul', 'ol']:
            #     process_list(element, content, processed_elements)

            # Process paragraphs by checking their parent hierarchy
            elif element.name == 'p':
                hierarchy_level = find_list_hierarchy_level(element)
                paragraph_text = ''
                
                # Process child elements to handle inline code and text
                for child in element.children:
                    if child.name == 'code':
                        # Handle inline code
                        code_text = child.get_text(strip=True)
                        paragraph_text += f" `{code_text}` "
                    else:
                        paragraph_text += child.get_text(strip=True)

                # Format with bullet points based on hierarchy level            
                if hierarchy_level == 1:
                    bullet_point = '-'
                elif hierarchy_level >= 2:
                    bullet_point = '*'
                else:
                    bullet_point= ''
                    
                formatted_text = f"{'  ' * hierarchy_level}{bullet_point}{paragraph_text.strip()}\n"
                
                # Append formatted text to content
                content.append(formatted_text)

            # Process images
            elif element.name == 'img':
                img_url = element.get('src')
                content.append(f"![Image]({img_url})\n")

            # Process videos
            elif element.name == 'video':
                video_url = element.get('src')
                content.append(f"[Video]({video_url})\n")


    return '\n'.join(content)

def find_list_hierarchy_level(element):
    """
    Traverse upwards from the given element to find its parent hierarchy level
    based on the number of list markers (<ul> or <ol>) encountered.

    Args:
        element (bs4.element.Tag): The current HTML element to start from.

    Returns:
        int: The hierarchy level of the element based on its parent lists.
    """
    level = 0
    # Traverse upwards until the parent with the 'article' class is found
    parent = element.parent
    while parent and 'article' not in parent.get('class', []):
        if parent.name in ['ul', 'ol']:
            level += 1
        parent = parent.parent

    return level

def save_content_to_file(content, file_name):
    """
    Save the content to a text file.

    Args:
        content (str): The content to be saved.
        file_name (str): The name of the file.
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)

if __name__ == "__main__":
    # Scrape the content from the Notion Help Center page
    article_url = 'https://www.notion.so/help/writing-and-editing-basics'
    formatted_content = scrape_article_content(article_url)

    # Save the scraped content to a text file
    file_name = 'notion_help_start_here_cleaned_with_images_and_code.txt'
    save_content_to_file(formatted_content, file_name)

    print(f"Content saved to {file_name}")
