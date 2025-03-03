from db_models import *
from model_config import model
from pydantic_ai import Agent, Tool,RunContext
import chainlit as cl
from agent_choc import detecte_choc_tool
from agent_souvenir import detecte_souvenir_tool
from agent_preference import detecte_preference_tool
import pandas as pd
import tools

NBR_DESEASE_TO_CHECK = 20

async def potentiel_desease(user_prompt, user_email, liste_maladie, mh):
    global NBR_DESEASE_TO_CHECK
    pp = """
    +---------------------------+
    |                           |
    |   ELSE        CONDITION   |
    |         DIAGNOSTIC        |
    |                           |
    +---------------------------+
    
    """
    print(pp)
    # if syptome existes dans la liste de maladie
    # else la maladie n'existe pas
    orchestrateur_agent = Agent(
        model,
        system_prompt = (
            "Tu es un expert en psychologie"
            "Ta mission principale est de détecter les tools a utiliser apartir de la discussion avec l'utilisateur "
            "- detecte_preference si une preference est détécté"
            "- detecte_maladie si des symptomes ont été détéctés"
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
    result_tools = ""
    if detetcte_tools_list and len(detetcte_tools_list.tools)> 0:
        print(detetcte_tools_list.tools)
        result_tools = {toolin.value: await getattr(tools, toolin.value)(user_prompt, user_email) for toolin in detetcte_tools_list.tools}


    df = pd.read_json("dataset_psychiatrie4.json")
    df = df[df['maladie'].isin(liste_maladie)]
    df = df.iloc[:, :-2]
    df['score'] = "0"
    liste_maladie_str = ""
    for index, row in df.iterrows():
        liste_maladie_str += "Maladie : "+row['maladie']+", Score : "+row['score'] + ", Descriprion :  "+row['description'] + ", Symptome" + row['symptome'] + "\n"
    
    

    if get_maladie(user_email) or get_choc(user_email) or get_souvenir(user_email) or get_preference(user_email):
        prompt_maladie_potentiel = f"""
        Vous êtes un agent psychiatre expérimenté spécialisé dans l'analyse des maladies psychiatriques.  
        Votre mission est d'identifier la maladie exacte de l'utilisateur en fonction des symptômes qu'il décrit, en vous basant sur la liste de maladies potentielles suivantes : {liste_maladie_str}.  

        ### Instructions :  
        - **Adoptez une posture neutre et bienveillante**, sans jugement.  
        - **Dirigez la conversation** de manière stratégique pour obtenir des informations précises sur les symptômes du patient.  
        - **Comparez les symptômes** décrits par l'utilisateur avec ceux des maladies listées.  
        - **Attribuez un score à chaque maladie** en fonction de la correspondance des symptômes :  
        - Augmentez le score des maladies correspondant aux symptômes rapportés.  
        - Plus un symptôme est spécifique à une maladie, plus l'augmentation du score doit être significative.  
        - Si un symptôme est partagé entre plusieurs maladies, répartissez le score de manière proportionnelle.  

        ### Méthodologie :  
        1. **Posez des questions ciblées et courtes** pour clarifier les symptômes et leur intensité.  
        2. **Mettez à jour les scores en fonction des réponses** afin d'affiner progressivement le diagnostic.  
        3. **Ne révélez jamais directement le nom de la maladie au patient** durant le processus.  
        4. **Lorsque vous avez identifié la maladie avec le score le plus élevé, retournez son nom entre deux parenthèses**.  

        **Exemple de réponse finale :**  
        Si la maladie détectée est la schizophrénie, vous devez simplement répondre :  
        ((schizophrénie))  
        Sans aucun texte supplémentaire.  
        """+get_maladie(user_email)+get_choc(user_email)+get_souvenir(user_email)+get_preference(user_email)
    else:
        prompt_maladie_potentiel = f"""
        Vous êtes un agent psychiatre expérimenté spécialisé dans l'analyse des maladies psychiatriques.  
        Votre mission est d'identifier la maladie exacte de l'utilisateur en fonction des symptômes qu'il décrit, en vous basant sur la liste de maladies potentielles suivantes : {liste_maladie_str}.  

        ### Instructions :  
        - **Adoptez une posture neutre et bienveillante**, sans jugement.  
        - **Dirigez la conversation** de manière stratégique pour obtenir des informations précises sur les symptômes du patient.  
        - **Comparez les symptômes** décrits par l'utilisateur avec ceux des maladies listées.  
        - **Attribuez un score à chaque maladie** en fonction de la correspondance des symptômes :  
        - Augmentez le score des maladies correspondant aux symptômes rapportés.  
        - Plus un symptôme est spécifique à une maladie, plus l'augmentation du score doit être significative.  
        - Si un symptôme est partagé entre plusieurs maladies, répartissez le score de manière proportionnelle.  

        ### Méthodologie :  
        1. **Posez des questions ciblées et courtes** pour clarifier les symptômes et leur intensité.  
        2. **Mettez à jour les scores en fonction des réponses** afin d'affiner progressivement le diagnostic.  
        3. **Ne révélez jamais directement le nom de la maladie au patient** durant le processus.  
        4. **Lorsque vous avez identifié la maladie avec le score le plus élevé, retournez son nom entre deux parenthèses**.  

        **Exemple de réponse finale :**  
        Si la maladie détectée est la schizophrénie, vous devez simplement répondre :  
        ((schizophrénie))  
        Sans aucun texte supplémentaire.  
        """
        
    


    print(prompt_maladie_potentiel)
    psychiatre_agent = Agent(
        model,
        system_prompt = prompt_maladie_potentiel,
        result_type=str,
        tools=[
            # detecte_desease_tool, 
            # detecte_choc_tool, 
            # detecte_preference_tool, 
            # detecte_souvenir_tool,
            ],    
    )
    async with psychiatre_agent.run_stream(user_prompt, message_history=mh) as response:
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
    if get_count_potential_desease(user_email) > NBR_DESEASE_TO_CHECK:
        exact_desease = get_top_desease(user_email)
        if exact_desease!='not yet':
            save_maladie_db(user_email,exact_desease)
    
