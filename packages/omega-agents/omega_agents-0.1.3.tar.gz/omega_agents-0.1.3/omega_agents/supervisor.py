## src/omega_agents/supervisor.py

"""
Supervisor (formerly "manager") - The main ReAct-based agent orchestration logic.
Handles:
- Creating ephemeral agent states
- Running conversations with multiple steps
- Tools usage (Plan/Thought/Action/Action Input/Observation)
- Optional output schema checking (pydantic)
- Verbose/debug modes

Note: The user can customize everything by passing relevant parameters.
"""

import json
from openai import OpenAI
from typing import Dict, List, Optional, Any, Union
from uuid import uuid4

from .config import DEFAULT_MODEL_NAME, DEFAULT_MAX_ITERATIONS
from .memory import AgentMemory
from .tools import ToolSchema
from .schemas import validate_output_with_custom_schema, validate_json_structure

class Supervisor:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model_name: Optional[str] = None,
        verbose: bool = False,
        debug: bool = False
    ):
        """
        :param base_url: LLM endpoint base URL
        :param api_key: API key or token for the LLM
        :param model_name: The model name to use (e.g. "gpt-4o-mini").
                          If None, we use the default from config.
        :param verbose: Whether to print normal logs
        :param debug: Whether to print detailed debug logs
        """
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model_name or DEFAULT_MODEL_NAME
        self.verbose = verbose
        self.debug = debug

        # Dictionary of global tools - user can register more
        self.tools_registry: Dict[str, ToolSchema] = {}

        # Agents ephemeral states
        self.agents: Dict[str, AgentMemory] = {}

    ###########################################################################
    # PUBLIC API
    ###########################################################################

    def register_tool(self, tool: Any):
        """
        Add a tool to the global registry. The tool must have a `.schema` attribute
        that is a ToolSchema, describing the tool's name, parameters, etc.
        """
        if not hasattr(tool, "schema"):
            raise ValueError("Tool must have a .schema attribute of type ToolSchema.")
        schema = tool.schema
        self.tools_registry[schema.name] = schema
        if self.verbose:
            print(f"[Supervisor] Registered tool '{schema.name}'")

    def create_agent(
        self,
        background: str,
        goal: Optional[str] = None,
        system_prompt: Optional[str] = None,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
        output_schema: Optional[Dict[str, Any]] = None,
        additional_instructions: Optional[List[str]] = None  # New option to add instructions
    ) -> str:
        """
        Create a new ephemeral agent. Returns the `agent_id`.
        :param background: The domain knowledge or role for the agent
        :param goal: Optional single-sentence goal or objective
        :param system_prompt: If you want to override the ReAct instructions
        :param max_iterations: Max conversation turns
        :param output_schema: JSON schema for output validation.
        :param additional_instructions: List of additional instructions for the agent.
        """

        if output_schema and not validate_json_structure(output_schema):
            raise ValueError("Provided output_schema is not a valid JSON structure.")
        
        agent_id = str(uuid4())
        memory = AgentMemory(verbose=self.verbose, debug=self.debug)
        memory.add_log("agent_created", {"agent_id": agent_id})

        # Default ReAct instructions if not overridden
        default_system_prompt = f"You are a helpful ReAct agent with the following background:\n{background}"

        # Add goal if it exists
        if goal:
            default_system_prompt += f"\nGoal: {goal}"

        tools_description = self._format_tools()
        if tools_description:
            # When tools are available, include instructions for tool usage
            default_system_prompt += (
                "\n\nYou have access to the following tools:\n"
                f"{self._format_tools()}\n\n"
                "When you need to use a tool, respond in this format:\n"
                "Plan: (brief plan)\n"
                "Thought: (your step-by-step reasoning - not to be revealed in Final Answer)\n"
                "Action: (tool name) // From one of the avaiable tools { " + ", ".join(self.tools_registry.keys()) + " }\n"
                "Action Input: (the valid input to the tool, in a JSON format representing the kwargs)\n"
                "When the tool responds, represent it as:\n"
                "Observation: (the tool result)\n\n"
                "Repeat the Plan, Thought, Action, Action Input and Observation steps as necessary.\n\n"
            )
        else:
            # When no tools are available, focus on Plan, Thought, and Observation
            default_system_prompt += (
                "\n\nWhen providing answers, follow this process:\n"
                "Plan: (brief plan)\n"
                "Thought: (your step-by-step reasoning - not to be revealed in Final Answer)\n"
                "Observation: (evidence or data gathered during reasoning, if applicable)\n"
                "Repeat the Plan, Thought and Observation steps as necessary.\n\n"
            )
        
        # Add output schema details if provided
        if output_schema:
            default_system_prompt += (
                f"Finally, provide a 'Final Answer:' that conforms to the following JSON schema:\n"
                f"```json\n{json.dumps(output_schema, indent=2)}\n```\n\n"
            )
        else:
            default_system_prompt += f"Finally, provide a 'Final Answer:' with your concluding statement.\n\n"
        
        if tools_description:
            default_system_prompt += (
            "\n- When using a tool, stop after Action Input: so the system can call the tool and return the response inside Observation."
        )
        
        default_system_prompt += (
            "\n- Do NOT reveal your chain of thought in the Final Answer."
            "\n- Please ALWAYS start with a Plan and Thought."
        )

        if additional_instructions:
            for instruction in additional_instructions:
                default_system_prompt += f"\n- {instruction}"

        final_system_prompt = system_prompt or default_system_prompt
        memory.add_message("system", final_system_prompt)

        # store ephemeral agent
        self.agents[agent_id] = memory

        # store additional custom config so we know how to handle
        memory.add_log("agent_config", {
            "background": background,
            "goal": goal,
            "max_iterations": max_iterations,
            "output_schema": output_schema,
            "additional_instructions": additional_instructions
        })

        # We store the config in the memory logs
        # We'll just keep the schema in memory logs for usage
        memory.add_log("output_schema", {"enabled": bool(output_schema)})

        # We'll return agent_id so the user can call run_agent with that ID
        return agent_id

    def run_agent(
        self,
        agent_id: str,
        user_input: Union[str, List[Dict[str, str]]],
        max_iterations: Optional[int] = None,
        output_schema: Optional[Dict[str, Any]] = None
    ) -> Union[str, Dict[str, Any]]:
        """
        Run the conversation for the specified agent with the user's input
        (either a single string or a list of messages). Return the final answer
        as a string or a dictionary if `output_schema` is forced and validated.

        :param agent_id: The ephemeral agent to run
        :param user_input: A single user query (string) or a list of messages
                           (dict with keys 'role' and 'content').
        :param max_iterations: Number of conversation turns (if None, use agent config or default).
        :param output_schema: If provided, the LLM's final output is forced to match
                              this pydantic model. Otherwise, unstructured text is returned.
        """
        if agent_id not in self.agents:
            raise ValueError(f"No agent found with id={agent_id}.")

        memory = self.agents[agent_id]
        memory.add_log("run_agent_start", {"agent_id": agent_id})

        # retrieve or fallback to default
        agent_config = self._get_agent_config(memory)
        agent_iterations = max_iterations or agent_config.get("max_iterations") or DEFAULT_MAX_ITERATIONS

        # incorporate user input
        if isinstance(user_input, str):
            memory.add_message("user", user_input)
        else:
            # user_input is a list of messages
            for msg in user_input:
                if "role" in msg and "content" in msg:
                    memory.add_message(msg["role"], msg["content"])

        # ReAct loop
        final_answer = None
        for iteration in range(1, agent_iterations + 1):
            memory.add_log("iteration", {"count": iteration})

            # 1) Call LLM
            llm_response = self._call_llm(memory.conversation)
            memory.add_message("assistant", llm_response)

            # 3) Attempt to parse Action + Action Input
            action_name, action_params = self._extract_action_and_input(llm_response)
            if action_name and action_name in self.tools_registry:
                # Check required params
                tool_schema = self.tools_registry[action_name]
                missing_params = [r for r in tool_schema.required if r not in action_params]
                if missing_params:
                    # error
                    obs_err = f"Observation: Error - missing required parameters {missing_params}"
                    memory.add_message("user", obs_err)
                    memory.add_log("tool_error", {
                        "tool": action_name,
                        "missing": missing_params
                    })
                    continue
                # Execute tool
                try:
                    result = tool_schema.tool.execute(memory.conversation, {}, **action_params)
                    observation_text = f"Observation: {json.dumps(result, indent=2)}"
                    memory.add_message("user", observation_text)
                    memory.add_log("tool_success", {"tool": action_name, "result": result})
                except Exception as e:
                    obs_err = f"Observation: Tool error: {str(e)}"
                    memory.add_message("user", obs_err)
                    memory.add_log("tool_exception", {
                        "tool": action_name,
                        "error": str(e)
                    })
            else:
                # 2) Check for final answer
                maybe_answer = self._extract_final_answer(llm_response)
                if maybe_answer:
                    final_answer = maybe_answer
                    memory.add_log("final_answer_detected", {"answer": final_answer})
                    break

        if not final_answer:
            if output_schema:
                return {
                    "error": "Error<max_iterations>\nNo final answer after max iterations.",
                    "raw_answer": ""
                }
            else:
                final_answer = "Error<max_iterations>\nNo final answer after max iterations."
            memory.add_log("max_iterations_reached", {"final_answer": final_answer})
        
        # optional schema validation
        if output_schema:
            try:
                validated = validate_output_with_custom_schema(final_answer, output_schema)
                if validated:
                    memory.add_log("schema_validation", {"valid": True, "data": validated})
                    return validated
                else:
                    memory.add_log("schema_validation", {"valid": False, "text": final_answer})
                    return {
                        "error": "Output validation failed",
                        "raw_answer": final_answer
                    }
            except Exception as e:
                return {
                    "error": str(e),
                    "raw_answer": final_answer
                }
        
        # Return unstructured text
        self._destroy_agent(agent_id)
        return final_answer

    def get_conversation_log(self, agent_id: str) -> List[Dict[str, str]]:
        """
        Return the conversation messages for debugging. The agent must still exist.
        """
        if agent_id not in self.agents:
            raise ValueError(f"No agent with id={agent_id}")
        return self.agents[agent_id].conversation

    def get_agent_logs(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Return the ephemeral logs for the agent. The agent must still exist.
        """
        if agent_id not in self.agents:
            raise ValueError(f"No agent with id={agent_id}")
        return self.agents[agent_id].logs

    ###########################################################################
    # INTERNAL METHODS
    ###########################################################################

    def _destroy_agent(self, agent_id: str):
        """
        Remove the agent from memory (ephemeral), so no leftover state is stored.
        """
        if agent_id in self.agents:
            del self.agents[agent_id]
            if self.verbose:
                print(f"[Supervisor] Agent {agent_id} destroyed.")

    def _get_agent_config(self, memory: AgentMemory) -> Dict[str, Any]:
        """
        Extract agent config from memory logs (where we stored it).
        """
        for entry in memory.logs:
            if entry["type"] == "agent_config":
                return entry["details"]
        return {}

    def _format_tools(self) -> str:
        """
        Return a text listing of globally registered tools.
        """
        lines = []
        for name, schema in self.tools_registry.items():
            p_str = ""
            for p, pinfo in schema.parameters.items():
                req_flag = "Required" if p in schema.required else "Optional"
                p_str += f"  - {p} ({req_flag}): {pinfo.get('description','')}\n"
            lines.append(f"Tool: {name}\nDescription: {schema.description}\nParameters:\n{p_str}")
        return "\n".join(lines)

    def _call_llm(self, conversation: List[Dict[str, str]]) -> str:
        """
        Make an async request to the LLM endpoint using OpenAI client.
        Return the text of the top choice.
        """
        try:
            client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key
            )
            
            response = client.chat.completions.create(
                model=self.model_name,
                messages=conversation,
                temperature=0.7
            )
            
            if not response.choices:
                raise ValueError("LLM response does not contain 'choices'.")
                
            return response.choices[0].message.content
            
        except Exception as e:
            error_message = f"Error calling LLM: {e}"
            if self.debug:
                print(f"[DEBUG] {error_message}")
            return error_message

    def _extract_final_answer(self, text: str) -> Optional[str]:
        """
        If 'Final Answer:' is present, return the rest of the text. Else None.
        """
        marker = "Final Answer:"
        idx = text.lower().find(marker.lower())
        if idx == -1:
            return None
        return text[idx + len(marker):].strip()

    def _extract_action_and_input(self, text: str) -> (Optional[str], Dict[str, Any]):
        """
        Look for lines like:
           Action: <tool>
           Action Input: {...}
        Return (action_name, action_params).
        """
        lines = text.splitlines()
        action_name = None
        action_input_str = None

        for line in lines:
            if line.strip().lower().startswith("action:"):
                parts = line.split(":", 1)
                if len(parts) == 2:
                    action_name = parts[1].strip()
            elif line.strip().lower().startswith("action input:"):
                parts = line.split(":", 1)
                if len(parts) == 2:
                    action_input_str = parts[1].strip()

        action_params = {}
        if action_input_str:
            try:
                action_params = json.loads(action_input_str)
            except json.JSONDecodeError:
                pass
        return action_name, action_params