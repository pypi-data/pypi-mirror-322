

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
# IMPORT SoftwareAI Functions
from softwareai.CoreApp._init_functions_ import *
#########################################
# IMPORT SoftwareAI Functions Submit Outputs
from softwareai.CoreApp._init_submit_outputs_ import _init_output_

from huggingface_hub import InferenceClient
from huggingface_hub import login
from telegram import Bot

# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *
#########################################

class Alfred:
    """softwareai/Docs/Agents/Alfred.md"""
    def __init__(self,

            ):
        pass

    class MemeinApplicationContext:
        def __init__(self,
                    appfb,
                    client,
                    nameApp,
                    descriptionApp,
                    watermark,
                    Debug=True,
                    lang="pt"


                ):
            self.Debug = Debug
            self.lang = lang
            self.appfb = appfb
            self.client = client
            self.user_threads = {}
            self.key = "AI_MemeinApplicationContext"
            self.nameassistant = "MemeinApplicationContext"
            self.model_select = "gpt-4o-mini-2024-07-18"
            self.nameApp = nameApp
            self.watermark = watermark 
            self.Upload_1_file_in_thread = None
            self.Upload_1_file_in_message = None
            self.Upload_1_image_for_vision_in_thread = None
            self.codeinterpreter = None
            self.vectorstore = None
            self.vectorstore_in_agent = None
            self.instruction = """
            com base no mini dataset de prompt atual crie outro prompt para memes diarios para  os canais de comunicacao do aplicativo adicione uma marca da agua {self.watermark} 
            responda semprem em ingles
            """
            self.descriptionApp = descriptionApp 
            hugfacetoken = hugKeys.hug_1_keys()
            login(hugfacetoken)
            self.InferenceClientMeme  = InferenceClient("prithivMLmods/Flux-Meme-Xd-LoRA", token=hugfacetoken)

        def main(self):


            # Autenticação do assistente de IA
            AI, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(
                self.appfb,
                self.client,
                self.key,
                self.instruction,
                self.nameassistant,
                self.model_select,
                response_format="json_object"
            )

            if self.Debug:
                if self.lang == "pt":
                    cprint(f"🔐 Autenticação concluída. Assistente: {nameassistant}, Modelo: {model_select}", 'cyan')
                else:
                    cprint(f"🔐 Authentication completed. Assistant: {nameassistant}, Model: {model_select}", 'cyan')

            prompt = f"""
            com base no mini dataset de prompt atual crie outro prompt para memes diarios para  os canais de comunicacao do aplicativo adicione uma marca da agua {self.watermark} 
            responda semprem em ingles

            aplicativo:
            {self.descriptionApp}

            

            mini dataset:

            meme, A cartoon drawing of a brown cat and a white sheep. The sheep is facing each other and the cat is facing towards the left side of the image. The brown cat has a black nose and a black mouth. The white sheep has a white body and black legs. The background is a light peach color. There is a text bubble above the brown cat that says "If you feel sad I can eat you".

            meme, A medium-sized painting of a white T-rex in the middle of a dark, stormy night. The t-rex is facing towards the left side of the frame, its head turned towards the right. Its mouth is open, revealing its sharp teeth. A rooster is standing in the foreground of the painting, with a red cap on its head. The roosters head is turned to the right, and the word "Remember who you are" is written in white text above it. The background is a deep blue, with dark gray clouds and a crescent moon in the upper left corner of the image. There are mountains in the background, and a few other animals can be seen in the lower right corner.


            meme, A cartoon drawing of two zebras facing each other. The zebra on the left is facing the right. The horse on the right is facing to the left. The zebrab is facing towards the right and has a black mane on its head. The mane is black and white. The sky is light blue and there are birds flying in the sky. There is a text bubble above the zebras head that says "UPGRADE MAN!"

            meme, A cartoon-style illustration showing a hooded hacker sitting in front of a computer with the message "VPN expired" flashing on the screen. In the corner of the image, a stylized safe with the NordVPN logo is being closed automatically. The hacker has a frustrated expression with a speech bubble saying, "No chance today!" At the bottom, the text: "Nord Auto Rotate – Changing servers, keeping you safe."
                        
            """

            if self.Debug:
                if self.lang == "pt":
                    cprint(f"📝 Prompt criado : {prompt}", 'cyan')
                else:
                    cprint(f"📝 Prompt created : {prompt}", 'cyan')

            # Instrução adicional para resposta em JSON
            self.adxitional_instructions = 'Responda no formato JSON Exemplo: {"newprompt": "..."}'

            # Chamada para gerar a resposta do assistente
            response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                mensagem=prompt,
                agent_id=AI,
                key=self.key,
                app1=self.appfb,
                client=self.client,
                model_select=model_select,
                aditional_instructions=self.adxitional_instructions
            )

            if self.Debug:
                if self.lang == "pt":
                    cprint(f"📨 Resposta recebida do assistente: {response}", 'cyan')
                else:
                    cprint(f"📨 Response received from assistant: {response}", 'cyan')

            try:
                response_dictload = json.loads(response)
                response_dict = response_dictload['newprompt']

                if self.Debug:
                    if self.lang == "pt":
                        cprint("✅ Resposta convertida para dicionário JSON.", 'green')
                    else:
                        cprint("✅ Response converted to JSON dictionary.", 'green')
            except Exception as e:
                response_dict = response
                if self.Debug:
                    if self.lang == "pt":
                        cprint(f"⚠️ Falha ao converter resposta para JSON: {str(e)}", 'red')
                    else:
                        cprint(f"⚠️ Failed to convert response to JSON: {str(e)}", 'red')

            full_hash = hashlib.sha256(response_dict.encode('utf-8')).hexdigest()
            MemeHash = full_hash[:13]

            tentativas = 15
            espera = 60
            for tentativa in range(tentativas):
                try:
                    if self.lang == "pt":
                        cprint(" Gerando Meme", 'green')
                    else:
                        cprint(" Generating meme.", 'green')
                    image = self.InferenceClientMeme.text_to_image(response_dict)
                    os.makedirs(os.path.join(os.path.dirname(__file__), f"Meme_{self.nameApp}"), exist_ok=True)
                    image_path = os.path.join(os.path.dirname(__file__), f"Meme_{self.nameApp}", f"{MemeHash}.png")
                    image.save(image_path)
                    return image_path
                except Exception as e:
                    print(f"Erro na tentativa {tentativa + 1}: {e}")
                    if tentativa < tentativas - 1:
                        print(f"Tentando novamente em {espera} segundos...")
                        time.sleep(espera)
                    else:
                        print("Falha após múltiplas tentativas. Tente mais tarde.")



    class NordVPN_Auto_Rotate:
        def __init__(self,
                    appfb,
                    client,
                    TOKEN,
                    CHANNEL_ID
                ):
            self.appfb = appfb
            self.client = client
            self.TOKEN = TOKEN
            self.agent = Bot(token=self.TOKEN)
            self.CHANNEL_ID = CHANNEL_ID
            self.user_threads = {}
            self.key = "AI_Alfred"
            self.nameassistantAlfred = "Alfred"
            self.model_selectAlfred = "gpt-4o-mini-2024-07-18"
            self.Upload_1_file_in_thread = None
            self.Upload_1_file_in_message = None
            self.Upload_1_image_for_vision_in_thread = None
            self.codeinterpreter = None
            self.vectorstore = None
            self.vectorstore_in_agent = None
            self.instruction = """

    ## Objetivo
    Oferecer suporte completo aos usuários do **NordVPN Auto Rotate**, garantindo a resolução rápida de problemas, registro organizado de tickets, e coleta de feedback para melhoria contínua.

    ---

    ## Diretrizes de Atendimento

    ### 1. **Boas-vindas e Agradecimento**
    - Agradeça ao cliente por escolher o NordVPN Auto Rotate.
    - Envie a seguinte mensagem padrão de boas-vindas:

    **Mensagem de Boas-vindas:**
    "Obrigado por escolher o **NordVPN Auto Rotate**. Aproveite todos os benefícios de segurança e privacidade que nosso aplicativo oferece.

    📥 **Download do Aplicativo:** [Clique aqui para baixar](https://www.mediafire.com/file/e8803j54knyj23p/Nord_Auto_Rotate.rar/file)

    📺 **Tutorial no YouTube:** [Assista ao vídeo](https://www.youtube.com/watch?v=E4fbZUVMMEI)

    📞 **Suporte via Telegram:** [Acesse o grupo de suporte](https://t.me/+dpGofyMuGUszY2Rh)"

    ---

    2. Solução de Problemas
      Para garantir uma resolução eficiente, todos os problemas relatados devem ser registrados imediatamente como um Ticket de Suporte no sistema. Isso permite que nossa equipe analise e resolva a questão de forma rápida e organizada.

      Procedimento para Solução de Problemas:
      Identifique o Problema Reportado:

      Solicite ao cliente uma descrição clara do erro e informações adicionais, como sistema operacional e o serial utilizado, se aplicável.
      Criação de Ticket:

      Use a função OpenSupportTicketProblem para registrar o problema no banco de dados.
      Parâmetros necessários:
      user_email: Email do cliente.
      issue_description: Descrição detalhada do problema.
      Mensagem ao Cliente Após Registro:

      "(emote) Seu problema foi registrado com sucesso e já está sendo analisado pela nossa equipe. Seu Ticket ID é: {ticket_id}. Retornaremos com uma solução o mais breve possível."
      Encaminhamento Interno:

      Nossa equipe de suporte analisará o ticket e trabalhará na solução. Assim que resolvido, o cliente será informado.
      Exemplos de Mensagens para Situações Específicas:
      Erro: Não conecta ao servidor

      Mensagem ao cliente:
      "(emote) Entendemos que está enfrentando dificuldades para conectar ao servidor. Vamos analisar e resolver isso rapidamente. Seu problema foi registrado sob o Ticket ID {ticket_id}."
      Erro: Licença inválida

      Mensagem ao cliente:
      "(emote) Parece que há um problema com a licença. Vamos verificar e corrigir isso para você. O problema foi registrado sob o Ticket ID {ticket_id}."
      Erro: Aplicativo não inicia

      Mensagem ao cliente:
      "(emote) O aplicativo não está iniciando corretamente? Não se preocupe, vamos ajudar. Registramos seu problema com o Ticket ID {ticket_id}."
      Coleta de Satisfação:

      Após a resolução, utilize a função RecordCSAT para coletar a pontuação de satisfação do cliente.
      "(emote) Gostaríamos de saber como avalia nosso atendimento! Por favor, forneça uma nota de 1 a 5 para sua experiência."
      Fechamento do Ticket:

      Após coletar o feedback, finalize o processo utilizando a função CloseSupportTicketProblem.
      Com esse fluxo, garantimos um suporte mais rápido e organizado, além de uma melhor experiência para o cliente.



    ### 3. **Gerenciamento de Tickets**

    #### Abertura de Tickets:
    - Utilize a função **OpenSupportTicketProblem** para registrar problemas reportados por clientes no banco de dados.
    - **Parâmetros necessários:**  
    - **user_email**: Email do cliente.  
    - **issue_description**: Descrição detalhada do problema relatado.

    - **Mensagem ao cliente:**  
    "Seu problema foi registrado com sucesso. Nosso time de suporte está analisando a questão. Seu Ticket ID é: **{ticket_id}**."

    #### Coleta de Satisfação:
    - Antes de fechar um ticket, utilize a função **RecordCSAT** para coletar a Pontuação de Satisfação do Cliente (CSAT).  
    - **Parâmetros necessários:**  
    - **ticketid**: ID do ticket em questão.  
    - **csat_score**: Nota de satisfação do cliente (de 1 a 5).  

    - **Mensagem ao cliente:**  
    "Poderia nos informar uma nota de 1 a 5 para avaliar sua experiência com nosso suporte? Sua opinião é muito importante para nós."

    #### Fechamento de Tickets:
    - Após a coleta da CSAT, utilize a função **CloseSupportTicketProblem** para fechar o ticket no banco de dados.
    - **Parâmetros necessários:**  
    - **ticketid**: ID do ticket a ser fechado.

    - **Mensagem ao cliente:**  
    "Obrigado por sua avaliação. O ticket foi encerrado. Caso precise de mais assistência, estamos à disposição!"

    ---

    ### 4. **Informações Técnicas**

    - **Licenciamento:**  
    - A licença permite instalação em até **2 dispositivos**.  
    - O serial é gerado automaticamente após a compra e vinculado ao hardware (CPU e disco).  
    - A licença tem validade de **30 dias**.

    - **Funcionalidades Principais:**  
    - Rotação automática de servidores NordVPN.  
    - Configuração de intervalos personalizados.  
    - Geração de relatórios de servidores utilizados.

    ---

    ### 5. **Passo a Passo para Uso do Aplicativo**

    1. **Instalação:**  
    - Baixe o aplicativo pelo link fornecido.  
    - Execute o instalador e siga as instruções.

    2. **Ativação:**  
    - Insira o serial enviado após a compra.  
    - O aplicativo validará o serial com o hardware.

    3. **Iniciar Rotação:**  
    - Clique no botão "Iniciar" para ativar a rotação automática.

    4. **Parar Rotação:**  
    - Clique em "Parar" quando desejar encerrar a rotação.

    5. **Visualizar Relatório:**  
    - Acesse o histórico de servidores clicando em "Visualizar Relatório".

    ---

    ### 6. **Termos de Serviço**

    - A licença é exclusiva e não pode ser compartilhada.  
    - O uso indevido resultará no cancelamento da licença.  
    - A garantia de reebolso é limitada a 12 horas após a compra.

    ---

    ### 7. **Contatos de Suporte**

    - 📧 **Email:** blocodesense@gmail.com  
    - 📞 **Telegram:** [Grupo de Suporte](https://t.me/+dpGofyMuGUszY2Rh)  
    - 🕘 **Horário de Atendimento:** Segunda a Sexta, das 09h às 18h

    ---

    ### **Mensagem de Encerramento**
    "Estamos à disposição para ajudá-lo a aproveitar ao máximo o **NordVPN Auto Rotate**. Qualquer dúvida, entre em contato pelo nosso suporte. Boa navegação!"

    ---

    ### **Funções Disponíveis**:

    #### **OpenSupportTicketProblem**  
    - **Objetivo:** Registra um ticket no banco de dados.  
    - **Parâmetros:**  
    - **user_email**: Email do cliente.  
    - **issue_description**: Descrição do problema.  
    - **Retorno:**  
    - Ticket ID gerado.

    #### **CloseSupportTicketProblem**  
    - **Objetivo:** Fecha um ticket existente.  
    - **Parâmetros:**  
    - **ticketid**: ID do ticket a ser fechado.

    #### **RecordCSAT**  
    - **Objetivo:** Coleta a Pontuação de Satisfação do Cliente.  
    - **Parâmetros:**  
    - **ticketid**: ID do ticket.  
    - **csat_score**: Nota de 1 a 5.

    ---

            """
            
            self.adxitional_instructions_Alfred = ""

        def Alfred(self, mensagem, user_id):
            AlfredID, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(
                self.appfb, 
                self.client, 
                self.key, 
                self.instruction, 
                self.nameassistantAlfred, 
                self.model_selectAlfred, 
                tools_Alfred
            )

            response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                    mensagem=mensagem,
                                                                    agent_id=AlfredID, 
                                                                    key=self.key,
                                                                    user_id=user_id,
                                                                    app1=self.appfb,
                                                                    client=self.client,
                                                                    tools=tools_Alfred,
                                                                    model_select=self.model_selectAlfred,
                                                                    aditional_instructions=self.adxitional_instructions_Alfred,
                                                                    AgentDestilation=False
                                                                    )
                        
            return response, total_tokens, prompt_tokens, completion_tokens


        async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text('Olá! Como posso ajudar você hoje?')

        async def reply_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_message = update.message.text
            user_id = update.message.from_user.id

            Alfred_response, total_tokens, prompt_tokens, completion_tokens = self.Alfred(user_message, user_id)
            await update.message.reply_text(Alfred_response)

        async def handle_channel_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Lida com mensagens enviadas para um canal específico."""
            if update.message.chat_id == self.CHANNEL_ID:
                user_message = update.message.text
                user_id = update.message.from_user.id  # Opcional, para rastrear o usuário

                Alfred_response, total_tokens, prompt_tokens, completion_tokens = self.Alfred(user_message, user_id)
                await update.message.reply_text(Alfred_response)

        async def send_image_to_channel(self, image_path, caption=None):
            """
            Envia uma imagem para o canal.
            :param image_path: Caminho ou URL da imagem a ser enviada.
            :param caption: Texto opcional para incluir como legenda.
            """
            try:
                await self.agent.send_photo(
                    chat_id=self.CHANNEL_ID,
                    photo=image_path,
                    caption=caption
                )
                print(f"Imagem enviada para o canal {self.CHANNEL_ID}.")
            except Exception as e:
                print(f"Erro ao enviar imagem para o canal: {e}")

        async def handle_task(self, image_path, caption):
            """
            Exemplo de função chamadora que envia a imagem.
            """
            await self.send_image_to_channel(image_path, caption)


        def main(self):
            app = Application.builder().token(self.TOKEN).build()
            
            # Handler para o comando /start
            app.add_handler(CommandHandler("start", self.start))

            # Handler para mensagens diretas
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.reply_message))

            # Handler para mensagens de canais
            app.add_handler(MessageHandler(filters.TEXT & filters.Chat(self.CHANNEL_ID), self.handle_channel_message))

            app.run_polling()

        def meme(self):
            nameApp = "Nord Auto Rotate"
            DescriptionApp = """
            Nord Auto Rotate is a robust and secure application designed to automate the rotation of NordVPN's VPN servers. With an intuitive interface and advanced features, the app ensures its users maintain privacy and security online by automatically switching between different VPN servers at set intervals.

            https://www.youtube.com/watch?v=E4fbZUVMMEI

            AI-Supported Group:
            https://t.me/+dpGofyMuGUszY2Rh

            Requirements
            NordVPN Subscription: To use Nord Auto Rotate, you must have an active NordVPN subscription. The application only works when the subscription is active, whether for 1 month or 1 year.


            Main Features:

            Automatic Server Rotation: Automatically switch between different NordVPN VPN servers to ensure online security and privacy.
            Custom Configuration: Set custom time intervals for server rotation.
            Monitoring and Reporting: Track VPN performance and view detailed usage reports.
            Integration with NordVPN: You must have an active subscription to NordVPN, either monthly or annually.

            Device Limitation: The Nord Auto Rotate license allows installation and use on up to 2 different computers. This limit is imposed to prevent misuse and unauthorized resale of the application.
            License Validity: The license is linked to the order serial. This serial is generated automatically after purchase.

            Security and Authentication:

            Unique Serial: Each license generates a unique serial that is checked against the CPU and disk serial number of the devices. This serial must be used to register the application on up to two computers.
            Serial Validity: The generated serial is valid for 30 days from the initial registration date. After this period, a license renewal will be required to continue using the application.
            Nord Auto Rotate is the ideal solution for those who want to keep their connection secure and anonymous with NordVPN, ensuring automatic and efficient rotation of VPN servers for continuous protection.


            """
            watemark = "@https://t.me/NVAR_suport"

            MemeinApplicationContext_class = Alfred.MemeinApplicationContext(
                                                                            self.appfb, 
                                                                            self.client,
                                                                            nameApp,
                                                                            DescriptionApp,
                                                                            watemark
                                                                            )
            image_path = MemeinApplicationContext_class.main()
            self.send_image_to_channel(image_path)
            caption=None
            async def main():
                await self.handle_task(image_path, caption)

            asyncio.run(main())