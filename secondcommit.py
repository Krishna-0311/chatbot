import pandas as pd
import random

# Load the dataset
salon_data = pd.read_csv('salons_slay.csv', encoding='latin1')  # Specify encoding

# Define welcome message
def welcome_message():
    return "🌟 Welcome to Slayweks! 🌟\nHow can I assist you today?"

# Function to handle greetings
def greet():
    greetings = ["Hi there!", "Hello!", "Hey!"]
    return random.choice(greetings)

# Function to ask user's preference for salon search
def ask_preference():
    return "🏢 Do you want to search for salons by brand or location?"

# Function to list all available brands
def list_brands():
    brands = salon_data['BRAND'].unique()
    return "🏢 Available brands: " + ", ".join(brands)

# Function to list all available locations
def list_locations():
    locations = salon_data['LOCATION'].unique()
    return "📍 Available locations: " + ", ".join(locations)

# Function to list all available service categories
def list_service_categories():
    service_categories = salon_data['SERVICE CATEGORY CODE'].unique()
    service_category_list = "\n".join([f"{index + 1}. {service}" for index, service in enumerate(service_categories)])
    return f"💅 Available service categories:\n{service_category_list}\nPlease enter the number of the service category you want: "

# Function to list all available service titles
def list_service_titles(service_category):
    service_titles = salon_data[salon_data['SERVICE CATEGORY CODE'] == service_category]['SERVICE TITLE'].unique()
    service_titles_list = "\n".join([f"{index + 11}. {title}" for index, title in enumerate(service_titles)])
    return f"💇‍♀️ Available service titles for {service_category}:\n{service_titles_list}\nPlease enter the number of the service title you want: "

# Function to list salons offering a specific service
def list_salons_by_service(service_category, service_title):
    salons = salon_data[(salon_data['SERVICE CATEGORY CODE'] == service_category) & (salon_data['SERVICE TITLE'] == service_title)]
    return salons[['BRANCH CODE', 'AMOUNT', 'PHONE NUMBER']]

# Function to handle unknown input
def handle_unknown():
    return "Sorry, I didn't understand that. Could you please repeat?"

# Function to generate a response
# Function to generate a response
# Function to generate a response
# Function to generate a response
def generate_response(input_text, context):
    if 'hi' in input_text.lower() or 'hello' in input_text.lower() or 'hey' in input_text.lower():
        return greet()
    elif 'brand' in input_text.lower():
        return list_brands()
    elif 'location' in input_text.lower():
        return list_locations()
    elif context.get('preference') == 'brand':
        context['brand'] = input_text.strip()
        return f"🏢 You've selected {context['brand']}. {list_service_categories()}"
    elif context.get('preference') == 'location':
        context['location'] = input_text.strip()
        return f"📍 You've selected {context['location']}. {list_service_categories()}"
    elif input_text.strip().isdigit() and int(input_text.strip()) in range(1, len(salon_data['SERVICE CATEGORY CODE'].unique()) + 1):
        context['service_category'] = salon_data['SERVICE CATEGORY CODE'].unique()[int(input_text.strip()) - 1]
        return list_service_titles(context['service_category'])
    elif context.get('service_category') and input_text.strip().isdigit():
        selected_title = int(input_text.strip())
        service_titles = salon_data[salon_data['SERVICE CATEGORY CODE'] == context['service_category']]['SERVICE TITLE'].unique()
        if selected_title in range(1, len(service_titles) + 1):
            context['service_title'] = service_titles[selected_title - 1]
            salons = list_salons_by_service(context['service_category'], context['service_title'])
            response = f"🏢 Salons offering {context['service_title']}:\n"
            for idx, salon in enumerate(salons.itertuples(), 1):
                response += f"{idx}. Branch Code: {salon[1]}, Amount: {salon[2]}, Phone Number: {salon[3]}\n"
            response += "\nPlease enter the number of the salon you want details for: "
            return response
        else:
            return handle_unknown()
    elif context.get('service_title') and input_text.strip().isdigit():
        selected_salon_index = int(input_text.strip()) - 1
        salons = list_salons_by_service(context['service_category'], context['service_title'])
        if selected_salon_index in range(len(salons)):
            selected_salon = salons.iloc[selected_salon_index]
            response = f"🏢 Salon Details:\n"
            response += f"**Branch Code:** {selected_salon['BRANCH CODE']}\n"
            response += f"**Amount:** {selected_salon['AMOUNT']}\n"
            response += f"**Phone Number:** {selected_salon['PHONE NUMBER']}\n"
            response += "\nThank you for visiting Slayweks!"
            print(response)  # Print the response
            return None  # Return None to terminate the conversation
        else:
            return handle_unknown()
    else:
        return handle_unknown()




# Main function
def main():
    context = {}
    print(welcome_message())
    print(ask_preference())
    while True:
        user_input = input("👤 You: ")
        response = generate_response(user_input, context)
        print("💬 Bot:")
        print(response)
        if isinstance(response, str) and response.startswith("🏢") or response.startswith("📍") or response.startswith("💅"):
            context['preference'] = user_input.lower()
        elif isinstance(response, pd.DataFrame):
            break

# Main execution
if __name__ == "__main__":
    main()
