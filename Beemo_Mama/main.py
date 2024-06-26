import discord
from discord.ext import commands
import random
import json
from collections import deque
import os

# 절대 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, 'config.json')
recent_musics_path = os.path.join(current_dir, 'recent_musics.json')
music_list_path = os.path.join(current_dir, 'music_list.json')
authorized_users_path = os.path.join(current_dir, 'authorized_users.json')

# config.json 파일에서 설정 읽기
try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except Exception as e:
    print(f"Error reading config.json: {e}")
    exit()

bot_token = config['bot_token']
authorized_user_id = int(config['authorized_user_id'])

# recent_musics.json 파일에서 최근 생성된 숫자 읽기
try:
    with open(recent_musics_path, 'r', encoding='utf-8') as f:
        recent_data = json.load(f)
        recent_musics = deque(recent_data['recent_musics'], maxlen=10)
except Exception as e:
    print(f"Error reading recent_musics.json: {e}")
    recent_musics = deque(maxlen=50)

# music_list.json 파일에서 음악 리스트 읽기
try:
    with open(music_list_path, 'r', encoding='utf-8') as f:
        music_data = json.load(f)
        music_list = music_data['music_list']
except Exception as e:
    print(f"Error reading music_list.json: {e}")
    music_list = []

# authorized_users.json 파일에서 권한 있는 사용자 목록 읽기
try:
    with open(authorized_users_path, 'r', encoding='utf-8') as f:
        authorized_users = set(json.load(f))
except Exception as e:
    print(f"Error reading authorized_users.json: {e}")
    authorized_users = set()

# 디스코드 인텐트 설정
intents = discord.Intents.default()
intents.message_content = True

# Bot 초기화
bot = commands.Bot(command_prefix='!', intents=intents)

# 봇 준비되었을 때 실행되는 이벤트
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# 사용자 권한 체크 함수
def check_authorization(user_id):
    return user_id == authorized_user_id or user_id in authorized_users

# "!랜덤곡" 명령어 처리
@bot.command(name='랜덤곡')
async def random_music_command(ctx):
    if check_authorization(ctx.author.id):
        try:
            recent_musics.clear()
            if not music_list:
                await ctx.send('음악 리스트가 비어 있습니다. music_list.json 파일을 확인하세요.')
                return
            random_music = random.choice(music_list)
            recent_musics.append(random_music)
            with open(recent_musics_path, 'w', encoding='utf-8') as f:
                json.dump({'recent_musics': list(recent_musics)}, f, ensure_ascii=False)
            await ctx.send(f'첫 곡: {random_music}')
        except Exception as e:
            await ctx.send(f'오류 발생: {e}')
    else:
        await ctx.send('님 권한 없음 ㅅㄱ.')

# "!다음곡" 명령어 처리
@bot.command(name='다음곡')
async def next_music_command(ctx):
    if check_authorization(ctx.author.id):
        try:
            if not music_list:
                await ctx.send('음악 리스트가 비어 있습니다. music_list.json 파일을 확인하세요.')
                return
            if not recent_musics:
                await ctx.send('최근에 생성된 곡이 없습니다. 먼저 !랜덤곡 명령어를 사용하세요.')
                return
            possible_music = [song for song in music_list if song not in recent_musics]
            if possible_music:
                random_music = random.choice(possible_music)
                recent_musics.append(random_music)
                with open(recent_musics_path, 'w', encoding='utf-8') as f:
                    json.dump({'recent_musics': list(recent_musics)}, f, ensure_ascii=False)
                await ctx.send(f'다음곡: {random_music}')
            else:
                await ctx.send('모든 음악이 최근에 사용되었습니다.')
        except Exception as e:
            await ctx.send(f'오류 발생: {e}')
    else:
        await ctx.send('님 권한 없음 ㅅㄱ.')

# "!경기시작" 명령어 처리
@bot.command(name='경기시작')
async def start_game_command(ctx):
    await ctx.send('경기 시자ㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏ악 하겠습니다!!!!!!!!!!!!!!')

# "!권한추가" 명령어 처리
@bot.command(name='권한추가')
async def add_authorization_command(ctx, user: discord.User):
    if ctx.author.id == authorized_user_id:
        if user.id in authorized_users:
            await ctx.send(f'{user.mention}이미 권한 있잖슴')
        else:
            authorized_users.add(user.id)
            with open(authorized_users_path, 'w', encoding='utf-8') as f:
                json.dump(list(authorized_users), f, ensure_ascii=False)
            await ctx.send(f'{user.mention}님 명령어 쓰셈')
    else:
        await ctx.send('권한 없음 ㅅㄱ')

# "!권한압수" 명령어 처리
@bot.command(name='권한압수')
async def remove_authorization_command(ctx, user: discord.User):
    if ctx.author.id == authorized_user_id:
        if user.id in authorized_users:
            authorized_users.remove(user.id)
            with open(authorized_users_path, 'w', encoding='utf-8') as f:
                json.dump(list(authorized_users), f, ensure_ascii=False)
            await ctx.send(f'{user.mention}님의 명령어 사용 권한을 압수했습니다.')
        else:
            await ctx.send(f'{user.mention}님은 권한이 없습니다.')
    else:
        await ctx.send('님 권한 없음 ㅅㄱ')        

# "!곡추가" 명령어 처리
@bot.command(name='곡추가')
async def add_music_command(ctx, *, song: str):
    if check_authorization(ctx.author.id):
        if song in music_list:
            await ctx.send(f'"{song}"은(는) 이미 목록에 있습니다.')
        else:
            music_list.append(song)
            with open(music_list_path, 'w', encoding='utf-8') as f:
                json.dump({'music_list': music_list}, f, ensure_ascii=False)
            await ctx.send(f'"{song}"을(를) 목록에 추가했습니다.')
    else:
        await ctx.send('님 권한 없음 ㅅㄱ')

# "!초기화" 명령어 처리
@bot.command(name='초기화')
async def reset_recent_musics(ctx):
    if check_authorization(ctx.author.id):
        recent_musics.clear()
        with open(recent_musics_path, 'w', encoding='utf-8') as f:
            json.dump({'recent_musics': list(recent_musics)}, f, ensure_ascii=False)
        await ctx.send('최근 곡 리스트가 초기화되었습니다.')
    else:
        await ctx.send('이 명령어를 사용할 권한이 없습니다.')

# "!리스트" 명령어 처리
@bot.command(name='리스트')
async def list_music_command(ctx):
    if check_authorization(ctx.author.id):
        if not music_list:
            await ctx.send('음악 리스트가 비어 있습니다.')
        else:
            await ctx.send('음악 리스트:\n' + '\n'.join(music_list))
    else:
        await ctx.send('님 권한 없음 ㅅㄱ')

# 봇 실행
try:
    bot.run(bot_token)
except Exception as e:
    print(f"Error running bot: {e}")
