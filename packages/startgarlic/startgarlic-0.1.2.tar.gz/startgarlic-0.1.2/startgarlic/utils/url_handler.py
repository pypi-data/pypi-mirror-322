from langchain.callbacks.base import BaseCallbackHandler
from langchain.tools import Tool
from typing import Dict, Any

class URLTracker(BaseCallbackHandler):
    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Track when a URL is accessed"""
        if kwargs.get('tool_name') == 'company_link':
            print(f"URL access tracked: {output}")

class URLHandler:
    def __init__(self, analytics_manager):
        self.analytics = analytics_manager
        self.callback_handler = URLTracker()
        
        # Create a tool for handling company links
        self.company_link_tool = Tool(
            name="company_link",
            func=self.process_company_link,
            description="Process and track company link clicks",
            callbacks=[self.callback_handler]
        )
    
    def process_company_link(self, company_data: Dict[str, str]) -> bool:
        """Process company link with verification"""
        try:
            company_name = company_data.get('name')
            website = company_data.get('website')
            
            if not company_name or not website:
                print("Missing company data")
                return False
            
            # Track the access with verification
            success = self.analytics.increment_access(company_name)
            
            if success:
                print(f"Successfully tracked access for {company_name}")
                return True
            else:
                print(f"Failed to track access for {company_name}")
                return False
                
        except Exception as e:
            print(f"Error processing link: {e}")
            return False
    
    def format_tracking_url(self, company_name: str, website: str) -> str:
        """Format company URL with tracking"""
        return f"{company_name} @ {website}"