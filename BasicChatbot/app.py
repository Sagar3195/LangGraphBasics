from typing import List, Dict 
from langgraph.graph import StateGraph, START, END 
from langchain_groq import ChatGroq 
from dotenv import load_dotenv 
import os

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

#Step1 : Define State 
class State(Dict):
  messages: List[Dict[str, str]]

#Step2 : Initialize StateGraph 
graph_builder = StateGraph(State)

#Initalize the LLM 
llm = ChatGroq(model= "gemma2-9b-it", temperature= 0)

#Define chatbot function 
def chatbot(state:State):
  response= llm.invoke(state["messages"])
  state["messages"].append({"role": "assitant", "content": response})
  return {"messages": state["messages"]}


#Add Nodes and Edges 
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


#Compile the graph 
graph= graph_builder.compile()

#Stream updates 
def stream_graph_updates(user_input: str):
  state = {"messages": [{"role": "user", "content": user_input}]}
  for event in graph.stream(state):
    for value in event.values():
      print("Assistant:", value["messages"][-1]["content"])

    
#Run the chatbot in a loop 
if __name__=="__main__":
  while True:
    try:
      user_input = input("User: ")
      if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodabye!!")
        break

      stream_graph_updates(user_input)
    except Exception as e:
      print(f"An error ocurred: {e}")
      break 

