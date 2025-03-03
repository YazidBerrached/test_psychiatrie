from db_models import *
from model_config import model
from pydantic_ai import Agent, Tool,RunContext
import chainlit as cl


async def starting_conv(user_prompt,user_email, mh):
        
        last_history = get_last_history(user_email)
        prompt_start_chat = f"""
        Vous etes a psychiatre expérimenté.\n, 
        Voici l'historique de la discussion : \n"{last_history}\n
        À chaque début de conversation, vérifie si l'utilisateur t'a parlé d'un problème ou d'une situation importante lors de la dernière discussion. Si c'est le cas, commence la conversation en demandant des nouvelles sur ce sujet de manière naturelle et bienveillante. Voici un exemple de structure à suivre :

            Si l'utilisateur avait mentionné un problème :
            "Salut [nom de l'utilisateur] ! La dernière fois, tu m'avais parlé de [résumé du problème]. Comment ça s'est passé ? Tu as pu trouver une solution ?"

            Si c'était un projet ou une situation en cours :
            "Hey [nom de l'utilisateur] ! La dernière fois, tu m'avais dit que tu travaillais sur [nom du projet/sujet]. Où en es-tu maintenant ?"

            Si aucune conversation précédente pertinente n'est trouvée :
            "Salut [nom de l'utilisateur] ! Comment vas-tu aujourd’hui ?"

            Adopte un ton amical, empathique et engageant pour encourager l'utilisateur à partager des mises à jour sur ce qu'il t'a confié précédemment."

        """
        first_talk_agent = Agent(
            model,
            system_prompt = prompt_start_chat,
            result_type=str,   
        )
    
        async with first_talk_agent.run_stream(user_prompt, message_history=mh) as response:
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

     # Debug