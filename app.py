import streamlit as st
from groq import Groq

# Page layout setup
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags instantly.")

# Secure API Key input or fetch from Streamlit Secrets
groq_api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

# Form controls for user selection
content_type = st.selectbox(
    "Content Type",
    ["Social Media Post", "Blog Intro", "Product Announcement", "Newsletter Snippet"]
)

platform = st.selectbox(
    "Target Platform",
    ["LinkedIn", "Twitter / X", "Instagram", "Facebook"]
)

topic = st.text_input("Topic", placeholder="e.g., Productivity hacks for remote software developers")

target_audience = st.text_input("Target Audience", placeholder="e.g., Tech professionals, beginners, entrepreneurs")

tone = st.selectbox(
    "Tone",
    ["Professional", "Casual & Engaging", "Witty & Humorous", "Inspirational", "Persuasive"]
)

# Button to trigger generation
if st.button("Generate Content", type="primary"):
    if not groq_api_key:
        st.error("Please enter your Groq API Key in the sidebar to proceed.")
    elif not topic or not target_audience:
        st.warning("Please fill in both the Topic and Target Audience fields.")
    else:
        try:
            # Initialize Groq client
            client = Groq(api_key=groq_api_key)

            # Construct system and user prompt
            prompt = f"""
            You are an expert content creator. Create a complete social media post based on the following details:
            - Content Type: {content_type}
            - Platform: {platform}
            - Topic: {topic}
            - Target Audience: {target_audience}
            - Tone: {tone}

            Requirements:
            1. Provide a main body post/caption formatted properly for {platform}.
            2. Include a strong call to action (CTA).
            3. Include 5-10 highly relevant hashtags at the end.
            """

            with st.spinner("Generating content..."):
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a professional social media and content strategist."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                )

                generated_text = response.choices[0].message.content

            st.success("Content Generated Successfully!")
            st.markdown("### Generated Post")
            st.write(generated_text)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")