# ✈️ TripCraft

### A Python-based travel itinerary planner that creates budget-friendly trip plans based on destination, duration, budget, and interests.

TripCraft is a beginner-friendly Python application that generates a personalized travel itinerary with estimated activity, food, and transportation costs.

---

## 🌍 Project Overview

Planning a trip can be time-consuming, especially when trying to balance activities and expenses.

TripCraft simplifies the initial planning process by allowing users to enter:

- Destination
- Number of travel days
- Total budget in CAD
- Personal interests

The application then generates a day-by-day itinerary, estimates the total cost, and displays the remaining budget.

---

## ✨ Features

- 🗺️ Enter a travel destination
- 📅 Generate a multi-day itinerary
- 💰 Estimate activity, food, and transportation expenses
- 🎯 Customize activities based on interests
- 📊 Calculate the estimated trip cost
- 💵 Display remaining budget or amount over budget
- ⚠️ Show a warning when the estimated cost exceeds the budget
- 📄 Save the itinerary as a text file
- ✅ Validate user inputs
- 🐍 Built using Python's standard library

---

## 🛠️ Technologies Used

- Python 3
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
├── trip_itinerary.txt
├── README.md
├── .gitignore
└── LICENSE
```

| File | Description |
|---|---|
| `tripcraft.py` | Main Python application |
| `trip_itinerary.txt` | Sample generated itinerary |
| `README.md` | Project documentation |
| `.gitignore` | Files ignored by Git |
| `LICENSE` | MIT License |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Dipika2020/tripcraft-python.git
```

### 2. Open the project folder

```bash
cd tripcraft-python
```

### 3. Run the application

```bash
python tripcraft.py
```

If your system uses `python3`, run:

```bash
python3 tripcraft.py
```

---

## 🧪 Example Usage

```text
Welcome to TripCraft!

Enter your destination: Paris
How many days is your trip? 3
What is your budget in CAD? 500
Enter your interests separated by commas:
history, food
```

### Example Result

```text
=============================================
                  TRIPCRAFT
=============================================
Destination: Paris
Duration: 3 days
Budget: $500.00

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

DAY 3
---------------------------------------------
- Explore a local food market - $15.00
- Visit a popular café - $12.00
- Food estimate - $30.00
- Transport estimate - $10.00

=============================================
Estimated total: $237.00
Remaining budget: $263.00
Status: Within budget
=============================================
```

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
Display Budget Summary
    ↓
Save Itinerary to Text File
```

---

## 📌 Current Limitations

This is the first version of TripCraft.

- Activities are based on predefined sample data.
- Budget calculations use predefined estimated costs.
- Prices are estimates and are not live prices.
- The application currently runs in the terminal.
- Flights, hotels, and live travel APIs are not included.
- Destination information is not retrieved in real time.

---

## 🔮 Future Improvements

- 🌐 Add a web interface using Flask or Streamlit
- 🤖 Add AI-powered itinerary recommendations
- 🌍 Integrate real travel and destination APIs
- 🏨 Add hotel and flight cost estimates
- 🗺️ Add map integration
- 📈 Add visual budget charts
- 📤 Export itineraries as PDF files
- ☁️ Deploy the application online

---

## 👩‍💻 Author

**Deepika Venkatesan**

Master's in Computer Science  
Cloud and DevOps Engineer | Python Developer

---

## 📄 License

This project is licensed under the MIT License.