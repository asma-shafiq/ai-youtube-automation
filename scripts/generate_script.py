#!/usr/bin/env python3
"""
Generate video scripts using OpenAI GPT-4
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
import openai

load_dotenv()

class ScriptGenerator:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key
        self.model = "gpt-4"
        
    def generate_from_topic(self, topic: str, theme: str = None) -> dict:
        """
        Generate a complete video script from a topic
        """
        print(f"[INFO] Generating script for topic: {topic}")
        
        prompt = f"""
Create a compelling YouTube video script for a faceless AI channel.

Topic: {topic}
{'Theme: ' + theme if theme else ''}

Requirements:
- Video length: 8-12 minutes (approximately 1200-1800 words)
- Tone: Informative yet engaging
- Structure: Hook (30s), Introduction (1m), Main Content (5-8m), Conclusion (1-2m), Call-to-Action (30s)
- Include natural transitions between sections
- Add [VISUAL: description] tags for background visuals
- Add [MUSIC: type] tags for music/sound effects
- Make it suitable for text-to-speech narration

Format the response as JSON with keys: title, hook, introduction, main_content, conclusion, cta, tags, keywords
"""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert YouTube scriptwriter for AI content channels. Create engaging, informative scripts."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            script_content = response['choices'][0]['message']['content']
            script_data = json.loads(script_content)
            
            script_data['topic'] = topic
            script_data['theme'] = theme
            script_data['generated_at'] = datetime.now().isoformat()
            script_data['model'] = self.model
            
            print(f"[SUCCESS] Script generated successfully")
            return script_data
            
        except Exception as e:
            print(f"[ERROR] Error generating script: {str(e)}")
            raise
    
    def save_script(self, script_data: dict, output_dir: str = "./content/scripts") -> str:
        """
        Save generated script to file
        """
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/script_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(script_data, f, indent=2)
        
        print(f"[INFO] Script saved to: {filename}")
        return filename


if __name__ == "__main__":
    generator = ScriptGenerator()
    topic = "The Rise of GPT-4: Latest Features and Capabilities"
    theme = "AI Tool Reviews"
    
    try:
        script = generator.generate_from_topic(topic, theme)
        generator.save_script(script)
        print("[SUCCESS] Script generation complete")
    except Exception as e:
        print(f"[ERROR] Failed: {e}")
