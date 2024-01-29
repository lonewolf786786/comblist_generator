import streamlit as st
from faker import Faker
import random
import string
import base64  # Needed for encoding the download data

fake = Faker()

# Function to generate a username based on the keyword
def generate_username(keyword, use_faker=True):
    if use_faker:
        username = fake.user_name()
    else:
        username = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    return f"{keyword}_{username}"

# Function to generate a realistic email
def generate_email(username):
    return fake.ascii_free_email()

# Function to generate a password
def generate_password(min_length=8, max_length=12):
    common_words = ['password', '123456', 'qwerty', 'abc123', 'letmein', 'monkey', 'dragon']
    base = random.choice(common_words)
    random_chars = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(random.randint(2, max_length - len(base))))
    return base + random_chars

# Function to create a combolist based on the given parameters
def create_combolist(keyword, num_entries=10, use_faker=True):
    combolist = []
    for _ in range(num_entries):
        username = generate_username(keyword, use_faker)
        email = generate_email(username)
        password = generate_password()
        combolist.append(f"{username}:{email}:{password}")
    return combolist

# Function to create a download button for the combolist
def download_button(combolist, filename):
    combolist_str = "\n".join(combolist)
    b64 = base64.b64encode(combolist_str.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download Combolist</a>'
    st.markdown(href, unsafe_allow_html=True)

# Streamlit UI setup
st.title("Combolist Generator")

# UI elements for user input
keyword = st.text_input("Enter a keyword (e.g., 'amazon'):", "amazon")
num_entries = st.number_input("Number of entries:", min_value=1, value=50)
show_combolist = st.checkbox("Show combolist in the portal")
generate_button = st.button("Generate Combolist")

# Handling the combolist generation and download
if generate_button:
    combolist = create_combolist(keyword, num_entries, True)
    download_button(combolist, f"{keyword}_combolist.txt")
    if show_combolist:
        st.text_area("Generated Combolist:", "\n".join(combolist), height=250)
