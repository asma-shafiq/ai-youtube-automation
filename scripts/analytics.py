#!/usr/bin/env python3
"""
Track and analyze channel analytics
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class AnalyticsTracker:
    def __init__(self):
        self.analytics_file = "./content/analytics.json"
        
    def log_upload(self, video_id: str, title: str, upload_time: datetime):
        """
        Log video upload
        """
        print(f"[INFO] Logging upload: {video_id}")
        
        data = self.load_analytics()
        
        data['uploads'].append({
            'video_id': video_id,
            'title': title,
            'upload_time': upload_time.isoformat(),
            'views': 0,
            'likes': 0,
            'comments': 0
        })
        
        self.save_analytics(data)
    
    def load_analytics(self) -> dict:
        """
        Load analytics data
        """
        if os.path.exists(self.analytics_file):
            with open(self.analytics_file, 'r') as f:
                return json.load(f)
        
        return {
            'uploads': [],
            'total_views': 0,
            'total_subscribers': 0,
            'last_updated': datetime.now().isoformat()
        }
    
    def save_analytics(self, data: dict):
        """
        Save analytics data
        """
        data['last_updated'] = datetime.now().isoformat()
        os.makedirs(os.path.dirname(self.analytics_file), exist_ok=True)
        
        with open(self.analytics_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"[SUCCESS] Analytics saved")
    
    def get_summary(self) -> dict:
        """
        Get analytics summary
        """
        data = self.load_analytics()
        
        return {
            'total_uploads': len(data['uploads']),
            'total_views': data['total_views'],
            'total_subscribers': data['total_subscribers'],
            'last_updated': data['last_updated']
        }


if __name__ == "__main__":
    tracker = AnalyticsTracker()
    print(json.dumps(tracker.get_summary(), indent=2))
