import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title('My parents new healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Display the table on the page.
streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

#function definition
def get_fruityvice_data(this_fruit_choice):
    #streamlit.write('The user entered ', fruit_choice)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)  
    
    # normalize the above data
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#New section to display Fruitvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
    #Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        streamlit.error("Please select the fruit to get information")
    else: 
        back_from_function = get_fruityvice_data(fruit_choice)
           
        # print this data
        streamlit.dataframe(back_from_function)
except:
    streamlit.text('Error')

streamlit.header("The fruit load list contains:")

#function to load fruit list when the button is clicked
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("Select * from fruit_load_list")
        return my_cur.fetchall() #fetchone()

#add button to load the fruit
if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close() #to close SF connection
    streamlit.dataframe(my_data_rows)


#except URLError as e:
#    streamlit.stop()
#streamlit.text("Hello from Snowflake:")
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")

#Allow end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+ new_fruit + "')")
        return "Thanks for adding " + new_fruit
        
add_my_fruit=streamlit.text_input("What fruit would you like to add?")
if streamlit.button('Add a fruit to the list list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    add_my_fruit=streamlit.text_input('Enter fruit name: ' )
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close() #to close SF connection
    streamlit.text(back_from_function)
