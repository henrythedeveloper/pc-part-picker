import utils
import streamlit as st
from .suggestion import suggest_build
from langchain.schema import AIMessage, HumanMessage

def chat_with_bot():
    st.subheader("Get PC Build Suggestions")

    # Initialize session state variables
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if "budget" not in st.session_state:
        st.session_state["budget"] = 0.0

    if "preferences" not in st.session_state:
        st.session_state["preferences"] = {}

    # Collect user budget and preferences
    budget_input = st.number_input("Enter your budget in USD", min_value=0.0, value=1000.0)
    st.session_state["budget"] = budget_input

    # brand_preference = st.selectbox("Preferred CPU Brand (optional)", options=["No Preference", "Intel", "AMD"])
    # if brand_preference != "No Preference":
    #     st.session_state["preferences"]["brand"] = brand_preference
    # else:
    #     st.session_state["preferences"].pop("brand", None)

    # Suggest a build
    build, remaining_budget = suggest_build(st.session_state["budget"], st.session_state["preferences"])

    # Display the suggested build
    st.subheader("Suggested PC Build")
    if build:
        total_price = 0
        for comp_type, comp in build.items():
            st.write(f"**{comp_type}:** {comp['name']} - ${comp['price']:.2f}")
            total_price += comp['price']
        st.write(f"**Total Price:** ${total_price:.2f}")
        st.write(f"**Remaining Budget:** ${remaining_budget:.2f}")
    else:
        st.write("Unable to suggest a build within your budget")

    # User prompt
    user_input = st.text_input("Ask any questions or request changes to the build:", key="user_input")

    if st.button("Submit Query"):
        if user_input:
            llm = utils.configure_llm()

            # Prepare messages
            messages = []

            # Build the full user message with context
            full_user_message = (
                "I have the following PC build:\n"
            )
            for comp_type, comp in build.items():
                full_user_message += f"- {comp_type}: {comp['name']} (${comp['price']:.2f})\n"
            full_user_message += f"Total Price: ${total_price:.2f}\n"
            full_user_message += f"Remaining Budget: ${remaining_budget:.2f}\n\n"
            full_user_message += "Please help me with the following:\n"
            full_user_message += user_input

            # Add previous chat history
            for chat in st.session_state["chat_history"]:
                if chat["role"] == "user":
                    messages.append(HumanMessage(content=chat["content"]))
                else:
                    messages.append(AIMessage(content=chat["content"]))

            # Add current user message
            messages.append(HumanMessage(content=full_user_message))

            try:
                # Call the llm instance directly with messages
                response = llm(messages)
                assistant_reply = response.content

            except Exception as e:
                st.error(f"An error occurred: {e}")
                return

            # Update chat history
            st.session_state["chat_history"].append({"role": "user", "content": full_user_message})
            st.session_state["chat_history"].append({"role": "assistant", "content": assistant_reply})

            # Display chat history
            for chat in st.session_state["chat_history"]:
                if chat["role"] == "user":
                    st.markdown(f"**You:** {chat['content']}")
                else:
                    st.markdown(f"**Assistant:** {chat['content']}")
        else:
            st.error("Please enter your question or request.")
