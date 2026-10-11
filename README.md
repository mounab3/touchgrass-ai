 <div align="center">

# 🌿 TouchGrass AI

### Less scrolling. More exploring. ☀️

**Your AI-powered nudge to step outside, touch grass, and make the most of your day.**

🌱 Get outside · 🌤️ Check the weather · 🗺️ Discover your next little adventure

<br>

<a href="https://touchgrass-ai-w61h.onrender.com">
  <img src="https://img.shields.io/badge/☀️_TRY_THE_LIVE_DEMO-245C36?style=for-the-badge&logo=render&logoColor=white" alt="Try the live demo">
</a>
<a href="https://github.com/mounab3/touchgrass-ai">
  <img src="https://img.shields.io/badge/🌿_EXPLORE_THE_CODE-3C8D5A?style=for-the-badge&logo=github&logoColor=white" alt="Explore the code">
</a>
<a href="#-how-it-works">
  <img src="https://img.shields.io/badge/🍃_HOW_IT_WORKS-D8F3A5?style=for-the-badge&labelColor=245C36" alt="How it works">
</a>

<br><br>

<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Gradio-FFB86B?style=flat-square&logo=gradio&logoColor=222222" alt="Gradio">
<img src="https://img.shields.io/badge/Open--Weight_AI-245C36?style=flat-square&logoColor=white" alt="Open-weight AI">
<img src="https://img.shields.io/badge/Weather-Open--Meteo-79BCE8?style=flat-square" alt="Open-Meteo">
<img src="https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=flat-square&logo=render&logoColor=222222" alt="Deployed on Render">

</div>

---

<div align="center">

> 🍃 **A little fresh air can change your whole day.**
>


</div>

## 🌼 What is TouchGrass AI?

TouchGrass AI is a small AI-powered project with one simple mission: **help people spend less time scrolling and more time experiencing the real world.**

Tell it your city, how much time you have, your energy level, and what you enjoy. It retrieves current weather information and uses AI to suggest a personalized outdoor mission that fits your day. 🌳

## ☀️ Try the Live Demo

🌐 **Website:** [Open TouchGrass AI](https://touchgrass-ai-w61h.onrender.com)

The application is deployed on **Render**, making it accessible through a public link without requiring visitors to clone the repository or install anything.


## 🌱 How it works

<div align="center">

| 🍀 You tell | 🌤️ It checks | 🌻 You get |
|:---:|:---:|:---:|
| Your city, time, energy and interests | Current weather conditions | A personalized outdoor mission |

</div>

### ✨ Features

- 🌍 **Your location:** Enter your city to retrieve weather information for your area.
- 🌦️ **Live weather:** Fetch current weather data using the Open-Meteo API.
- 🧠 **AI-generated missions:** Receive creative activity ideas tailored to your preferences.
- ⏳ **Time-friendly suggestions:** Find something to do even when you only have a few minutes.
- 🔋 **Energy-aware ideas:** Get suggestions that suit how energetic or relaxed you feel.
- 🎨 **Interactive interface:** Enter your preferences and discover your next mission.
- 🌧️ **Weather-conscious suggestions:** Unfavorable conditions can prompt safer alternatives.

## 🍃 A Little Preview

<div align="center">

<!-- Add these screenshots to the screenshots/ folder to display them here. -->

<img src="screenshots/touchgrass-home.png" alt="TouchGrass AI home screen" width="85%">

*Choose your city, available time, energy level, and interests.*

<br><br>

<img src="screenshots/touchgrass-mission.png" alt="An AI-generated outdoor mission" width="85%">

*Get your personalized mission and take the first step outside!*

</div>

## 🌳 The Technology

<div align="center">

| Technology | What it does |
|:---|:---|
| 🐍 **Python** | Application logic and data processing |
| 🎨 **Gradio** | Interactive web interface |
| 🌤️ **Open-Meteo API** | City geocoding and current weather information |
| 🤖 **OpenRouter API** | Connects the app to the selected AI model |
| 🌿 **NVIDIA Nemotron 3 Ultra** | Generates personalized outdoor activity suggestions |
| 🔐 **python-dotenv** | Loads local configuration and API keys from environment variables |
| 🚀 **Render** | Hosts the public web application |

</div>

### 💚 Why Open-Weight AI?

TouchGrass AI explores how open-weight models can be used to create practical applications that encourage healthier relationships with technology.

Instead of building another tool designed to keep people scrolling, this project uses AI to help turn a few preferences into a reason to go outside.


## 🚀 Get Started

Want to explore or run your own copy of TouchGrass AI? Follow these steps.

### 1. 🌱 Clone the repository

```bash
git clone https://github.com/mounab3/touchgrass-ai.git
cd touchgrass-ai
```

### 2. 🪴 Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. 🌿 Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. 🔑 Configure your API key

Create a file named `.env` in the project folder:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your own OpenRouter API key.


### 5. ☀️ Start your adventure

```bash
python app.py
```

Open the local URL displayed in your terminal, usually:

[http://127.0.0.1:7860](http://127.0.0.1:7860)

That's it! You're ready to generate your first outdoor mission. 🌻

## 🗺️ Project Structure

```text
touchgrass-ai/
│
├── app.py              # Main application and AI logic
├── requirements.txt    # Python dependencies
├── .env                # Private API key (local only)
├── .gitignore          # Files Git should ignore
├── README.md           # Project documentation
│
└── screenshots/        # Optional app screenshots
    ├── touchgrass-home.png
    └── touchgrass-mission.png
```

## 🌻 What's Next?

TouchGrass AI is a learning project, and there is plenty of room to grow!

- [ ] 🌿 Improve activity suggestions and personalization.
- [ ] 🗺️ Explore more reliable local recommendations.
- [ ] 📱 Make the interface even friendlier on mobile.
- [ ] 🌞 Test the app with more users and different weather conditions.
- [ ] 🌳 Add more ways to encourage small, screen-free adventures.
- [ ] 🌦️ Improve resilience when external APIs are temporarily unavailable.

## 🤝 Contributing

Have an idea that could help people spend more time outside?

You're welcome to explore the code, suggest improvements, or open an issue. Small contributions can grow into something meaningful. 🌱

1. Fork the repository.
2. Create a branch for your changes.
3. Make your improvements.
4. Submit a pull request.

## 💌 

I built TouchGrass AI as part of my journey exploring open-source AI and practical software development.

I wanted to experiment with a different use of AI: creating something that encourages people to disconnect from their screens and reconnect with the world around them.

🌿 Every small step outside counts.

---

<div align="center">

### 🌞 Made with curiosity, code, and a little love for the outdoors.

**TouchGrass AI · Less scrolling. More exploring.** 🍃

[☀️ Try the Live Demo](https://touchgrass-ai-w61h.onrender.com) · [🌿 View the Source Code](https://github.com/mounab3/touchgrass-ai)

</div>