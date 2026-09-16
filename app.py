import streamlit as st
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
            selected_activities.extend(ACTIVITIES[interest])

    activities_needed = days * 2

    activities = [
        selected_activities[index % len(selected_activities)]
        for index in range(activities_needed)
    ]

    daily_food_cost = 30
    daily_transport_cost = 10

    total_activity_cost = sum(
        cost for _, cost in activities
    )

    total_food_cost = days * daily_food_cost
    total_transport_cost = days * daily_transport_cost

    estimated_total = (
        total_activity_cost
        + total_food_cost
        + total_transport_cost
    )

    remaining_budget = budget - estimated_total

    # -----------------------------
    # Summary cards
    # -----------------------------
    st.success(
        f"Your itinerary for **{destination.title()}** is ready!"
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

    # -----------------------------
    # Budget status
    # -----------------------------
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
            "💡 Try reducing the number of paid activities."
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
                f'<div class="activity">📌 {activity} '
                f'<b>(${cost:.2f})</b></div>'
            )

        day_html += (
            f'<div class="activity">🍽️ Food estimate '
            f'<b>(${daily_food_cost:.2f})</b></div>'
            f'<div class="activity">🚗 Transport estimate '
            f'<b>(${daily_transport_cost:.2f})</b></div>'
            "</div>"
        )

        st.markdown(
            day_html,
            unsafe_allow_html=True,
        )

        activity_index += 2

    # -----------------------------
    # Download itinerary
    # -----------------------------
    itinerary_text = (
        f"TRIPCRAFT\n"
        f"Destination: {destination}\n"
        f"Duration: {days} days\n"
        f"Budget: ${budget:.2f}\n"
        f"Created: {date.today()}\n\n"
    )

    activity_index = 0

    for day in range(1, days + 1):
        itinerary_text += f"DAY {day}\n"

        for _ in range(2):
            activity, cost = activities[activity_index]
            itinerary_text += (
                f"- {activity} - ${cost:.2f}\n"
            )
            activity_index += 1

        itinerary_text += (
            f"- Food estimate - ${daily_food_cost:.2f}\n"
            f"- Transport estimate - ${daily_transport_cost:.2f}\n\n"
        )

    itinerary_text += (
        f"Estimated total: ${estimated_total:.2f}\n"
        f"Remaining budget: ${remaining_budget:.2f}\n"
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
        "👈 Enter your trip details in the sidebar and "
        "click **Generate Itinerary** to begin."
    )