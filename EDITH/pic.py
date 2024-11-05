import requests
import os
import time
from typing import List, Optional
from string import punctuation
from random import choice
from requests.exceptions import RequestException
import pyttsx3
import random



class AiForceimagger:
    """Image provider for Airforce API"""

    AVAILABLE_MODELS = [
        "flux",
        "flux-realism",
        "flux-anime",
        "flux-3d",
        "flux-disney",
        "flux-pixel",
        "flux-4o",
        "any-dark"
    ]

    def __init__(self, api_token: str = None, timeout: int = 60, proxies: dict = {}):
        """Initializes the AiForceimagger class.

        Args:
            api_token (str, optional): Your Airforce API token. If None, it will use the environment variable "AIRFORCE_API_TOKEN". Defaults to None.
            timeout (int, optional): HTTP request timeout in seconds. Defaults to 60.
            proxies (dict, optional): HTTP request proxies (socks). Defaults to {}.
        """
        self.api_endpoint = "https://api.airforce/imagine2"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.proxies.update(proxies)
        self.timeout = timeout
        self.prompt: str = "AI-generated image - webscout"
        self.image_extension: str = "png"
        self.engine = pyttsx3.init()

    def generate(
            self,
            prompt: str,
            amount: int = 1,
            additives: bool = True,
            model: str = "flux-realism",
            width: int = 768,
            height: int = 768,
            seed: Optional[int] = None,
            max_retries: int = 3,
            retry_delay: int = 5
    ) -> List[bytes]:
        """Generate image from prompt

        Args:
            prompt (str): Image description.
            amount (int, optional): Total images to be generated. Defaults to 1.
            additives (bool, optional): Try to make each prompt unique. Defaults to True.
            model (str, optional): The model to use for image generation.
                                    Defaults to "flux". Available options: "flux", "flux-realism".
            width (int, optional): Width of the generated image. Defaults to 768.
            height (int, optional): Height of the generated image. Defaults to 768.
            seed (int, optional): Seed for the random number generator. Defaults to None.
            max_retries (int, optional): Maximum number of retry attempts. Defaults to 3.
            retry_delay (int, optional): Delay between retries in seconds. Defaults to 5.

        Returns:
            List[bytes]: List of generated images as bytes.
        """
        assert bool(prompt), "Prompt cannot be null"
        assert isinstance(amount, int), f"Amount should be an integer only not {type(amount)}"
        assert amount > 0, "Amount should be greater than 0"
        assert model in self.AVAILABLE_MODELS, f"Model should be one of {self.AVAILABLE_MODELS}"

        ads = lambda: (
            ""
            if not additives
            else choice(punctuation)
                 + choice(punctuation)
                 + choice(punctuation)
                 + choice(punctuation)
                 + choice(punctuation)
        )

        self.prompt = prompt
        response = []
        for _ in range(amount):
            url = f"{self.api_endpoint}?model={model}&prompt={prompt}&size={width}:{height}"
            if seed:
                url += f"&seed={seed}"

            for attempt in range(max_retries):
                try:
                    resp = self.session.get(url, timeout=self.timeout)
                    resp.raise_for_status()
                    response.append(resp.content)
                    break
                except RequestException as e:
                    if attempt == max_retries - 1:
                        print(f"Failed to generate image after {max_retries} attempts: {e}")
                        raise
                    else:
                        print(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)

        return response

    def save(
            self,
            response: List[bytes],
            name: str = None,
            dir: str = os.getcwd(),
            filenames_prefix: str = "",
    ) -> List[str]:
        """Save generated images

        Args:
            response (List[bytes]):
            name (str, optional): Name of the image. Defaults to None.
            dir (str, optional): Directory to save the image. Defaults to os.getcwd().
            filenames_prefix (str, optional): Prefix for the filename. Defaults to "".

        Returns:
            List[str]: List of saved image filenames.
        """
        filenames = []
        for i, img in enumerate(response):
            filename = f"{filenames_prefix}{name}_{i}.{self.image_extension}" if name else f"{filenames_prefix}{i}.{self.image_extension}"
            with open(os.path.join(dir, filename), "wb") as f:
                f.write(img)
            filenames.append(filename)
        return filenames

    def speak(self, text: str):
        """Speak the given text

        Args:
            text (str): Text to speak
        """
        self.engine.say(text)
        self.engine.runAndWait()

    def generate_and_speak(self, prompt: str, **kwargs):
        """Generate image from prompt and speak the prompt

        Args:
            prompt (str): Image description
            **kwargs: Additional keyword arguments for the generate method
        """
        response = self.generate(prompt, **kwargs)
        self.speak(prompt)
        return response

    def generate_random_image(self):
        """Generate a random image"""
        models = self.AVAILABLE_MODELS
        model = random.choice(models)
        width = random.randint(100, 1000)
        height = random.randint(100, 1000)
        self.speak("What image would you like to generate?")
        prompt = input()
        response = self.generate(prompt, model=model, width=width, height=height)
        self.speak(f"I am generating a {prompt}.")
        self.speak(f"The image is a {model} model with a width of {width} and a height of {height}.")
        return response


# Example usage:
imager = AiForceimagger()
response = imager.generate_random_image()
filenames = imager.save(response, name="random_image")
print(filenames)


def img():
    class AiForceimagger:
        """Image provider for Airforce API"""

        AVAILABLE_MODELS = [
            "flux",
            "flux-realism",
            "flux-anime",
            "flux-3d",
            "flux-disney",
            "flux-pixel",
            "flux-4o",
            "any-dark"
        ]

        def __init__(self, api_token: str = None, timeout: int = 60, proxies: dict = {}):
            """Initializes the AiForceimagger class.

            Args:
                api_token (str, optional): Your Airforce API token. If None, it will use the environment variable "AIRFORCE_API_TOKEN". Defaults to None.
                timeout (int, optional): HTTP request timeout in seconds. Defaults to 60.
                proxies (dict, optional): HTTP request proxies (socks). Defaults to {}.
            """
            self.api_endpoint = "https://api.airforce/imagine2"
            self.headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
            }
            self.session = requests.Session()
            self.session.headers.update(self.headers)
            self.session.proxies.update(proxies)
            self.timeout = timeout
            self.prompt: str = "AI-generated image - webscout"
            self.image_extension: str = "png"
            self.engine = pyttsx3.init()

        def generate(
                self,
                prompt: str,
                amount: int = 1,
                additives: bool = True,
                model: str = "flux-realism",
                width: int = 768,
                height: int = 768,
                seed: Optional[int] = None,
                max_retries: int = 3,
                retry_delay: int = 5
        ) -> List[bytes]:
            """Generate image from prompt

            Args:
                prompt (str): Image description.
                amount (int, optional): Total images to be generated. Defaults to 1.
                additives (bool, optional): Try to make each prompt unique. Defaults to True.
                model (str, optional): The model to use for image generation.
                                        Defaults to "flux". Available options: "flux", "flux-realism".
                width (int, optional): Width of the generated image. Defaults to 768.
                height (int, optional): Height of the generated image. Defaults to 768.
                seed (int, optional): Seed for the random number generator. Defaults to None.
                max_retries (int, optional): Maximum number of retry attempts. Defaults to 3.
                retry_delay (int, optional): Delay between retries in seconds. Defaults to 5.

            Returns:
                List[bytes]: List of generated images as bytes.
            """
            assert bool(prompt), "Prompt cannot be null"
            assert isinstance(amount, int), f"Amount should be an integer only not {type(amount)}"
            assert amount > 0, "Amount should be greater than 0"
            assert model in self.AVAILABLE_MODELS, f"Model should be one of {self.AVAILABLE_MODELS}"

            ads = lambda: (
                ""
                if not additives
                else choice(punctuation)
                     + choice(punctuation)
                     + choice(punctuation)
                     + choice(punctuation)
                     + choice(punctuation)
            )

            self.prompt = prompt
            response = []
            for _ in range(amount):
                url = f"{self.api_endpoint}?model={model}&prompt={prompt}&size={width}:{height}"
                if seed:
                    url += f"&seed={seed}"

                for attempt in range(max_retries):
                    try:
                        resp = self.session.get(url, timeout=self.timeout)
                        resp.raise_for_status()
                        response.append(resp.content)
                        break
                    except RequestException as e:
                        if attempt == max_retries - 1:
                            print(f"Failed to generate image after {max_retries} attempts: {e}")
                            raise
                        else:
                            print(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                            time.sleep(retry_delay)

            return response

        def save(
                self,
                response: List[bytes],
                name: str = None,
                dir: str = os.getcwd(),
                filenames_prefix: str = "",
        ) -> List[str]:
            """Save generated images

            Args:
                response (List[bytes]):
                name (str, optional): Name of the image. Defaults to None.
                dir (str, optional): Directory to save the image. Defaults to os.getcwd().
                filenames_prefix (str, optional): Prefix for the filename. Defaults to "".

            Returns:
                List[str]: List of saved image filenames.
            """
            filenames = []
            for i, img in enumerate(response):
                filename = f"{filenames_prefix}{name}_{i}.{self.image_extension}" if name else f"{filenames_prefix}{i}.{self.image_extension}"
                with open(os.path.join(dir, filename), "wb") as f:
                    f.write(img)
                filenames.append(filename)
            return filenames

        def speak(self, text: str):
            """Speak the given text

            Args:
                text (str): Text to speak
            """
            pyttsx3.speak.engine.say(text)
            pyttsx3.speak.engine.runAndWait()

        def generate_and_speak(self, prompt: str, **kwargs):
            """Generate image from prompt and speak the prompt

            Args:
                prompt (str): Image description
                **kwargs: Additional keyword arguments for the generate method
            """
            response = self.speak(prompt, **kwargs)
            pyttsx3.speak(prompt)
            return response

        def generate_random_image(self):
            """Generate a random image"""
            models = self.AVAILABLE_MODELS
            model = random.choice(models)
            width = random.randint(100, 1000)
            height = random.randint(100, 1000)
            self.speak("What image would you like to generate?")
            prompt = pyttsx3.speak()
            response = self.generate(pyttsx3.speak(), model=model, width=width, height=height)
            self.speak(f"I am generating a {prompt}.")
            self.speak(f"The image is a {model} model with a width of {width} and a height of {height}.")
            return response

    # Example usage:
    imager = AiForceimagger()
    response = imager.generate_random_image()
    filenames = imager.save(response, name="random_image")
    print(filenames)
