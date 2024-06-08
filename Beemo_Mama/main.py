import discord
from discord.ext import commands
import random
import json
from collections import deque
import os

# 절대 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, 'config.json')
recent_numbers_path = os.path.join(current_dir, 'recent_numbers.json')
music_list_path = os.path.join(current_dir, 'music_list.json')

# config.json 파일에서 설정 읽기
try:
    with open(config_path, 'r') as f:
        config = json.load(f)
except Exception as e:
    print(f"Error reading config.json: {e}")
    exit()

bot_token = config['bot_token']
authorized_user_id = int(config['authorized_user_id'])

# recent_numbers.json 파일에서 최근 생성된 숫자 읽기
try:
    with open(recent_numbers_path, 'r') as f:
        recent_data = json.load(f)
        recent_numbers = deque(recent_data['recent_numbers'], maxlen=10)
except Exception as e:
    print(f"Error reading recent_numbers.json: {e}")
    recent_numbers = deque(maxlen=10)

# music_list.json 파일에서 음악 리스트 읽기
try:
    with open(music_list_path, 'r') as f:
        music_data = json.load(f)
        music_list = music_data['music_list']
except Exception as e:
    print(f"Error reading music_list.json: {e}")
    music_list = []

# 디스코드 인텐트 설정
intents = discord.Intents.default()
intents.message_content = True

# Bot 초기화
bot = commands.Bot(command_prefix='!', intents=intents)

# 봇 준비되었을 때 실행되는 이벤트
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# "!랜덤곡" 명령어 처리
@bot.command(name='랜덤곡')
async def random_music_command(ctx):
    if ctx.author.id == authorized_user_id:
        try:
            recent_numbers.clear()
            if not music_list:
                await ctx.send('음악 리스트가 비어 있습니다. music_list.json 파일을 확인하세요.')
                return
            random_music = random.choice(music_list)
            recent_numbers.append(random_music)
            with open(recent_numbers_path, 'w') as f:
                json.dump({'recent_numbers': list(recent_numbers)}, f)
            await ctx.send(f'첫 곡: {random_music}')
        except Exception as e:
            await ctx.send(f'오류 발생: {e}')
    else:
        await ctx.send('이 명령어를 사용할 권한이 없습니다.')

# "!다음곡" 명령어 처리
@bot.command(name='다음곡')
async def next_music_command(ctx):
    if ctx.author.id == authorized_user_id:
        try:
            if not music_list:
                await ctx.send('음악 리스트가 비어 있습니다. music_list.json 파일을 확인하세요.')
                return
            if not recent_numbers:
                await ctx.send('최근에 생성된 곡이 없습니다. 먼저 !랜덤곡 명령어를 사용하세요.')
                return
            possible_music = [song for song in music_list if song not in recent_numbers]
            if possible_music:
                random_music = random.choice(possible_music)
                recent_numbers.append(random_music)
                with open(recent_numbers_path, 'w') as f:
                    json.dump({'recent_numbers': list(recent_numbers)}, f)
                await ctx.send(f'다음곡: {random_music}')
            else:
                await ctx.send('모든 음악이 최근에 사용되었습니다.')
        except Exception as e:
            await ctx.send(f'오류 발생: {e}')
    else:
        await ctx.send('님 권한 없음 ㅅㄱ')

# "!경기시작" 명령어 처리
@bot.command(name='경기시작')
async def start_game_command(ctx):
    await ctx.send('경기 시자ㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏ악 하겠습니다!!!!!!!!!!!!!!')

# 봇 실행
try:
    bot.run(bot_token)
except Exception as e:
    print(f"Error running bot: {e}")
