import discord
from discord import app_commands
import torch
import requests
import json
intents = discord.Intents.default()
groq_api="your_groq_api_key_here"
intents.members = True
intents.message_content = True
bot = discord.Client(intents=intents)
DISCORD_TOKEN="your_discord_token_here"
JINA_TOKEN="your_jina_token_here"
JINA_URL="your_jina_url_here"
jina_headers={
    "Content-Type": "application/json",
    "Authorization": f"Bearer {JINA_TOKEN}"
}
def clean_text(text):
    stop_words = ["a", "the", "is", "of", "in", "to", "and", "about"]
    text_lower=text.lower()
    words=text_lower.split()
    important=[]
    for w in words:
        if w not in stop_words:
            important.append(w)
    end=" ".join(important)
    return end
with open("library_vault1.json", "r") as f:
    loaded_data = json.load(f)
titles=loaded_data["titles"]
ratings = loaded_data["ratings"]  # NEW
covers = loaded_data["covers"]   # NEW
tags = loaded_data["tags"]    
year=loaded_data["year"]
Y_last = torch.tensor(loaded_data["embeddings"], dtype=torch.float32)
@bot.event
async def on_ready():
    print(f"✅ AI Bot is online! Model ready.")
channel_id=[1491573348151590972]
@bot.event
async def on_message(messages):
    if messages.author == bot.user :
        return
    if messages.channel.id in channel_id:
        promot=f""
        SYSTEM INSTRUCTION:
You are a classification and response agent. Your job is to analyze the USER_MESSAGE and determine if it contains a request for manga, manhwa, or manhua (titles, tags, or descriptions).
OUTPUT FORMAT:
You must output ONLY a valid JSON object. Do not include any conversational text before or after the JSON.
SCHEMA:
{{
  "skip": boolean,
  "text": "string"
}}
LOGIC:
1. If the message DOES NOT mention manga/manhua/manhwa:
   - "skip": true
   - "text": "Hi there! I'm here to help you find manga, manhwa, or manhua you'll love. Just let me know the title, a tag, or a brief description of what you’re looking for."

2. If the message DOES mention manga/manhua/manhwa(titel or desciption or tags):
   - "skip": false
   - "text": "Here are some recommendations that match your request, presented in a clean, easy-to-read format:"
   USER_MESSAGE:
"{messages.content}"
       "
        url="https://api.groq.com/openai/v1/chat/completions"
        header={
            "Authorization":f"Bearer {groq_api}",
            "Content-Type":"application/json"
        }
        body={
            "model":"openai/gpt-oss-120b",
            "messages":[
                {{"role":"user","content":promot}}
            ]
        }
        groq_requast=requests.post(url , headers=header,json=body)
        groq_respond=groq_requast.json()
        
        ai_data=json.loads(groq_respond['choices'][0]['message']['content'])
        if ai_data['skip']==False :
            payload={
            "model":"jina-embeddings-v2-base-en",
           "input": clean_text(messages.content)
             }
            jina_requast = requests.post(JINA_URL, headers=jina_headers, json=payload)
            jina_result = jina_requast.json()
            jina_firesult=jina_result.get("data")
            result=jina_firesult[0]["embedding"]
            user_tensor = torch.tensor(result).unsqueeze(0)
            all_scores = torch.nn.functional.cosine_similarity(user_tensor, Y_last, dim=1)  
            values, indices = torch.topk(all_scores, k=min(6, len(titles)))
            recommendations = []
            for i in range(1, len(indices)):
                idx = indices[i].item()
                score = values[i].item()
                recommendations.append(f"{i}. **{titles[idx]}** (Score: {score:.2f}),(rating :{ratings[idx]}),(tags:{tags[idx]}),(year :{year[idx]}),(cover : {covers[idx]})")   
            await messages.channel.send(ai_data['text'])
            for j in range(0,len(recommendations)):
                await messages.channel.send(f" {recommendations[j]}\n ")
        else:
            await messages.channel.send(ai_data['text'])
bot.run(DISCORD_TOKEN)