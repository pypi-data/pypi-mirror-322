

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

# IMPORT SoftwareAI Functions
from softwareai.CoreApp._init_functions_ import *
#########################################
# IMPORT SoftwareAI Functions Submit Outputs
from softwareai.CoreApp._init_submit_outputs_ import _init_output_


class Alfred:
    """softwareai/Docs/Agents/Alfred.md"""
    def __init__(self,
                appfb,
                client,
                TOKEN,
                CHANNEL_ID
            ):
        self.appfb = appfb
        self.client = client
        self.TOKEN = TOKEN
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

### 2. **Solução de Problemas**

#### Problemas Comuns e Soluções:
- **Erro: Não conecta ao servidor**  
  🔎 *Causa:* Falha de conexão com o NordVPN.  
  ✅ *Solução:* Verifique se o NordVPN está ativo e com assinatura válida.

- **Erro: Licença inválida**  
  🔎 *Causa:* Serial incorreto ou vencido.  
  ✅ *Solução:* Confirme o serial usado e informe que a licença tem validade de 30 dias. Oriente sobre a renovação.

- **Erro: Aplicativo não inicia**  
  🔎 *Causa:* Requisitos do sistema não atendidos.  
  ✅ *Solução:* Verifique se o Python 3.x está instalado e se o NordVPN está atualizado.

---

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


    class NordVPN_Auto_Rotate:
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


        def main(self):
            app = Application.builder().token(self.TOKEN).build()
            app.add_handler(CommandHandler("start", self.start))
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.reply_message))

            app.run_polling()

