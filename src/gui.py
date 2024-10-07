from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
import re
import weather_data_analysis as an

# a function to link button for temperature trend for all cities available to the corresponding function
def date_combiner() -> tuple[str, str]:
    """
    Combines user input from GUI fields to create starting and ending timestamps.

    Returns:
        tuple: A tuple containing the starting and ending timestamps in ISO format.
            - starting_date (str): The start timestamp (e.g., '2024-10-01T10:00:00').
            - ending_date (str): The end timestamp (e.g., '2024-10-07T18:00:00').
    """
    start_year = starting_year_entry.get()
    start_month = starting_month_entry.get()
    start_day = starting_day_entry.get()
    start_hour = starting_hour_entry.get()
    start_minute = starting_minute_entry.get()

    end_year = ending_year_entry.get()
    end_month = ending_month_entry.get()
    end_day = ending_day_entry.get()
    end_hour = ending_hour_entry.get()
    end_minute = ending_minute_entry.get()

    starting_date = start_year + "-" + start_month + "-" + start_day + "T" + start_hour + ":" + start_minute + ":00"
    ending_date = end_year + "-" + end_month + "-" + end_day + "T" + end_hour + ":" + end_minute + ":00"

    return starting_date, ending_date


def on_button_click_plot_graph() -> None:
    """
    Handles the button click event for plotting the temperature trends graph.

    Retrieves the starting and ending timestamps from user input, then calls the
    mean_temperature_per_hr_comp_diff_city function to plot the graph.
    """
    starting_date, ending_date = date_combiner()

    try:
        an.mean_temperature_per_hr_comp_diff_city(starting_date, ending_date)
    except (TypeError, AttributeError, ValueError):
        text="Input Error" + "\n"
        text_area.insert(1.0, text)


def clear_text_area() -> None:
    """
    Clears the messages displayed in the text area.

    """
    text_area.delete(1.0, tk.END)


# clear the default text in the date entry box
def clear_default_text(event: tk.Event) -> None:
    """
    Clears the default text in the date entry box when the user interacts with it.

    Args:
        event (tk.Event): The event triggered by the widget (e.g., a mouse click).

    """
    entry = event.widget # get the widget that triggered the event

    year_condition = entry.get() == 'yyyy'
    month_condition = entry.get() == 'mm'
    day_condition = entry.get() == 'dd'
    hour_condition = entry.get() == 'HH'
    minute_condition = entry.get() == 'MM'
    total_condition = year_condition or month_condition or \
          day_condition or hour_condition or minute_condition

    if total_condition:
        entry.delete(0, tk.END) # delete the content from the begining to the end 
        entry.config(fg="black")


def display_input() -> bool:
    """
    Displays the selected city, function, and date interval to the user.

    Returns:
        bool: True if input is valid, False otherwise.
    """
    city = city_combo.get()
    function = function_combo.get()
    starting_date, ending_date = date_combiner()
    date_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
    if city and function and re.match(date_pattern, starting_date) and re.match(date_pattern, ending_date):
        messagebox.showinfo(
            message=f"{function} for {city} starting from {starting_date} to {ending_date}",
            title="Input"
        )
        return True
    else: 
        messagebox.showinfo(
            message=f"Incorrect input of city, function or interval",
            title="Error"
        )
        return False

# Connect the enter button to plot the graph or print out weather
def on_button_click_print_data_or_plot_graph() -> None:
    """
    Handles the button click event for printing weather data or plotting the temperature trends graph.

    Retrieves user input (city, function, and date interval) and performs the corresponding action.
    """
    is_correct_input = display_input()
    if is_correct_input:
        function = function_combo.get()
        starting_date, ending_date = date_combiner()
        city = city_combo.get()
        # Execute the print function if selected one
        if re.match(r'\bPrint\b', function):
           df = an.fetch_data_from_db(city, starting_date, ending_date)
           text_area.insert(1.0, df) 
        
        else:
            an.temperature_trends_graph(city, starting_date, ending_date)
    else:
        text = 'Input Error' +'\n'
        text_area.insert(1.0, text)


# initialize the root
root = tk.Tk()
root.title("Weather Data Analysis GUI") # title at top
root.geometry("435x400") # size of window

# interval label
label_interval = tk.Label(root, text="Please enter the interval: ")
label_interval.grid(row=0, column=0)

# entry for starting year
starting_year_entry = tk.Entry(root, width=4)
starting_year_entry.place(x=135, y=0)
starting_year_entry.insert(0, 'yyyy')
starting_year_entry.config(fg='gray')
starting_year_entry.bind("<FocusIn>", clear_default_text)

# entry for starting month
starting_month_entry = tk.Entry(root, width=4)
starting_month_entry.place(x=165, y=0)
starting_month_entry.insert(0, 'mm')
starting_month_entry.config(fg='gray')
starting_month_entry.bind("<FocusIn>", clear_default_text)

# entry for starting day
starting_day_entry = tk.Entry(root, width=3)
starting_day_entry.place(x=195, y=0)
starting_day_entry.insert(0, 'dd')
starting_day_entry.config(fg='gray')
starting_day_entry.bind("<FocusIn>", clear_default_text)

# entry for starting hour
starting_hour_entry = tk.Entry(root, width=3)
starting_hour_entry.place(x=219, y=0)
starting_hour_entry.insert(0, 'HH')
starting_hour_entry.config(fg='gray')
starting_hour_entry.bind("<FocusIn>", clear_default_text)

# entry for starting minute
starting_minute_entry = tk.Entry(root, width=4)
starting_minute_entry.place(x=243, y=0)
starting_minute_entry.insert(0, 'MM')
starting_minute_entry.config(fg='gray')
starting_minute_entry.bind("<FocusIn>", clear_default_text)

# to
label_to = tk.Label(root,text="to")
label_to.place(x=275, y=0)

# entry for ending year
ending_year_entry = tk.Entry(root, width=4)
ending_year_entry.place(x=296, y=0)
ending_year_entry.insert(0, 'yyyy')
ending_year_entry.config(fg='gray')
ending_year_entry.bind("<FocusIn>", clear_default_text)

# entry for ending month
ending_month_entry = tk.Entry(root, width=4)
ending_month_entry.place(x=325, y=0)
ending_month_entry.insert(0, 'mm')
ending_month_entry.config(fg='gray')
ending_month_entry.bind("<FocusIn>", clear_default_text)

# entry for ending day
ending_day_entry = tk.Entry(root, width=3)
ending_day_entry.place(x=354, y=0)
ending_day_entry.insert(0, 'dd')
ending_day_entry.config(fg='gray')
ending_day_entry.bind("<FocusIn>", clear_default_text)

# entry for ending hour
ending_hour_entry = tk.Entry(root, width=3)
ending_hour_entry.place(x=376, y=0)
ending_hour_entry.insert(0, 'HH')
ending_hour_entry.config(fg='gray')
ending_hour_entry.bind("<FocusIn>", clear_default_text)

# entry for ending minute
ending_minute_entry = tk.Entry(root, width=4)
ending_minute_entry.place(x=400, y=0)
ending_minute_entry.insert(0, 'MM')
ending_minute_entry.config(fg='gray')
ending_minute_entry.bind("<FocusIn>", clear_default_text)

# separator betweeen timestamp section and other section
separator1 = ttk.Separator(root, orient='horizontal')
separator1.place(x=0, y=25, relwidth=1)

# label for the plot of temperature trend for all cities available
all_city_plot_label = tk.Label(root, text="Plot the temperature trend for all cities available")
all_city_plot_label.place(x=85, y=30)

# button for temperature trend for all cities available
plot_graph_button = ttk.Button(text="Plot Graph", command=on_button_click_plot_graph)
plot_graph_button.place(x=180, y=60)


# label for city selection
city_label = tk.Label(root, text="City")
city_label.place(x=90, y=100)

# combobox for city selection
city_combo = ttk.Combobox(
    state="readonly",
    values=["Hong Kong", "New York", "Tokyo"]
)
city_combo.place(x=35, y=130)

# separator betweeen city section and function senction
separator2 = ttk.Separator(root, orient='vertical')
separator2.place(x=220, y=95, relheight=0.18)

# label for function selection
function_label = tk.Label(root, text="function")
function_label.place(x=300, y=100)


# combobox for function selection
function_combo = ttk.Combobox(
    state="readonly",
    values=["Print weather data", "Plot temperature graph"]
)
function_combo.place(x=260, y=130)

# separator for all city trend graph and other section
separator3 = ttk.Separator(root, orient='horizontal')
separator3.place(x=0, y=95, relwidth=1)

# button for the confirmation of the input of city and function
enter_button = ttk.Button(text="Enter", command=on_button_click_print_data_or_plot_graph)
enter_button.place(x=330, y=360)

# text area to show the weather data or error messages
text_area = ScrolledText(root, width=45, height=11)
text_area.place(x=30, y=170)

# button to clear the messages on the text area
clear_button = ttk.Button(text="Clear", command=clear_text_area)
clear_button.place(x=20, y=360)

root.mainloop()
