import feedparser
import arxiv
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# CONFIGURATION
RSS_FEEDS = [
    # AI companies (low volume but important)
    'https://openai.com/blog/rss',
    'https://deepmind.com/blog/feed.xml',
    'https://ai.meta.com/blog/feed/',
    'https://www.anthropic.com/index.xml',
    
    # AI news sources (high volume, more balanced)
    'https://venturebeat.com/category/ai/feed/',
    'https://thenextweb.com/feed/',  # includes AI news
    'https://www.techradar.com/rss/news/artificial-intelligence',
    'https://feeds.arstechnica.com/arstechnica/technology-lab',  # tech & AI

]

ARXIV_QUERY = 'cat:cs.AI OR cat:cs.CL OR cat:cs.LG'
ARXIV_MAX_RESULTS = 5
OUTPUT_FILE = 'ai_news_digest.html'

# FUNCTIONS
def fetch_rss_articles():
    articles = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.published if 'published' in entry else '',
                'summary': entry.summary if 'summary' in entry else ''
            })
    return articles

def fetch_arxiv_papers():
    search = arxiv.Search(
        query=ARXIV_QUERY,
        max_results=ARXIV_MAX_RESULTS,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    papers = []
    for result in search.results():
        papers.append({
            'title': result.title,
            'authors': ', '.join([author.name for author in result.authors]),
            'summary': result.summary[:500] + '...',
            'pdf_url': result.pdf_url,
            'published': result.published.strftime("%Y-%m-%d")
        })
    return papers

def render_html(articles, papers):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')
    html_content = template.render(
        date=datetime.now().strftime("%Y-%m-%d"),
        articles=articles,
        papers=papers
    )
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)

# MAIN
if __name__ == '__main__':
    print("Fetching RSS articles...")
    rss_articles = fetch_rss_articles()

    print("Fetching arXiv papers...")
    arxiv_papers = fetch_arxiv_papers()

    print("Rendering HTML report...")
    render_html(rss_articles, arxiv_papers)

    print(f"Done! Report saved to {OUTPUT_FILE}")
