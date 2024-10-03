import streamlit as st

from typing import List, Optional, Tuple

from dotenv import load_dotenv

from pathlib import Path

from pydantic import TypeAdapter

from llama_index.core.llms import ChatMessage

from main import Ashley

load_dotenv()

PERSIST_DIR = Path("persist")

chat_message_list = TypeAdapter(List[ChatMessage])


def save_ashley_instance_to_disk (instance: Ashley, messages: List[ChatMessage]) :
    
    if not PERSIST_DIR.exists() :
        PERSIST_DIR.mkdir()
        
    with open(PERSIST_DIR / "messages.json", "w") as f :
        f.write(chat_message_list.dump_json(messages).decode())
        
    return
    
def remove_ashley_instance_from_disk () :
    for f in PERSIST_DIR.glob("*") :
        if f.is_file() :
            f.unlink()
            
    return
    

def get_new_ashley_instance (api_key: str) -> Ashley :
    ashley = Ashley.from_defaults(api_key=api_key)
    
    return ashley

def load_ashley_instance_from_disk (api_key: Optional[str] = None) -> Tuple[Ashley, List[ChatMessage]] :
    ashley = Ashley.from_defaults(api_key=api_key)
    
    with open("persist/messages.json", "r") as fp :
        messages = chat_message_list.validate_json(fp.read())
    
    return ashley, messages

if "messages" not in st.session_state :
    st.session_state["messages"] = []

st.header("🦙 Ashley DEMO 🦙")

settings_tab, chat_tab = st.tabs(["Settings", "Chat"])

with settings_tab :
    cohere_api_key = st.text_input("Cohere API Key", type="password")
    
with chat_tab :
    @st.fragment
    def chat_tab_interface () :
        if "ashley_instance" in st.session_state and st.session_state["ashley_instance"]:
            if st.button("Remove") :
                st.session_state["ashley_instance"] = None
                st.session_state["messages"] = []
                
                st.rerun()
            
            if st.button("Save") :
                with st.spinner("Saving to disk...") :
                    save_ashley_instance_to_disk(
                        instance=st.session_state["ashley_instance"],
                        messages=st.session_state["messages"]
                    )
                
            if st.button("Remove from Disk") :
                with st.spinner("Removing from disk...") :
                    remove_ashley_instance_from_disk()
                
            
            for msg in st.session_state["messages"] :
                with st.chat_message(name=msg.role) :
                    st.write(msg.content)
                    
            if input_message := st.chat_input() :
                msg = ChatMessage(content=input_message)
                st.session_state["messages"].append(msg)
                
                with st.spinner("Generating...") :
                    res = st.session_state["ashley_instance"].chat(msg)
                st.session_state["messages"].append(res)
                
                st.rerun()

        
        
            
        else :
            if st.button("New") :
                with st.spinner("Initializing Ashley...") :
                    st.session_state["ashley_instance"] = get_new_ashley_instance(
                        api_key=cohere_api_key
                    )
                    
                st.rerun()
            
            if st.button("Load") :
                ashley, messages = load_ashley_instance_from_disk(
                    api_key=cohere_api_key
                )
                
                st.session_state["ashley_instance"] = ashley
                st.session_state["messages"] = messages
                
                st.rerun()
            
    chat_tab_interface()
    