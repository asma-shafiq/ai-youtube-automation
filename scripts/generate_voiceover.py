#!/usr/bin/env python3
"""
Generate voiceovers using ElevenLabs API
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

class VoiceoverGenerator:
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.voice_id = os.getenv('ELEVENLABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')
        self.base_url = "https://api.elevenlabs.io/v1"
        
    def text_to_speech(self, text: str, output_path: str = None) -> str:
        """
        Convert text to speech using ElevenLabs
        """
        print(f"[INFO] Generating voiceover for {len(text)} characters")
        
        url = f"{self.base_url}/text-to-speech/{self.voice_id}"
        
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "text": text,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"./content/voiceovers/voiceover_{timestamp}.mp3"
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            file_size = os.path.getsize(output_path) / (1024 * 1024)
            print(f"[SUCCESS] Voiceover generated: {output_path} ({file_size:.2f} MB)")
            
            return output_path
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error generating voiceover: {str(e)}")
            raise
    
    def generate_from_script(self, script_data: dict, output_dir: str = "./content/voiceovers") -> str:
        """
        Generate voiceover from complete script sections
        """
        full_text = ""
        for section in ['hook', 'introduction', 'main_content', 'conclusion', 'cta']:
            if section in script_data:
                text = script_data[section]
                text = text.replace('[VISUAL:', '').replace('[MUSIC:', '').replace(']', '')
                full_text += text + " "
        
        return self.text_to_speech(full_text.strip(), f"{output_dir}/voiceover_final.mp3")


if __name__ == "__main__":
    generator = VoiceoverGenerator()
    sample_text = "Welcome to AI Daily Insights. Today we're exploring the latest developments in artificial intelligence."
    
    try:
        audio_file = generator.text_to_speech(sample_text)
        print(f"[SUCCESS] Generated audio: {audio_file}")
    except Exception as e:
        print(f"[ERROR] Failed: {e}")
