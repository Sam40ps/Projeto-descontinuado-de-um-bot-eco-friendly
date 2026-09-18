import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

FATOS_POLUICAO = [
"Mais de 8 milhões de toneladas de plástico entram nos oceanos a cada ano.",
"A poluição do ar causa cerca de 7 milhões de mortes prematuras anualmente no mundo.",
"Uma garrafa PET leva em média 450 anos para se decompor completamente na natureza.",
"Cerca de 99% da população mundial respira ar que excede os limites de qualidade da OMS.",
"O lixo eletrônico é a corrente de resíduos que mais cresce no planeta."
]

DICAS_ECOLOGICAS = [
"🥤 Zero Plástico: Substitua garrafas descartáveis por uma garrafa reutilizável.",
"🛍️ Compras Sustentáveis: Leve sacolas de pano (ecobags) ao supermercado.",
"🔌 Vampiros de Energia: Desconecte aparelhos da tomada quando não estiver usando.",
"🚲 Mobilidade Verde: Prefira caminhar, ir de bicicleta ou usar transporte público.",
"♻️ Descarte Correto: Separe o lixo orgânico do reciclável e busque pontos de coleta adequados."
]

PERGUNTAS_QUIZ = [
{
"pergunta": "Quanto tempo uma garrafa de plástico PET leva para se decompor?",
"opcoes": ["A) 50 anos", "B) 100 anos", "C) 450 anos", "D) 1000 anos"],
"resposta": "c"
},
{
"pergunta": "Qual destes materiais pode ser reciclado infinitas vezes sem perder qualidade?",
"opcoes": ["A) Plástico", "B) Vidro", "C) Papel", "D) Isopor"],
"resposta": "b"
}
]

quizzes_ativos = {}

@commands.command(name="fato")
async def fato_poluicao(ctx):
    fato = random.choice(FATOS_POLUICAO)
    embed = discord.Embed(
        title="🌍 Fato Sobre a Poluição",
        description=fato,
        color=discord.Color.dark_green()
    )
    await ctx.send(embed=embed)


@commands.command(name="dica")
async def dica_ecologica(ctx):
    dica = random.choice(DICAS_ECOLOGICAS)
    embed = discord.Embed(
        title="🌱 Dica de Sustentabilidade",
        description=dica,
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)


@commands.command(name="pegada")
async def pegada_carbono(ctx, meio_transporte: str, km: float):
    meio = meio_transporte.lower()

    emissoes = {
    "carro": 0.19,
    "moto": 0.10,
    "onibus": 0.08,
    "aviao": 0.25,
    "bike": 0.0,
    "pe": 0.0
    }

    if meio not in emissoes:
        await ctx.send("Opção inválida! Meios aceitos: `carro`, `moto`, `onibus`, `aviao`, `bike`, `pe`.")
        return

    co2_total = emissoes[meio] * km

    embed = discord.Embed(
        title="📊 Estimativa de Emissão de Carbono",
        color=discord.Color.gold()
    )
    embed.add_field(name="Trajeto", value=f"{km} km usando {meio.capitalize()}", inline=False)
    embed.add_field(name="Emissão Estimada", value=f"{co2_total:.2f} kg de CO2", inline=False)

    if co2_total == 0:
        embed.set_footer(text="Ótima escolha! Esse meio de transporte não emite CO2 direto. 🌱")
    else:
        embed.set_footer(text="Considere substituir trajetos curtos por caminhada ou bicicleta.")

    await ctx.send(embed=embed)


@commands.command(name="quiz")
async def iniciar_quiz(ctx):
    if ctx.channel.id in quizzes_ativos:
        await ctx.send("Já existe um quiz em andamento neste canal!")
        return

    questao = random.choice(PERGUNTAS_QUIZ)
    quizzes_ativos[ctx.channel.id] = questao["resposta"]

    opcoes_texto = "\n".join(questao["opcoes"])
    embed = discord.Embed(
        title="🧠 Quiz Ambiental",
        description=f"{questao['pergunta']}\n\n{opcoes_texto}\n\nResponda usando: `!resposta `",
        color=discord.Color.teal()
    )
    await ctx.send(embed=embed)


@commands.command(name="resposta")
async def responder_quiz(ctx, escolha: str):
    channel_id = ctx.channel.id

    if channel_id not in quizzes_ativos:
        await ctx.send("Nenhum quiz ativo no momento. Use `!quiz` para iniciar!")
        return

    if escolha.lower() == quizzes_ativos[channel_id]:
        await ctx.send(f"🎉 Resposta correta, {ctx.author.mention}!")
        del quizzes_ativos[channel_id]
    else:
        await ctx.send(f"❌ Resposta incorreta, {ctx.author.mention}. Tente novamente!")

bot.run("Seu token aqui")
