#***********************AVISOS***********************
# Retire o cursor da tela quando o jogo começar para evitar erros
# a opção 'score' no menu somente abre depois de jogar 1 vez
# A pontuação somente vai salvar no banco se após jogar o usuário entrar na opção 'score' do menu
# Os itens listados são alguns erros que surgiram e ainda estão presentes no projeto devido ao pouco tempo que foi disponibilizado para a realização do mesmo.

import pygame,sys
import os
from pygame.locals import *
from tkinter import *
from tkinter import messagebox
import mysql.connector
import random
from random import randint
#from pygame import key


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption("SA Project")

janela_x = 900
janela_y = 640
MONITOR = [pygame.display.Info().current_w, pygame.display.Info().current_h]
janela = pygame.display.set_mode((janela_x, janela_y))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 50, 200)
green = (0, 255, 0)
red = (255, 0, 0)

fundomenu = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Imagens', 'FundoMenu.png')),(900, 640))
fundo = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Imagens', 'bg.png')),(900, 640))
gameover = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Imagens', 'Gameover.jpg')),(900, 640))

music = pygame.mixer.Sound(os.path.join('Assets', 'Sons', 'Music.mp3'))
gameover = pygame.mixer.Sound(os.path.join('Assets', 'Sons', 'GameOver.ogg'))
pygame.mixer.Sound.set_volume(music, 0.2)
pygame.mixer.Sound.set_volume(gameover, 0.3)

font = pygame.font.Font('EightBit.ttf', 40)
clock = pygame.time.Clock()
click = False

global tempo_f
tempo_f = 0

#===================
def draw_texto(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
#===================
def menu():
    con = mysql.connector.connect(host='localhost', database='sa', user='root', password='')
    cursor = con.cursor()
    # funções
    def limitar_tamanho(p):
        if len(p) > 12:
            return False
        return True

    def login():
        global pega_id
        usuario_log = str(usuario_login.get())
        senha_login = str(senha_log.get())
        validar = False

        if not (senha_login == '' or usuario_log == ''):
            cursor.execute('SELECT * FROM jogadores')
            for i in cursor:
                if usuario_log.lower() in i and senha_login in i:
                    print("sucesso")
                    pega_id = i[0]
                    validar = True
                    master.destroy()
                    main()
            if validar == False:
                messagebox.showwarning('Erro de Login', 'Usuario ou senha incorretos')
        else:
            messagebox.showwarning('Erro de Login','Caixa em branco, por gentileza preencha todos os dados para prosseguir.')

    def registrar():
        usuario_info = str(usuario_cad.get())
        senha_info1 = str(senha_cad.get())
        senha_info2 = str(senha_cad2.get())

        if senha_info1 == senha_info2 and not (senha_info1 == '' or senha_info2 == '' or usuario_info == ''):
            cursor.execute('INSERT INTO jogadores (usuario,senha) VALUES(%s,%s)', (usuario_info.lower(), senha_info1))
            con.commit()
            messagebox.showinfo('Cadastro concluído', 'Cadastro concluído com sucesso')

            ent_usuario1.delete(0, END)
            ent_senha1.delete(0, END)
            ent_senha2.delete(0, END)
            master1.destroy()

        else:
            messagebox.showerror('Erro de Cadastro', 'Verifique os dados informados e tente novamente')
            ent_usuario1.delete(0, END)
            ent_senha1.delete(0, END)
            ent_senha2.delete(0, END)

    def deletar():
        usuario_del = str(usuario_excluir.get())
        senha_del = str(senha_Del.get())
        validar = False

        if not (usuario_del == '' or senha_del == ''):
            cursor.execute('SELECT * FROM jogadores')
            for i in cursor:
                if usuario_del.lower() in i and senha_del in i:
                    validar = True
                    id_del = int(i[0])
            if validar == True:
                cursor.execute("DELETE FROM jogadores WHERE id = '%s'", (id_del,))
                con.commit()
                messagebox.showinfo('Sucesso', 'Conta deletada com sucesso')
                master2.destroy()
            else:
                messagebox.showwarning('Erro', 'Usuario ou senha incorretos')
        else:
            messagebox.showwarning('Erro de Login','Caixa em branco, por gentileza preencha todos os dados para prosseguir.')

        ent_usuario2.delete(0, END)
        ent_senha3.delete(0, END)

    # telas

    def excluirConta():
        global master2
        master2 = Toplevel()
        master2.title('Deletar conta')
        master2.geometry('490x560+610+153')
        master2.resizable(width=False, height=False)
        img3 = PhotoImage(file='Imagens\\excluir.png')
        fundo3 = Label(master2, image=img3)
        fundo3.pack()

        # caixas de entrada
        global usuario_excluir, ent_usuario2, ent_senha3

        limitador = master2.register(func=limitar_tamanho)

        usuario_excluir = StringVar()
        ent_usuario2 = Entry(master2, validate='key', validatecommand=(limitador, '%P'), textvariable=usuario_excluir,bd=2, font=('Calibri', 15), justify=CENTER)
        ent_usuario2.place(width=392, height=45, x=49, y=150)

        ent_senha3 = Entry(master2, validate='key', validatecommand=(limitador, '%P'), textvariable=senha_Del, show='*',bd=2, font=('Calibri', 15), justify=CENTER)
        ent_senha3.place(width=392, height=45, x=49, y=256)

        # botão

        excluir = Button(master2, text='Excluir', bd=2, font=('Calibri', 15), justify=CENTER, command=deletar)
        excluir.place(width=141, height=47, x=175, y=361)

        master2.mainloop()

    def tela_cadastro():
        global master1
        master1 = Toplevel()
        master1.title('Tela de cadastro')
        master1.geometry('490x560+610+153')
        master1.resizable(width=False, height=False)
        img2 = PhotoImage(file='Imagens\\cadastro.png')
        fundo2 = Label(master1, image=img2)
        fundo2.pack()

        # caixas de entrada

        global usuario_cad, ent_usuario1, ent_senha1, ent_senha2

        limitador = master1.register(func=limitar_tamanho)

        usuario_cad = StringVar()
        ent_usuario1 = Entry(master1, validate='key', validatecommand=(limitador, '%P'), textvariable=usuario_cad, bd=2,font=('Calibri', 15), justify=CENTER)
        ent_usuario1.place(width=392, height=45, x=49, y=112)

        ent_senha1 = Entry(master1, validate='key', validatecommand=(limitador, '%P'), textvariable=senha_cad, show='*',bd=2, font=('Calibri', 15), justify=CENTER)
        ent_senha1.place(width=392, height=45, x=49, y=212)

        ent_senha2 = Entry(master1, validate='key', validatecommand=(limitador, '%P'), textvariable=senha_cad2,show='*', bd=2, font=('Calibri', 15), justify=CENTER)
        ent_senha2.place(width=392, height=45, x=49, y=315)

        # botão

        cadastrar = Button(master1, text='Cadastrar', bd=2, font=('Calibri', 15), justify=CENTER, command=registrar)
        cadastrar.place(width=141, height=47, x=175, y=405)

        master1.mainloop()

    def tela_principal():
        global master, img1
        master = Tk()
        master.title("Login")
        master.geometry('490x560+610+153')
        master.resizable(width=False, height=False)
        img1 = PhotoImage(file="Imagens\\fundo.png")
        fundo = Label(master, image=img1)
        fundo.pack()

        # senhas das 3 telas

        global senha_log, senha_cad, senha_cad2, senha_Del

        senha_log = StringVar()
        senha_cad = StringVar()
        senha_cad2 = StringVar()
        senha_Del = StringVar()

        # caixas de entrada

        limitador = master.register(func=limitar_tamanho)

        global usuario_login
        usuario_login = StringVar()
        ent_usuario = Entry(master, validate='key', validatecommand=(limitador, '%P'), textvariable=usuario_login, bd=2,font=('Calibri', 15), justify=CENTER)
        ent_usuario.place(width=392, height=45, x=49, y=128)

        ent_senha = Entry(master, validate='key', validatecommand=(limitador, '%P'), textvariable=senha_log, show='*', bd=2, font=('Calibri', 15), justify=CENTER)
        ent_senha.place(width=392, height=45, x=49, y=258)

        # botões

        entrar = Button(master, text='Entrar', bd=2, font=('Calibri', 15), justify=CENTER, command=login)
        entrar.place(width=141, height=47, x=66, y=362)

        entra_cadastro = Button(master, text='Cadastrar-se', bd=2, font=('Calibri', 15), justify=CENTER,command=tela_cadastro)
        entra_cadastro.place(width=141, height=47, x=278, y=362)

        entra_excluir = Button(master, text='Excluir Conta', bd=2, font=('Calibri', 15), justify=CENTER,command=excluirConta)
        entra_excluir.place(width=141, height=47, x=175, y=450)

        master.mainloop()

    tela_principal()
    cursor.close()
    con.close()

#===================
def main():
    menu = pygame.mixer.Sound(os.path.join('Assets', 'Sons', 'Menu.ogg'))
    pygame.mixer.Sound.set_volume(menu, 0.05)
    run = True
    while run:
        pygame.mixer.Sound.play(menu, -1)
        pygame.display.update()
        clock.tick(120)
        janela.blit(fundomenu, (0,0))

        draw_texto('S.A Project', font, (WHITE), janela, 350, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(400, 200, 105, 35)
        button_3 = pygame.Rect(400, 250, 105, 35)
        button_2 = pygame.Rect(400, 300, 105, 35)

        if button_1.collidepoint((mx, my)):
            if click:
                pygame.mixer.stop()
                pygame.mixer.Sound.play(music, -1)
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        if button_3.collidepoint((mx, my)):
            if click:
                score()

        pygame.draw.rect(janela, (BLACK), button_1)
        pygame.draw.rect(janela, (BLACK), button_2)
        draw_texto('Play', font, (WHITE), janela, 400, 200)
        draw_texto('Score', font, (WHITE), janela, 400, 250)
        draw_texto('Exit', font, (WHITE), janela, 400, 300)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
    pygame.quit()
#===================
def game():
    # definindo as cores
    green = (0, 255, 0)
    red = (255, 0, 0)
    texto = font.render("Score: ", True, (255, 255, 255), (0, 0, 0))
    pos_texto = texto.get_rect()
    pos_texto.center = (65, 50)
    timer = 0
    tempo_s = 0

    def draw_fundo():
        janela.blit(fundo, (0, 0))

    # classe da nave
    class Nave(pygame.sprite.Sprite):
        def __init__(self, x, y, life):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Imagens', 'Ship.png')), (55, 55))
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            self.life_start = life
            self.life_remaining = life
            self.last_shot = pygame.time.get_ticks()

        def update(self):
            vel = 30
            # definindo o cooldown dos tiros (CD)
            CD = 700  # millisegundos

            # Movimentação da nave e suas limitações de espaço.
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.rect.x > 10:
                self.rect.x -= vel
            if key[pygame.K_RIGHT] and self.rect.x <= 840:
                self.rect.x += vel
            if key[pygame.K_UP] and self.rect.y >= 400:
                self.rect.y -= vel
            if key[pygame.K_DOWN] and self.rect.y <= 540:
                self.rect.y += vel
            # pausar e despausar a música
            if key[pygame.K_m]:
                pygame.mixer.pause()
            if key[pygame.K_n]:
                pygame.mixer.unpause()

            # Funcionará para limitar o "Fire rate" dos tiros
            time_now = pygame.time.get_ticks()

            # tiro
            if key[pygame.K_SPACE] and time_now - self.last_shot > CD:
                bullet = Bullets(self.rect.centerx, self.rect.top)
                bullet_group.add(bullet)
                self.last_shot = time_now

            # desenhando a barrinha de vida
            pygame.draw.rect(janela, red, (self.rect.x, (self.rect.bottom + 10), 55, 7))
            if self.life_remaining > 0:
                pygame.draw.rect(janela, green, (
                    self.rect.x, (self.rect.bottom + 10), int(55 * (self.life_remaining / self.life_start)), 7))

            # sistema de colisão para perder vida
            if pygame.sprite.spritecollide(nave, enemies, True):
                self.life_remaining -= 1
                if self.life_remaining < 1:
                    nave.kill()
                    pygame.mixer.stop()
                    main()

    # classe do tiro da nave
    class Bullets(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(
                pygame.image.load(os.path.join('Assets', 'Imagens', 'bullet2.png')),
                (10, 30))
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

        def update(self):
            # velocidade que o tiro é disparado
            self.rect.y -= 30
            # limita os disparos na tela
            if self.rect.bottom < 80:
                self.kill()
            # Colisão da bala com os inimigos
            if pygame.sprite.spritecollide(self, enemies, True):
                self.kill()

    # classe dos inimigos
    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super(Enemy, self).__init__()
            self.surf = pygame.transform.scale(
                pygame.image.load(os.path.join('Assets', 'Imagens', "Enemy" + str(random.randint(1, 3)) + ".png")), (75, 75))
            # A posicao inicial e gerada aleatoriamente, assim como a velocidade
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(0, 840),
                    random.randint(-500, -200),
                )
            )
            self.speed = random.randint(5, 20)

        def update(self):
            self.rect.y += self.speed
            if self.rect.y >= 640:
                nave.life_remaining -= 1
                self.kill()
                if nave.life_remaining < 1:
                    tempo_f = tempo_s
                    nave.kill()
                    pygame.mixer.stop()
                    main()

    #def mostrar_pontos(x, y):
        #pontuacao = font.render('Pontos: ' +str(t), False, 'WHITE')
        #janela.blit(pontuacao, (0, 0))
#====================================================

    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 1500)

    # criando grupo sprite
    nave_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()

    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    # criando o player
    nave = Nave(int(janela_x - 450), janela_y - 50, 3)
    nave_group.add(nave)

    janela_aberta = True
    while janela_aberta:
        # limtia o fps
        clock.tick(120)

        pygame.time.delay(50)
        draw_fundo()
        #mostrar_pontos(10, 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                janela_aberta = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.mixer.stop()
                    main()
                    janela_aberta = False
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

        # updatando a nave
        nave.update()

        # updatando os sprites groups
        bullet_group.update()
        # aliens_group.update()
        enemies.update()

        for entity in all_sprites:
            janela.blit(entity.surf, entity.rect)

        # desenhando o sprite group
        nave_group.draw(janela)
        bullet_group.draw(janela)
        # aliens_group.draw(janela)

        janela.blit(texto, pos_texto)


        if (timer < 20):
            timer += 1
        else:
            tempo_s += 1
            texto = font.render("Score: " + str(tempo_s), True, (255, 255, 255))
            timer = 0

        global mp
        mp = 0

        if tempo_s > mp:
            mp = tempo_s


        pygame.display.update()

    pygame.quit()
#===================

#salve somente quando clicar em 'score' no menu principal após a gameplay
def update_score():
    con = mysql.connector.connect(host='localhost', database='sa', user='root', password='')
    cursor = con.cursor()
    global pont
    cursor.execute('UPDATE jogadores SET pontuacao=0 WHERE pontuacao IS NULL')
    cursor.execute("SELECT * FROM jogadores")
    id=pega_id
    pontuacao=mp
    for i in cursor:
        if i[0]==id:
            pont = int(i[-1])
    if pontuacao > pont:
        cursor.execute("UPDATE jogadores SET pontuacao='%s' WHERE id = '%s'",(pontuacao,id))
        con.commit()
    cursor.close()
    con.close()
def score():
    run3 = True
    while run3:
        update_score()
        pygame.display.update()
        clock.tick(120)
        janela.blit(fundomenu, (0, 0))

        draw_texto('Maior Pontuacao', font, (WHITE), janela, 350, 100)

        pontuacao = font.render('Pontos: ' +str(pont), False, 'WHITE')
        janela.blit(pontuacao, (300, 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run3 = False

if __name__ == "__main__":
    menu()

