import discord
from discord.ext import commands
import random
import json
from collections import deque

# config.json 파일에서 설정 읽기
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except Exception as e:
    print(f"Error reading config.json: {e}")
    exit()

bot_token = config['bot_token']
authorized_user_id = int(config['authorized_user_id'])

# recent_numbers.json 파일에서 최근 생성된 숫자 읽기
try:
    with open('recent_numbers.json', 'r') as f:
        recent_data = json.load(f)
        recent_numbers = deque(recent_data['recent_numbers'], maxlen=10)
except Exception as e:
    print(f"Error reading recent_numbers.json: {e}")
    recent_numbers = deque(maxlen=10)

# 디스코드 인텐트 설정
intents = discord.Intents.default()
intents.message_content = True

# Bot 초기화
bot = commands.Bot(command_prefix='!', intents=intents)

# 봇 준비되었을 때 실행되는 이벤트
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# "!random" 명령어 처리
@bot.command(name='random')
async def random_command(ctx, arg=None):
    if ctx.author.id == authorized_user_id:
        if arg is None:
            await ctx.send('올바른 형식: !random [숫자] 또는 !random again')
            return

        try:
            if arg.lower() == 'again':
                if not recent_numbers:
                    await ctx.send('최근에 생성된 숫자가 없습니다. 먼저 !random [숫자] 명령어를 사용하세요.')
                    return
                max_number = max(recent_numbers)
                possible_numbers = [i for i in range(1, max_number + 1) if i not in recent_numbers]
                print(f"possible_numbers: {possible_numbers}")

                if possible_numbers:
                    random_number = random.choice(possible_numbers)
                    recent_numbers.append(random_number)
                    with open('recent_numbers.json', 'w') as f:
                        json.dump({'recent_numbers': list(recent_numbers)}, f)
                    await ctx.send(f'랜덤 숫자: {random_number}')
                else:
                    await ctx.send('모든 숫자가 최근에 사용되었습니다.')

            else:
                max_number = int(arg)
                recent_numbers.clear()
                possible_numbers = list(range(1, max_number + 1))
                random_number = random.choice(possible_numbers)
                recent_numbers.append(random_number)
                with open('recent_numbers.json', 'w') as f:
                    json.dump({'recent_numbers': list(recent_numbers)}, f)
                await ctx.send(f'랜덤 숫자: {random_number}')

        except ValueError:
            await ctx.send('올바른 형식: !random [숫자] 또는 !random again')
    else:
        await ctx.send('이 명령어를 사용할 권한이 없습니다.')

# 봇 실행
try:
    bot.run(bot_token)
except Exception as e:
    print(f"Error running bot: {e}")
