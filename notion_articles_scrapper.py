import requests
from bs4 import BeautifulSoup

def scrape_chapters(base_url, reference_url):
    """
    Scrape all chapters links from the Notion help reference page.

    Returns:
        dict: A dictionary with chapter names as keys and their URLs as values.
    """
    # Make a request to the reference page
    reference_page = requests.get(reference_url)
    soup = BeautifulSoup(reference_page.text, 'lxml')

    # Find all chapter links
    chapters_html = soup.find_all('a', class_='helpCenterArticleGrid_titleLink__hTrdL')
    chapters = {chapter.text: base_url + chapter['href'] for chapter in chapters_html}

    return chapters


def scrape_articles(base_url, chapter_name, chapter_url):
    """
    Scrape intro to chapter and all article links from a given chapter page.

    Args:
        chapter_name (str): The name of the chapter.
        chapter_url (str): The URL of the chapter.

    Returns:
        str: A string of the chapter's introduction.
        dict: A dictionary with article titles as keys and their URLs as values for the given chapter.
    """
    print(f"Scraping articles from chapter: {chapter_name} - {chapter_url}")
    chapter_page = requests.get(chapter_url)
    soup = BeautifulSoup(chapter_page.text, 'lxml')

    # Find the introduction of the chapter
    chapter_intro = soup.find('meta', attrs={'name': 'description'})['content']
    
    # Find all article links within the chapter
    articles_tags = soup.find_all('h3', class_='title_title__DWL5N title_titleSizeXxs__G6KYV title_titleWeightBold__838EK title_titleFamilyInter__Ra6_Q')

    articles_by_chapter = {}
    # Extract the URL and title for each article
    for article in articles_tags:
        article_title = article.text.strip()
        article_link = article.find_parent('a', href=True)

        if article_link:  # Ensure the parent <a> tag exists
            article_url = base_url + article_link['href']
            articles_by_chapter[article_title] = article_url

    return chapter_intro, articles_by_chapter


if __name__ == "__main__":
    # Use the functions to scrape chapters and articles
    base_url = 'https://www.notion.so'
    reference_url = 'https://www.notion.so/help/reference'

    chapters = scrape_chapters(base_url=base_url, reference_url=reference_url)
    print("Chapters found:", chapters)

    articles = {}
    chapter_intros = {}
    for chapter_name, chapter_url in chapters.items():
        chapter_intros[chapter_name], articles[chapter_name] = scrape_articles(base_url, chapter_name, chapter_url)

    print(articles[chapter_name])
