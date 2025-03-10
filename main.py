import streamlit as st
import pandas as pd
import datetime
import json
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Title
st.title("Employee News Updater")
# TODO: if json files exist
# Load schedule data (JSON format with grouped days)
# uploaded_file = st.file_uploader("schedule", type=["json"])
uploaded_file = open("schedule.json")
news_file = open("news.json")
emplyees_file = open("employees.json")
col1, col2 = st.columns(2)

schedule_data = json.load(uploaded_file)
# today = datetime.date.today().strftime("%Y-%m-%d")

if "last_selected_date" not in st.session_state:
    st.session_state["last_selected_date"] = None
    st.session_state["news"] = set()


with st.sidebar:
    st.subheader("Select Date")
    selected_date = st.date_input("Choose a date:", datetime.date.today())
    selected_date_str = selected_date.strftime("%Y-%m-%d")
 # If the date changes, reset all fields
    if selected_date_str != st.session_state["last_selected_date"]:
        st.session_state["news"] = set()
        st.session_state["last_selected_date"] = selected_date_str
        
# Find today's schedule
today_schedule = next((day for day in schedule_data if day["date"] == selected_date_str), None)
employees_all: pd.DataFrame = pd.read_json(emplyees_file)
# Display today's schedule
with col2:
    st.subheader(f"Employees Working Today ({selected_date_str}):")
    if today_schedule:
        employees_today = pd.DataFrame(today_schedule["schedule"])
        employees_today.drop(columns=["scheduleId"], inplace=True)  # Remove unnecessary column
        with st.expander("Employee Details"):
            st.write(employees_today)
    else:
        st.write("No employees scheduled for today.")

# Input news updates
with col1:
    st.subheader("Today's news/updates")
    new_update_choice = st.radio("Do want to add anything?", ["Yes", "No"], index=None, horizontal=True)
    if new_update_choice == "Yes":
        news_input = set(st.text_area("News for today: (One title per line)").split("\n")) #TODO: seperate by \n
        # remove empty strings and string with only spaces
        news_input = {news.strip() for news in news_input if news.strip()}
        if st.button("Save News"):
            if news_input:
                st.session_state["news"] = news_input #TODO: add a feature that if user returns to add news, it will add to existing news
                st.success("News updated for today!")
    else:
        pass

#check if employees_all have a "news" column, if not, add it
if "news" not in employees_all.columns:
    employees_all["news"] = [set() for _ in range(len(employees_all))]

else:
    employees_all["news"] = employees_all["news"].apply(lambda x: set(x))

#append todays news to employees_all
employees_all["news"] =  employees_all["news"].apply(lambda x: x | st.session_state.get("news", set()))


with col1:
    # Display news 
    if "news" in st.session_state:
        st.subheader("Today's News:")
        st.markdown("\n".join(f"- {item}" for item in st.session_state["news"]))
    
    manual_update_choice= st.radio("Do you want to update each employee manually?", ["Yes", "No"], index=None, horizontal=True)

if manual_update_choice == "Yes":
    updated_employees = st.multiselect("Mark employees who received the news:", employees_today["employeeId"].tolist())
    if st.button("Confirm Updates"):
        st.session_state["updated_employees"] = updated_employees
        st.success(f"Updated employees: {', '.join(map(str, updated_employees))}")
        # remove todays news from selected employees
        for employee_id in updated_employees:
            employees_all.loc[employees_all["employeeId"] == employee_id, "news"] = employees_all["news"].apply(lambda x: x - st.session_state.get("news", set()))

elif manual_update_choice == "No":
    st.write("The list will be updated automatically.")
    # remove todays news from all today's employees
    for employee_id in employees_today["employeeId"].tolist():
        employees_all.loc[employees_all["employeeId"] == employee_id, "news"] = employees_all["news"].apply(lambda x: x - st.session_state.get("news", set()))

# update employees.json
# ask user if they want to update employees.json
# if yes, update employees.json
if st.button("Update employees.json"):
    employees_all.to_json("employees.json", orient="records", indent=4)
    st.success("employees.json updated!")

