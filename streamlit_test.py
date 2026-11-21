# import streamlit as st
# import re

# st.set_page_config(page_title="Page Title", layout="wide")

# st.markdown("""
#     <style>
#         .reportview-container {
#             margin-top: -2em;
#         }
#         #MainMenu {visibility: hidden;}
#         .stDeployButton {display:none;}
#         footer {visibility: hidden;}
#         #stDecoration {display:none;}
#     </style>
# """, unsafe_allow_html=True)

# st.write("Here's our first attempt at using data to create a table:")

# st.divider()

# # Define the regex pattern
# email_pattern = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# # Create the input field
# email = st.text_input("Enter your email:")

# # Check if the input matches the regex
# if email:  # Only check if there's some input
#     if re.match(email_pattern, email):
#         st.success("Valid email address.")
#     else:
#         st.error("Invalid email. Please enter a valid email address.")
        
# st.divider()

# # Create the input field
# username = st.text_input("Enter your username:")
# password = st.text_input("Enter your password:", type="password")

# # Check if the input matches the regex
# if username and password:  # Only check if there's some input
#     if username == "admin" and password == "admin":
#         st.success("Valid credentials.")
#     else:
#         st.error("Invalid credentials. Please enter valid credentials.")

# # button save file
# if st.button("Save file"):
#     with open("data.txt", "w") as file:
#         #save data from inputs to file
#         file.write(f"Email: {email}\n")
#         file.write(f"Username: {username}\n")
#         file.write(f"Password: {password}\n")
        
#         st.success("File saved successfully.")


    
import dash
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State
import re

# Inicjalizacja aplikacji Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Here's our first attempt at using data to create a table:"),
    html.Div([
        dcc.Input(id='email-input', type='email', placeholder="Enter your email:"),
        html.Div(id='email-output')
    ]),
    html.Div([
        dcc.Input(id='username-input', type='text', placeholder="Enter your username:"),
        dcc.Input(id='password-input', type='password', placeholder="Enter your password:"),
        html.Div(id='credentials-output')
    ]),
    html.Button('Save File', id='save-button', n_clicks=0),
    html.Div(id='save-output')
])

@app.callback(
    Output('email-output', 'children'),
    [Input('email-input', 'value')]
)
def check_email(email):
    if email:
        email_pattern = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_pattern, email):
            return None
        else:
            return "Invalid email. Please enter a valid email address."
    return ''

@app.callback(
    Output('save-output', 'children'),
    Input('save-button', 'n_clicks'),
    State('email-input', 'value'),
    State('username-input', 'value'),
    State('password-input', 'value')
)
def save_file(n_clicks, email, username, password):
    if n_clicks > 0:
        with open("data.txt", "w") as file:
            file.write(f"Email: {email}\n")
            file.write(f"Username: {username}\n")
            file.write(f"Password: {password}\n")
        
        # Instrukcja dla użytkownika, jak zamknąć aplikację
        return "File saved successfully. Please close this tab to exit."
    return ''


if __name__ == '__main__':
    app.run_server(debug=True)


