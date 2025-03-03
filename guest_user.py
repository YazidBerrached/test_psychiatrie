
from db_models import *
from model_config import model
from pydantic_ai import Agent, Tool,RunContext
import chainlit as cl
from agent_choc import detecte_choc_tool
from agent_souvenir import detecte_souvenir_tool
from agent_preference import detecte_preference_tool
import pandas as pd
import tools


async def guest_user(user_prompt, user_email, mh): 
    orchestrateur_agent = Agent(
        model,
        system_prompt = (
            "Tu es un expert en psychologie"
            "Ta mission principale est de détecter les tools a utiliser apartir de la discussion avec l'utilisateur "
            "- detecte_preference si une preference est détécté"
            "- detecte_maladie si des symptomes psychiatrique ont été détéctés"
            "- detecte_choc si un choc émotionnel a été détécté"
            "- detecte_souvenir si un souvenir a été détécté"  
            "Si plusieurs tools déja mentionnés sont détectés, retourne-les sous forme d'une liste Python valide. example : ['detecte_preference', 'detecte_maladie']. "
            "Si aucun outil n'est détecté, retourne []. "
            "Ne mets pas de texte supplémentaire, ne mets pas de guillemets autour de la liste."
        ),
        result_type=tools.ToolName,   
    )
    detetcte_tools_list = orchestrateur_agent.run_sync(user_prompt)
    detetcte_tools_list =detetcte_tools_list.data
    
    # detetcte_tools_str= ', '.join(detetcte_tools_list)
    # if detetcte_tools_list:  
    #     list_tool = [globals()[nom] for nom in detetcte_tools_list]
    # else :
    #     list_tool=[]
    result_tools = ""
    if detetcte_tools_list and len(detetcte_tools_list.tools)> 0:
        print(detetcte_tools_list.tools)
        result_tools = {toolin.value: await getattr(tools, toolin.value)(user_prompt, user_email) for toolin in detetcte_tools_list.tools}

    pp = """
    +---------------------------+
    |                           |
    |   ELSE        CONDITION   |
    |      MALADIE EMPTY        |
    |                           |
    +---------------------------+
    
    """
    print(pp)
    system_prompt_master = ""
    print('NAME :  ', user_email)
    
    if get_maladie(user_email) or get_choc(user_email) or get_souvenir(user_email) or get_preference(user_email):
        system_prompt_master = f"""
        Tu es un agent psychiatre.  
        Ta mission est d'accompagner le patient dans son cheminement psychologique.  

        1. Adopte une posture neutre et bienveillante, sans jugement. 
        2. voici quelque information suplementaire {result_tools} 

        **N’active un outil que si l'information du patient le justifie.**  
        **Si les informations sont insuffisantes, pose des questions avant de lancer une analyse. **
        
        """+get_maladie(user_email)+get_choc(user_email)+get_souvenir(user_email)+get_preference(user_email)

    else :
        system_prompt_master = f"""
        Tu es un agent psychiatre.  
        Ta mission est d'accompagner le patient dans son cheminement psychologique.  

        1. Adopte une posture neutre et bienveillante, sans jugement. 
        2. voici quelque information suplementaire {result_tools} 

        **N’active un outil que si l'information du patient le justifie.**  
        **Si les informations sont insuffisantes, pose des questions avant de lancer une analyse. **
        
        """

    master_agent = Agent(
        model,
        system_prompt = system_prompt_master,
        result_type=str, 
    )
    
    print(system_prompt_master)
    async with master_agent.run_stream(user_prompt, message_history=mh) as response:
        msg = cl.Message("", author="AI Agent")
        final_msg_content = ""  # Variable pour stocker le message final

        async for rest in response.stream():
            await msg.stream_token(rest, True)
            final_msg_content += rest  # Stocker chaque token reçu

        
        await msg.update()
        mh = response.all_messages() 
        cl.user_session.set("message_history", mh)
    all_msgs = response.all_messages()
    if all_msgs:
        Assis_msg = all_msgs[-1]
    mh_str = str(mh)

    save_to_db(user_email, "user", user_prompt)
    save_to_db(user_email, "assistant", Assis_msg.parts[0].content)
# save_to_db(user_email, "CONVERSATION", mh_str)


