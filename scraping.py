import os

from notion_articles_scrapper import scrape_articles, scrape_chapters
from article_contents_scrapper import scrape_article_content, find_list_hierarchy_level, save_content_to_file

base_url = 'https://www.notion.so'
reference_url = 'https://www.notion.so/help/reference'


if __name__ == "__main__":
    # Ensure the 'txt_files' directory exists
    if not os.path.exists('txt_files'):
        os.makedirs('txt_files/')

    # Use the functions to scrape chapters and articles
    chapters = scrape_chapters(base_url=base_url, reference_url=reference_url)
    print("Chapters found:", chapters)

    for chapter_name, chapter_url in chapters.items():
        # Scrape the chapter introduction and articles
        chapter_intro, articles_by_chapter = scrape_articles(base_url, chapter_name, chapter_url)

        # Initialize content for the chapter's text file
        chapter_content = f"<{chapter_name}>\n\n{chapter_intro}\n\n"

        # Scrape and append content for each article in the chapter
        for article_title, article_url in articles_by_chapter.items():
            article_content = scrape_article_content(article_url)
            chapter_content += f"\n\n{article_content}\n"

        # Define file path for saving the chapter content
        file_path = os.path.join('txt_files/', f"{chapter_name.replace('. ', '_').replace(' ', '_')}.txt")

        # Save the chapter content to a file
        save_content_to_file(chapter_content, file_path)

     
