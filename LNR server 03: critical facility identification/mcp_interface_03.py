import streamlit as st
import subprocess
import os
import threading
import queue
import time
import logging

# Define the path to the script
script_path = r"C:/Users/86131/OneDrive/王泓宇/@mcp/Codes/mcp client_multi_server_global_planning_taobao.py"

# Custom CSS for larger fonts, wider sidebar, and icons
st.markdown("""
    <style>
        /* Increase font size for headers */
        .stTitle {
            font-size: 5rem !important;
        }
        .stHeader {
            font-size: 3rem !important;
        }
        /* Increase font size for text and inputs */
        .stMarkdown, .stText, .stTextArea {
            font-size: 3rem !important;
        }
        /* Significantly larger font size for specific input labels */
        .stSelectbox label, .stSlider label, .stTextInput label {
            font-size: 3.6rem !important;
        }
        /* Style for buttons */
        .stButton > button {
            font-size: 3rem !important;
            padding: 0.5rem 1rem;
        }
        /* Style for code blocks */
        .stCodeBlock {
            font-size: 1.1rem !important;
        }
        /* Icon styling */
        .icon {
            vertical-align: middle;
            margin-right: 8px;
        }
        /* Double the sidebar width */
        [data-testid="stSidebar"] {
            width: 400px !important;
        }
        [data-testid="stSidebar"] .stSidebarContent {
            width: 400px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Set up the layout with a sidebar and main content area
st.set_page_config(layout="wide")

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

# Main content area
st.title("Urban Lifeline Network Recovery (ULNR) Agent")

# Task input box (fake, does not affect code execution)
task_input = st.text_area("Enter Task Description", height=100,
                          help="This input is for display only. The original script will run regardless of the input.")

# Placeholder for real-time output
output_container = st.empty()
error_container = st.empty()

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

                # Display output in real-time using st.code
                st.subheader("📜 Script Output (stdout):")
                with output_container.container():
                    output_area = st.code("", language="text", line_numbers=True)

                st.subheader("⚠️ Script Errors (stderr):")
                with error_container.container():
                    error_area = st.code("", language="text", line_numbers=True)

                # Update output in real-time
                while process.poll() is None or not stdout_queue.empty() or not stderr_queue.empty():
                    try:
                        # Update stdout
                        while True:
                            try:
                                line = stdout_queue.get_nowait()
                                output_text += line
                                output_container.code(output_text, language="text", line_numbers=True)
                            except queue.Empty:
                                break

                        # Update stderr
                        while True:
                            try:
                                line = stderr_queue.get_nowait()
                                error_text += line
                                error_container.code(error_text, language="text", line_numbers=True)
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
                    st.success("✅ Script executed successfully!")
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