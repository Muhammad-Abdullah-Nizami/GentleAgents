import json
from gentleagents.engines.openai_client import interact
from gentleagents.validations.models import TaskResponse, NextTaskResponse
from gentleagents.queries.query import get_team_system, get_team_followup, get_team_summary, get_team_initial_task

class Team:
    def __init__(self, lead_agent, agents):
        """
        Initialize a Team with a lead agent and multiple agents.
        
        Args:
            lead_agent (Agent): The agent responsible for managing tasks.
            agents (list): A list of other Agent instances available for task execution.
        """
        if lead_agent.tools:
            raise ValueError("Lead agent should not have any tools.")
        
        self.lead_agent = lead_agent
        self.agents = {agent.name: agent for agent in agents}
    
    def assign_tasks(self, task_prompt):
        try:
            self.lead_agent.chat_history = [{"role": "user", "content": task_prompt}]
            system_prompt = get_team_system(self.lead_agent.name)
            for agent in self.agents.values():
                system_prompt += f"- {agent.name}: {agent.role}. Tools: {', '.join(agent.tools.keys()) if agent.tools else 'None'}\n"
        
            system_prompt += get_team_initial_task()
            response = interact(system_prompt=system_prompt, user_message=task_prompt, model=self.lead_agent.model)
            if not response:
                return "Error: Could not assign tasks."

            response_text = response.choices[0].message.content.strip()
            if not response_text:
                return "Error: Lead agent returned an empty response. Ensure your prompt forces a JSON output."

            try:
                task_data = json.loads(response_text)
                parsed_response = TaskResponse(**task_data)
            except (json.JSONDecodeError, ValueError) as e:
                return f"Error parsing task response: {e}\nRaw response: {response_text}"

            all_agent_responses = []

            while parsed_response.task:
                assignment = parsed_response.task
                if assignment.agent in self.agents:
                    result = self.agents[assignment.agent].start_agent(assignment.task)
                    all_agent_responses.append(f"{assignment.agent} completed: {result}")
                else:
                    all_agent_responses.append(f"Error: No agent named {assignment.agent}.")

                self.lead_agent.chat_history.append({"role": "assistant", "content": "\n".join(all_agent_responses)})
                followup_prompt = get_team_followup(self.lead_agent.chat_history, self.lead_agent.name)
                followup_response = interact(system_prompt=f"{self.lead_agent.name} checking for further tasks",
                                            user_message=followup_prompt,
                                            model=self.lead_agent.model)
                if not followup_response:
                    break

                followup_text = followup_response.choices[0].message.content.strip()

                try:
                    next_task_data = json.loads(followup_text)
                    next_response = NextTaskResponse(**next_task_data)
                except (json.JSONDecodeError, ValueError) as e:
                    return f"Error parsing followup task response: {e}\nRaw response: {followup_text}"

                if not next_response.continue_ or not next_response.task:
                    break

                parsed_response = TaskResponse(task=next_response.task)

            summary_prompt = get_team_summary(task_prompt, all_agent_responses)


            final_response = interact(system_prompt=f"{self.lead_agent.name} summarizing tasks",
                                    user_message=summary_prompt,
                                    model=self.lead_agent.model)
            return final_response.choices[0].message.content if final_response else "Error in final summary."

        except Exception as e:
            return f"Critical error in task assignment: {e}"

