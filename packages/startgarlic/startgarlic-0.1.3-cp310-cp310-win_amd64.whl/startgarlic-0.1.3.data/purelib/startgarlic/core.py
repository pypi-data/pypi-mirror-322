from .utils.database import DatabaseManager
from .utils.embeddings import EmbeddingManager
# from .utils.analytics import AnalyticsManager
from .utils.prompts import PromptManager
from .utils.auction import AuctionManager
from typing import List, Dict, Optional
import numpy as np

class Garlic:
    def __init__(self):
        """Initialize RAG system"""
        try:
            self.db = DatabaseManager()
            self.embedding_manager = EmbeddingManager()
            self.prompt_manager = PromptManager()
            self.auction_manager = AuctionManager()
            
            # Load companies data
            self.df = self.db.get_companies()
            print(f"Loaded {len(self.df)} companies")
            
        except Exception as e:
            print(f"Error initializing system: {e}")
            raise

    def find_similar_companies(self, query: str, top_k: int = 5) -> List[dict]:
        """Find companies similar to the query"""
        try:
            print(f"Processing query: {query}")  # Debug print
            
            # Create query embedding
            query_embedding = self.embedding_manager.embed_query(query)
            
            if len(query_embedding) == 0:
                print("Error: Failed to create query embedding")
                return []
            
            print(f"Created query embedding of length {len(query_embedding)}")  # Debug print
            
            # Convert to list for Supabase
            query_embedding = query_embedding.tolist()
            
            # Get similar companies with scores
            results = self.db.search_similar_companies(query_embedding, top_k)
            
            if not results:
                print("No similar companies found for query:", query)
                return []
            
            print(f"Found {len(results)} companies:")  # Debug print
            for r in results:
                print(f"- {r.get('name', 'Unknown')}: {r.get('similarity', 0):.2%}")
            
            return results
            
        except Exception as e:
            print(f"Error finding similar companies: {e}")
            print(f"Full error details: {str(e)}")  # More detailed error
            return []

    def generate_response(self, query: str, chat_history: Optional[List] = None) -> Dict:
        """Find and auction relevant companies"""
        try:
            # Get candidate companies
            print(f"Finding similar companies for query: {query}")  # Debug log
            candidates = self.find_similar_companies(query)
            print(f"Found candidates: {candidates}")  # Debug log
            
            # Select ad through auction mechanism
            print("Running auction...")  # Debug log
            selected_companies = self.auction_manager.select_ad(candidates)
            print(f"Selected companies: {selected_companies}")  # Debug log
            
            # Format response
            formatted_text = self.prompt_manager.format_prompt(
                query=query,
                companies=selected_companies,
                chat_history=chat_history
            )
            
            # Track views for selected company
            if selected_companies:
                self.db.increment_views(selected_companies)
            
            return {
                "query": query,
                "text": formatted_text,
                "companies": selected_companies
            }
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return {
                "query": query,
                "text": "I couldn't find any relevant companies.",
                "companies": []
            }

    # def track_company_interaction(self, company_name: str, interaction_type: str = 'view'):
    #     """Track company interactions (view/access)"""
    #     try:
    #         if interaction_type == 'view':
    #             self.analytics.increment_views([{'name': company_name}])
    #         elif interaction_type == 'access':
    #             self.analytics.increment_access(company_name)
    #     except Exception as e:
    #         print(f"Error tracking interaction: {e}")

    # def get_company_analytics(self, company_name: str = None):
    #     """Get detailed analytics for a company"""
    #     return self.analytics.get_company_stats(company_name)

    # def get_trending_companies(self, days: int = 7, limit: int = 5):
    #     """Get trending companies"""
    #     return self.analytics.get_trending_companies(days, limit)
