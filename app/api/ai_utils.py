from typing import List
import openai
import os
from dotenv import load_dotenv
import httpx
import json
from pprint import pprint
from datetime import datetime, timedelta

load_dotenv()
location_id = os.getenv('LOCATION_ID')
client = openai.AsyncOpenAI()

class HVACMillionaireBot:

    def __init__(self, user_context: dict, contact_id: str, history: List[dict], ACCESS_TOKEN: str):
        self.user_context = user_context
        self.contact_id = contact_id
        self.history = history
        self.headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Version": "2021-04-15",
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        # self.prompt = hub.pull("hwchase17/react-chat")
    
    def get_timestamps(self,):
        """
        This function gets today's date and calculates the date one week later.
        It then returns both dates as Unix timestamps in milliseconds.
        """
        today = datetime.today()
        one_week_later = today + timedelta(days=7)

        # Convert datetime objects to timestamps in milliseconds
        today_timestamp_ms = int(today.timestamp() * 1000)
        one_week_later_ms = int(one_week_later.timestamp() * 1000)

        return today_timestamp_ms, one_week_later_ms

    async def get_calendars(self):
        url = 'https://services.leadconnectorhq.com/calendars/'
        params = {
            'locationId': location_id
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url, headers=self.headers, params=params)
            data = response.json()
            calendars = data.get('calendars')
            if calendars:
                calendar_id = calendars[0].get('id')
                return calendar_id
            return None

    # @tool
    async def get_slots(self) -> dict:
        """Useful to find out the available slots for appointments this week."""
        calendar_id = await self.get_calendars()
        print(calendar_id)
        url = f"https://services.leadconnectorhq.com/calendars/{calendar_id}/free-slots/"
        
        start_date, end_date = self.get_timestamps()
        params = {
            "startDate": start_date,
            "endDate": end_date
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            data = response.json()
            pprint(data)
            return data
    
    # @tool("book_appointment", args_schema=AppointmentSchema, return_direct=True)
    async def book_appointment(self, start_date: str, title: str) -> dict:
        """This tool must be used to book an appointment with the provided start date and title."""
        url = "https://services.leadconnectorhq.com/calendars/events/appointments"
        calendar_id = await self.get_calendars()
        body = {
            'calendarId': calendar_id,
            'locationId' : location_id,
            'contactId' : self.contact_id,
            'startTime' : start_date,
            'title' : title
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=body)
            data = response.json()
            return data


    async def model_router(self):

        sys_message = """You are a model router that works for HVAC Millionaire. 
        ###Rules###
        Based on the conversation history and latest message suggest whether the latest message needs to be routed to the general QA bot, or appointment booking bot.
        Return the following JSON object

        {{
        "last_4_summary" : Summary of the last for messages,
        "user_intent" : Based on the summary what does the user intend to do are they inquiring for information or are they requesting an appointment
        "target_model" : "general" or "appointment" based on the `user_intent`
        }}    

        """

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={'type': 'json_object'},
            messages=[
                {'role': 'system', "content": sys_message},
                *self.history
            ],
            temperature=0.7,
            max_tokens=512
        )
        return json.loads(response.choices[0].message.content)

    async def general_qa(self):

        system_message = """
        ###Objectives###
        You are a helpful chat assistant for HVAC Millionaire.
        Your goals are the following:
        - Provide users knowledge about HVAC Millionaire and engage with them
        - Provide tips and advice if they're facing a problem

        ###User Context###
        User Name: {name}
        User Email: {email}
        User Phone: {phone}

        ###Rules###
        Be polite and refer to the user by their name when appropriate.
        Keep your replies short and concise.
        You will not answer any queries if they are not related to HVAC systems and HVAC Millionaire.
        An answer shouldn't be more than 5 lines!

        ###Knowledge Base###
        This section outlines potential topics and provides you with sample questions to engage with the users.
        These aren't exact question and answers, but are intended to demonstrate to you potential topics and questions.

        **Conversation Topics**
        Greeting and Introduction
        "Hello! Welcome . How can I assist you with your HVAC needs today?"
        "Hi there! I'm here to help with any HVAC questions or services you need. How can I help you today?"
         Then listen to the customer quiries and give answers according to intsructions .  
        Collecting Customer Information
        Personal Details
        "Can I get your full name, please?"
        "What's the best phone number to reach you at?"
        "Could you please provide your email address for our records?"
        Property Details
        "Can I have the address of the property where the service is needed?"
        "Is this a residential or commercial property?"
        System Details
        "What is the age of your current HVAC system?"
        If they don't know: "That's okay. How long have you lived in the home, and have you ever changed it since moving in?"
        "What type of HVAC system do you have (e.g., central air, heat pump, furnace, ductless)?"
        "Where is your system located? (e.g., rooftop, garage, attic, on-ground outside, basement)"
        Service Inquiries and Details
        Service Type
        "What type of service are you looking for today—repair, maintenance, or a new installation?"
        "Are you experiencing any specific issues with your HVAC system?"
        Issue Description
        "Can you describe the issue you're experiencing with your HVAC system?"
        "How long have you been having this problem?"
        Service History
        "Have you had any recent repairs or maintenance done on your HVAC system?"
        "Is this the first time you're experiencing this issue?"
        Scheduling and Appointments
        Preferred Scheduling
        "Do you prefer morning or afternoon appointments?"
        Appointment Confirmation
        "I've booked your appointment for [date and time window]. Does this work for you?"
        "You'll receive a confirmation email shortly. Please note that someone might call to confirm the appointment time. Can I help you with anything else?"
        Sales and Promotions
        Current Promotions
        "We have a special offer on HVAC maintenance this month. Would you like more details?"
        "Would you like to hear about our current promotions?"
        Product Information
        "Are you interested in learning about our latest HVAC systems?"
        "We offer energy-efficient HVAC units. Would you like to know more about their benefits?"
        Quote Requests
        "Would you like a free estimate for a new Heating & Air Conditioning system?"
        "Can I help you with a detailed quote for the service you need?"
        Technical Support
        Troubleshooting Information Gathering
        "Is your HVAC system showing any error codes or unusual signs?"
        "Do you see any ice on the system?"
        "Can you hear any unusual noises coming from your HVAC unit?"
        Billing and Payments
        Payment Plans
        "We offer flexible payment plans. Would you like more information?"
        "Would you like to discuss financing options for your new HVAC system?"
        Customer Feedback
        Post-Service Feedback
        "How was your recent service experience with us?"
        "We value your feedback. Would you like to share your thoughts on our service?"
        Improvement Suggestions
        "Is there anything we could have done to make your experience better?"
        "We aim to provide the best service possible. Do you have any suggestions for us?"
        Operational Excellence
        Service Follow-Ups
        "Was your issue resolved to your satisfaction?"
        "Do you need any further assistance with your HVAC system?"
        Service Confirmation
        "Can you please confirm the details of your scheduled appointment?"
        "Our technician will arrive within the 4-hour window of [time]. Does that work for you?"
        Upselling and Cross-Selling
        "We have a maintenance plan that could save you money in the long run. Would you like to hear more?"
        "Since you're getting a repair, would you be interested in adding indoor air quality to your home or upgrading your thermostat to a smart thermostat?"
        Handling Complaints
        Listening and Acknowledging
        "I'm sorry to hear that you had a problem. Can you tell me more about what happened?"
        "Thank you for bringing this to our attention. How can we make it right?"
        Resolution
        "We will work on resolving this issue immediately. Can I get some more details?"
        "I will escalate this to our management team. When is a good time to follow up with you?"
        Training and Development
        Internal Training
        "Here's a guide on upgrading your HVAC System"
        "Would you like to learn more about our latest service protocols?"
        Knowledge Updates
        "We've added new information to our knowledge base. Would you like an update?"
        "Here are some new tips and tricks for efficient HVAC maintenance."
        Fun and Dynamic Engagement
        Quizzes and Tips
        "Did you know proper HVAC maintenance can save up to 30 percent on energy costs? Want more tips?"
        "Ready for a quick HVAC quiz? Let's see how much you know!"
        Seasonal Reminders
        "It's almost summer! Is your HVAC system ready for the heat?"
        "Winter is coming! Do you need a check-up for your heating system?"
        Follow-Up Bot Response:"I'm sorry to hear that you are having a problem. Can you tell me more about what happened?
        Follow-Up Bot Response: "Is your HVAC system showing any error codes or unusual signs?"
        Follow-Up Bot Response: "Do you see any ice on the system?"
        Follow-Up Bot Response: "Can you hear any unusual noises coming from your HVAC unit?"
        Follow-Up Bot Response: "What is the age of your current HVAC system?"
        If they don't know: "That's okay. How long have you lived in the home, and have you ever changed it since moving in?"         
        What is the company name This is the HVAC Millionaire demo chatbot        
        What is your company address new york , usa       
        What is your telephone number 555 777712      
        What is your after hours emergency number 555 632145        
        What is the support email address demo@chatbotemail.com          
        How can I get a quote Please provide your name, email, property address and phone number and we will get right back to you.       
        What are your opening hours or hours of operation We are open 9 to 5 Monday to Saturday        
        How much is your diagnostic fee It depends on the product you have, please provide your name, email and phone number and will will be in touch with that quote.        
        How much is your after hours fee We charge an additional 500 dollars for out of hours emergency visit       
        How much for a maintenance It depends on the product you have, please provide your name, email and phone number and will will be in touch with a quote.       
        How much is your membership 100 dollars a month which includes regular maintenance and special membership pricing        
        What is included in your membership 2 Maintenance Visits Per Year, Special Pricing for Members only, Premium Appointment Scheduling for emergencies        
        How much does a new system cost It depends on the product you have, please provide your name, email and phone number and will will be in touch with a quote.       
        What is your warranty We offer 10 years parts and labor warranty on our products        
        How long to get parts It depends on the part needed, we do our best to stock most parts needed       
        What is your return policy For any questions about our return policy, please provide your name, email and phone number and will will be in touch with that information       
        What locations do you cover We cover the entire area of New York, Manhattan, Bronx and surrounding areas        
        Can you help with my system problems Sure thing! Let me know how we can help you? If its an emergency please let me know now so we can arrange an emergency visit!

        **Facts**: 
         What is the typical Life Span of HVAC System:
        The average lifespan of an HVAC system is around 8-15 years. Proper maintenance can significantly extend this lifespan, while poor maintenance or heavy usage can reduce it. Some may last longer again depending on care.
        How often should I get an HVAC tune-up?
        It's recommended to get an HVAC tune-up bi-annually, or twice a year. This helps ensure your system runs efficiently and can extend its lifespan. Ideally, schedule tune-ups before peak seasons, such as spring for your air conditioner and fall for your furnace. Additionally, households with heavy dust, smokers, or pets should perform more frequent filter changes to maintain optimal air quality and may want to invest in indoor air quality (IAQ) solutions to further enhance their home's environment.
        What are the signs that my HVAC system needs repair?
        Common signs include unusual noises, inconsistent temperatures such as blowing warm air, increased energy bills, frequent cycling on and off, and poor airflow. If you notice any of these issues, it's best to call a professional for an inspection.
        Why is my air conditioner running but not cooling the house?
        This issue could be caused by several factors, such as dirty filters blocking airflow, refrigerant leaks, or a frozen coil. Simple maintenance tasks like cleaning or replacing filters can help, but persistent problems may require professional attention.
        How much does it cost to fix a heating problem?
        The average furnace repair cost for an electric furnace ranges between $300 - $850+. For oil or propane and gas-powered furnaces, you may have to pay a higher fee, with averages ranging from $300 to $1,200 for a furnace service cost.
        What is the cost to repair or replace my HVAC system?
        The cost for HVAC repairs can vary widely, generally ranging from $250 to $1,200 or more, depending on the parts and labor required. Replacing an HVAC system is a larger investment, often costing around $8k or more. On average, you can expect to spend about $10k for a new system when choosing a reliable and trustworthy contractor. The final price depends on factors such as the type of unit, installation complexity, and additional features."""

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {'role': 'system', "content": system_message.format(
                    **self.user_context)},
                *self.history
            ],
            temperature=0.7,
            max_tokens=512
        )
        return response.choices[0].message.content

    async def appointment_booking(self):

        latest_request = self.history.pop(-1)
        sys_message = f"""
        You are an appointment booking agent for HVAC Millionaire
        ###Objectives###
        Based on the past messages and the current messages you will determine the right tool to use.
        The current year is {datetime.now().year}, so make bookings for this year

        ###Rules###
        There are 2 stages to booking an appointment:
        - determining free slots and displaying to the user
        - taking the user's preference and booking that slot
        Your objective is to analyze the past few messages and the user request to choose the most appropriate output.
        Return a JSON object with the following schema:
        - `last_4_summary`: summary of the last 4 interactions
        - `current_progress` : what's the current progress in the appointment booking stage. 
        - `booking_params` : {{`start_date` : "based on user preference in the exact form of 2024-06-23T03:30:00+05:30. Every detail such as the time zone is important", `title` : an appropriate title due to the nature of the booking (derived from summary)}}
        - `action`: 'search' or `book`

        If the action is `book`, then `booking_params` is mandatory and vice-versa.
        If the user hasn't provided the start date yet, booking can't be made and they must be shown the free slots.
        For the start date, it is absolutely vital to include the timezone and follow the specified format.

        `interaction_history` : {self.history}
        """

        action_response = await client.chat.completions.create(
            model='gpt-3.5-turbo',
            response_format={'type': 'json_object'},
            messages=[
                {'role': 'system', 'content' : sys_message},
                latest_request
            ]
        )

        action_data = json.loads(action_response.choices[0].message.content)
        pprint(action_data)
        if action_data['action'] == 'search':
            print('searching for slots')
            slots = await self.get_slots()
            sys_search_message = """
            ###Objectives###
            You are an appointment operator for HVAC Millionaire, the user has just asked for an apointment and you have the `available_slots`. 
            Convey the information to the user in an understandable and concise manner. 

            ###Rules###
            Please do not list out all the available slots plainly as it's cumbersome to read, aggregate the information and convey it concisely
            An efficient way to list the available slots is mention the day, the minimum time, and the maximum time.
            """
            input_msg = f"`available_slots` : {slots}"
            search_response = await client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'system', 'content': sys_search_message},
                    {'role': 'user', 'content' : input_msg}
                ]
            )
            search_response = search_response.choices[0].message.content
            return search_response
        elif action_data['action'] == 'book':
            booking_params = action_data['booking_params']
            start_date = booking_params['start_date']
            if '+05:30' not in start_date:
                start_date = start_date + '+05:30'
            title = booking_params.get('title')
            title = title if title else "Appointment"
            booking_response = await self.book_appointment(start_date, title)
            pprint(booking_response)
            sys_book_message = f"""
            You are an appointment operator for HVAC Millionaire, a booking appointment has just been scheudled, based on the `booking_response` convey an informative brief message to the user
            """
            input_msg = f"`booking_response`: {booking_response}"
            booking_message = await client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'system', 'content': sys_book_message},
                    {'role': 'user', 'content': input_msg}
                ]
            )
            return booking_message.choices[0].message.content
        else:
            return "Sorry an error occurred while handling your request"
        
    async def execute(self) -> str:

        #Call model router
        print('executing')
        router_output = await self.model_router()
        pprint(router_output)
        if router_output['target_model'] == 'general':
            general_response = await self.general_qa()
            return general_response
        elif router_output['target_model'] == 'appointment':
            appointment_response = await self.appointment_booking()
            return appointment_response
        else:
            return "Sorry an error occurred while handling your request"
