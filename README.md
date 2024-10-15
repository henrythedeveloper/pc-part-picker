# **PC Part Picker**

## **Overview**

Welcome to the **PC Part Picker**! This application helps you build your own custom PC based on your budget and preferences. Simply input your budget and any specific preferences (like your favorite CPU brand), and the app will suggest a PC build tailored just for you.

## **Features**

- **Budget-Based Suggestions**: Get PC component recommendations that fit within your budget.
- **Preference Selection**: Choose your preferred CPU brand (Intel or AMD) if you have one.
- **Interactive Chat**: Ask questions or request changes to the suggested build through a chat interface.
- **Detailed Component Information**: View the components selected for you, including their names and prices.
- **Remaining Budget Calculation**: See how much of your budget remains after the suggested build.

## **How It Works**

1. **Input Your Budget**: Enter the amount you're willing to spend on your new PC.
2. **Select Preferences**: Choose your preferred CPU brand, or leave it as "No Preference".
3. **Get Suggestions**: The app will generate a PC build that fits your budget and preferences.
4. **Interact with the Assistant**: Use the chat interface to ask questions or request modifications to the build.
5. **Finalize Your Build**: Review the suggested components and make any desired changes.

---

## **Getting Started**

### **Prerequisites**

- **Python 3.7 or higher**
- **pip** (Python package manager)

### **Installation Steps**

1. **Clone the Repository**

  ```bash
  git clone https://github.com/yourusername/pc-part-picker.git
  cd pc-part-picker
  ```
   
2. **Create a Virtual Environment (Optional but Recommended)**

  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
  ```

3. **Install Dependencies**
  ```bash
  pip install -r requirements.txt
  ```

4. **Set Up the NVIDIA API Key**
The application requires an NVIDIA API key to function. You need to add this API key to the application securely.

  Steps:
  - Create a `.streamlit` Folder
    In the root directory of the project, create a folder named .streamlit:

  ```bash
  mkdir .streamlit
  ```
  - Create a `secrets.toml` File
    Inside the `.streamlit` folder, create a file named `secrets.toml`:

  ```bash
  touch .streamlit/secrets.toml
  ``` 
  **Note**: Replace `"your_actual_api_key_here"` with your actual NVIDIA API key.
  **Important**: Do not commit your `secrets.toml` file to version control (e.g., GitHub) to keep your API key secure.

5. **Run the Application**

```bash
streamlit run app.py
```

6. **Interact with the Application**
- Open the URL provided by Streamlit in your web browser.
- Input your budget and preferences.
- Review the suggested PC build.
- Use the chat interface to ask questions or request changes.

7. **Deactivate the Virtual Environment (If Activated)**
When you're done using the application, you can deactivate the virtual environment by running:

```bash
Deactivate
```
**Note**: This returns your terminal session to the global Python environment.

---

## **File Explanations**

### **1. `app.py`**

#### **Purpose**: 
This is the main file that runs the Streamlit application.

#### **Overview**:
- Imports:
	- `streamlit` for building the web interface.
	- `chat_with_bot` function from `components.chat_interface` to handle user interaction.

- Functionality:
	- Sets up the page configuration with a title and icon.
	- Displays the main title and a brief introduction to the app.
	- Calls the `chat_with_bot()` function to start the interactive chat interface.

---

### **2. `components/chat_interface.py`**

#### **Purpose**: Handles the user interface for collecting input and interacting with the assistant.

#### **Overview**:
- Imports:
	- `streamlit` for creating UI elements.
	- `utils`for configuring the language model.
	- `suggest_build function` from `components.suggestion` for generating component suggestions.
	- `AIMessage`, `HumanMessage` from `langchain.schema` for structuring chat messages.
- **Functionality**:
	- Collects user input for budget and CPU brand preference.
	- Generates a suggested PC build based on the user's budget and preferences.
	- Displays the suggested build with component names and prices.
	- Provides an input field for the user to ask questions or request changes.
	- Handles the chat interaction by sending messages to the language model and displaying responses.

#### **Usage**:

This module is called by `app.py` and does not need to be run separately. It defines the `chat_with_bot()`function that creates the chat interface within the app.

---

### **3. `components/suggestion.py`**

#### **Purpose**: 
Contains the logic for suggesting a PC build based on the user's budget and preferences.

#### **Overview**:
- **Imports**:
	- `load_components` from `components.data_loader` to access component data.
- **Functionality**:
    
	- Defines the `suggest_build()` function.
	- Loads component data from the JSON file.
	- Filters components based on the user's preferences (like CPU brand).
	- Selects the best components that fit within the user's budget.
	- Prioritizes components by importance and price.

#### **Usage**:
This module is used by `chat_interface.py` to generate the initial PC build suggestion. It is not run directly.

---

### **4. `components/data_loader.py`**

#### **Purpose**:
Handles loading of component data from a JSON file.

#### **Overview**:
- **Imports**:
	- `json` for parsing JSON files.
	- `os` for file path handling.
- **Functionality**:
	- Defines the `load_components()` function.
	- Opens and reads the `components_data.json` file.
	- Parses the JSON data and returns it as a Python dictionary.

#### **Usage**:
This module is used by `suggestion.py` to access the available PC components. It is not run directly.

---

### **5. `components_data.json`**

#### **Purpose**:
Stores data about available PC components, including CPUs, motherboards, GPUs, RAM, storage devices, power supplies, and cases.
#### **Overview**:
- **Structure**:
	- The data is organized into categories, each containing a list of components.
	- Each component has details like name, brand, price, and specifications.
- **Example Data**:
```json
  {
  "cpus": [
    {
      "name": "Intel Core i9-12900K",
      "brand": "Intel",
      "socket": "LGA1700",
      "price": 599.99,
      "cores": 16,
      "threads": 24
    }
    // More CPUs...
  ],
  "motherboards": [
    // Motherboard data...
  ],
  // Other component categories...
}
```
#### **Usage**:
This file is read by `data_loader.py` to provide component information to the rest of the application. You can update this file to add or modify components.

---

### **6. `utils.py`**

#### **Purpose**:
Configures the language model used for generating assistant responses.
#### **Overview**:
- **Imports**:
	- `streamlit` for accessing secrets.
	- Language model classes from `langchain` or the specific LLM library you're using.
- **Functionality**:
	- Defines the `configure_llm()` function.
	- Retrieves the API key from the `secrets.toml` file.
	- Configures and returns the language model instance.
#### **Usage**:
- **API Key Setup**:
	- The API key is securely stored in `.streamlit/secrets.toml`.
	- Streamlit automatically loads secrets from this file, making them accessible via `st.secrets`.
- **Example `utils.py` Implementation**:
  ```python
	import streamlit as st
	from langchain.chat_models import ChatOpenAI  # Adjust based on your LLM
	
	def configure_llm():
	nvidia_api_key = st.secrets["api_keys"]["nvidia_api_key"]
	llm = ChatOpenAI(
	openai_api_key=nvidia_api_key,
	model_name="gpt-3.5-turbo",  # Replace with your model
	temperature=0.7,
	max_tokens=1024
	)
	return llm
    ```
#### **Note**:
- Adjust the model configuration based on the LLM you're using.
- Ensure the necessary libraries are installed.

---

### **7. `requirements.txt`**

#### **Purpose**:
Lists all the Python libraries and dependencies required to run the application.
#### **Overview**:

- **Example Entries**:

```bash
streamlit
langchain
openai  # If using OpenAI's models
```
#### **Usage**:

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

### **8. `.streamlit/secrets.toml`**

#### **Purpose**: 
Securely stores secrets like API keys for the application.
#### **Overview**:

- **Structure**:
```toml
nvidia_api_key = "your_actual_api_key_here"
```
- **Usage**:
	- Streamlit automatically loads the secrets from this file.
	- Access the secrets in your code using `st.secrets`, for example:
```python
  nvidia_api_key = st.secrets["api_keys"]["nvidia_api_key"]
```
- **Security Note**:
	- Do **not** commit this file to version control systems like GitHub.
	- Add `.streamlit/secrets.toml` to your `.gitignore` file to prevent accidental commits.

---

## **Troubleshooting**

- **API Key Errors**:
    - Ensure your API key is correctly added to `.streamlit/secrets.toml`.
    - Check that you have the necessary permissions and that the API key is valid.
    - Make sure the key is accessed in `utils.py` using `st.secrets`.
- **Module Not Found Errors**:
    - Verify that all required libraries are installed.
    - Ensure your Python environment is activated if you're using a virtual environment.
- **LLM Response Issues**:
    - Adjust the `max_tokens` parameter in `utils.py` if responses are being cut off.
    - Simplify input messages if you encounter context length limitations.
- **Common Errors with `secrets.toml`**:
    - **File Not Found**: Ensure that the `.streamlit` folder and `secrets.toml` file are correctly named and located in the root directory.
    - **Incorrect Formatting**: Make sure the `secrets.toml` file uses proper TOML syntax.

