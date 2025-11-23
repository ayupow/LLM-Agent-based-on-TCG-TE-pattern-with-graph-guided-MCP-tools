# Agent-based-on-graphRAG-and-MCP-for-urban-lifeline-network-recovery


## ⚠️ Important Notice ⚠️
## __As the paper is under review, all contents in this repository are currently not permitted for reuse by anyone until this announcement is removed. Thank you for your understanding! 🙏__


## 1. Overview & Objectives

This repository contains the complete implementation, experimental data, and supplementary results for the paper **"Multi-Agent Recovery of Urban Lifeline Networks via GraphRAG-Enhanced Knowledge Retrieval and Monte-Carlo Planning"** (title placeholder).  

The work proposes a hybrid agent framework that combines:
- GraphRAG for structured retrieval over interdependent infrastructure networks
- Monte-Carlo Planning (MCP) for long-horizon decision making under uncertainty
- Multi-agent collaboration for coordinated recovery scheduling

The framework is evaluated on real-world urban lifeline systems (power, water, transportation, communication) subjected to extreme events.


## 2. Videos of agents operation

### 2.1 Operation of the developed prototype

↓↓↓ A snippet of using the **developed prototype** to run the TS-ReAct-based agents driven by GPT-4o

https://github.com/user-attachments/assets/a79ed28e-a42a-4bc7-8c49-fa07a2e0df50

↓↓↓ A snippet of **updating the tool kit in the prototype**

https://github.com/user-attachments/assets/310db01b-bbd3-462c-945c-60fbf6867e14

The full video to showcase the prototype and tool kit updating can be found in: https://github.com/ayupow/Smart-Agents-for-the-Recovery-of-Interdependent-Infrastructure-Networks/blob/dc852aa1b25333338bf60541742478caf6d58be8/Videos/Operation%20of%20the%20TS-ReAct%20agent%20prototype.mp4

### 2.2 Operation of agents based on ReAct pattern

↓↓↓ A snippet of running the **ReAct-based agents driven by GPT-4o, GPT-4, and GPT-3.5 Turbo**.

https://github.com/user-attachments/assets/9cf85f36-af04-480f-bbde-e37f10f18738

The full video can be found here (https://github.com/ayupow/Smart-Agents-for-the-Recovery-of-Interdependent-Infrastructure-Networks/blob/dc852aa1b25333338bf60541742478caf6d58be8/Videos/Operations%20of%20agents%20based%20on%20ReAct%20pattern/ReAct-based%20agents%20driven%20by%20GPT-4o%2C%20GPT-4%2C%20and%20GPT-3.5%20Turbo.mp4)
 
↓↓↓ A snippet of running the **ReAct-based agents driven by Qwen2.5, Deepseek-V3, Gemma-2, Llama-3.1, and Mixtral MoE**.

https://github.com/user-attachments/assets/3f849a87-8716-4c5d-b26d-61c32f97b54e

The full video can be found here (https://github.com/ayupow/Smart-Agents-for-the-Recovery-of-Interdependent-Infrastructure-Networks/blob/dc852aa1b25333338bf60541742478caf6d58be8/Videos/Operations%20of%20agents%20based%20on%20ReAct%20pattern/ReAct-based%20agents%20driven%20by%20Qwen2.5%2C%20Deepseek-V3%2C%20Gemma-2%2C%20Llama-3.1%2C%20and%20Mixtral%20MoE.mp4)

### 2.3 Operation of agents based on TS-ReAct pattern

↓↓↓ A snippet of running the **TS agent based on TS-ReAct pattern**. 

https://github.com/user-attachments/assets/710dad92-1f76-4e51-84bd-471268bc73bb

The full video can be found here (https://github.com/ayupow/Smart-Agents-for-the-Recovery-of-Interdependent-Infrastructure-Networks/blob/dc852aa1b25333338bf60541742478caf6d58be8/Videos/Operations%20of%20agents%20based%20on%20TS-ReAct%20pattern/TS-ReAct-based-ReAct-agent.mp4)

↓↓↓ A snippet of running the **ReAct agent based on TS-ReAct pattern**. 

https://github.com/user-attachments/assets/2ba0f564-1b8a-412e-92bf-dd5e7bb09ad6

The full video can be found here (https://github.com/ayupow/Smart-Agents-for-the-Recovery-of-Interdependent-Infrastructure-Networks/blob/dc852aa1b25333338bf60541742478caf6d58be8/Videos/Operations%20of%20agents%20based%20on%20TS-ReAct%20pattern/TS-ReAct-based-TS-agent.mp4)


## 3. Repository Structure
├── data/                  # Network datasets and damage scenarios
├── tools/                 # 52 custom recovery tools (graph operations, simulation, etc.)
├── agents_reAct/          # Baseline ReAct agents (8 LLMs)
├── agents_graphRAG_MCP/   # Proposed GraphRAG + MCP agents (main contribution)

├── prototype/             # Interactive prototype with dynamic tool registration

├── experiments/           # Scripts for all reported experiments

├── results/               # Raw and processed results (will be linked)

└── videos/                # Demonstration videos (to be added)


## 4. Acknowledgments

This work heavily relies on excellent open-source projects, including but not limited to:
- LangGraph & LangChain
- 
- Microsoft GraphRAG
- 
- Hugging Face Transformers & leaderboard projects
- 
- NetworkX, PyTorch Geometric, and numerous LLM providers (OpenAI, Anthropic, Qwen, Llama, etc.)

We are deeply grateful to all contributors of these foundational tools.

## 5. How to Reuse This Repository

### 5.1 Importing the Lifeline Recovery Tool Set
1. Copy all tool definition files from `tools/` into your target agent directory.
2. Import the tools using the standardized registry pattern shown in the example notebooks.

### 5.2 Running Baseline ReAct Agents
- Directory: `agents_reAct/`
- Supports 8 different LLMs (GPT-4o, Claude-3, Llama-3.1-405B, Qwen2.5, etc.)
- Ready-to-run scripts with configuration YAMLs

### 5.3 Running the Proposed GraphRAG + MCP Agents
- Directory: `agents_graphRAG_MCP/`
- Same 8 backbone LLMs
- Includes GraphRAG index construction scripts and MCP search configurations

### 5.4 Running the Interactive Prototype
- Directory: `prototype/`
- Dynamic tool registration/hot-reloading
- Web-based GUI + terminal interface
- Supports on-the-fly addition of new recovery actions

## 6. Supplementary Materials


