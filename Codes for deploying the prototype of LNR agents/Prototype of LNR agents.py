import streamlit as st
import subprocess
import os
import threading
import queue
import time
import logging
import json
import re

# Define the path to the script
script_path = r"C:/Users/86131/OneDrive/王泓宇/@mcp/Codes/mcp client_multi_server_global_planning_taobao.py"
script_dir = os.path.dirname(script_path)

# Custom CSS for larger fonts, wider sidebar, icons, and uniform button sizes
st.markdown("""
    <style>
        /* Set a global font size to ensure all text is larger */
        .stApp, .stApp * {
            font-size: 1.2rem !important; /* Base font size for all elements */
        }
        /* Increase font size for headers */
        .stTitle {
            font-size: 8.0rem !important; /* Increased for larger title */
        }
        .stHeader {
            font-size: 2.2rem !important;
        }
        /* Increase font size for specific input labels */
        .stSelectbox label, .stSlider label, .stTextInput label, .stFileUploader label {
            font-size: 4.0rem !important;
        }
        /* Ensure help text and secondary text are larger */
        .stMarkdown, .stText, .stTextArea, .stForm, .stButton > button, .stAlert, .stSpinner {
            font-size: 1.6rem !important;
        }
        /* Style for code blocks */
        .stCodeBlock {
            font-size: 1.4rem !important;
        }
        /* Icon styling */
        .icon {
            vertical-align: middle;
            margin-right: 8px;
        }
        /* Sidebar width */
        [data-testid="stSidebar"] {
            width: 400px !important;
        }
        [data-testid="stSidebar"] .stSidebarContent {
            width: 400px !important;
        }
        /* Uniform button styling for tool and server buttons, aligned with sidebar components */
        .stButton > button {
            width: 380px !important; /* Match sidebar content width minus padding */
            height: 50px !important; /* Fixed height for consistency */
            font-size: 1.6rem !important; /* Consistent font size */
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto !important; /* Center buttons */
            padding: 0 !important; /* Remove default padding */
            box-sizing: border-box !important; /* Include padding/borders in width */
        }
    </style>
""", unsafe_allow_html=True)

# Set up the layout with a sidebar and main content area
st.set_page_config(layout="wide")

# Function to get existing server names from the script
def get_server_names():
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()
        pattern = r"MultiServerMCPClient\(\s*(\{.*?\}\s*)\)"
        match = re.search(pattern, script_content, re.DOTALL)
        if not match:
            return []
        dict_str = match.group(1)
        server_dict = json.loads(dict_str.replace("'", '"'))
        return list(server_dict.keys())
    except Exception as e:
        st.error(f"❌ Error reading server names: {str(e)}")
        return []

# Function to append new server or tool to the script
def append_to_script(config, config_type="server", server_name=None, uploaded_file=None):
    try:
        # Read the script content
        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()

        # Find the MultiServerMCPClient dictionary using regex
        pattern = r"MultiServerMCPClient\(\s*(\{.*?\}\s*)\)"
        match = re.search(pattern, script_content, re.DOTALL)
        if not match:
            st.error("❌ Could not find MultiServerMCPClient dictionary in the script.")
            return False

        dict_str = match.group(1)
        dict_start, dict_end = match.start(1), match.end(1)

        # Detect the indentation level
        lines = script_content[:dict_start].splitlines()
        indent_line = next((line for line in lines[::-1] if line.strip()), "")
        indent = len(indent_line) - len(indent_line.lstrip())
        indent_str = " " * indent

        # Parse the dictionary manually by finding the last entry
        last_entry_end = dict_str.rfind("}")
        if last_entry_end == -1:
            st.error("❌ Invalid dictionary structure in MultiServerMCPClient.")
            return False

        # Extract the existing dictionary content (without the closing brace)
        existing_content = dict_str[:last_entry_end].rstrip()
        if existing_content.endswith(","):
            existing_content = existing_content[:-1]  # Remove trailing comma if present

        if config_type == "server":
            # Server configuration
            if isinstance(config, dict) and "name" in config:
                # Quick-create form case
                server_name = config["name"]
                server_data = {
                    "command": config["command"],
                    "transport": config["transport"],
                    "args": config["args"]
                }
            elif isinstance(config, dict) and len(config) == 1:
                # JSON upload case
                server_name = list(config.keys())[0]
                server_data = config[server_name]
                if not all(key in server_data for key in ["command", "transport", "args"]):
                    st.error("❌ Server configuration must include 'command', 'transport', and 'args'.")
                    return False
            else:
                st.error("❌ Invalid server configuration format.")
                return False

            # Validate server data
            if server_data["transport"] not in ["stdio", "tcp", "http"]:
                st.error("❌ Transport must be one of: stdio, tcp, http.")
                return False
            if not isinstance(server_data["args"], list):
                st.error("❌ Args must be a list.")
                return False

            # Format the new server entry with proper indentation
            new_entry = f',\n{indent_str}    "{server_name}": {{\n{indent_str}        "command": "{server_data["command"]}",\n{indent_str}        "transport": "{server_data["transport"]}",\n{indent_str}        "args": {json.dumps(server_data["args"])}\n{indent_str}    }}'

        elif config_type == "tool":
            # Tool configuration
            tool_name = config["name"]
            tool_data = {
                "function": config["function"],
                "description": config["description"]
            }

            # Validate tool name
            if " " in tool_name or len(tool_name) > 64:
                st.error("❌ Tool name must have no whitespace and be 64 characters or less.")
                return False
            if not tool_name.replace("-", "_").isidentifier():
                st.error("❌ Tool name must be a valid identifier (alphanumeric, hyphens, or underscores).")
                return False

            # Read the existing server dictionary
            server_dict = json.loads(dict_str.replace("'", '"'))
            if server_name not in server_dict:
                st.error(f"❌ Server '{server_name}' not found in the script.")
                return False

            # Add or update tools dictionary in the selected server
            if "tools" not in server_dict[server_name]:
                server_dict[server_name]["tools"] = {}
            server_dict[server_name]["tools"][tool_name] = tool_data

            # Convert back to string with proper indentation
            new_entry = f",\n{indent_str}    \"{server_name}\": {json.dumps(server_dict[server_name], indent=4, ensure_ascii=False).replace('/n', f'/n{indent_str}    ')}"
            # Find the position of the server in the existing content
            server_pattern = rf'"{server_name}":\s*{{[^}}]*}}'
            match = re.search(server_pattern, existing_content, re.DOTALL)
            if not match:
                st.error(f"❌ Could not find server '{server_name}' in the dictionary.")
                return False
            existing_content = existing_content[:match.start()] + existing_content[match.end():].lstrip(",")
            if existing_content.endswith(","):
                existing_content = existing_content[:-1]

        # Combine the updated dictionary
        updated_dict_str = f"{existing_content}{new_entry}\n{indent_str}}}"

        # Replace the old dictionary with the new one
        updated_script = script_content[:dict_start] + updated_dict_str + script_content[dict_end:]

        # Save the updated script
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(updated_script)

        # If a .py file was uploaded, save it to the script directory
        if uploaded_file:
            file_path = os.path.join(script_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ Uploaded .py file saved to: {file_path}")

        return True

    except Exception as e:
        st.error(f"❌ Error updating script: {str(e)}")
        return False

# Sidebar for parameter settings
with st.sidebar:
    st.header("🔧 Parameter Settings")

    # LLM selection
    llm_options = ["claude-sonnet-4-20250514", "claude-3-7-sonnet-20250219", "DeepSeek-V3-0324",
                   "gpt-5-2025-08-07", "gpt-4.1-2025-04-14", "gpt-4o-2024-08-06",
                   "qwen3-235b-a22b-instruct-2507", "qwen-max-2025-01-25"]
    selected_llm = st.selectbox("Select LLM to empower ULNR agent", llm_options)

    # Model temperature
    temperature = st.slider("Set Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.1)

    # Tool graph JSON path
    tool_graph_path = st.text_input("Update Tool Graph of ULNR", value="tool_graph.json")

    # Add spacing before the new buttons
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Button for integrating a new tool
    if st.button("🛠️ Integrate a New Tool to Existing Servers"):
        st.session_state.page = "integrate_tool"

    # Button for MCP server integration
    if st.button("🌐 Integrate a New MCP Server"):
        st.session_state.page = "integrate_server"
    else:
        # Ensure the default page is shown unless a button is clicked
        if "page" not in st.session_state:
            st.session_state.page = "main"

# Main content area
if st.session_state.get("page") == "integrate_tool":
    st.title("🛠️ Integrate a New Tool to Existing Servers")

    # Back to main page button
    if st.button("⬅️ Back to Main"):
        st.session_state.page = "main"

    st.subheader("Tool Integration Form")
    with st.form(key="tool_form"):
        # Select existing server
        server_names = get_server_names()
        if not server_names:
            st.error("❌ No servers found in the script. Please integrate a server first.")
        else:
            selected_server = st.selectbox("Select Server", server_names)
            tool_name = st.text_input("Tool Name", value="new_tool")
            uploaded_file = st.file_uploader("Upload Tool Function (.py)", type=["py"])
            tool_description = st.text_area(
                "Tool Description (AIOE Format)",
                value='{\n    "aim": "",\n    "input_output": "",\n    "expectation": ""\n}',
                height=150,
                help="Enter the tool description in AIOE format: {'Aim of the tool': '', 'Input specification': ' ', 'Output specification': '', 'Expectation after execution': ''}"
            )

            submit_button = st.form_submit_button("✅ Confirm Tool Integration")

            if submit_button:
                if not tool_name or not uploaded_file or not tool_description:
                    st.error("❌ All fields (Tool Name, Tool Function File, and Tool Description) are required.")
                elif " " in tool_name or len(tool_name) > 64:
                    st.error("❌ Tool name must have no whitespace and be 64 characters or less.")
                elif not tool_name.replace("-", "_").isidentifier():
                    st.error("❌ Tool name must be a valid identifier (alphanumeric, hyphens, or underscores).")
                else:
                    try:
                        # Validate JSON format of tool description
                        description_data = json.loads(tool_description)
                        if not all(key in description_data for key in ["aim", "input_output", "expectation"]):
                            st.error("❌ Tool description must include 'aim', 'input_output', and 'expectation' in JSON format.")
                        else:
                            tool_config = {
                                "name": tool_name,
                                "function": uploaded_file.name,
                                "description": description_data
                            }
                            if append_to_script(tool_config, config_type="tool", server_name=selected_server, uploaded_file=uploaded_file):
                                st.success(f"✅ Tool '{tool_name}' added to server '{selected_server}' successfully!")
                    except json.JSONDecodeError:
                        st.error("❌ Invalid JSON format in tool description.")

elif st.session_state.get("page") == "integrate_server":
    st.title("🌐 Integrate a New MCP Server")

    # Back to main page button
    if st.button("⬅️ Back to Main"):
        st.session_state.page = "main"

    st.subheader("Option 1: Upload JSON Configuration")
    json_file = st.file_uploader("Upload JSON file", type=["json"])
    st.markdown("**Example JSON Format:**")
    st.code("""
{
    "server_name": {
        "command": "",
        "transport": "",
        "args": [""]
    }
}
    """, language="json")
    if json_file:
        try:
            json_data = json.load(json_file)
            if not isinstance(json_data, dict) or len(json_data) != 1:
                st.error("❌ JSON must contain exactly one server configuration.")
            else:
                server_name = list(json_data.keys())[0]
                server_config = json_data[server_name]
                if not all(key in server_config for key in ["command", "transport", "args"]) or not isinstance(server_config["args"], list):
                    st.error("❌ JSON must have 'command', 'transport', and 'args' (as a list).")
                elif server_config["transport"] not in ["stdio", "tcp", "http"]:
                    st.error("❌ Transport must be one of: stdio, tcp, http.")
                else:
                    if st.button("✅ Confirm JSON Upload"):
                        if append_to_script(json_data, config_type="server"):
                            st.success(f"✅ Server '{server_name}' added to the script successfully!")
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON file.")

    st.subheader("Option 2: Quick Create")
    with st.form(key="server_form"):
        server_name = st.text_input("Server Name", value="new_mcp_server")
        transport_type = st.selectbox("Transport Type", options=["stdio", "tcp", "http"])
        command = st.text_input("Command", value="python")
        uploaded_file = st.file_uploader("Upload .py File for Args", type=["py"])

        submit_button = st.form_submit_button("Create Server")

        if submit_button:
            if not server_name or not command or not uploaded_file:
                st.error("❌ All fields (Server Name, Command, and .py File) are required.")
            elif not server_name.isidentifier():
                st.error("❌ Server Name must be a valid identifier (alphanumeric, no spaces, no special characters).")
            else:
                server_config = {
                    "name": server_name,
                    "command": command,
                    "transport": transport_type,
                    "args": [uploaded_file.name]
                }
                if append_to_script(server_config, config_type="server", uploaded_file=uploaded_file):
                    st.success(f"✅ Server '{server_name}' added to the script successfully!")

else:
    st.title("Urban Lifeline Network Recovery (ULNR) Agent")

    # Task input box (fake, does not affect code execution)
    task_input = st.text_area("Enter Task Description", height=100,
                              help="This input is for display only. The original script will run regardless of the input.")

    # Placeholder for real-time output
    output_container = st.empty()
    error_container = st.empty()

    # Custom CSS for resizable and scrollable text areas
    st.markdown("""
        <style>
            /* Style for resizable text areas */
            .resizable-textarea textarea {
                resize: vertical !important; /* Allow vertical resizing only */
                min-height: 100px !important;
                max-height: 600px !important;
                overflow-y: auto !important; /* Enable vertical scrolling */
                width: 100% !important;
                font-family: monospace !important; /* Mimic code font */
                font-size: 1.4rem !important;
                background-color: #f8f8f8 !important;
                border: 1px solid #ccc !important;
                padding: 10px !important;
            }
            /* Ensure the resize handle is visible */
            .resizable-textarea textarea::-webkit-resizer {
                background-color: #ccc;
                border-radius: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Verify if the script exists
    if not os.path.exists(script_path):
        st.error(f"❌ Script not found at: {script_path}")
        st.write("Please check the file path and ensure the script exists.")
    else:
        st.write("Click the button below to run the MCP client script.")
        if st.button("🚀 Run"):
            with st.spinner("⏳ Running the script... This may take some time."):
                try:
                    # Set PYTHONUNBUFFERED to disable output buffering
                    env = os.environ.copy()
                    env["PYTHONUNBUFFERED"] = "1"

                    # Redirect logging to stdout
                    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
                    env["PYTHONWARNINGS"] = "ignore"  # Suppress warnings if needed

                    # Initialize queues for stdout and stderr
                    stdout_queue = queue.Queue()
                    stderr_queue = queue.Queue()

                    # Function to read stream and put into queue
                    def read_stream(stream, q):
                        for line in iter(stream.readline, ''):
                            q.put(line)
                        stream.close()

                    # Start the subprocess
                    process = subprocess.Popen(
                        ["python", script_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        bufsize=1,  # Line buffered
                        universal_newlines=True,
                        env=env
                    )

                    # Start threads to read stdout and stderr
                    stdout_thread = threading.Thread(target=read_stream, args=(process.stdout, stdout_queue))
                    stderr_thread = threading.Thread(target=read_stream, args=(process.stderr, stderr_queue))
                    stdout_thread.start()
                    stderr_thread.start()

                    # Initialize output buffers
                    output_text = ""
                    error_text = ""

                    # Display output in real-time using st.text_area
                    st.subheader("📜 Script Output (stdout):")
                    with output_container.container():
                        output_area = st.text_area(
                            "Script Output",
                            value="",
                            height=200,  # Initial height
                            key="output_area",
                            disabled=True,  # Read-only
                            help="This is the stdout output of the script. Scroll to view more, and drag the bottom-right corner to resize.",
                            placeholder="Waiting for script output..."
                        )

                    st.subheader("⚠️ Script Errors (stderr):")
                    with error_container.container():
                        error_area = st.text_area(
                            "Script Errors",
                            value="",
                            height=200,  # Initial height
                            key="error_area",
                            disabled=True,  # Read-only
                            help="This is the stderr output of the script. Scroll to view more, and drag the bottom-right corner to resize.",
                            placeholder="Waiting for script errors..."
                        )

                    # Counter for line numbers
                    stdout_line_count = 0
                    stderr_line_count = 0

                    # Update output in real-time
                    while process.poll() is None or not stdout_queue.empty() or not stderr_queue.empty():
                        try:
                            # Update stdout
                            while True:
                                try:
                                    line = stdout_queue.get_nowait()
                                    stdout_line_count += 1
                                    # Prepend line number
                                    output_text += f"{stdout_line_count:4d} | {line}"
                                    output_container.text_area(
                                        "Script Output",
                                        value=output_text,
                                        height=200,
                                        key=f"output_area_{stdout_line_count}",
                                        disabled=True,
                                        help="This is the stdout output of the script. Scroll to view more, and drag the bottom-right corner to resize.",
                                        placeholder="Waiting for script output..."
                                    )
                                except queue.Empty:
                                    break

                            # Update stderr
                            while True:
                                try:
                                    line = stderr_queue.get_nowait()
                                    stderr_line_count += 1
                                    # Prepend line number
                                    error_text += f"{stderr_line_count:4d} | {line}"
                                    error_container.text_area(
                                        "Script Errors",
                                        value=error_text,
                                        height=200,
                                        key=f"error_area_{stderr_line_count}",
                                        disabled=True,
                                        help="This is the stderr output of the script. Scroll to view more, and drag the bottom-right corner to resize.",
                                        placeholder="Waiting for script errors..."
                                    )
                                except queue.Empty:
                                    break

                            # Small delay to prevent excessive CPU usage
                            time.sleep(0.1)
                        except Exception as e:
                            st.error(f"❌ Error reading output: {str(e)}")
                            break

                    # Wait for threads to finish
                    stdout_thread.join()
                    stderr_thread.join()

                    # Check final process status
                    return_code = process.wait(timeout=3600)  # 1-hour timeout
                    if return_code == 0:
                        st.success("✅ Agent executed successfully!")
                        # Display output length for debugging
                        st.info(f"📏 Captured stdout length: {len(output_text)} characters")
                        st.info(f"📏 Captured stderr length: {len(error_text)} characters")
                    else:
                        st.error(f"❌ Script failed with return code: {return_code}")

                    # Save output to a file for debugging
                    with open("script_output.log", "w", encoding="utf-8") as f:
                        f.write("=== stdout ===\n")
                        f.write(output_text)
                        f.write("\n=== stderr ===\n")
                        f.write(error_text)

                except subprocess.TimeoutExpired:
                    process.terminate()
                    st.error("⏰ Script execution timed out after 1 hour.")
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")

