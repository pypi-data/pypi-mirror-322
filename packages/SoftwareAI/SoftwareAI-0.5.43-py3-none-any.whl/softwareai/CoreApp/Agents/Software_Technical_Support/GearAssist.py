

#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI All Paths 
from softwareai.CoreApp._init_paths_ import *
#########################################
# IMPORT SoftwareAI Instructions
from softwareai.CoreApp._init_Instructions_ import *
#########################################
# IMPORT SoftwareAI Tools
from softwareai.CoreApp._init_tools_ import *
#########################################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *
#########################################
# IMPORT SoftwareAI _init_environment_
from softwareai.CoreApp._init_environment_ import init_env



class GearAssist:
    def __init__(self
                ):
        pass

    def GearAssist_Technical_Support(self, 
                                    Ticketid,
                                    vectorstore_in_assistant = None,
                                    vectorstore_in_Thread = None,
                                    Upload_1_file_in_thread = None,
                                    Upload_1_file_in_message = None,
                                    Upload_1_image_for_vision_in_thread = None,
                                    Upload_list_for_code_interpreter_in_thread = None
                                    
                                ):
        

       
        instruction_GearAssist = """

        """
        key = "GearAssist_Technical_Support"
        nameassistant = "GearAssist Technical Support"
        model_select = "gpt-4o-mini-2024-07-18"
        key_openai = OpenAIKeysteste.keys()
        client = OpenAIKeysinit._init_client_(key_openai)
        GearAssist_Technical_Support_AI, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appcompany, client, key, instruction_GearAssist, nameassistant, model_select, tools_GearAssist, vectorstore_in_assistant)


        mensaxgem = """
        user_email
        user_Problem
        """  
        adxitional_instructions = ""
        mensaxgemfinal = mensaxgem
        
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensaxgemfinal,
                                                                agent_id=GearAssist_Technical_Support_AI, 
                                                                key=key,
                                                                app1=appcompany,
                                                                client=client,
                                                                tools=tools_GearAssist,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions
                                                                )
                                                
                
        print(response)



