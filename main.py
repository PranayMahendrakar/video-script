#!/usr/bin/env python3
"""
Automated Video Script Generator - Llama-Based Content Creator
Creates engaging scripts for educational or marketing videos
Author: Pranay M
"""

import ollama
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.markdown import Markdown
import json

console = Console()

VIDEO_TYPES = {
    1: "Educational Tutorial", 2: "Product Demo", 3: "Explainer Video",
    4: "Marketing Promo", 5: "How-To Guide", 6: "Documentary Style",
    7: "Testimonial", 8: "Company Introduction", 9: "Social Media Short",
    10: "Webinar/Presentation"
}

TONES = ["professional", "casual", "enthusiastic", "authoritative", "friendly", "humorous"]

class VideoScriptGenerator:
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.video_type = None
        self.tone = "professional"
        self.target_audience = "general"
        self.brand_voice = None
    
    def set_video_type(self, type_id: int):
        if type_id in VIDEO_TYPES:
            self.video_type = VIDEO_TYPES[type_id]
            return True
        return False
    
    def generate_script(self, topic: str, duration_minutes: int = 5) -> dict:
        prompt = f"""Create a complete video script for a {duration_minutes}-minute {self.video_type or 'video'}.

Topic: {topic}
Tone: {self.tone}
Target Audience: {self.target_audience}
{f'Brand Voice: {self.brand_voice}' if self.brand_voice else ''}

Return JSON:
{{
    "title": "video title",
    "hook": "attention-grabbing opening (first 5 seconds)",
    "introduction": {{
        "duration": "30 seconds",
        "narration": "script text",
        "visual_notes": "what to show"
    }},
    "main_sections": [
        {{
            "section_title": "section name",
            "duration": "time",
            "narration": "script text",
            "visual_notes": "visual suggestions",
            "b_roll_ideas": ["b-roll suggestions"],
            "graphics_needed": ["on-screen text/graphics"]
        }}
    ],
    "call_to_action": {{
        "narration": "CTA script",
        "visual_notes": "CTA visuals"
    }},
    "outro": {{
        "narration": "closing script",
        "end_screen_suggestions": ["end screen elements"]
    }},
    "total_word_count": 500,
    "estimated_duration": "{duration_minutes} minutes",
    "key_messages": ["main takeaways"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def generate_hook(self, topic: str, style: str = "question") -> dict:
        prompt = f"""Create 5 different video hooks for: {topic}

Hook styles needed:
1. Question hook - Start with an intriguing question
2. Statistic hook - Start with a surprising fact
3. Story hook - Start with a mini story
4. Problem hook - Highlight a pain point
5. Bold statement - Make a bold claim

Return JSON:
{{
    "hooks": [
        {{
            "style": "hook style",
            "text": "hook script (5-10 seconds)",
            "visual_suggestion": "what to show"
        }}
    ],
    "recommended": "which hook is best for this topic"
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def generate_storyboard(self, script: str) -> dict:
        prompt = f"""Create a storyboard breakdown for this video script.

Script:
{script}

Return JSON:
{{
    "scenes": [
        {{
            "scene_number": 1,
            "duration": "5 seconds",
            "shot_type": "wide/medium/close-up/b-roll",
            "visual_description": "what camera shows",
            "audio": "narration/music/sfx",
            "text_overlay": "on-screen text if any",
            "transition": "cut/fade/dissolve"
        }}
    ],
    "total_scenes": 10,
    "production_notes": ["filming notes"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def generate_social_variations(self, script: str) -> dict:
        prompt = f"""Adapt this video script for different social platforms.

Original Script:
{script}

Create versions for:
1. YouTube (full length)
2. TikTok/Reels (15-60 seconds)
3. LinkedIn (professional, 2 minutes)
4. Twitter/X (30-second teaser)

Return JSON:
{{
    "youtube": {{
        "title": "optimized title",
        "description": "video description",
        "tags": ["relevant tags"],
        "script_adaptation": "any script changes"
    }},
    "tiktok_reels": {{
        "hook": "attention-grabbing start",
        "condensed_script": "short version script",
        "trending_elements": ["trends to incorporate"]
    }},
    "linkedin": {{
        "professional_angle": "business focus",
        "script_adaptation": "professional version"
    }},
    "twitter": {{
        "teaser_script": "30-second teaser",
        "tweet_copy": "tweet to accompany"
    }}
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def generate_thumbnail_ideas(self, topic: str, title: str) -> dict:
        prompt = f"""Generate thumbnail ideas for a video about: {topic}
Title: {title}

Return JSON:
{{
    "thumbnail_concepts": [
        {{
            "concept": "description",
            "text_overlay": "thumbnail text (3-5 words max)",
            "color_scheme": "colors to use",
            "emotion_to_convey": "feeling",
            "elements": ["visual elements to include"]
        }}
    ],
    "best_practices": ["thumbnail tips"],
    "a_b_test_suggestions": ["variations to test"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def generate_seo_package(self, topic: str, script: str) -> dict:
        prompt = f"""Create an SEO package for a video about: {topic}

Script excerpt:
{script[:500]}

Return JSON:
{{
    "titles": ["5 title variations with keywords"],
    "description": "500-character description with keywords",
    "tags": ["20 relevant tags"],
    "hashtags": ["10 hashtags for social"],
    "keywords": {{
        "primary": ["main keywords"],
        "secondary": ["supporting keywords"],
        "long_tail": ["long-tail phrases"]
    }},
    "chapters": [
        {{
            "timestamp": "0:00",
            "title": "chapter title"
        }}
    ]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def improve_script(self, script: str, feedback: str) -> str:
        prompt = f"""Improve this video script based on the feedback.

Original Script:
{script}

Feedback:
{feedback}

Provide the improved script with:
1. Better engagement
2. Clearer messaging
3. Stronger call-to-action
4. More visual variety suggestions"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    
    def generate_series(self, topic: str, num_episodes: int = 5) -> dict:
        prompt = f"""Plan a {num_episodes}-part video series on: {topic}

Return JSON:
{{
    "series_title": "series name",
    "series_description": "overall series description",
    "target_audience": "who this is for",
    "episodes": [
        {{
            "episode_number": 1,
            "title": "episode title",
            "topic_focus": "main topic",
            "key_points": ["points to cover"],
            "duration": "estimated length",
            "hook_idea": "episode-specific hook"
        }}
    ],
    "series_arc": "how episodes connect",
    "cross_promotion": "how to promote between episodes"
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def _parse_json(self, content: str) -> dict:
        try:
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(content[start:end])
        except:
            pass
        return {"raw_response": content}


def display_menu():
    table = Table(title="🎬 Video Script Generator", show_header=True)
    table.add_column("Option", style="cyan", width=6)
    table.add_column("Feature", style="green")
    table.add_column("Description", style="white")
    
    table.add_row("1", "Generate Script", "Create complete video script")
    table.add_row("2", "Generate Hooks", "Create attention-grabbing openings")
    table.add_row("3", "Storyboard", "Create visual storyboard")
    table.add_row("4", "Social Versions", "Adapt for different platforms")
    table.add_row("5", "Thumbnails", "Generate thumbnail ideas")
    table.add_row("6", "SEO Package", "Create titles, tags, descriptions")
    table.add_row("7", "Improve Script", "Enhance existing script")
    table.add_row("8", "Plan Series", "Create multi-episode series")
    table.add_row("9", "Settings", "Set video type, tone, audience")
    table.add_row("0", "Exit", "Close application")
    
    console.print(table)


def main():
    console.print(Panel.fit(
        "[bold blue]🎬 Automated Video Script Generator[/bold blue]\n"
        "[green]AI-Powered Script Creation for Any Video[/green]\n"
        "[dim]Author: Pranay M[/dim]",
        border_style="blue"
    ))
    
    generator = VideoScriptGenerator()
    
    while True:
        display_menu()
        console.print(f"[dim]Type: {generator.video_type or 'Not set'} | Tone: {generator.tone} | Audience: {generator.target_audience}[/dim]")
        
        choice = Prompt.ask("\n[cyan]Select option[/cyan]", default="0")
        
        if choice == "0":
            console.print("[yellow]Goodbye! Happy creating! 🎬[/yellow]")
            break
        
        elif choice == "9":
            console.print("\n[bold]Video Types:[/bold]")
            for tid, name in VIDEO_TYPES.items():
                console.print(f"  {tid}: {name}")
            type_id = IntPrompt.ask("Select type", default=1)
            generator.set_video_type(type_id)
            generator.tone = Prompt.ask("Tone", choices=TONES, default="professional")
            generator.target_audience = Prompt.ask("Target audience", default="general")
            generator.brand_voice = Prompt.ask("Brand voice (optional)", default="")
            console.print("[green]✓ Settings updated[/green]")
            continue
        
        if choice == "1":
            topic = Prompt.ask("Video topic")
            duration = IntPrompt.ask("Duration (minutes)", default=5)
            with console.status("[bold green]Generating script..."):
                script = generator.generate_script(topic, duration)
            console.print(Panel(Markdown(f"```json\n{json.dumps(script, indent=2)}\n```"),
                               title="📝 Video Script"))
        
        elif choice == "2":
            topic = Prompt.ask("Video topic")
            with console.status("[bold green]Creating hooks..."):
                hooks = generator.generate_hook(topic)
            console.print(Panel(Markdown(f"```json\n{json.dumps(hooks, indent=2)}\n```"),
                               title="🎣 Video Hooks"))
        
        elif choice == "3":
            console.print("[dim]Paste script (end with 'EOF'):[/dim]")
            lines = []
            while True:
                line = input()
                if line.strip() == "EOF":
                    break
                lines.append(line)
            with console.status("[bold green]Creating storyboard..."):
                storyboard = generator.generate_storyboard("\n".join(lines))
            console.print(Panel(Markdown(f"```json\n{json.dumps(storyboard, indent=2)}\n```"),
                               title="🎞️ Storyboard"))
        
        elif choice == "4":
            console.print("[dim]Paste script (end with 'EOF'):[/dim]")
            lines = []
            while True:
                line = input()
                if line.strip() == "EOF":
                    break
                lines.append(line)
            with console.status("[bold green]Creating platform versions..."):
                versions = generator.generate_social_variations("\n".join(lines))
            console.print(Panel(Markdown(f"```json\n{json.dumps(versions, indent=2)}\n```"),
                               title="📱 Platform Versions"))
        
        elif choice == "5":
            topic = Prompt.ask("Video topic")
            title = Prompt.ask("Video title")
            with console.status("[bold green]Generating thumbnails..."):
                thumbnails = generator.generate_thumbnail_ideas(topic, title)
            console.print(Panel(Markdown(f"```json\n{json.dumps(thumbnails, indent=2)}\n```"),
                               title="🖼️ Thumbnail Ideas"))
        
        elif choice == "6":
            topic = Prompt.ask("Video topic")
            script = Prompt.ask("Brief script/description")
            with console.status("[bold green]Creating SEO package..."):
                seo = generator.generate_seo_package(topic, script)
            console.print(Panel(Markdown(f"```json\n{json.dumps(seo, indent=2)}\n```"),
                               title="🔍 SEO Package"))
        
        elif choice == "7":
            console.print("[dim]Paste script (end with 'EOF'):[/dim]")
            lines = []
            while True:
                line = input()
                if line.strip() == "EOF":
                    break
                lines.append(line)
            feedback = Prompt.ask("What should be improved?")
            with console.status("[bold green]Improving script..."):
                improved = generator.improve_script("\n".join(lines), feedback)
            console.print(Panel(Markdown(improved), title="✨ Improved Script"))
        
        elif choice == "8":
            topic = Prompt.ask("Series topic")
            episodes = IntPrompt.ask("Number of episodes", default=5)
            with console.status("[bold green]Planning series..."):
                series = generator.generate_series(topic, episodes)
            console.print(Panel(Markdown(f"```json\n{json.dumps(series, indent=2)}\n```"),
                               title="📺 Series Plan"))
        
        console.print("\n" + "="*50)


if __name__ == "__main__":
    main()
