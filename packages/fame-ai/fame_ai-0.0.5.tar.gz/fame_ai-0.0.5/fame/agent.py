from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import os
import random
from typing import Optional, Dict, List, Any
from fame.integrations.replicate_integration import ReplicateIntegration
from fame.integrations.openrouter_integration import OpenRouterIntegration
from fame.integrations.twitter_integration import TwitterIntegration
from fame.core.facets_of_personality import FacetsOfPersonality
from fame.core.abilities_and_knowledge import AbilitiesAndKnowledge
from fame.core.mood_and_emotions import MoodAndEmotions
from .utils.tweet_validator import TweetValidator
from .utils.path_utils import resolve_profile_path
from dotenv import load_dotenv
from pathlib import Path


class Agent:
    def __init__(
        self,
        env_file: str,
        facets_of_personality: str,
        abilities_knowledge: str,
        mood_emotions: str,
        environment_execution: list,
        profile_image_path: Optional[str] = None,
    ):
        """Initialize the agent with its core components."""
        # Load environment variables
        load_dotenv(env_file)

        # Initialize integrations
        self.openrouter_integration = OpenRouterIntegration(
            api_key=os.getenv("OPENROUTER_API_KEY")
        )

        # Initialize core components
        self.facets = FacetsOfPersonality(
            description=facets_of_personality, llm=self.openrouter_integration
        )
        self.abilities = AbilitiesAndKnowledge(abilities_knowledge)
        self.mood = MoodAndEmotions(mood_emotions)

        # Store profile image path
        self.profile_image_path = profile_image_path or os.getenv("PROFILE_IMAGE_PATH")

        # Initialize Twitter integration with credentials from env
        self.twitter_integration = TwitterIntegration(
            consumer_key=os.getenv("X_CONSUMER_KEY"),
            consumer_secret=os.getenv("X_CONSUMER_SECRET"),
            access_token=os.getenv("X_ACCESS_TOKEN"),
            access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET"),
        )

        # Initialize other integrations
        self.replicate_integration = ReplicateIntegration(
            api_key=os.getenv("REPLICATE_API_KEY")
        )

        # Initialize utilities
        self.tweet_validator = TweetValidator()

        # Set up environment execution
        self.environment = environment_execution

    def post_tweet(self, instruction: str) -> Dict[str, Any]:
        """Post a text-only tweet based on the given instruction."""
        try:
            print("\nGenerating tweet content from instruction...")

            # Get personality context
            personality = self.facets.get_personality_context()
            abilities = self.abilities.get_knowledge_context()
            mood = self.mood.get_mood_context()

            print("\nBuilding prompt with personality context...")
            # Build the prompt with personality context
            prompt = (
                f"You are a social media personality with these traits:\n"
                f"- Personality: {personality}\n"
                f"- Knowledge & Abilities: {abilities}\n"
                f"- Current Mood: {mood}\n\n"
                f"Write a concise tweet following this instruction:\n{instruction}\n\n"
                f"Requirements:\n"
                f"1. MUST be under 280 characters (including spaces and emojis)\n"
                f"2. Be engaging and authentic to your personality\n"
                f"3. Use clear, concise language\n"
                f"4. Include 1-2 relevant emojis\n"
                f"5. Add 1-2 relevant hashtags\n\n"
                f"Focus on the most important point and keep it brief."
            )

            print("\nGenerating tweet text using OpenRouter...")
            # Generate tweet text
            tweet_text = self.openrouter_integration.generate_text(prompt=prompt)
            if not tweet_text:
                print("Failed to generate tweet text")
                return {
                    "status": "failed",
                    "message": "Failed to generate tweet text",
                }

            print(f"\nGenerated tweet text: {tweet_text}")

            # Clean and validate the tweet
            cleaned_tweet = self.tweet_validator.clean_tweet_text(tweet_text)
            is_valid, validation_details = self.tweet_validator.validate_tweet(
                cleaned_tweet
            )

            # If tweet is too long, try to generate a shorter version
            if not is_valid and "exceeds 280 characters" in validation_details:
                print("\nTweet too long, generating shorter version...")
                shorter_prompt = (
                    f"{prompt}\n\n"
                    f"IMPORTANT: Your previous response was too long. "
                    f"Make it MUCH shorter while keeping the key message. "
                    f"Use shorter words and fewer details. "
                    f"Current length: {len(cleaned_tweet)}, needs to be under 280."
                )

                tweet_text = self.openrouter_integration.generate_text(
                    prompt=shorter_prompt
                )
                if tweet_text:
                    cleaned_tweet = self.tweet_validator.clean_tweet_text(tweet_text)
                    is_valid, validation_details = self.tweet_validator.validate_tweet(
                        cleaned_tweet
                    )

            if not is_valid:
                print(f"Tweet validation failed: {validation_details}")
                return {
                    "status": "failed",
                    "message": f"Tweet validation failed: {validation_details}",
                }

            print("\nPosting tweet...")
            # Post the tweet
            result = self.twitter_integration.post_tweet(cleaned_tweet)
            print(f"Twitter API response: {result}")

            return result

        except Exception as e:
            print(f"Error in post_tweet: {str(e)}")
            return {
                "status": "failed",
                "message": f"Error posting tweet: {str(e)}",
            }

    def _generate_base_image_prompt(self, for_face_swap: bool = False) -> str:
        """Generate a base image prompt based on personality."""
        try:
            print("\nGenerating base image prompt...")

            # Get personality context
            personality = self.facets.get_personality_context()
            abilities = self.abilities.get_knowledge_context()
            mood = self.mood.get_mood_context()

            # Generate multiple scene descriptions
            scene_prompt = (
                f"Create 10 different natural, candid lifestyle photograph descriptions.\n\n"
                f"Person details:\n"
                f"Personality: {personality}\n"
                f"Knowledge & Abilities: {abilities}\n"
                f"Current Mood: {mood}\n\n"
                f"Requirements for each scene:\n"
                f"1. Start with the person's demographic details (age, gender, ethnicity)\n"
                f"2. Describe a realistic scene that shows their personality\n"
                f"3. Include what they're doing and wearing\n"
                f"4. Describe the environment and lighting\n"
                f"5. Make it feel natural and candid\n"
                f"6. No studio or posed photos\n\n"
                f"Format:\n"
                f"Begin with 'A [age] [gender] [ethnicity] person...'\n"
                f"Example: If personality mentions 'high school girl', start with 'A young female teenager...'\n\n"
                f"Return ONLY a valid JSON array of strings containing exactly 10 scene descriptions.\n"
                f"Example format:\n"
                f"[\n"
                f'  "Scene description 1 here...",\n'
                f'  "Scene description 2 here...",\n'
                f'  "Scene description 3 here..."\n'
                f"]\n\n"
                f"Ensure the output is a properly formatted JSON array. No additional text or explanation."
            )

            # Generate the scenes using LLM
            scenes_json = self.openrouter_integration.generate_text(prompt=scene_prompt)
            if not scenes_json:
                print("No response from LLM")
                return ""

            try:
                # Clean the response
                cleaned_json = scenes_json.strip()
                if not cleaned_json.startswith("["):
                    # Try to find the JSON array
                    import re

                    match = re.search(r"\[(.*?)\]", cleaned_json, re.DOTALL)
                    if match:
                        cleaned_json = match.group(0)
                    else:
                        print("Could not find JSON array in response")
                        return ""

                # Parse JSON array
                import json

                scenes = json.loads(cleaned_json)

                if not isinstance(scenes, list) or len(scenes) == 0:
                    print("Invalid scenes format or empty list")
                    return ""

                # Randomly select one scene
                import random

                selected_scene = random.choice(scenes)

                print(f"\nSelected scene from {len(scenes)} options: {selected_scene}")

                # Add technical notes for face swapping and photography
                if for_face_swap:
                    selected_scene += (
                        "\n\nPhotography setup: Shot with a professional DSLR camera, 85mm portrait lens at f/2.8. "
                        "Natural window lighting from the front-left, supplemented with a soft fill light. "
                        "Camera positioned at eye level, subject's face at 3/4 angle. "
                        "Sharp focus on facial features, subtle background blur. "
                        "High-end color grading, ultra-realistic photographic style, 4K resolution. "
                        "Absolutely no artistic filters, no anime style, no illustration effects. "
                        "This must look like a professional photograph taken with high-end equipment."
                    )

                return selected_scene

            except json.JSONDecodeError as e:
                print(f"Failed to parse scenes JSON: {str(e)}")
                print(f"Raw response: {scenes_json}")
                return ""

        except Exception as e:
            print(f"Error generating base image prompt: {str(e)}")
            return ""

    def _generate_image_prompt(self, for_face_swap: bool = False) -> str:
        """Generate a prompt for image generation."""
        try:
            # Get personality context
            personality = self.facets.get_personality_context()

            # Generate multiple scene descriptions
            print("\nGenerating diverse scene options...")
            scene_prompt = (
                f"You are a scene description generator. Generate 10 different photo scene descriptions "
                f"for someone with this personality:\n{personality}\n\n"
                f"Requirements for each scene:\n"
                f"1. Natural, candid moment\n"
                f"2. Show their interests and personality\n"
                f"3. Include environmental details\n"
                f"4. Each scene must be unique and different\n"
                f"5. Maximum 100 words per scene\n"
                f"6. Subject's face must be clearly visible\n"
                f"7. Natural front-facing or 3/4 angle of face\n"
                f"8. Well-lit facial features\n"
                f"9. Professional camera quality\n\n"
                f"Return ONLY a valid JSON array of strings containing exactly 10 scene descriptions.\n"
                f"Example format:\n"
                f"[\n"
                f'  "Scene description 1 here...",\n'
                f'  "Scene description 2 here...",\n'
                f'  "Scene description 3 here..."\n'
                f"]\n\n"
                f"Ensure the output is a properly formatted JSON array. No additional text or explanation."
            )

            # Get scenes from LLM
            scenes_json = self.openrouter_integration.generate_text(prompt=scene_prompt)
            if not scenes_json:
                print("No response from LLM")
                return ""

            try:
                # Clean the response
                cleaned_json = scenes_json.strip()
                if not cleaned_json.startswith("["):
                    # Try to find the JSON array
                    import re

                    match = re.search(r"\[(.*?)\]", cleaned_json, re.DOTALL)
                    if match:
                        cleaned_json = match.group(0)
                    else:
                        print("Could not find JSON array in response")
                        return ""

                # Parse JSON array
                import json

                scenes = json.loads(cleaned_json)

                if not isinstance(scenes, list) or len(scenes) == 0:
                    print("Invalid scenes format or empty list")
                    return ""

                # Randomly select one scene
                import random

                selected_scene = random.choice(scenes)

                print(f"\nSelected scene from {len(scenes)} options: {selected_scene}")

                # Add technical notes for face swapping and photography
                if for_face_swap:
                    selected_scene += (
                        "\n\nPhotography setup: Shot with a professional DSLR camera, 85mm portrait lens at f/2.8. "
                        "Natural window lighting from the front-left, supplemented with a soft fill light. "
                        "Camera positioned at eye level, subject's face at 3/4 angle. "
                        "Sharp focus on facial features, subtle background blur. "
                        "High-end color grading, ultra-realistic photographic style, 4K resolution. "
                        "Absolutely no artistic filters, no anime style, no illustration effects. "
                        "This must look like a professional photograph taken with high-end equipment."
                    )

                return selected_scene

            except json.JSONDecodeError as e:
                print(f"Failed to parse scenes JSON: {str(e)}")
                print(f"Raw response: {scenes_json}")
                return ""

        except Exception as e:
            print(f"Error generating image prompt: {str(e)}")
            return ""

    def post_image_tweet(
        self, prompt: str = "", tweet_text: str = "", use_face_swap: bool = False
    ) -> Dict[str, Any]:
        """Generate and post a tweet with an image."""
        try:
            # Verify face swap requirements
            if use_face_swap:
                if not self.profile_image_path:
                    return {
                        "status": "failed",
                        "message": "Face swap requested but no profile image path provided",
                    }
                if not os.path.exists(self.profile_image_path):
                    return {
                        "status": "failed",
                        "message": f"Profile image not found at: {self.profile_image_path}",
                    }
                print(f"\nUsing profile image for face swap: {self.profile_image_path}")

            # Generate image prompt if not provided
            if not prompt:
                prompt = self._generate_image_prompt(for_face_swap=use_face_swap)
                if not prompt:
                    return {
                        "status": "failed",
                        "message": "Failed to generate image prompt",
                    }

            # Generate image
            print("\nGenerating image...")
            image_path = self.replicate_integration.generate_image(prompt=prompt)
            if not image_path:
                return {
                    "status": "failed",
                    "message": "Failed to generate image",
                }

            # Apply face swap with better logging
            if use_face_swap and self.profile_image_path:
                print("\nApplying face swap...")
                print(f"Base image: {image_path}")
                print(f"Face image: {self.profile_image_path}")
                swapped_image = self.replicate_integration.face_swap(
                    base_image_path=image_path, face_image_path=self.profile_image_path
                )
                if swapped_image:
                    print(f"Face swap successful, new image: {swapped_image}")
                    image_path = swapped_image
                else:
                    print("Face swap failed, using original image")
                    print("Check if both images are valid and face is clearly visible")

            # Generate tweet text if not provided
            if not tweet_text:
                print("\nGenerating tweet text...")
                personality = self.facets.get_personality_context()
                tweet_prompt = (
                    f"Write a tweet from the first-person perspective of someone with this personality:\n"
                    f"{personality}\n\n"
                    f"They are posting about this image: {prompt}\n\n"
                    f"Requirements:\n"
                    f"1. Write in their authentic voice\n"
                    f"2. Include 1-2 relevant emojis\n"
                    f"3. Add 1-2 relevant hashtags\n"
                    f"4. Keep it under 280 characters\n"
                    f"5. Make it personal and genuine\n"
                    f"6. Write as if they took the photo themselves\n\n"
                    f"Write only the tweet, no commentary."
                )
                tweet_text = self.openrouter_integration.generate_text(
                    prompt=tweet_prompt
                )
                if not tweet_text:
                    return {
                        "status": "failed",
                        "message": "Failed to generate tweet text",
                    }

            # Clean and validate the tweet
            cleaned_tweet = self.tweet_validator.clean_tweet_text(tweet_text)
            is_valid, validation_details = self.tweet_validator.validate_tweet(
                cleaned_tweet
            )

            if not is_valid:
                print(f"Tweet validation failed: {validation_details}")
                return {
                    "status": "failed",
                    "message": f"Tweet validation failed: {validation_details}",
                }

            print("\nPosting tweet with image...")
            # Post tweet with image using post_tweet_with_media
            result = self.twitter_integration.post_tweet_with_media(
                text=cleaned_tweet, media_path=image_path
            )
            print(f"Twitter API response: {result}")

            return result

        except Exception as e:
            print(f"Error posting image tweet: {str(e)}")
            return {
                "status": "failed",
                "message": f"Error posting image tweet: {str(e)}",
            }
