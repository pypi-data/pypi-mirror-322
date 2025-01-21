import pygame, sys
from typehandler import *

pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption('example')
clock = pygame.time.Clock()
font = pygame.font.SysFont('MS Gothic', 32)

words = {'りんご食べたい':'りんごたべたい',
         'for i in range(0, 10):':'for i in range(0, 10):',
         '1+1=2':'1+1=2',
         'print("AはBと言った")':'print("AはBといった")',
         'I want to eat salmon.':'I want to eat salmon.'}

def main():
    process = Process(words)
    while True:
        process.update_show_roman()    #これ必須
        screen.fill((255, 255, 255))
        text_roman = font.render(process.show_roman, True, (192, 192, 192))    #入力例
        text_input = font.render(process.input, True, (0, 0, 0))               #現在の入力
        text_sentence = font.render(process.sentence, True, (0, 0, 0))         #お題の文章
        text_next = font.render('next=>'+process.next, True, (192, 192, 192))  #次の文章
        pygame.draw.line(screen, (0, 128, 255), (0, 50), (600, 50), 5)         #青い線を描画
        pygame.draw.line(screen, (255, 128, 0), (0, 150), (600, 150), 5)       #オレンジの線を描画
        screen.blit(text_roman, (30,60))
        screen.blit(text_input, (30,60))
        screen.blit(text_sentence, (30, 100))
        screen.blit(text_next, (180, 150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                key_name = event.unicode                  #これを使えばシフト入力も対応できるから楽
                if not process.check_ignore(key_name):    #シフトとかファンクションキーとかは正誤判定しない
                    process.main(key_name)                #この一文で正誤判定から文章の切り替えまで全部やってくれる！
        pygame.display.update()
        clock.tick(50)    #fpsは50くらいがおすすめ

if __name__ == '__main__':
    main()