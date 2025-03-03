from db_models import *
from model_config import model
from pydantic_ai import Agent, Tool,RunContext
import chainlit as cl
from agent_choc import detecte_choc_tool
from agent_souvenir import detecte_souvenir_tool
from agent_preference import detecte_preference_tool


async def desease_exist(maladie_exacte, user_prompt, user_email, mh):
    pp =f"""
    +---------------------------+
    |                           |
    |   ELSE        CONDITION   |
    |      MALADIE EXISTS       |
    |      {maladie_exacte}     |
    |                           |
    +---------------------------+

    """
    print(pp)
    print("maladie exacte : ", maladie_exacte)
    if get_maladie(user_email) or get_choc(user_email) or get_souvenir(user_email) or get_preference(user_email):
        exacte_maladie_prompt = f"""
        Vous etes un agent psychiatre expérimenté.\n,
        vous devez prendre en considération la maladie de l'utilisateur suivante : {maladie_exacte}.\n
        et prendre en consideration les symptomes de cette maladie
        Ta mission est d'accompagner le patient dans son cheminement psychologique. 
        1. Adopte une posture neutre et bienveillante, sans jugement.
        2. Détecte les événements marquants (ex : décès, divorce, licenciement, etc.) **seulement si le patient en parle spontanément**.  
        3. Identifie les souvenirs (ex : enfance, adolescence) **uniquement si le patient y fait référence**.  
        4. Détecte les préférences (ex : cinéma, jeu d’échecs) **si elles sont exprimées**.  
        **N’active un outil que si l'information du patient le justifie.**  
        **Si les informations sont insuffisantes, pose des questions avant de lancer une analyse. **
        """+get_maladie(user_email)+get_choc(user_email)+get_souvenir(user_email)+get_preference(user_email)
    else :
        exacte_maladie_prompt = f"""
        Vous etes un agent psychiatre expérimenté.\n,
        vous devez prendre en considération la maladie de l'utilisateur suivante : {maladie_exacte}.\n
        et prendre en consideration les symptomes de cette maladie
        Ta mission est d'accompagner le patient dans son cheminement psychologique. 
        1. Adopte une posture neutre et bienveillante, sans jugement.
        2. Détecte les événements marquants (ex : décès, divorce, licenciement, etc.) **seulement si le patient en parle spontanément**.  
        3. Identifie les souvenirs (ex : enfance, adolescence) **uniquement si le patient y fait référence**.  
        4. Détecte les préférences (ex : cinéma, jeu d’échecs) **si elles sont exprimées**.  
        **N’active un outil que si l'information du patient le justifie.**  
        **Si les informations sont insuffisantes, pose des questions avant de lancer une analyse. **
        """ 
    psychologue_agent = Agent(
        model,
        system_prompt = exacte_maladie_prompt,
        result_type=str,
        tools=[
            detecte_choc_tool, 
            detecte_preference_tool, 
            detecte_souvenir_tool,
            ],    
    )
    async with psychologue_agent.run_stream(user_prompt, message_history=mh) as response:
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
    save_to_db(user_email, "user", user_prompt)
    save_to_db(user_email, "assistant", Assis_msg.parts[0].content)