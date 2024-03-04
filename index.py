# coding:utf-8
import pygame
from pygame.locals import *
import time
import random
import sys
import math
import os

# 初始化pygame环境
pygame.init()

# 创建一个长宽分别为480/650窗口
screen = pygame.display.set_mode((480, 650))
screen.fill((255, 255, 255))

# 设置窗口标题
pygame.display.set_caption("外星人入侵")

# 敌飞机图片数组
e1 = []
e1.append(pygame.image.load("images/enemy1.png"))
e1.append(pygame.image.load("images/enemy1_down1.png"))
e1.append(pygame.image.load("images/enemy1_down2.png"))
e1.append(pygame.image.load("images/enemy1_down3.png"))
e1.append(pygame.image.load("images/enemy1_down4.png"))
e1.append(pygame.image.load("images/enemy1_down5.png"))
e2 = []
e2.append(pygame.image.load("images/enemy2.png"))
e2.append(pygame.image.load("images/enemy2_down1.png"))
e2.append(pygame.image.load("images/enemy2_down2.png"))
e2.append(pygame.image.load("images/enemy2_down3.png"))
e2.append(pygame.image.load("images/enemy2_down4.png"))
e2.append(pygame.image.load("images/enemy2_down5.png"))
e3 = []
e3.append(pygame.image.load("images/enemy3_1.png"))
e3.append(pygame.image.load("images/enemy3_2.png"))
e3.append(pygame.image.load("images/enemy3_down1.png"))
e3.append(pygame.image.load("images/enemy3_down2.png"))
e3.append(pygame.image.load("images/enemy3_down3.png"))
e3.append(pygame.image.load("images/enemy3_down4.png"))
e3.append(pygame.image.load("images/enemy3_down5.png"))
e3.append(pygame.image.load("images/enemy3_down6.png"))
e3.append(pygame.image.load("images/enemy3_down7.png"))
h = []
h.append(pygame.image.load("images/hero.png"))
h.append(pygame.image.load("images/hero_down1.png"))
h.append(pygame.image.load("images/hero_down2.png"))
h.append(pygame.image.load("images/hero_down3.png"))
h.append(pygame.image.load("images/hero_down4.png"))
# 背景图片
bg = pygame.image.load("images/bg1.png")
# 子弹图片
bullet_image = pygame.image.load("images/bullet_1.png")
scaled_bullet_image = pygame.transform.scale(bullet_image, (10, 30))  # 设置新的尺寸
b = []
b.append(scaled_bullet_image)
# 开始游戏图片
startgame = pygame.image.load("images/startGame.png")
# logo图片
logo = pygame.image.load("images/logo1.png")
# 暂停图片
pause = pygame.image.load("images/game_pause_nor.png")
# 重新开始按钮
restart_icon = pygame.image.load("images/restart.png")
restart_icon = pygame.transform.scale(restart_icon, (100, 100))  # 设置合适的新尺寸
# 排行榜按钮
sorting_icon = pygame.image.load("images/sorting1.png")
sorting_icon = pygame.transform.scale(sorting_icon, (250, 80))  # 设置合适的新尺寸
# 回到开始按钮
back_button = pygame.image.load("images/back_button.png")
#back_button = pygame.transform.scale(back_button, (200, 100))  # 设置合适的新尺寸

gold_image = pygame.image.load("images/gold_medal.png")  # 加载金牌图片
gold_image = pygame.transform.scale(gold_image, (30, 30))  # 调整图片大小

silver_image = pygame.image.load("images/silver_medal.png")  # 加载银牌图片  
silver_image = pygame.transform.scale(silver_image, (30, 30))  # 调整图片大小

bronze_image = pygame.image.load("images/bronze_medal.png")  # 加载铜牌图片
bronze_image = pygame.transform.scale(bronze_image, (30, 30))  # 调整图片大小
def restart_game():
    # GameVar.state = GameVar.STATES["START"]
    GameVar.score = 0
    GameVar.heroes = 3  # 此处重置生命值，应与GameVar类属性初始化时的生命值一致
    GameVar.hero = Hero(0, 0, 60, 75, 1, 1, h, 1)  # 重置英雄机
    GameVar.enemies = []  # 清空敌机列表
    GameVar.bullets = []  # 清空子弹列表
    GameVar.props_buff = []  # 清空药水列表
    GameVar.props = []  # 清空炸弹列表
    # 重置Boss相关状态
    GameVar.boss = []
    GameVar.last_boss_score = 0
    GameVar.boss_warning_start_time = None
    # 可能还需要添加其他的重置逻辑
    GameVar.state = GameVar.STATES["SELECTION"]
    GameVar.countdown_start = None
    GameVar.bombs = 0
    GameVar.round = 1


def handle_restart_click(mouse_pos):
    restart_button_position = (200, 400)
    restart_button_rect = pygame.Rect(restart_button_position, (80, 80))
    if restart_button_rect.collidepoint(mouse_pos):
        restart_game()


def handle_sorting_click(mouse_pos):
    sorting_button_position = (150, 500)
    sorting_button_rect = pygame.Rect(sorting_button_position, (200, 100))
    if sorting_button_rect.collidepoint(mouse_pos):
        show_sorting_screen()


def handleEvent():
    for event in pygame.event.get():
        # 按ESC退出游戏
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        # 监听鼠标移动事件
        if event.type == pygame.MOUSEMOTION:
            # 只有当游戏处于运行状态(或警告状态)时才根据鼠标的坐标修改英雄机的坐标
            if GameVar.state in [GameVar.STATES["RUNNING"], GameVar.STATES["BOSS_WARNING"]]:
                GameVar.hero.x = event.pos[0] - GameVar.hero.width / 2
                GameVar.hero.y = event.pos[1] - GameVar.hero.height / 2

        # 点击左键切换为运行状态
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if GameVar.state == GameVar.STATES["START"]:
                GameVar.state = GameVar.STATES["SELECTION"]

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 \
                and GameVar.state == GameVar.STATES['GAME_OVER']:
            mouse_pos = pygame.mouse.get_pos()
            handle_restart_click(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 \
                and GameVar.state == GameVar.STATES['GAME_OVER']:
            mouse_pos = pygame.mouse.get_pos()
            handle_sorting_click(mouse_pos)

        # 键盘事件
        if event.type == KEYDOWN:
            # 按下空格键切换为暂停状态
            if event.key == K_SPACE:
                if GameVar.state == GameVar.STATES["RUNNING"]:
                    GameVar.state = GameVar.STATES["PAUSE"]
                elif GameVar.state == GameVar.STATES["PAUSE"]:
                    GameVar.state = GameVar.STATES["RUNNING"]
            # 按下3键释放大招
            if event.key == K_3 and GameVar.charge_ready:
                if GameVar.selected_ability == 'barrage':
                    GameVar.charge_ready = False
                    GameVar.charge_progress = 0
                    fire_barrage(GameVar.hero)  # 发射弹幕

                elif GameVar.selected_ability == 'laser':
                    GameVar.charge_ready = False
                    GameVar.charge_progress = 0
                    fire_laser(GameVar.hero)  # 发射瞬时激光
            # 按下2键释放炸弹
            if event.key == K_2 and GameVar.bombs > 0:
                for enemy in GameVar.enemies:
                    enemy.down = True  # 摧毁所有敌机
                    enemy.frameIndex = enemy.frameCount  # 切换到坠毁效果的第一帧
                GameVar.bombs -= 1  # 减少一个炸弹

            # 游戏中按下5键重新开始游戏
            elif event.key == K_5:
                restart_game()


# 工具方法-判断时间间隔是否到了
def isActionTime(lastTime, interval):
    if lastTime == 0:
        return True
    currentTime = time.time()
    return currentTime - lastTime >= interval


# 工具方法-写文字方法
def renderText(text, position, view, color=(255, 255, 255)):
    # 设置字体样式和大小
    my_font = pygame.font.Font("STLITI.TTF", 40)
    # 渲染文字
    text = my_font.render(text, True, color)
    view.blit(text, position)


# 工具方法-判断鼠标是否移出了游戏区域
def isMouseOut(x, y):
    if x >= 479 or x <= 0 or y > 649 or y <= 0:
        return True
    else:
        return False


# 工具方法-判断鼠标是否移入了游戏区域
def isMouseOver(x, y):
    if x > 1 and x < 479 and y > 1 and y < 648:
        return True
    else:
        return False


# 定义Sky类
class Sky(object):
    def __init__(self):
        self.width = 480
        self.height = 852
        self.img = bg
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = -self.height

    def paint(self, view):
        view.blit(self.img, (self.x1, self.y1))
        view.blit(self.img, (self.x2, self.y2))

    def step(self):
        self.y1 = self.y1 + 1
        self.y2 = self.y2 + 1
        if self.y1 > self.height:
            self.y1 = -self.height
        if self.y2 > self.height:
            self.y2 = -self.height


# 定义父类FlyingObject
class FlyingObject(object):
    def __init__(self, x, y, width, height, life, frames, baseFrameCount):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.life = life
        # self.img = img
        # 敌飞机移动的时间间隔
        self.lastTime = 0
        self.interval = 0.01
        # 添加掉落属性和删除属性
        self.down = False
        self.canDelete = False
        # 实现动画所需属性
        self.frames = frames
        self.frameIndex = 0
        self.img = self.frames[self.frameIndex]
        self.frameCount = baseFrameCount

    def paint(self, view):
        view.blit(self.img, (self.x, self.y))

    def step(self):
        # 判断是否到了移动的时间间隔
        if not isActionTime(self.lastTime, self.interval):
            return
        self.lastTime = time.time()
        # 控制移动速度
        self.y = self.y + 2

    # 碰撞检测方法
    def hit(self, component):
        c = component
        return self.x - c.width < c.x < self.x + self.width and c.y > self.y - c.height and c.y < self.y + self.height

    # 处理碰撞发生后要做的事
    def bang(self):
        self.life -= 1
        if self.life <= 0:
            # 生命值为0时将down置为True
            self.down = True
            # 将frameIndex切换为销毁动画的第一张
            self.frameIndex = self.frameCount

            if hasattr(self, "score"):
                GameVar.score += self.score

    def laser_bang(self):
        self.life -= 4  # 被激光击中后受到200点伤害
        if self.life <= 0:
            # 生命值为0时将down置为True
            self.down = True
            # 将frameIndex切换为销毁动画的第一张
            self.frameIndex = self.frameCount

            # 因为现在没有销毁动画，所以死亡后立即删除
            # if self.down == True:
            # self.canDelete = True
            # 播放击败音效
            explosion_sound.play()

            if hasattr(self, "score"):
                GameVar.score += self.score

    # 越界处理
    def outOfBounds(self):
        return self.y > 650

    # 实现动画
    def animation(self):
        if self.down:
            # 销毁动画播放完后将canDelete置为True
            if self.frameIndex == len(self.frames):
                self.canDelete = True
            else:
                self.img = self.frames[self.frameIndex]
                self.frameIndex += 1
        else:
            self.img = self.frames[self.frameIndex % self.frameCount]
            self.frameIndex += 1


# 定义Enemy类
class Enemy(FlyingObject):
    def __init__(self, x, y, width, height, type, life, frames, baseFrameCount):
        FlyingObject.__init__(self, x, y, width, height, life, frames, baseFrameCount)
        self.x = random.randint(0, 480 - self.width)
        self.y = -self.height
        self.type = type

    def bang(self):
        self.life -= 1
        if self.life <= 0:
            # 生命值为0时将down置为True
            self.down = True
            # 将frameIndex切换为销毁动画的第一张
            self.frameIndex = self.frameCount
            explosion_sound.play()
            if hasattr(self, "score"):
                GameVar.score += self.score

    # 实现动画
    def animation(self):
        if self.down:
            # 销毁动画播放完后将canDelete置为True
            if self.frameIndex == len(self.frames):
                self.canDelete = True
                if self.type == 1:
                    GameVar.score += 10
                elif self.type == 2:
                    GameVar.score += 20
                else:
                    GameVar.score += 50
            else:
                self.img = self.frames[self.frameIndex]
                self.frameIndex += 1
        else:
            self.img = self.frames[self.frameIndex % self.frameCount]
            self.frameIndex += 1


class EnemyBullet(FlyingObject):
    def __init__(self, x, y, width, height, frames, baseFrameCount):
        super().__init__(x, y, width, height, 1, frames, baseFrameCount)
        self.velocity_y = 3

    def step(self):
        self.y += self.velocity_y

    def outOfBounds(self):
        return self.y > 650

    def bang(self):
        self.life -= 1
        if self.life <= 0:
            # 生命值为0时将down置为True
            self.down = True
            # 将frameIndex切换为销毁动画的第一张
            self.frameIndex = self.frameCount
            explosion_sound.play()
            if hasattr(self, "score"):
                GameVar.score += self.score


class Boss(FlyingObject):
    def __init__(self, x, y, width, height, frames, baseFrameCount):
        super().__init__(x, y, width, height, 100 * GameVar.round, frames, baseFrameCount)
        self.max_life = 100 * GameVar.round  # 设置最大生命值
        self.moving_right = True
        self.shoot_last_time = 0
        self.shoot_interval = 0.7  # 射击间隔


    def paint(self, view):
        super().paint(view)
        # 绘制血量条
        draw_health_bar(view, self.x, self.y - 10, self.life, self.max_life, self.width, 5, (255, 0, 0))

    def step(self):
        if self.y < 100:
            self.y += 1
        else:
            if self.moving_right:
                self.x += 1
                if self.x + self.width > 480:
                    self.moving_right = False
            else:
                self.x -= 1
                if self.x < 0:
                    self.moving_right = True

        current_time = time.time()
        if current_time - self.shoot_last_time > self.shoot_interval:
            self.shoot()
            self.shoot_last_time = current_time

    def shoot(self):
        bullet = EnemyBullet(self.x + self.width / 2, self.y + self.height, 9, 21, enemy_bullet_frames, 1)
        GameVar.bullets.append(bullet)

    def bang(self):
        self.life -= 1
        if self.life <= 0:
            self.down = True
            self.frameIndex = self.frameCount  # 切换到坠毁效果的第一帧
            # 播放击败音效
            boss_explosion_sound.play()

    def laser_bang(self):
        self.life -= 4  # 被激光击中后受到200点伤害
        if self.life <= 0:
            # 生命值为0时将down置为True
            self.down = True
            # 将frameIndex切换为销毁动画的第一张
            self.frameIndex = self.frameCount

            explosion_sound.play()


    def animation(self):
        if self.down:
            # 销毁动画播放完后将canDelete置为True
            if self.frameIndex == len(self.frames):
                self.canDelete = True
                GameVar.heroes += 1
                GameVar.round += 1
            else:
                self.img = self.frames[self.frameIndex]
                self.frameIndex += 1
        else:
            self.img = self.frames[self.frameIndex % self.frameCount]
            self.frameIndex += 1


class Hero(FlyingObject):
    def __init__(self, x, y, width, height, state, life, frames, baseFrameCount):
        FlyingObject.__init__(self, x, y, width, height, life, frames, baseFrameCount)
        self.width = 60
        self.height = 75
        self.x = 480 / 2 - self.width / 2
        self.y = 650 - self.height - 30
        # 射击时间间隔
        self.shootLastTime = 0
        self.shootInterval = 0.2
        self.max_life = life  # 设置最大生命值
        self.state = state
        self.state_change_time = None  # 添加状态改变时间记录

    def shoot(self):
        if not isActionTime(self.shootLastTime, self.shootInterval):
            return
        if self.state == 1:
            self.shootLastTime = time.time()
            GameVar.bullets.append(Bullet(self.x + self.width / 2 - 5, self.y - 10, 9, 21, 1, b, 1))
        elif self.state == 2:
            self.shootLastTime = time.time()
            left_bullet_x = self.x + self.width / 2 - 5 - 20  # 假设左侧子弹向左偏移20像素
            right_bullet_x = self.x + self.width / 2 - 5 + 20  # 假设右侧子弹向右偏移20像素
            GameVar.bullets.append(Bullet(left_bullet_x, self.y - 10, 9, 21, 1, b, 1))
            GameVar.bullets.append(Bullet(right_bullet_x, self.y - 10, 9, 21, 1, b, 1))

    # 添加获取炸弹的方法
    def get_bomb(self):
        GameVar.bombs += 1

# 定义Bullet类
class Bullet(FlyingObject):
    def __init__(self, x, y, width, height, life, frames, baseFrameCount):
        FlyingObject.__init__(self, x, y, width, height, life, frames, baseFrameCount)

    # 重写step方法
    def step(self):
        self.y = self.y - 2

    # 重写判断是否越界的方法
    def outOfBounds(self):
        return self.y < -self.height


# 定义弹幕类，用于飞机的第一种大招
class BarrageBullet(Bullet):
    def __init__(self, x, y, width, height, life, frames, baseFrameCount, angle):
        super().__init__(x, y, width, height, life, frames, baseFrameCount)
        self.angle = math.radians(angle)  # 将角度转换为弧度
        self.speed = 5  # 子弹速度
        # 计算速度向量
        self.velocity_x = self.speed * math.cos(self.angle)
        self.velocity_y = -self.speed * math.sin(self.angle)  # y轴向下为正，因此取反

    def step(self):
        # 根据速度向量更新子弹位置
        self.x += self.velocity_x
        self.y += self.velocity_y
        # 如果子弹超出屏幕范围，则标记为可删除
        if self.x < 0 or self.x > screen.get_width() or self.y < 0 or self.y > screen.get_height():
            self.canDelete = True


# 加载激光图片
blue_laser_image = pygame.image.load('blue_laser.png')
blue_laser_image = pygame.transform.scale(blue_laser_image, (15, 650))  # 假设你想要的激光宽度为8像素，高度与屏幕相同


# 定义激光类，用于飞机的第二种大招
class Laser(FlyingObject):
    def __init__(self, x, y, width, height, duration, color, frames, baseFrameCount):
        super().__init__(x, y, width, height, 1, frames, baseFrameCount)
        self.end_time = time.time() + duration
        self.color = color
        self.image = pygame.transform.scale(blue_laser_image, (width, height))  # 调整激光图片大小以匹配激光的尺寸

    def paint(self, view):
        if time.time() < self.end_time:
            view.blit(self.image, (self.x, self.y))

    def step(self):
        # 激光不移动，但我们可以在这里处理碰撞
        pass

    def outOfBounds(self):
        return time.time() > self.end_time

    def hit(self, component):
        # 检查激光是否与传入的对象相交（在一条垂直线上）
        return (
                self.x < component.x + component.width
                and self.x + self.width > component.x
                and self.y < component.y + component.height
        )


class BombProp(FlyingObject):
    def __init__(self, x, y, width, height, frames, baseFrameCount):
        super().__init__(x, y, width, height, 1, frames, baseFrameCount)
        self.velocity_y = 2

    def step(self):
        self.y += self.velocity_y

    def outOfBounds(self):
        return self.y > 650


# Boss 图像尺寸
boss_width, boss_height = 200, 150
boss_image = pygame.image.load("boss.png")
boss_image = pygame.transform.scale(boss_image, (boss_width, boss_height))
boss_frames = [boss_image]
boss_crash_frames = [
    pygame.transform.scale(pygame.image.load("images/boss_crash_1.png"), (200, 150)),
    pygame.transform.scale(pygame.image.load("images/boss_crash_2.png"), (200, 150)),
    pygame.transform.scale(pygame.image.load("images/boss_crash_3.png"), (200, 150)),
    pygame.transform.scale(pygame.image.load("images/boss_crash_4.png"), (200, 150)),
    pygame.transform.scale(pygame.image.load("images/boss_crash_5.png"), (200, 150))
]
boss_frames.extend(boss_crash_frames)

boss_x = 480 / 2 - boss_width / 2  # 屏幕中央
boss_y = -boss_height  # 屏幕顶部之上
# 假设 Boss 只有一个静态图像
boss_bullet_image = pygame.image.load("images/bullet1.png")
boss_bullet_image = pygame.transform.scale(boss_bullet_image, (10, 20))
enemy_bullet_frames = [boss_bullet_image]

bomb_width = 100  # 假设炸弹的宽度
bomb_height = 100  # 假设炸弹的高度
bomb_image = pygame.image.load("images/bomb.png")
bomb_image = pygame.transform.scale(bomb_image, (bomb_width, bomb_height))
bomb_frames = [bomb_image]  # 假设炸弹的图像
buff_width = 100  # 假设buff的宽度
buff_height = 100  # 假设buff的高度
buff_image = pygame.image.load("images/buff.png")
buff_image = pygame.transform.scale(buff_image, (bomb_width, bomb_height))
buff_frames = [buff_image]  # 假设buff的图像


def componentEnter():
    if GameVar.boss:
        return
    if GameVar.score >= GameVar.last_boss_score + 300 and \
            GameVar.state != GameVar.STATES["BOSS_WARNING"]:
        GameVar.state = GameVar.STATES["BOSS_WARNING"]
        GameVar.boss_warning_start_time = None  # 重置警告开始时间
        GameVar.last_boss_score = GameVar.score  # 更新 last_boss_score
        return
    # 判断是否到了产生敌飞机的时间
    if not isActionTime(GameVar.lastTime, GameVar.interval):
        return
    GameVar.lastTime = time.time()

    # 生成炸弹掉落物的逻辑
    current_time = time.time()
    if current_time - GameVar.last_bomb_time >= 10:  # 每10秒生成一个炸弹
        bomb_x = random.randint(0, 480 - bomb_width)  # 随机生成炸弹的水平位置
        GameVar.props.append(BombProp(bomb_x, 0, bomb_width, bomb_height, bomb_frames, 1))
        GameVar.last_bomb_time = current_time  # 更新生成炸弹的时间

    if current_time - GameVar.last_buff_time >= 15:  # 每15秒生成一个药水
        bomb_y = random.randint(0, 480 - bomb_width) + 10  # 随机生成药水的水平位置
        GameVar.props_buff.append(BombProp(bomb_y, 0, bomb_width, bomb_height, buff_frames, 1))
        GameVar.last_buff_time = current_time  # 更新生成药水的时间

    # 随机生成坐标
    x = random.randint(0, 480 - 57)
    x1 = random.randint(0, 480 - 50)
    x2 = random.randint(0, 480 - 169)
    # 根据随机整数的值生成不同的敌飞机
    n = random.randint(0, 9)
    if n <= 5:
        # 因为列表初始值为空，所以这里可以使用append或insert进行添加元素，append会将新增的追加到末尾，但insert会将新增的插入到指定位置
        GameVar.enemies.append(Enemy(x, 0, 57, 45, 1, 5 * GameVar.round, e1, 1))
    elif 6 <= n <= 8:
        GameVar.enemies.append(Enemy(x1, 0, 50, 68, 2, 10 * GameVar.round, e2, 1))
    elif n == 9:
        # 将大飞机放在列表中索引为0的位置
        if len(GameVar.enemies) == 0 or GameVar.enemies[0].type != 3:
            GameVar.enemies.insert(0, Enemy(x2, 0, 169, 258, 3, 50 * GameVar.round, e3, 2))


def draw_hero_icon_and_charge():
    # 英雄图标的位置
    icon_pos_x = screen.get_width() - GameVar.hero_icon_size[0] - 20
    icon_pos_y = screen.get_height() - GameVar.hero_icon_size[1] - 20
    hero_icon_rect = pygame.Rect(icon_pos_x, icon_pos_y, *GameVar.hero_icon_size)
    screen.blit(GameVar.hero_icon, hero_icon_rect)  # 绘制英雄图标

    # 圆环的半径应该根据图标大小决定，这里假设我们使用英雄图标宽度的一半作为半径
    radius = GameVar.hero_icon_size[0] // 2
    # 圆环的中心就是图标的中心
    center_x = icon_pos_x + radius // 2
    center_y = icon_pos_y + radius // 2
    # 绘制环形充能标识
    # 由于draw.arc绘制的是一个圆环的一部分，所以我们创建一个正方形的Rect，使得圆环能够完整的绘制在这个正方形内
    charge_rect = pygame.Rect(center_x, center_y, radius * 2, radius * 2)
    start_angle = 90  # 充能从顶部开始顺时针
    end_angle = start_angle + (360 * GameVar.charge_progress)
    pygame.draw.arc(screen, (0, 255, 0), charge_rect, math.radians(start_angle), math.radians(end_angle), 5)


def update_charge():
    if GameVar.charge_progress < GameVar.charge_full:
        GameVar.charge_progress += GameVar.charge_rate
    # 检测充能是否已满，但还未释放大招
    elif GameVar.charge_progress >= GameVar.charge_full and not GameVar.charge_ready:
        GameVar.charge_ready = True  # 标记充能已满


def fire_barrage(hero):
    # 发射扇形弹幕
    num_bullets = 20  # 弹幕中子弹的数量
    spread_angle = 120  # 扇形区域的角度范围
    hero_angle = 90  # 英雄机正上方的角度

    # 以飞机的中心正前方为发射中心点
    center_x = hero.x + hero.width // 2 - 4
    center_y = hero.y

    for i in range(num_bullets):
        # 计算每颗子弹的发射角度
        angle = (hero_angle - spread_angle / 2) + (spread_angle / num_bullets) * i
        # 创建弹幕子弹并将其添加到子弹列表
        bullet = BarrageBullet(center_x, center_y, 9, 21, 1, b, 1, angle)
        GameVar.bullets.append(bullet)


def fire_laser(hero):
    # 计算激光的位置，使其从英雄机中心发射
    laser_x = hero.x + hero.width // 2
    laser_y = 0  # 从屏幕顶部发射
    laser_width = 15  # 激光宽度
    laser_height = hero.y  # 激光长度
    laser_duration = 0.1  # 激光持续时间（秒）
    laser_color = (0, 0, 255)  # 蓝色激光

    # 创建激光对象并添加到子弹列表
    laser = Laser(laser_x, laser_y, laser_width, laser_height, laser_duration, laser_color, b, 1)
    GameVar.bullets.append(laser)

    # 发射激光时暂停发射子弹
    GameVar.hero.shootLastTime = time.time() + laser_duration


# 画组件方法
def paintComponent(view):
    # 判断是否到了飞行物重绘的时间
    if not isActionTime(GameVar.paintLastTime, GameVar.paintInterval):
        return
    GameVar.paintLastTime = time.time()

    # 调用sky对象的paint方法
    GameVar.sky.paint(view)
    # 画敌飞机并实现敌飞机移动
    for enemy in GameVar.enemies:
        enemy.paint(view)

    # 画英雄机
    GameVar.hero.paint(view)
    # 画子弹
    for bullet in GameVar.bullets:
        bullet.paint(view)
    # 写分数和生命值
    renderText("SCORE:" + str(GameVar.score), (0, 0), screen)
    renderText("LIFE:" + str(GameVar.heroes), (350, 0), screen)
    # 写炸弹数量
    renderText("Bomb:" + str(GameVar.bombs), (350, 30), screen)
    # 写轮数
    renderText("round:" + str(GameVar.round), (0, 30), screen)

    for prop in GameVar.props:
        prop.paint(view)

    for prop in GameVar.props_buff:
        prop.paint(view)


# 组件移动方法
def componentStep():
    # 调用sky对象的step方法
    GameVar.sky.step()

    # 移动和更新敌机
    for enemy in GameVar.enemies:
        enemy.step()

    # 子弹移动
    bullets_to_remove = []
    for bullet in GameVar.bullets:
        bullet.step()

        # 如果是激光，检查与敌机的碰撞
        if isinstance(bullet, Laser):
            enemies_to_remove = []
            for enemy in GameVar.enemies:
                if bullet.hit(enemy):
                    enemy.laser_bang()  # 摧毁敌机
                    # enemies_to_remove.append(enemy)

            for boss in GameVar.boss:
                if bullet.hit(boss):
                    boss.laser_bang()  # 摧毁boss
                    # enemies_to_remove.append(enemy)
            # 移除被摧毁的敌机
            # GameVar.enemies = [enemy for enemy in GameVar.enemies if enemy not in enemies_to_remove]

            # 标记激光移除
            bullets_to_remove.append(bullet)

    for prop in GameVar.props:
        prop.step()

    for prop in GameVar.props_buff:
        prop.step()

# 绘制血量条
def draw_health_bar(screen, x, y, current_health, max_health, bar_width, bar_height, color):
    health_ratio = current_health / max_health
    current_bar_width = int(bar_width * health_ratio)
    health_bar_background = pygame.Rect(x, y, bar_width, bar_height)
    health_bar_foreground = pygame.Rect(x, y, current_bar_width, bar_height)
    pygame.draw.rect(screen, (128, 128, 128), health_bar_background)  # 灰色背景
    pygame.draw.rect(screen, color, health_bar_foreground)  # 当前血量


def checkHit():
    # 检测英雄机是否被敌方子弹击中
    for bullet in GameVar.bullets:
        if isinstance(bullet, EnemyBullet) and GameVar.hero.hit(bullet):
            GameVar.hero.bang()  # 英雄机被击中
            bullet.bang()  # 敌方子弹被销毁

    # 检测敌机是否和英雄机相撞
    for enemy in GameVar.enemies:
        if enemy.down:
            continue

        if GameVar.hero.hit(enemy):
            enemy.bang()
            GameVar.hero.bang()

        # 检测英雄机的子弹是否击中敌机
        for bullet in GameVar.bullets:
            if isinstance(bullet, Bullet) and enemy.hit(bullet):
                enemy.bang()
                bullet.bang()

    # 检测英雄机的子弹是否击中 Boss
    for boss in GameVar.boss:
        if boss.down:
            continue

        if GameVar.hero.hit(boss):
            boss.bang()
            GameVar.hero.bang()

        # 检测英雄机的子弹是否击中敌机
        for bullet in GameVar.bullets:
            if isinstance(bullet, Bullet) and boss.hit(bullet):
                boss.bang()
                bullet.bang()

    # 检测英雄机是否与炸弹掉落物碰撞
    for prop in GameVar.props:
        if isinstance(prop, BombProp) and GameVar.hero.hit(prop):
            # 增加英雄机的炸弹数量
            GameVar.hero.get_bomb()
            # 标记炸弹掉落物为可删除
            prop.canDelete = True
            prop.bang()  # 炸弹被获取后消失

    for prop in GameVar.props_buff:
        if isinstance(prop, BombProp) and GameVar.hero.hit(prop):
            GameVar.hero.state = 2
            GameVar.hero.state_change_time = time.time()  # 记录状态改变的时间
            # 标记炸弹掉落物为可删除
            prop.canDelete = True
            prop.bang()  # 炸弹被获取后消失

# 删除无效组件
def deleteComponent():
    # 检查 Boss 是否被击毁
    GameVar.boss = [boss for boss in GameVar.boss if not (boss.canDelete or boss.outOfBounds())]

    # 删除越界或被击毁的敌机
    GameVar.enemies = [enemy for enemy in GameVar.enemies if not (enemy.canDelete or enemy.outOfBounds())]

    # 删除越界或被击毁的子弹
    GameVar.bullets = [bullet for bullet in GameVar.bullets if not (bullet.canDelete or bullet.outOfBounds())]
    # 删除越界或已被收集的炸弹掉落物
    GameVar.props = [prop for prop in GameVar.props if not (prop.canDelete or prop.outOfBounds())]

    # 删除越界或已被收集的炸弹掉落物
    GameVar.props_buff = [prop for prop in GameVar.props_buff if not (prop.canDelete or prop.outOfBounds())]

    # 检查英雄机是否被击毁
    if GameVar.hero.canDelete:
        hero_x, hero_y = GameVar.hero.x, GameVar.hero.y
        GameVar.heroes -= 1  # 减少一个生命
        hero_hit_sound.play()
        if GameVar.heroes == 0:
            write_score(GameVar.score)
            GameVar.state = GameVar.STATES["GAME_OVER"]
        else:
            GameVar.hero = Hero(hero_x, hero_y, 60, 75, 1, 1, h, 1)  # 重置英雄机


# 组件的动画
def componentAnimation():
    # 敌飞机播放动画
    for enemy in GameVar.enemies:
        enemy.animation()
    # boss播放动画
    for boss in GameVar.boss:
        boss.animation()
    # 子弹播放动画
    for bullet in GameVar.bullets:
        bullet.animation()
    # 英雄机播放动画
    GameVar.hero.animation()


# 加载图片
barrage_image = pygame.image.load('barrage.png')
laser_image = pygame.image.load('laser.png')
barrage_image = pygame.transform.scale(barrage_image, (200, 300))
laser_image = pygame.transform.scale(laser_image, (200, 300))


def show_ability_selection_screen():
    running = True
    screen_width, screen_height = screen.get_size()  # 获取屏幕尺寸
    barrage_rect = barrage_image.get_rect()
    laser_rect = laser_image.get_rect()

    # 将图片并排居中
    total_width = barrage_rect.width + laser_rect.width
    spacing = 20  # 两张图片之间的间隔
    barrage_rect.topleft = ((screen_width - total_width) // 2, (screen_height - barrage_rect.height) // 2)
    laser_rect.topleft = (barrage_rect.topright[0] + spacing, barrage_rect.topright[1])

    # 设置字体
    font = pygame.font.Font('STLITI.TTF', 36)  # 可以替换为你喜欢的字体和大小

    # 创建文本
    title_text = font.render('请选择你的大招吧！', True, (255, 255, 255))  # 白色
    barrage_label = font.render('弹幕', True, (255, 255, 255))
    laser_label = font.render('激光', True, (255, 255, 255))

    # 计算文本位置
    title_rect = title_text.get_rect(center=(screen_width // 2 + 10, 100))
    barrage_label_rect = barrage_label.get_rect(center=(barrage_rect.centerx, barrage_rect.bottom + 20))
    laser_label_rect = laser_label.get_rect(center=(laser_rect.centerx, laser_rect.bottom + 20))

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if barrage_rect.collidepoint(mouse_pos):
                    GameVar.selected_ability = 'barrage'
                    running = False
                elif laser_rect.collidepoint(mouse_pos):
                    GameVar.selected_ability = 'laser'
                    running = False

        GameVar.sky.paint(screen)
        GameVar.sky.step()

        # 显示图片
        screen.blit(barrage_image, barrage_rect)
        screen.blit(laser_image, laser_rect)
        # 显示文本
        screen.blit(title_text, title_rect)
        screen.blit(barrage_label, barrage_label_rect)
        screen.blit(laser_label, laser_label_rect)

        # 绘制选择框
        if barrage_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 0, 0), barrage_rect, 3)  # 红色框
        else:
            pygame.draw.rect(screen, (128, 128, 128), barrage_rect, 3)  # 灰色框

        if laser_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 0, 0), laser_rect, 3)  # 红色框
        else:
            pygame.draw.rect(screen, (128, 128, 128), laser_rect, 3)  # 灰色框

        pygame.display.flip()
        pygame.time.wait(10)

        if not running:
            GameVar.state = GameVar.STATES["COUNTDOWN"]


def show_boss_warning(screen):
    font = pygame.font.Font('STLITI.TTF', 48)
    warning_text = font.render("前方高能", True, (255, 0, 0))
    warning_sound = pygame.mixer.Sound("music/warning.mp3")
    warning_sound.play(1)  # 在一个声道上播放第一个音效
    text_rect = warning_text.get_rect(center=(screen.get_width() / 2, 50))
    screen.blit(warning_text, text_rect)


# 使用类属性存储游戏中的变量，以减少全局变量的数量
class GameVar(object):
    sky = None
    # 英雄机对象
    hero = None
    enemies = []
    boss = []  # 初始时没有Boss
    last_boss_score = 0
    # 存放子弹的列表
    bullets = []
    # 存放道具的列表
    props = []
    bombs = 0
    round = 1 # 击败boss数量作为轮数
    props_buff = []
    last_bomb_time = 0  # 上次生成炸弹的时间
    last_buff_time = 0  # 上次生成药水的时间
    charge_progress = 0
    charge_rate = 0.01  # 充能速率，每帧增加的量
    charge_full = 1  # 充能满值
    hero_icon = h[0]  # 假设h[0]是hero图标的图片
    hero_icon_size = (40, 40)  # 英雄图标大小
    charge_ready = False  # 充能完成标志
    # 玩家选择的能力
    selected_ability = None
    # 产生敌飞机的时间间隔
    lastTime = 0
    interval = 0.5  # 单位为秒
    # 重绘飞行物的时间间隔
    paintLastTime = 0
    paintInterval = 0.04
    # 分数和生命值
    score = 0
    heroes = 3
    # 控制游戏状态
    STATES = {"START": 1, "SELECTION": 2, "COUNTDOWN": 3, "RUNNING": 4, "PAUSE": 5, "GAME_OVER": 6, "SORTING": 7, "BOSS_WARNING": 8}
    state = STATES["START"]
    countdown_start = None  # 倒计时开始的时间
    boss_warning_start_time = None
    boss_warning_duration = 3  # 预留3秒钟的警告时间
    boss_warning_flash_duration = 0.5  # 文字闪烁的间隔时间


# 创建sky对象
GameVar.sky = Sky()
# 创建英雄机对象
GameVar.hero = Hero(0, 0, 60, 75, 1, 1, h, 1)


# 显示开始界面
def show_start_screen():
    GameVar.sky.paint(screen)
    GameVar.sky.step()
    screen.blit(logo, (30, 100))
    screen.blit(startgame, (150, 400))


def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)


def stop_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.stop()


# 假设这些是你的音乐文件路径
start_music = 'music/start_music.mp3'
selection_music = 'music/selection_music.mp3'
countdown_music = 'music/ready.mp3'
running_music = 'music/running_music.mp3'
pause_music = 'music/pause_music.mp3'
game_over_music = 'music/game_over_music.mp3'
boss_warning_music = 'music/boss_warning_music.mp3'
countdown_images = {
    3: pygame.image.load('images/3.png'),
    2: pygame.image.load('images/2.png'),
    1: pygame.image.load('images/1.png')
}


# 游戏状态控制
def controlState():
    global current_music  # 用于跟踪当前播放的音乐
    if GameVar.state == GameVar.STATES["START"]:
        if current_music != 'start':
            play_music(start_music)
            current_music = 'start'
        show_start_screen()
    elif GameVar.state == GameVar.STATES["SELECTION"]:
        if current_music != 'select':
            play_music(selection_music)
            current_music = 'select'
        show_ability_selection_screen()  # 玩家选择能力
    elif GameVar.state == GameVar.STATES["COUNTDOWN"]:
        paintComponent(screen)
        screen_width, screen_height = screen.get_size()
        current_time = time.time()
        if current_music != 'count':
            play_music(countdown_music)
            current_music = 'count'

        # 开始倒计时
        if GameVar.countdown_start is None:
            GameVar.countdown_start = current_time

        elapsed_time = current_time - GameVar.countdown_start
        countdown_number = 3 - int(elapsed_time * 1.5)  # 计算倒计时的数字

        if countdown_number <= 0:
            GameVar.state = GameVar.STATES["RUNNING"]  # 切换到RUNNING状态
        else:
            screen.blit(countdown_images[countdown_number], (screen_width / 2 - 150, screen_height / 2 - 100))  # 显示倒计时图片


    elif GameVar.state == GameVar.STATES["RUNNING"]:
        if current_music != 'running':
            play_music(running_music)
            current_music = 'running'
        componentEnter()
        # 画组件
        paintComponent(screen)
        # 组件移动
        componentStep()
        # 播放组件动画
        componentAnimation()
        # 英雄机发射子弹
        GameVar.hero.shoot()
        # 更新充能
        update_charge()
        # 绘制英雄图标和充能标识
        draw_hero_icon_and_charge()
        # 碰撞检测
        checkHit()
        # 删除无效组件
        deleteComponent()

        if GameVar.boss:
            isdead = 0
            for boss in GameVar.boss:
                boss.step()
                boss.paint(screen)

        # 检查英雄机状态持续时间
        if GameVar.hero.state == 2 and GameVar.hero.state_change_time is not None:
            if time.time() - GameVar.hero.state_change_time > 5:  # 检查是否已过5秒
                GameVar.hero.state = 1  # 将状态改回1
                GameVar.hero.state_change_time = None  # 重置状态改变时间

    elif GameVar.state == GameVar.STATES["PAUSE"]:
        paintComponent(screen)
        GameVar.sky.step()
        screen.blit(pause, (0, 0))
    elif GameVar.state == GameVar.STATES["GAME_OVER"]:
        paintComponent(screen)
        GameVar.sky.step()
        # renderText("游戏结束", (160, 320), screen, (0, 0, 0))
        # 加载图片
        gameover_image = pygame.image.load("images/gameover1.png")

        # 假设您希望图片尺寸与原先文字的尺寸相似
        gameover_image = pygame.transform.scale(gameover_image, (360, 120))

        # 渲染图片到屏幕上
        screen.blit(gameover_image, (60, 100))
        stop_music(running_music)
        # 设置重新开始图标的位置
        restart_button_position = (200, 400)
        screen.blit(restart_icon, restart_button_position)
        sorting_button_position = (125, 500)
        screen.blit(sorting_icon, sorting_button_position)

    elif GameVar.state == GameVar.STATES["SORTING"]:
        show_sorting_screen()

    if GameVar.state == GameVar.STATES["BOSS_WARNING"]:
        componentEnter()
        # 画组件
        paintComponent(screen)
        # 组件移动
        componentStep()
        # 播放组件动画
        componentAnimation()
        # 英雄机发射子弹
        GameVar.hero.shoot()
        # 更新充能
        update_charge()
        # 绘制英雄图标和充能标识
        draw_hero_icon_and_charge()
        # 碰撞检测
        checkHit()
        # 删除无效组件
        deleteComponent()
        # 闪烁警告文字的逻辑
        current_time = time.time()
        if GameVar.boss_warning_start_time is None:
            GameVar.boss_warning_start_time = current_time

        elapsed_time = current_time - GameVar.boss_warning_start_time
        if elapsed_time > GameVar.boss_warning_duration:
            # 警告结束，Boss出现
            GameVar.state = GameVar.STATES["RUNNING"]
            GameVar.boss.append(Boss(boss_x, boss_y, boss_width, boss_height, boss_frames, 1))
        elif int(elapsed_time / GameVar.boss_warning_flash_duration) % 2 == 0:
            show_boss_warning(screen)


def show_sorting_screen():
    GameVar.sky = Sky()
    GameVar.sky.paint(screen)
    GameVar.sky.step()

    # 绘制排行榜
    draw_ranking("score-records.txt")

    back_button_pos = (150, 550)
    # 绘制按钮 
    screen.blit(back_button, back_button_pos)
    # 更新显示
    pygame.display.update()

    running = True
    pos = None
    while running:
        # 获取鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
            if pos:
                if back_button_pos[0] < pos[0] < back_button_pos[0] + 200:
                    # 设置状态回到主菜单
                    restart_game()
                    running = False


def draw_ranking(filename):
    with open(filename) as f:
        scores = [int(line) for line in f.read().splitlines()]

    scores.sort(reverse=True)
    rankings = scores[:10]

    row_font = pygame.font.Font(None, 30)

    # 加载并设置标题图片
    title_image = pygame.image.load('ranking.png')
    title_image = pygame.transform.scale(title_image, (150, 150))
    title_rect = title_image.get_rect()
    title_rect.centerx = screen.get_rect().centerx
    title_rect.top = 20
    screen.blit(title_image, title_rect)
    # # 绘制标题
    # title = row_font.render("Ranking Board - TOP 10", True, (0, 0, 255))
    # title_rect = title.get_rect()
    # title_rect.centerx = screen.get_rect().centerx
    # title_rect.top = 20
    # screen.blit(title, title_rect)
    medal_images = [gold_image, silver_image, bronze_image] 
    for i, score in enumerate(rankings):
        # 设置颜色
        color = (255, 255 - i * 10, 255 - i * 10)

        # 绘制名次
        text = row_font.render(f"{i + 1}.", True, (0, 0, 0))
        text_rect = text.get_rect()

        # 绘制分数
        score_text = row_font.render(f"{score}", True, color)
        score_rect = score_text.get_rect()

        # 设置位置
        text_rect.centerx = screen.get_rect().centerx - 50
        score_rect.centerx = screen.get_rect().centerx + 50
        text_rect.top = score_rect.top = 50 + i * 30 + 50 + 100

        # 绘制文本
        screen.blit(text, text_rect)
        screen.blit(score_text, score_rect)
        
        # 绘制奖牌图片（在排名为1，2，3时）
        if i < 3:  # 只在排名为1，2，3时绘制奖牌图片
            medal_rect = medal_images[i].get_rect()
            medal_rect.centerx = screen.get_rect().centerx - 48  # 调整奖牌图片的X坐标
            medal_rect.top = 39 + i * 30 + 50 + 100  # 调整奖牌图片的Y坐标
            screen.blit(medal_images[i], medal_rect)
    pygame.display.flip()


def write_score(score):
    # 打开文件并写入score
    with open('score-records.txt', 'a') as f:
        f.write(str(score) + '\n')


pygame.mixer.init()
current_music = None  # 追踪当前播放的音乐

explosion_sound = pygame.mixer.Sound('music/explosion1.mp3')
explosion_sound.set_volume(0.5)  # 设置音量为50%
boss_explosion_sound = pygame.mixer.Sound('music/explosion2.mp3')
boss_explosion_sound.set_volume(0.5)  # 设置音量为50%
hero_hit_sound = pygame.mixer.Sound('music/hero_hit.mp3')
hero_hit_sound.set_volume(0.5)  # 设置音量为50%
# music = pygame.mixer.Sound('music/background2.mp3')
# music.play(-1)

while True:
    # 游戏状态控制
    controlState()
    # 更新屏幕内容
    pygame.display.update()
    # 监听有没有按下退出按钮
    handleEvent()
    # 等待0.01秒后再进行下一次循环
    time.sleep(0.01)
