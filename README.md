# ✈️ TripCraft

### A Python-based travel itinerary planner that creates budget-friendly trip plans based on destination, duration, budget, and interests.

TripCraft is a travel itinerary planning application that generates personalized multi-day trip plans based on user preferences. It includes a terminal-based Python application and a Streamlit web interface with live weather information.

---

## 🌍 Project Overview

Planning a trip can be time-consuming, especially when balancing activities, personal interests, and expenses.

TripCraft simplifies the initial planning process by allowing users to enter:

- Destination
- Number of travel days
- Total budget in CAD
- Personal interests

The application generates a day-by-day itinerary, estimates activity, food, and transportation costs, and displays the remaining budget.

The Streamlit interface also retrieves live weather forecasts for the selected destination.

---

## ✨ Features

### Core Itinerary Planning

- 🗺️ Enter a travel destination
- 📅 Generate a multi-day itinerary
- 💰 Estimate activity, food, and transportation expenses
- 🎯 Customize activities based on interests
- 📊 Calculate the estimated trip cost
- 💵 Display remaining budget or amount over budget
- ⚠️ Show a warning when the estimated cost exceeds the budget
- 📄 Save the itinerary as a text file
- ✅ Validate user inputs

### Streamlit Web Interface

- 🌐 Interactive web interface built with Streamlit
- 🎨 Colorful and user-friendly layout
- 🌦️ Live weather forecast using Open-Meteo APIs
- 🌡️ Display daily minimum and maximum temperatures
- ☔ Display precipitation probability
- 💡 Provide weather-based travel suggestions
- 📥 Download the generated itinerary
- 📱 Responsive layout with sidebar trip inputs

---

## 🛠️ Technologies Used

- Python 3
- Streamlit
- Requests
- Open-Meteo Geocoding API
- Open-Meteo Weather API
- Lists and dictionaries
- Functions
- Loops
- Conditional statements
- Exception handling
- String formatting
- File handling
- Git and GitHub

---

## 📂 Project Structure

```text
tripcraft-python/
│
├── tripcraft.py
├── app.py
├── trip_itinerary.txt
├── README.md
├── .gitignore
└── LICENSE
```

| File | Description |
|------|-------------|
| `tripcraft.py` | Terminal-based Python itinerary planner |
| `app.py` | Streamlit web application |
| `trip_itinerary.txt` | Sample generated itinerary |
| `README.md` | Project documentation |
| `.gitignore` | Files ignored by Git |
| `LICENSE` | MIT License |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Dipika2020/tripcraft-python.git
```

### 2. Open the Project Folder

```bash
cd tripcraft-python
```

### 3. Run the Terminal Application

```bash
python tripcraft.py
```

If your system uses `python3`, run:

```bash
python3 tripcraft.py
```

### 4. Install Web Application Dependencies

```bash
pip install streamlit requests
```

If your system uses `pip3`, run:

```bash
pip3 install streamlit requests
```

### 5. Run the Streamlit Web Application

```bash
streamlit run app.py
```

The Streamlit application will open in your browser.

---

## 🧪 Example Usage

### User Input

```text
Destination: Toronto
Duration: 2 days
Budget: $250 CAD
Interests: history, food
```

### Example Terminal Result

```text
=============================================
                  TRIPCRAFT
=============================================
Destination: Toronto
Duration: 2 days
Budget: $250.00

DAY 1
---------------------------------------------
- Visit a historical landmark - $25.00
- Explore a museum - $20.00
- Food estimate - $30.00
- Transport estimate - $10.00

DAY 2
---------------------------------------------
- Visit an old town or heritage area - $15.00
- Try a traditional local meal - $30.00
- Food estimate - $30.00
- Transport estimate - $10.00

=============================================
Estimated total: $170.00
Remaining budget: $80.00
Status: Within budget
=============================================
```

The Streamlit interface displays the itinerary in a web page along with:

- Estimated trip cost
- Remaining budget
- Daily itinerary cards
- Live weather forecast
- Weather-based travel advice
- Downloadable itinerary

---

## 🎯 Supported Interests

TripCraft currently supports:

- `history`
- `food`
- `nature`
- `shopping`
- `culture`

Example:

```text
history, food, nature
```

---

## 💡 How It Works

```text
User Input
    ↓
Validate Trip Details
    ↓
Match Activities to Interests
    ↓
Generate Daily Itinerary
    ↓
Calculate Estimated Costs
    ↓
Compare Cost with Budget
    ↓
Retrieve Destination Weather
    ↓
Display Itinerary and Weather Summary
    ↓
Download or Save Itinerary
```

---

## 🌦️ Live Weather Integration

The Streamlit application uses the Open-Meteo APIs to retrieve weather information.

### API Services Used

#### Open-Meteo Geocoding API

Converts the destination name into latitude and longitude coordinates.

#### Open-Meteo Forecast API

Retrieves the weather forecast for the selected travel duration.

The application displays:

- Daily maximum temperature
- Daily minimum temperature
- Precipitation probability
- Weather condition
- Basic weather-based travel advice

No API key is required for the current Open-Meteo integration.

---

## 📌 Current Limitations

- Activities are based on predefined sample data.
- Budget calculations use estimated costs.
- Prices are not live market prices.
- Flights and hotel prices are not included.
- The application does not currently retrieve live attractions or restaurant information.
- Weather data depends on the availability of the Open-Meteo APIs.
- The itinerary does not yet use advanced AI-based recommendations.
- The application is currently run locally.

---

## 🔮 Future Improvements

- 🤖 Add AI-powered itinerary recommendations
- 🌍 Integrate live attractions, restaurants, and destination APIs
- 🏨 Add hotel and flight cost estimates
- 🗺️ Add map integration
- 📈 Add visual budget charts
- 💱 Add live currency conversion
- 📤 Export itineraries as PDF files
- ⭐ Add user ratings and saved trips
- ☁️ Deploy the application online
- 🔐 Add user accounts and saved travel preferences

---

## 👩‍💻 Author

**Deepika Venkatesan**

Master's in Computer Science  
Cloud and DevOps Engineer | Python Developer

---

## 📄 License

This project is licensed under the MIT License.