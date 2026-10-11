
import os

import gradio as gr
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"

client = None
if OPENROUTER_API_KEY:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )


def get_weather(city):
    """Find a city and retrieve its current weather from Open-Meteo."""

    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    geocoding_response = requests.get(
        geocoding_url,
        params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        },
        timeout=15,
    )
    geocoding_response.raise_for_status()

    places = geocoding_response.json().get("results", [])

    if not places:
        return None

    place = places[0]
    latitude = place["latitude"]
    longitude = place["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_response = requests.get(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,apparent_temperature,"
                "precipitation,wind_speed_10m,weather_code"
            ),
            "timezone": "auto",
        },
        timeout=15,
    )
    weather_response.raise_for_status()

    current = weather_response.json()["current"]

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

    code = current["weather_code"]
    description = weather_descriptions.get(code, "conditions not classified")

    weather_summary = (
        f"Weather in {place['name']}, {place.get('country', '')}: "
        f"{description}; "
        f"temperature {current['temperature_2m']}°C; "
        f"feels like {current['apparent_temperature']}°C; "
        f"precipitation {current['precipitation']} mm; "
        f"wind speed {current['wind_speed_10m']} km/h."
    )

    return weather_summary


def generate_mission(location, time_available, energy, interests):
    """Generate an outdoor mission using Gemini and current weather."""

    if not location or not location.strip():
        return "📍 Please enter your city or area first."

    if client is None:
        return "⚠️ OpenRouter API key is missing. Check your .env file."

    selected_interests = (
        ", ".join(interests) if interests else "Anything outdoors"
    )

    try:
        weather = get_weather(location.strip())

        if weather is None:
            return (
                "📍 I couldn't find that city. "
                "Please check the spelling and try again."
            )

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

        mission = response.choices[0].message.content


        if not mission:
            return "🌱 The AI returned no text. Please try again."

        return f"{mission}\n\n---\n🌦️ **Weather used:** {weather}"

    except Exception as error:
        print(f"Mission generation failed: {error}")
        return (
            "⚠️ I couldn't generate your mission. "
            "Please check the technical error in your terminal."
        )


with gr.Blocks(title="TouchGrass AI") as demo:
    gr.Markdown(
        """
        # 🌿 TouchGrass AI
        ### Your little push to step outside.

        Get a personalized outdoor mission based on your interests,
        available time, energy, and current weather.
        """
    )

    location = gr.Textbox(
        label="📍 Your city or area",
        placeholder="e.g., Tunis",
    )

    time_available = gr.Radio(
        choices=["10 minutes", "20 minutes", "30 minutes", "1 hour"],
        label="⏱️ How much time do you have?",
        value="20 minutes",
    )

    energy = gr.Radio(
        choices=["Low", "Medium", "High"],
        label="⚡ What's your energy level?",
        value="Medium",
    )

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

    generate_button = gr.Button(
        "🌱 Generate my mission",
        variant="primary",
    )

    output = gr.Markdown()

    generate_button.click(
        fn=generate_mission,
        inputs=[location, time_available, energy, interests],
        outputs=output,
    )

    gr.Markdown(
        "Weather data provided by [Open-Meteo](https://open-meteo.com/)."
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
    )
