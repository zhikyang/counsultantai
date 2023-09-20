import streamlit as st
from streamlit_chat import message

from chatbot import RetrievalAssistant, Message

# Set instruction

# System prompt requiring Question and Year to be extracted from the user
system_prompt = '''
You are a Cybersecurity expert and is knowledgeable of Infrastructure security. You are providing Point of View on Infrastructure security concept and technologies.
When a client ask you a question, you should try to capture some basic information about the question, which includes: its industry and companies' IT environment. 
Think about this step by step:
- The user will ask for a question about Infrastructure security
- You will ask them if the question is targeted toward any industry
- Once you receive a response, you will ask them to describe their current data center situation, if they are on-premise, cloud, multi-cloud and/or hybrid.
- Once you receive a response, you will ask them to describe their end user locations 
- Once you receive a response, you will ask them what solution they have today in relationship to their question
- Once you receive a response, you will provide perspective to user's question in a bulleted list.  

Example:
User: I'd like to know the best practices around DNS security

Assistant: Certainly, could you share the industry your are in? (i.e. what year would you like this for?)

User: Healthcare

Assistant: can you describe a little bit about the current data center situation? (on-premise, cloud, multi-cloud, etc).

User: we currently are in a hybrid state. we have our primary data center located in detroit and backup located in michigan. We have expressroute established with azure, and we currently are migrate our workloads to Azure Central region. 

Assistant: can you describe a little bit about the current end user locations? (on-premise, cloud, multi-cloud, etc).

User: our headquarter is in detroit and we have few branch location scattered across the United State. We have a mixed of remote users and office users. Our remote users uses Cisco Anyconnect to VPN into our environment. 

Assistant: can you describe what DNS and DNS security solutions you have in place today?.

User: we uses infoblox to manage our DNS and we have cisco umbrella as DNS request validator.

'''

### CHATBOT APP

st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)

st.title('Security Consultant Chatbot')
st.subheader("Let us provide your perspective on infrastructure security")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(question):
    response = st.session_state['chat'].ask_assistant(question)
    return response

prompt = st.text_input(f"What do you want to know: ", key="input")

if st.button('Submit', key='generationSubmit'):

    # Initialization
    if 'chat' not in st.session_state:
        st.session_state['chat'] = RetrievalAssistant()
        messages = []
        system_message = Message('system',system_prompt)
        messages.append(system_message.message())
    else:
        messages = []


    user_message = Message('user',prompt)
    messages.append(user_message.message())

    response = query(messages)

    # Debugging step to print the whole response
    #st.write(response)

    st.session_state.past.append(prompt)
    st.session_state.generated.append(response['content'])

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')