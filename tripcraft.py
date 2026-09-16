from datetime import date

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

def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))

            if value > 0:
                return value

            print("Please enter a number greater than zero.")

        except ValueError:
            print("Please enter a valid whole number.")


def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))

            if value > 0:
                return value

            print("Please enter an amount greater than zero.")

        except ValueError:
            print("Please enter a valid amount.")

def select_activities(interests, days):
    selected_activities = []

    for interest in interests:
        if interest in ACTIVITIES:
            selected_activities.extend(ACTIVITIES[interest])

    if not selected_activities:
        selected_activities = [
            ("Explore the city", 15),
            ("Visit a popular attraction", 25),
            ("Try local food", 30),
        ]

    return [
        selected_activities[index % len(selected_activities)]
        for index in range(days * 2)
    ]

# budget-handling func
def get_budget_status(budget, estimated_total):
    difference = budget - estimated_total

    if difference >= 0:
        return (
            f"Remaining budget: ${difference:.2f}\n"
            "Status: Within budget"
        )

    return (
        f"Over budget by: ${abs(difference):.2f}\n"
        "Status: Consider reducing activities"
    )


def generate_itinerary(destination, days, budget, interests):
    activities = select_activities(interests, days)

    daily_food_cost = 30
    daily_transport_cost = 10

    total_activity_cost = sum(cost for _, cost in activities)
    total_food_cost = days * daily_food_cost
    total_transport_cost = days * daily_transport_cost

    estimated_total = (
        total_activity_cost
        + total_food_cost 
        + total_transport_cost
    )

    lines = []

    lines.append("=" * 45)
    lines.append("                      TRIPCRAFT")
    lines.append("=" * 45)
    lines.append(f"Destination: {destination}")
    lines.append(f"Duration: {days} days")
    lines.append(f"Budget: ${budget:.2f}")
    lines.append(f"Created: {date.today()}")
    lines.append("")

    activity_index = 0

    for day in range(1, days + 1):
        lines.append(f"DAY {day}")
        lines.append("-" * 45)

        for _ in range(2):
            activity, cost = activities[activity_index]
            lines.append(f"- {activity} - ${cost:.2f}")
            activity_index += 1

        lines.append(f"- Food estimate - ${daily_food_cost:.2f}")
        lines.append(f"- Transport estimate - ${daily_transport_cost:.2f}")
        lines.append("")

    lines.append("=" * 45)
    lines.append(f"Estimated total: ${estimated_total:.2f}")

        # remaining_budget = budget - estimated_total

        # if remaining_budget >= 0:
        #     lines.append(f"Remaining budget: ${remaining_budget:.2f}")
        #     lines.append("Status: Within budget")

        # else:
        #     lines.append(f"over budget by: ${abs(remaining_budget):.2f}")
        #     lines.append("Status: Consider reducing activities")
    
    budget_status = get_budget_status(budget, estimated_total)

    for line in budget_status.split("\n"):
        lines.append(line)
    #budget warning feature
    if estimated_total > budget:
        lines.append("")
        lines.append("💡 Tip: Try selecting fewer paid activities.")

    lines.append("=" * 45)

    return "\n".join(lines)

def show_menu():
    print("\n========== TRIPCRAFT ==========")
    print("1. Create a new itinerary")
    print("2. View supported interests")
    print("3. Exit")
    print("=" * 32)

def show_supported_interests():
    print("\nSupported interests:")

    for interest in ACTIVITIES:
        print(f" - {interest.title()}")

def save_itinerary(itinerary):
    filename = "trip_itinerary.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(itinerary)

    print(f"\nYour itinerary was saved to {filename}")

def create_itinerary():
    destination = input('\nEnter your destination: ').strip()

    days = get_positive_integer(
        "How many days is your trip? "
    )
    budget = get_positive_float(
        "What is your budget in CAD? "
    )

    interests_input = input(
        "Enter your interests separated by commas "
        "(history, food, nature, shopping, culture): "
    )

    interests = [
        interest.strip().lower()
        for interest in interests_input.split(",")
    ]

    itinerary = generate_itinerary(
        destination,
        days,
        budget,
        interests,
    )

    print("\n")
    print(itinerary)

    save_choice = input(
        "\nWould you like to save this itinerary? (yes/no): "
    ).strip().lower()

    if save_choice in ["yes", "y"]:
        save_itinerary(itinerary)

def main():
    print("\nWelcome to TripCraft!\n")

    # destination = input("Enter your destination: ").strip()
    # days = get_positive_integer("How many days is your trip? ")
    # budget = get_positive_float("What is your budget in CAD? ")

    # interests_input = input(
    #     "Enter your interests separated by commas "
    #     "(history, food, nature, shopping, culture): "
    # )

    # interests = [
    #     interest.strip().lower()
    #     for interest in interests_input.split(",")
    # ]

    # itinerary = generate_itinerary(
    #     destination, 
    #     days,
    #     budget,
    #     interests,
    # )

    # print("\n")
    # print(itinerary)

    # save_choice = input(
    #     "\nWould you like to save this itinerary? (yes/no): "
    # ).strip().lower()

    # if save_choice in ["yes", "y"]:
    #     save_itinerary(itinerary)

    while True:
        show_menu()

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            create_itinerary()

        elif choice == "2":
            show_supported_interests()

        elif choice == "3":
            print("\nThank you for using TripCraft. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

    