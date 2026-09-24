import streamlit as st
import requests

from math import radians, sin, cos, sqrt, atan2
from datetime import date


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="TripCraft",
    page_icon="✈️",
    layout="wide",
)


# -----------------------------
# Activity data
# -----------------------------

ACTIVITIES = {
    "history": [
        ("Visit a historical landmark", 25),
        ("Explore a museum", 20),
        ("Visit an old town or heritage area", 15),
    ],

    "food": [
        ("Try a traditional local meal", 30),
        ("Explore a local food market", 15),
        ("Visit a popular café", 12),
    ],

    "nature": [
        ("Visit a scenic park", 10),
        ("Explore a nature trail", 15),
        ("Enjoy a viewpoint or garden", 12),
    ],

    "shopping": [
        ("Explore local shopping streets", 20),
        ("Visit a local market", 15),
        ("Browse souvenir shops", 10),
    ],

    "culture": [
        ("Visit a cultural attraction", 20),
        ("Attend a local cultural activity", 25),
        ("Explore an art gallery", 18),
    ],
}


# -----------------------------
# Weather functions
# -----------------------------

def get_coordinates(destination):
    """Find latitude and longitude for a destination."""

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": destination,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    if "results" not in data or not data["results"]:
        return None

    location = data["results"][0]

    return {
        "name": location["name"],
        "country": location.get("country", ""),
        "latitude": location["latitude"],
        "longitude": location["longitude"],
    }


def get_weather(latitude, longitude, days):
    """Get a live weather forecast."""

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
            "weather_code",
        ],
        "forecast_days": min(days, 16),
        "timezone": "auto",
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


# -----------------------------
# Nearby attractions
# OpenStreetMap + Overpass API
# -----------------------------

def get_nearby_attractions(latitude, longitude):
    """Find nearby attractions using OpenStreetMap."""

    overpass_url = (
        "https://overpass.kumi.systems/api/interpreter"
    )

    query = f"""
    [out:json][timeout:60];

    (
        nwr["tourism"="attraction"](
            around:10000,{latitude},{longitude}
        );

        nwr["tourism"="museum"](
            around:10000,{latitude},{longitude}
        );

        nwr["tourism"="gallery"](
            around:10000,{latitude},{longitude}
        );

        nwr["tourism"="viewpoint"](
            around:10000,{latitude},{longitude}
        );

        nwr["tourism"="zoo"](
            around:10000,{latitude},{longitude}
        );

        nwr["tourism"="theme_park"](
            around:10000,{latitude},{longitude}
        );

        nwr["historic"](
            around:10000,{latitude},{longitude}
        );

        nwr["leisure"="park"](
            around:10000,{latitude},{longitude}
        );

        nwr["leisure"="garden"](
            around:10000,{latitude},{longitude}
        );
    );

    out center tags;
    """

    try:
        response = requests.post(
            overpass_url,
            data=query,
            headers={
                "User-Agent": "TripCraft/1.0 (travel planner)"
            },
            timeout=70,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("elements", [])

    except requests.RequestException as error:
        st.error(
            f"OpenStreetMap request failed: {error}"
        )
        return []


# -----------------------------
# Attraction helper functions
# -----------------------------

def get_place_name(place):
    """Return the place name."""

    tags = place.get("tags", {})

    return tags.get(
        "name",
        "Unnamed attraction",
    )


def get_place_category(place):
    """Convert OpenStreetMap tags into readable categories."""

    tags = place.get("tags", {})

    tourism = tags.get("tourism")
    historic = tags.get("historic")
    leisure = tags.get("leisure")

    category_map = {
        "attraction": "Tourist Attraction",
        "museum": "Museum",
        "gallery": "Art Gallery",
        "viewpoint": "Viewpoint",
        "zoo": "Zoo",
        "theme_park": "Theme Park",
    }

    historic_map = {
        "castle": "Historic Castle",
        "monument": "Historic Monument",
        "memorial": "Memorial",
        "archaeological_site": "Archaeological Site",
        "ruins": "Historic Ruins",
        "building": "Historic Building",
    }

    leisure_map = {
        "park": "Park",
        "garden": "Garden",
        "water_park": "Water Park",
    }

    if tourism in category_map:
        return category_map[tourism]

    if historic in historic_map:
        return historic_map[historic]

    if leisure in leisure_map:
        return leisure_map[leisure]

    return "Point of Interest"


def calculate_attraction_score(
    attraction,
    selected_interests,
):
    """
    Score an attraction according to the user's
    selected interests.
    """

    tags = attraction.get("tags", {})

    tourism = tags.get("tourism", "")
    historic = tags.get("historic", "")
    leisure = tags.get("leisure", "")

    score = 0

    interests = [
        interest.lower()
        for interest in selected_interests
    ]

    # -------------------------
    # History
    # -------------------------

    if "history" in interests:

        if historic:
            score += 5

        if tourism == "museum":
            score += 4

        if tourism == "attraction":
            score += 2

    # -------------------------
    # Culture
    # -------------------------

    if "culture" in interests:

        if tourism == "museum":
            score += 5

        if tourism == "gallery":
            score += 5

        if tourism == "attraction":
            score += 2

    # -------------------------
    # Nature
    # -------------------------

    if "nature" in interests:

        if leisure == "park":
            score += 5

        if leisure == "garden":
            score += 5

        if tourism == "viewpoint":
            score += 4

    return score

#helper func for live itinerary attractions
def select_itinerary_attractions(
    attractions,
    days,
):
    """
    Select live attractions for the itinerary.

    Returns up to two attractions per day.
    """

    required_attractions = days * 2

    return attractions[:required_attractions]


# -----------------------------
# Distance calculation
# -----------------------------

def calculate_distance(
    latitude_1,
    longitude_1,
    latitude_2,
    longitude_2,
):
    """Calculate approximate distance between two coordinates."""

    earth_radius_km = 6371

    latitude_difference = radians(
        latitude_2 - latitude_1
    )

    longitude_difference = radians(
        longitude_2 - longitude_1
    )

    a = (
        sin(latitude_difference / 2) ** 2
        + cos(radians(latitude_1))
        * cos(radians(latitude_2))
        * sin(longitude_difference / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a),
    )

    return earth_radius_km * c


# -----------------------------
# Weather descriptions
# -----------------------------

def weather_description(code):
    """Convert a weather code into readable text."""

    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Light snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Light rain showers",
        81: "Moderate rain showers",
        82: "Heavy rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail",
    }

    return descriptions.get(
        code,
        "Unknown conditions",
    )


# -----------------------------
# Custom styling
# -----------------------------

st.markdown(
    """
    <style>

    .main {
        background-color: #f5f7fb;
    }

    .trip-title {
        text-align: center;
        color: #4f46e5;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .trip-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    .metric-card {
        background-color: white;
        padding: 1.2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        text-align: center;
    }

    .day-card {
        background-color: white;
        padding: 1.2rem;
        border-radius: 15px;
        border-left: 6px solid #6366f1;
        margin-bottom: 1rem;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
    }

    .activity {
        padding: 0.4rem 0;
        font-size: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<div class="trip-title">✈️ TripCraft</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="trip-subtitle">'
    "Create a personalized travel itinerary in seconds"
    "</div>",
    unsafe_allow_html=True,
)


# -----------------------------
# Sidebar inputs
# -----------------------------

st.sidebar.header("🧳 Plan Your Trip")

destination = st.sidebar.text_input(
    "📍 Destination",
    placeholder="e.g. Toronto",
)

days = st.sidebar.number_input(
    "📅 Number of days",
    min_value=1,
    max_value=30,
    value=2,
)

budget = st.sidebar.number_input(
    "💰 Budget in CAD",
    min_value=1.0,
    value=200.0,
    step=10.0,
)

interests = st.sidebar.multiselect(
    "🎯 Choose your interests",
    options=list(ACTIVITIES.keys()),
    default=["history", "food"],
    format_func=lambda interest: interest.title(),
)

generate_button = st.sidebar.button(
    "✨ Generate Itinerary",
    use_container_width=True,
)


# -----------------------------
# Generate itinerary
# -----------------------------

if generate_button:

    if not destination.strip():
        st.warning("Please enter a destination.")
        st.stop()

    if not interests:

        st.info(
            "No interests selected. General activities will be used."
        )

        selected_activities = [
            ("Explore the city", 15),
            ("Visit a popular attraction", 25),
            ("Try local food", 30),
        ]

    else:

        selected_activities = []

        for interest in interests:

            selected_activities.extend(
                ACTIVITIES[interest]
            )

    # ======================================
    # Get live destination and weather data
    # ======================================

    with st.spinner(
        "Finding destination and checking live weather ..."
    ):

        try:

            location = get_coordinates(
                destination
            )

            if location is None:

                st.warning(
                    "We could not find that destination. "
                    "Please try a more specific city name."
                )

                st.stop()

            weather = get_weather(
                location["latitude"],
                location["longitude"],
                days,
            )

        except requests.RequestException:

            st.error(
                "Live weather data is temporarily unavailable. "
                "Please try again later."
            )

            st.stop()

    # ======================================
    # Calculate itinerary costs
    # ======================================

    activities_needed = days * 2

    activities = [
        selected_activities[
            index % len(selected_activities)
        ]
        for index in range(activities_needed)
    ]

    daily_food_cost = 30
    daily_transport_cost = 10

    total_activity_cost = sum(
        cost
        for _, cost in activities
    )

    total_food_cost = (
        days * daily_food_cost
    )

    total_transport_cost = (
        days * daily_transport_cost
    )

    estimated_total = (
        total_activity_cost
        + total_food_cost
        + total_transport_cost
    )

    remaining_budget = (
        budget - estimated_total
    )

    # -----------------------------
    # Summary cards
    # -----------------------------

    st.success(
        f"Your itinerary for "
        f"**{destination.title()}** is ready!"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            '<div class="metric-card">'
            "📍<br><b>Destination</b><br>"
            f"{destination.title()}"
            "</div>",
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            '<div class="metric-card">'
            "📅<br><b>Duration</b><br>"
            f"{days} days"
            "</div>",
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            '<div class="metric-card">'
            "💰<br><b>Estimated Cost</b><br>"
            f"${estimated_total:.2f}"
            "</div>",
            unsafe_allow_html=True,
        )

    with col4:

        st.markdown(
            '<div class="metric-card">'
            "💵<br><b>Budget Remaining</b><br>"
            f"${remaining_budget:.2f}"
            "</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ======================================
    # Live weather forecast
    # ======================================

    st.header("🌤️ Live Weather Forecast")

    st.caption(
        f"Weather for {location['name']}, "
        f"{location['country']}"
    )

    weather_dates = weather["daily"]["time"]

    max_temperatures = weather["daily"][
        "temperature_2m_max"
    ]

    min_temperatures = weather["daily"][
        "temperature_2m_min"
    ]

    rain_probabilities = weather["daily"][
        "precipitation_probability_max"
    ]

    weather_codes = weather["daily"][
        "weather_code"
    ]

    weather_columns = st.columns(
        min(len(weather_dates), 4)
    )

    for index, weather_date in enumerate(
        weather_dates
    ):

        column = weather_columns[
            index % len(weather_columns)
        ]

        with column:

            st.markdown(
                f"### Day {index + 1}"
            )

            st.write(
                f"📅 {weather_date}"
            )

            st.write(
                f"🌡️ "
                f"{min_temperatures[index]}°C – "
                f"{max_temperatures[index]}°C"
            )

            st.write(
                f"🌧️ Rain chance: "
                f"{rain_probabilities[index]}%"
            )

            st.write(
                weather_description(
                    weather_codes[index]
                )
            )

    # ======================================
    # Weather-based advice
    # ======================================

    first_day_rain = rain_probabilities[0]

    if first_day_rain >= 60:

        st.warning(
            "☔ Rain is likely on your first day. "
            "Consider museums, cafés, galleries, "
            "or other indoor attractions."
        )

    elif first_day_rain >= 30:

        st.info(
            "🌦️ There is a moderate chance of rain "
            "on your first day. Consider carrying "
            "an umbrella."
        )

    else:

        st.success(
            "☀️ Outdoor activities may be suitable "
            "on your first day."
        )

    st.divider()

    # ======================================
    # Nearby attractions
    # ======================================

    st.subheader("📍 Nearby Attractions")

    with st.spinner(
        "Finding nearby attractions..."
    ):

        attractions = get_nearby_attractions(
            location["latitude"],
            location["longitude"],
        )

    # -----------------------------
    # Filter and process attractions
    # -----------------------------

    valid_attractions = []

    allowed_types = {
        "attraction",
        "museum",
        "gallery",
        "viewpoint",
        "zoo",
        "theme_park",
    }

    allowed_historic_types = {
        "castle",
        "monument",
        "memorial",
        "archaeological_site",
        "ruins",
        "building",
    }

    allowed_leisure_types = {
        "park",
        "garden",
        "water_park",
    }

    for attraction in attractions:

        tags = attraction.get(
            "tags",
            {}
        )

        # Must have a name
        if "name" not in tags:
            continue

        tourism_type = tags.get(
            "tourism",
            ""
        )

        historic_type = tags.get(
            "historic",
            ""
        )

        leisure_type = tags.get(
            "leisure",
            ""
        )

        # Keep travel-focused places
        if (
            tourism_type not in allowed_types
            and historic_type not in allowed_historic_types
            and leisure_type not in allowed_leisure_types
        ):
            continue

        center = attraction.get(
            "center",
            {}
        )

        attraction_latitude = attraction.get(
            "lat"
        )

        attraction_longitude = attraction.get(
            "lon"
        )

        # Ways usually use center coordinates
        if attraction_latitude is None:

            attraction_latitude = center.get(
                "lat"
            )

        if attraction_longitude is None:

            attraction_longitude = center.get(
                "lon"
            )

        if (
            attraction_latitude is None
            or attraction_longitude is None
        ):
            continue

        # Calculate distance
        distance = calculate_distance(
            location["latitude"],
            location["longitude"],
            attraction_latitude,
            attraction_longitude,
        )

        # Calculate interest score
        score = calculate_attraction_score(
            attraction,
            interests,
        )

        valid_attractions.append(
            {
                "name": get_place_name(
                    attraction
                ),
                "category": get_place_category(
                    attraction
                ),
                "distance": distance,
                "latitude": attraction_latitude,
                "longitude": attraction_longitude,
                "website": tags.get(
                    "website"
                ),
                "wikidata": tags.get(
                    "wikidata"
                ),
                "score": score,
            }
        )

    # -----------------------------
    # Sort attractions
    # -----------------------------

    valid_attractions.sort(
        key=lambda place: (
            -place["score"],
            place["distance"],
        )
    )

    # Show only top 10
    valid_attractions = (
        valid_attractions[:10]
    )

    # -----------------------------
    # Display attractions
    # -----------------------------

    if not valid_attractions:

        st.warning(
            "No nearby attractions were found "
            "for this destination."
        )

    else:

        for attraction in valid_attractions:

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### 📍 "
                    f"{attraction['name']}"
                )

                st.write(
                    f"**Category:** "
                    f"{attraction['category']}"
                )

                st.write(
                    f"**Distance:** "
                    f"{attraction['distance']:.2f} km"
                )

                map_url = (
                    "https://www.openstreetmap.org/"
                    f"?mlat={attraction['latitude']}"
                    f"&mlon={attraction['longitude']}"
                    "#map=18/"
                    f"{attraction['latitude']}/"
                    f"{attraction['longitude']}"
                )

                st.markdown(
                    f"[🗺️ View on OpenStreetMap]"
                    f"({map_url})"
                )

                if attraction["website"]:

                    st.markdown(
                        "[🌐 Visit website]"
                        f"({attraction['website']})"
                    )

    # -----------------------------
    # Budget status
    # -----------------------------

    st.header("💰 Budget Summary")

    if remaining_budget >= 0:

        st.success(
            f"✅ You are within budget by "
            f"${remaining_budget:.2f}."
        )

    else:

        st.error(
            f"⚠️ You are over budget by "
            f"${abs(remaining_budget):.2f}."
        )

        st.info(
            "💡 Try reducing the number "
            "of paid activities."
        )

    # -----------------------------
    # Daily itinerary
    # -----------------------------

    st.header("🗺️ Your Travel Itinerary")

    activity_index = 0

    for day in range(1, days + 1):

        day_activities = activities[
            activity_index:activity_index + 2
        ]

        day_html = f"""
        <div class="day-card">

            <h3>🌞 Day {day}</h3>
        """

        for activity, cost in day_activities:

            day_html += (
                f'<div class="activity">'
                f"📌 {activity} "
                f"<b>(${cost:.2f})</b>"
                f"</div>"
            )

        day_html += (
            f'<div class="activity">'
            f"🍽️ Food estimate "
            f"<b>(${daily_food_cost:.2f})</b>"
            f"</div>"
        )

        day_html += (
            f'<div class="activity">'
            f"🚗 Transport estimate "
            f"<b>(${daily_transport_cost:.2f})</b>"
            f"</div>"
        )

        day_html += "</div>"

        st.markdown(
            day_html,
            unsafe_allow_html=True,
        )

        activity_index += 2

    # -----------------------------
    # Download itinerary
    # -----------------------------

    itinerary_text = (
        "TRIPCRAFT\n"
        f"Destination: {destination}\n"
        f"Duration: {days} days\n"
        f"Budget: ${budget:.2f}\n"
        f"Created: {date.today()}\n\n"
    )

    activity_index = 0

    for day in range(1, days + 1):

        itinerary_text += (
            f"DAY {day}\n"
        )

        for _ in range(2):

            activity, cost = activities[
                activity_index
            ]

            itinerary_text += (
                f"- {activity} - "
                f"${cost:.2f}\n"
            )

            activity_index += 1

        itinerary_text += (
            f"- Food estimate - "
            f"${daily_food_cost:.2f}\n"
            f"- Transport estimate - "
            f"${daily_transport_cost:.2f}\n\n"
        )

    itinerary_text += (
        f"Estimated total: "
        f"${estimated_total:.2f}\n"
        f"Remaining budget: "
        f"${remaining_budget:.2f}\n"
    )

    st.download_button(
        label="📥 Download Itinerary",
        data=itinerary_text,
        file_name="trip_itinerary.txt",
        mime="text/plain",
        use_container_width=True,
    )

else:

    st.info(
        "👈 Enter your trip details in the sidebar "
        "and click **Generate Itinerary** to begin."
    )