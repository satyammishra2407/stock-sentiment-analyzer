# expert_analysis/news_service.py
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Complete Indian stocks keywords mapping
COMPANY_KEYWORDS = {
    # 🏆 Nifty 50 Stocks - Complete List
    'RELIANCE': ['reliance industries', 'mukesh ambani', 'ril', 'jio', 'reliance'],
    'TCS': ['tata consultancy', 'tcs', 'tata sons'],
    'HDFCBANK': ['hdfc bank', 'hdfc', 'banking stock'],
    'INFY': ['infosys', 'narayana murthy', 'it major'],
    'HINDUNILVR': ['hindustan unilever', 'hul', 'unilever'],
    'ICICIBANK': ['icici bank', 'icici', 'private bank'],
    'KOTAKBANK': ['kotak mahindra bank', 'kotak bank'],
    'SBIN': ['state bank of india', 'sbi', 'public sector bank'],
    'BHARTIARTL': ['bharti airtel', 'airtel', 'telecom'],
    'ITC': ['itc limited', 'itc', 'cigarette', 'fmcg'],
    'LT': ['larsen & toubro', 'l&t', 'engineering'],
    'HCLTECH': ['hcl technologies', 'hcl tech'],
    'AXISBANK': ['axis bank', 'banking'],
    'MARUTI': ['maruti suzuki', 'maruti', 'auto'],
    'ASIANPAINT': ['asian paints', 'paints'],
    'DMART': ['avenue supermarts', 'dmart', 'retail'],
    'SUNPHARMA': ['sun pharmaceutical', 'sun pharma'],
    'TITAN': ['titan company', 'titan', 'watches'],
    'ULTRACEMCO': ['ultratech cement', 'ultratech'],
    'WIPRO': ['wipro limited', 'wipro'],
    'NESTLEIND': ['nestle india', 'nestle'],
    'POWERGRID': ['power grid corporation', 'powergrid'],
    'NTPC': ['ntpc limited', 'ntpc', 'power'],
    'ONGC': ['oil and natural gas corporation', 'ongc'],
    'COALINDIA': ['coal india', 'coalindia'],
    'BAJFINANCE': ['bajaj finance', 'bajaj fin'],
    'TECHM': ['tech mahindra', 'techm'],
    'ADANIPORTS': ['adani ports', 'adani ports & sez'],
    'TATAMOTORS': ['tata motors', 'tatamotors', 'auto'],
    'BAJAJFINSV': ['bajaj finserv', 'bajaj finserv'],
    'GRASIM': ['grasim industries', 'grasim'],
    'JSWSTEEL': ['jsw steel', 'jsw'],
    'HDFCLIFE': ['hdfc life insurance', 'hdfc life'],
    'DRREDDY': ['dr reddys laboratories', 'dr reddy'],
    'CIPLA': ['cipla limited', 'cipla'],
    'TATASTEEL': ['tata steel', 'tatasteel'],
    'SBILIFE': ['sbi life insurance', 'sbi life'],
    'HINDALCO': ['hindalco industries', 'hindalco'],
    'BRITANNIA': ['britannia industries', 'britannia'],
    'DIVISLAB': ['divis laboratories', 'divis'],
    'EICHERMOT': ['eicher motors', 'eicher', 'royal enfield'],
    'UPL': ['upl limited', 'upl', 'agrochemicals'],
    'BAJAJ-AUTO': ['bajaj auto', 'bajaj auto'],
    'SHREECEM': ['shree cement', 'shreecem'],
    'HEROMOTOCO': ['hero motocorp', 'hero', 'motocorp'],
    'INDUSINDBK': ['indusind bank', 'indusind'],
    'APOLLOHOSP': ['apollo hospitals', 'apollo'],
    'BPCL': ['bharat petroleum', 'bpcl'],
    'HDFCAMC': ['hdfc asset management', 'hdfc amc'],
    
    # 🚀 Other Popular Indian Stocks
    'VEDL': ['vedanta limited', 'vedanta'],
    'ZOMATO': ['zomato limited', 'zomato'],
    'PAYTM': ['one97 communications', 'paytm'],
    'IRCTC': ['irctc limited', 'irctc'],
    'TATAPOWER': ['tata power', 'tatapower'],
    'M&M': ['mahindra & mahindra', 'mahindra'],
    'PIDILITIND': ['pidilite industries', 'pidilite'],
    
    # 📈 Mid Cap Stocks
    'BERGEPAINT': ['berger paints', 'berger'],
    'DABUR': ['dabur india', 'dabur'],
    'GODREJCP': ['godrej consumer', 'godrej'],
    'HAVELLS': ['havells india', 'havells'],
    'MOTHERSON': ['motherson sumi', 'motherson'],
    
    # 🏦 Banks & Financials
    'BANDHANBNK': ['bandhan bank', 'bandhan'],
    'FEDERALBNK': ['federal bank', 'federal'],
    'IDFCFIRSTB': ['idfc first bank', 'idfc'],
    
    # 💊 Pharma
    'BIOCON': ['biocon limited', 'biocon'],
    'LUPIN': ['lupin limited', 'lupin'],
    'TORNTPHARM': ['torrent pharmaceuticals', 'torrent pharma'],
    
    # 🔧 IT & Tech
    'MINDTREE': ['mindtree limited', 'mindtree'],
    'MPHASIS': ['mphasis limited', 'mphasis'],
    'PERSISTENT': ['persistent systems', 'persistent'],
    
    # 🛒 Retail & FMCG
    'DIXON': ['dixon technologies', 'dixon'],
    'VBL': ['varun beverages', 'varun'],
    
    # 🏭 Infrastructure
    'ADANIENSOL': ['adani energy solutions', 'adani energy'],
    'ADANIGREEN': ['adani green energy', 'adani green'],
    
    # 🚗 Auto & Ancillaries
    'BOSCHLTD': ['bosch limited', 'bosch'],
    'MOTHERSON': ['motherson sumi', 'motherson'],
    
    # 📱 Telecom
    'IDEA': ['vodafone idea', 'vi', 'vodafone'],
}

def get_stock_news(company, num_articles=15):
    """Fetch live news specifically for Indian stocks"""
    if not NEWS_API_KEY or NEWS_API_KEY == "your_newsapi_key_here":
        return []
    
    # Clean company name (remove .NS if present)
    clean_company = company.replace('.NS', '').replace('.BO', '').upper()
    
    try:
        # Get company specific keywords
        company_keywords = COMPANY_KEYWORDS.get(clean_company, [clean_company.lower()])
        
        # Build targeted search queries
        search_queries = []
        
        # Query 1: Company name + Indian stock keywords
        for keyword in company_keywords:
            search_queries.extend([
                f'"{keyword}" India stock market',
                f'"{keyword}" NSE BSE',
                f'"{keyword}" share price India',
                f'"{keyword}" quarterly results',
                f'"{keyword}" sensex nifty'
            ])
        
        # Query 2: For well-known companies, add more specific terms
        if clean_company in ['RELIANCE', 'INFY', 'TCS', 'HDFCBANK', 'HINDUNILVR', 'ICICIBANK']:
            search_queries.extend([
                f'"{clean_company}" stock analysis',
                f'"{clean_company}" investors',
                f'"{clean_company}" financial results',
                f'"{clean_company}" earnings'
            ])
        
        all_articles = []
        
        for query in search_queries[:8]:  # Limit to 8 queries to avoid rate limits
            params = {
                'q': query,
                'language': 'en',
                'sortBy': 'relevancy',  # Changed to relevancy for better results
                'pageSize': min(5, num_articles),
                'apiKey': NEWS_API_KEY
            }
            
            try:
                response = requests.get("https://newsapi.org/v2/everything", params=params, timeout=15)
                
                if response.status_code == 200:
                    articles = response.json().get('articles', [])
                    
                    # Filter only relevant Indian stock news
                    for article in articles:
                        if is_relevant_indian_stock_news(article, clean_company):
                            all_articles.append(article)
                
                # Small delay to avoid rate limiting
                import time
                time.sleep(0.3)
                
            except Exception as e:
                print(f"Query failed {query}: {e}")
                continue
        
        # Remove duplicates based on title
        seen_titles = set()
        unique_articles = []
        
        for article in all_articles:
            title = article.get('title', '')
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_articles.append(article)
        
        # If no relevant news found, try broader search as fallback
        if not unique_articles:
            unique_articles = fallback_news_search(clean_company, num_articles)
        
        return unique_articles[:num_articles]
        
    except Exception as e:
        print(f"Error fetching news for {company}: {e}")
        return fallback_news_search(clean_company, num_articles)

def is_relevant_indian_stock_news(article, company):
    """Check if article is relevant to Indian stock market"""
    title = article.get('title', '').lower()
    description = article.get('description', '').lower()
    content = f"{title} {description}"
    
    # Must contain company name or related keywords
    company_keywords = COMPANY_KEYWORDS.get(company, [company.lower()])
    has_company = any(keyword in content for keyword in company_keywords)
    
    if not has_company:
        return False
    
    # Should contain stock/financial keywords
    financial_keywords = ['stock', 'share', 'market', 'price', 'invest', 'financial', 'results', 'profit', 'revenue', 'earning', 'dividend', 'sensex', 'nifty']
    has_financial = any(keyword in content for keyword in financial_keywords)
    
    # Should NOT contain irrelevant content
    irrelevant_keywords = ['job', 'career', 'recruitment', 'hiring', 'event', 'conference', 'seminar', 'sports', 'entertainment']
    has_irrelevant = any(keyword in content for keyword in irrelevant_keywords)
    
    return has_financial and not has_irrelevant

def fallback_news_search(company, num_articles):
    """Fallback search when primary method fails"""
    try:
        params = {
            'q': f'{company} stock India NSE BSE',
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': num_articles,
            'apiKey': NEWS_API_KEY
        }
        
        response = requests.get("https://newsapi.org/v2/everything", params=params, timeout=10)
        
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return articles[:num_articles]
        
    except Exception as e:
        print(f"Fallback search failed: {e}")
    
    return []

def format_time(published_at):
    """Convert ISO time to readable format"""
    try:
        if not published_at:
            return "Recent"
        
        pub_time = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
        now = datetime.now(pub_time.tzinfo)
        diff = now - pub_time
        
        if diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds >= 3600:
            return f"{diff.seconds // 3600}h ago"
        else:
            return f"{diff.seconds // 60}m ago"
    except:
        return "Recent"