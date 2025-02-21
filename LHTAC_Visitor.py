from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import json
from datetime import datetime

# File to store visitor data
data_file = "visitors.json"

# Function to load visitor data
def load_data():
    try:
        with open(data_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Function to save visitor data
def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f, indent=4)

# Function to log full visitor details when they sign out
def log_sign_out(visitor):
    """Log full visitor details when signing out."""
    log_entry = (
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Visitor Signed Out\n"
        f"Name: {visitor['first_name']} {visitor['last_name']}\n"
        f"Email: {visitor['email']}\n"
        f"Company: {visitor['company']}\n"
        f"Purpose: {visitor['purpose']}\n"
        f"------------------------------\n"
    )

    try:
        with open("signout_log.txt", "a") as log_file:
            log_file.write(log_entry)
        print("Sign-out recorded successfully.")
    except Exception as e:
        print(f"Failed to log sign-out: {e}")

class VisitorApp(App):
    def build(self):  
        self.layout = BoxLayout(orientation='vertical')  
        self.show_home()
        return self.layout

    def show_home(self):
        self.layout.clear_widgets()
        self.signin_button = Button(text="Sign In", on_press=self.sign_in_screen)
        self.signout_button = Button(text="Sign Out", on_press=self.sign_out_screen)
        self.layout.add_widget(self.signin_button)
        self.layout.add_widget(self.signout_button)

    def sign_in_screen(self, instance):
        self.layout.clear_widgets()
        self.first_name = TextInput(hint_text="First Name")
        self.last_name = TextInput(hint_text="Last Name")
        self.email = TextInput(hint_text="Email")
        self.company = TextInput(hint_text="Company")
        self.purpose = TextInput(hint_text="Purpose of Visit")
        self.submit_button = Button(text="Submit", on_press=self.submit_sign_in)
        self.back_button = Button(text="Back", on_press=lambda x: self.show_home())

        self.layout.add_widget(self.first_name)
        self.layout.add_widget(self.last_name)
        self.layout.add_widget(self.email)
        self.layout.add_widget(self.company)
        self.layout.add_widget(self.purpose)
        self.layout.add_widget(self.submit_button)
        self.layout.add_widget(self.back_button)

    def submit_sign_in(self, instance):
        data = load_data()
        entry = {
            "first_name": self.first_name.text.strip(),
            "last_name": self.last_name.text.strip(),
            "email": self.email.text.strip(),
            "company": self.company.text.strip(),
            "purpose": self.purpose.text.strip()
        }
        if all(entry.values()):
            data.append(entry)
            save_data(data)
            self.show_home()
        else:
            popup = Popup(title="Error", content=Label(text="All fields must be filled in."), size_hint=(0.6, 0.4))
            popup.open()

    def sign_out_screen(self, instance):
        self.layout.clear_widgets()
        self.first_name = TextInput(hint_text="First Name")
        self.last_name = TextInput(hint_text="Last Name")
        self.signout_button = Button(text="Sign Out", on_press=self.submit_sign_out)
        self.back_button = Button(text="Back", on_press=lambda x: self.show_home())

        self.layout.add_widget(self.first_name)
        self.layout.add_widget(self.last_name)
        self.layout.add_widget(self.signout_button)
        self.layout.add_widget(self.back_button)

    def submit_sign_out(self, instance):
        data = load_data()
        first_name = self.first_name.text.strip()
        last_name = self.last_name.text.strip()
        
        for visitor in data:
            if visitor["first_name"].lower() == first_name.lower() and visitor["last_name"].lower() == last_name.lower():
                data.remove(visitor)
                save_data(data)
                log_sign_out(visitor)  # Log full visitor details on sign-out
                self.show_home()
                return
        
        popup = Popup(title="Error", content=Label(text="Name not found. Try again."), size_hint=(0.6, 0.4))
        popup.open()

if __name__ == "__main__":
    VisitorApp().run()
