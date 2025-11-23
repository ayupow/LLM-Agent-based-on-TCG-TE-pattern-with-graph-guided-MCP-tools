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



↓↓↓ A snippet of **updating the tool kit in the prototype**



The full video to showcase the prototype and tool kit updating can be found in: 

### 2.2 Operation of agents based on ReAct pattern

↓↓↓ A snippet of running the **ReAct-based agents driven by GPT-4o, GPT-4, and GPT-3.5 Turbo**.



The full video can be found here ()
 
↓↓↓ A snippet of running the **ReAct-based agents driven by Qwen2.5, Deepseek-V3, Gemma-2, Llama-3.1, and Mixtral MoE**.



The full video can be found here ()

### 2.3 Operation of agents based on TS-ReAct pattern

↓↓↓ A snippet of running the **TS agent based on TS-ReAct pattern**. 



The full video can be found here ()

↓↓↓ A snippet of running the **ReAct agent based on TS-ReAct pattern**. 



The full video can be found here ()


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


