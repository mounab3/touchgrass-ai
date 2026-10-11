
# Import modules for environment settings, caching, logging, web requests, and the app.
import os  # Reads environment variables such as the API key and server port.
import time  # Tracks cache age and pauses before retrying a rate-limited request.
import traceback  # Prints detailed errors to the terminal for debugging.
import gradio as gr  # Builds the web interface.
import requests  # Sends HTTP requests to Open-Meteo.
from dotenv import load_dotenv  # Loads private settings from the local .env file.
from openai import OpenAI  # Connects to OpenRouter using the OpenAI-compatible API.

# Load environment variables from .env when running locally.
load_dotenv()

# Read the API key privately; configure the same variable in Render's Environment settings.
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Select the open-weight AI model used to generate missions through OpenRouter.
MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"

# Create the AI client only when an API key is available.
client = None
if OPENROUTER_API_KEY:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )


# Store successful weather results in memory for 10 minutes.
_weather_cache = {}
WEATHER_CACHE_SECONDS = 600


def get_weather(city):
    """Find a city and retrieve its current weather from Open-Meteo."""

    # Normalize the city name for caching and remove extra spaces.
    city = city.strip()
    cache_key = city.casefold()

    # Reuse recent weather data instead of sending repeated requests.
    cached = _weather_cache.get(cache_key)
    if cached and time.time() - cached["time"] < WEATHER_CACHE_SECONDS:
        print(f"Using cached weather for {city}", flush=True)
        return cached["summary"]

    def fetch_json(url, params):
        """Request JSON data and retry once after a rate-limit response."""

        # Allow at most two attempts so a temporary 429 can recover.
        for attempt in range(2):
            response = requests.get(url, params=params, timeout=15)

            # Wait briefly before retrying when Open-Meteo limits requests.
            if response.status_code == 429 and attempt == 0:
                retry_after = response.headers.get("Retry-After", "2")

                try:
                    delay = min(max(float(retry_after), 1), 5)
                except ValueError:
                    delay = 2

                print(
                    f"Open-Meteo rate limit reached; retrying in {delay} seconds.",
                    flush=True,
                )
                time.sleep(delay)
                continue

            # Raise an error for unsuccessful responses and return parsed JSON.
            response.raise_for_status()
            return response.json()

        raise RuntimeError("Weather request failed after retry.")

    # Find the city's coordinates using Open-Meteo's geocoding service.
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    geocoding_data = fetch_json(
        geocoding_url,
        {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        },
    )

    # Stop if the service cannot find a matching city.
    places = geocoding_data.get("results", [])
    if not places:
        return None

    # Extract the first matching city's name and coordinates.
    place = places[0]
    latitude = place["latitude"]
    longitude = place["longitude"]

    # Request current weather conditions for the selected coordinates.
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_data = fetch_json(
        weather_url,
        {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,apparent_temperature,"
                "precipitation,wind_speed_10m,weather_code"
            ),
            "timezone": "auto",
        },
    )

    # Extract the current weather measurements from the API response.
    current = weather_data["current"]

    # Convert Open-Meteo weather codes into readable descriptions.
    weather_descriptions = {
        0: "clear sky",
        1: "mainly clear",
        2: "partly cloudy",
        3: "overcast",
        45: "foggy",
        48: "foggy with depositing rime",
        51: "light drizzle",
        53: "moderate drizzle",
        55: "dense drizzle",
        61: "light rain",
        63: "moderate rain",
        65: "heavy rain",
        71: "light snow",
        73: "moderate snow",
        75: "heavy snow",
        80: "light rain showers",
        81: "moderate rain showers",
        82: "heavy rain showers",
        95: "thunderstorm",
        96: "thunderstorm with hail",
        99: "thunderstorm with heavy hail",
    }

    # Use a fallback description if a code is missing from the dictionary.
    code = current["weather_code"]
    description = weather_descriptions.get(
        code, "conditions not classified"
    )

    # Combine the measurements into a concise summary for the AI prompt.
    weather_summary = (
        f"Weather in {place['name']}, {place.get('country', '')}: "
        f"{description}; "
        f"temperature {current['temperature_2m']}°C; "
        f"feels like {current['apparent_temperature']}°C; "
        f"precipitation {current['precipitation']} mm; "
        f"wind speed {current['wind_speed_10m']} km/h."
    )

    # Save successful results with a timestamp so they can be reused.
    _weather_cache[cache_key] = {
        "time": time.time(),
        "summary": weather_summary,
    }

    return weather_summary


def generate_mission(location, time_available, energy, interests):
    """Generate a personalized outdoor mission using AI and current weather."""

    # Require a city or area before making external requests.
    if not location or not location.strip():
        return "📍 Please enter your city or area first."

    # Avoid an unnecessary request if the API key is missing.
    if client is None:
        return "⚠️ OpenRouter API key is missing. Check your configuration."

    # Convert the selected interests into text for the AI prompt.
    selected_interests = (
        ", ".join(interests) if interests else "Anything outdoors"
    )

    try:
        # Retrieve current conditions before asking the AI for a mission.
        weather = get_weather(location.strip())

        # Explain how to correct the input if no matching city was found.
        if weather is None:
            return (
                "📍 I couldn't find that city. "
                "Please check the spelling and try again."
            )

        # Give the AI the user's preferences, real weather, and safety rules.
        prompt = f"""
You are TouchGrass AI, a friendly outdoor activity coach.

Create ONE personalized outdoor mission using these details:
- City: {location}
- Available time: {time_available}
- Energy level: {energy}
- Interests: {selected_interests}
- Current weather data: {weather}

Instructions:
- Use the supplied weather data when choosing an activity.
- Do not invent weather information.
- If conditions are rainy, stormy, very windy, or otherwise unsuitable,
  suggest a safer sheltered alternative or recommend waiting.
- Keep the mission safe, affordable, and realistic.
- Match the user's time, energy, and interests.
- Give it a creative title and 2 to 4 simple steps.
- End with one encouraging sentence.
- Be concise, friendly, and use a few suitable emojis.
- Do not invent specific venues, landmarks, walking routes, or local facts.
- If you cannot verify a location, suggest a general outdoor activity instead.
- Prioritize public, accessible places and personal safety.
- Never encourage users to go somewhere isolated or unsafe.
"""

        # Send the prompt to the selected model through OpenRouter.
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.7,
            max_tokens=400,
        )

        # Extract the generated mission from the model's response.
        mission = response.choices[0].message.content

        # Handle an empty AI response without displaying a blank result.
        if not mission:
            return "🌱 The AI returned no text. Please try again."

        # Display the mission together with the weather information used.
        return f"{mission}\n\n---\n🌦️ **Weather used:** {weather}"

    except Exception as e:
        # Print the underlying exception so it appears in Render's logs.
        print(f"Mission generation failed: {e!r}", flush=True)
        traceback.print_exc()

        # Show a friendly message instead of leaving the output blank.
        return (
            "⚠️ I couldn't generate your mission. "
            "Please try again in a moment."
        )


# Build the page and its input controls using Gradio Blocks.
with gr.Blocks(title="TouchGrass AI") as demo:

    # Introduce the app and explain what it does.
    gr.Markdown(
        """
        # 🌿 TouchGrass AI
        ### Your little push to step outside.

        Get a personalized outdoor mission based on your interests,
        available time, energy, and current weather.
        """
    )

    # Collect the city or area used for the weather lookup.
    location = gr.Textbox(
        label="📍 Your city or area",
        placeholder="e.g., Tunis",
    )

    # Let users choose how long their outdoor activity can last.
    time_available = gr.Radio(
        choices=["10 minutes", "20 minutes", "30 minutes", "1 hour"],
        label="⏱️ How much time do you have?",
        value="20 minutes",
    )

    # Let users select the amount of energy they have.
    energy = gr.Radio(
        choices=["Low", "Medium", "High"],
        label="⚡ What's your energy level?",
        value="Medium",
    )

    # Allow users to select multiple activity interests.
    interests = gr.Dropdown(
        choices=[
            "Nature",
            "Walking",
            "Photography",
            "Learning something new",
            "Relaxing",
            "Exploring my city",
        ],
        label="💚 What sounds fun?",
        multiselect=True,
    )

    # Create the button that starts mission generation.
    generate_button = gr.Button(
        "🌱 Generate my mission",
        variant="primary",
    )

    # Display the generated mission as formatted Markdown.
    output = gr.Markdown()

    # Pass the selected inputs to generate_mission when clicked.
    generate_button.click(
        fn=generate_mission,
        inputs=[location, time_available, energy, interests],
        outputs=output,
    )

    # Credit the weather-data provider on the page.
    gr.Markdown(
        "Weather data provided by [Open-Meteo](https://open-meteo.com/)."
    )


if __name__ == "__main__":
    # Use localhost locally and Render's required network binding when deployed.
    is_render = bool(os.environ.get("PORT"))
    demo.launch(
        server_name="0.0.0.0" if is_render else "127.0.0.1",
        server_port=int(os.environ.get("PORT", 7860)),
    )

