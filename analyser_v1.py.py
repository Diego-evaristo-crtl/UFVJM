from PIL import Image
from glob import glob
from collections import Counter
from colorsys import rgb_to_hls
from time import time, sleep
import os
import shutil
from re import split as REsplit
from sys import exit

print(os.getcwd())
class Handler():
    def __init__(self):
        self.counter = Counter()
        
    def SearchImg(self, path : str):
        returning = []    
        
        images = glob(path) # consegue todos os arquivos correspondentes ao path
        for img in images:
            if not os.path.isfile(img):
                images.remove(img)
        if not images: 
            return [None] # retorna None se não ouver nenhum arquivo correspondente
        
        for img_path in images: 
            img = Image.open(img_path)
            # itera entre os paths e cria os respectivos arquivos
             
            imgMap = Image.new('RGB', img.size)
            # cria o mapa da imagem
            
            self.counter = Counter(red=0, green=0)
            suspicious = False
            percentages = {}
            # cria os value holders  
             
            def getImgPixelValue(pixel): # analisa os pixeis para definir se são 'green', 'red', ou 'others'
                
                if pixel[1] > pixel[0]-10 and pixel[1] > pixel[2]-10: # True = green
                    self.counter['green'] += 1
                    return (0,255,0)
                elif pixel[0] > pixel[1] and pixel[0] > pixel[2]: # True = gree|red
                    try: # tenta transformar os valores RGB para HSL para analise mais profunda
                        hsl_pixel = rgb_to_hls(pixel[0], pixel[1], pixel[2])
                        if pixel[2] < 150 and (hsl_pixel[1] < 55 or hsl_pixel[2] > 115): # True = green
                            self.counter['green'] +=1
                            return (0,255,0)
                        elif hsl_pixel[0] > 180 and hsl_pixel[1] < 110:
                            self.counter['red'] += 1
                            return (255,0,0)
                        else: # red
                            self.counter['red'] += 1
                            return (255,0,0)
                    except: # caso não consiga, assume que seja red
                        self.counter['red'] += 1
                        return (255,0,0)
                else: # others
                    return (100,100,255)
            
            # itera entre as cordenadas x e y da imagem
            for x in range(img.size[0]):
                for y in range(img.size[1]):
                                        
                    # adiciona o pixel modificado ao mapa da imagem 'counter' já atualizado em 'getImgPixelValue'
                    imgMap.putpixel(xy=(x,y), value=getImgPixelValue(img.getpixel((x,y)))) 
            
            # cria as porcentagens com base nos valores de 'counter'
            for key, value in self.counter.items():
                percentages[key] = (value/self.counter.total()) * 100
            
            # analisa as porcentagens para encontrar padrões suspeitos/desvios de media na imagem
            if 65 > percentages['green'] or percentages['green'] > 97:
                suspicious = True
            elif 5 > percentages['red'] or percentages['red'] > 26:
                suspicious = True

            # retorna uma tuple com o counter dos pixels, as porcentagens, e outra touple com o mapa de imagem e imagem         
            returning.append((percentages, suspicious, img, imgMap))
            print(f"        {os.path.basename(img_path)} scaneado")
        return returning


#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################

def Default():
                # consegue o path para criar a pasta default
                installDefaultPath = input("aonde deseja instalar a pasta default?\n : ").strip()
                nomeDaPasta = input("deseja utilizar um nome especifico da pasta? (blank para default)\n : ").strip()
                
                # faz a verificação dos valores passados
                if nomeDaPasta == '':
                    nomeDaPasta = 'PASTA_DEFAULT'
                # cria a pasta default e configura a sua config
                print("    configurando...")
                sleep(0.5)
                # faz a instalação da pasta
                os.mkdir(os.path.join(installDefaultPath, nomeDaPasta))
                # configura as config's
                with open(DEFAULT_PATH_CONFIG_ABSOLUTE_PATH, 'w') as default_path_config:
                    default_path_config.write(os.path.join(installDefaultPath, nomeDaPasta))
                print("    configurado com sucesso")

################################################################################################################################################

handler = Handler()

HELP_MESSAGE = ('\n=============' + '\nforma de uso:\n' + '=============\n\n' +
                '> --default: reseta todo o programa, incluindo suas configurações, pastas default, etc. USE COM PREUCAUÇÃO\n'
                '> -a ou --ajuda : mostra esta mensagem\n' +
                '> -sd ou --scanear-default : scaneia todos arquivos da pasta padrão\n' +
                '>-sed ou --scanear-em-default [caminho]: scaneia um arquivo ou pasta correspondente a [caminho] na pasta padrão\n' +
                '> -sp [caminho da pasta] ou --scanear-pasta [caminho da pasta] : scaneia uma pasta dentro da pasta default\n' +
                '> -mp [caminho da pasta] ou --mover-pasta [caminho da pasta] : copia todos os arquivos da pasta correspondente a [caminho da pasta] na pasta default\n' +
                '> -cp [caminho da pasta] ou --copiar [caminho da pasta] : copia todos os arquivos da pasta correspondente a [caminho da pasta] na pasta default\n'
                '> -ls ou --listar: lista todos os arquivos na pasta default ou em uma pasta dentro desta\n' +
                '> --manual : mostra uma explicação mais detalhada do programa e caminhos de arquivos\n' +
                '> -f ou --fechar : fecha o programa\n' +
                '> -l ou --limpar : limpa o terminal/tela\n' +
                '======================'*5 + '\ntodos os comandos são sensiveis, então digite os corretamente, letra por letra, para garantir o funcionamento, não use espaços\n' + '======================'*5
                )


COMMAND_LIST = (
    '-a', '--ajuda', '-sd', '--scanear-default', '-sed', '--scanear-em-default' '-sp', '--scanear-pasta',
    '-mp', '--mover-pasta', '-cp', '--copiar', '-ls', '--list', '--manual', '-f', '--fechar', '-l',
    '--limpar', '--default'
    )

COMMAND_NOT_FOUND_MESSAGE = '\n\n'+'============'*3 + '\ncomando não encontrado, use -a ou --ajuda\n' + '============'*3+'\n\n\n'

FILE_NOT_FOUND_MESSAGE = '\n\n'+'================='*7+'\n arquivo não encontrado, certifique-se de que seus arquivos não contem espaços em seus nomes use -lm ou --link-manual para mais informações sobre como usar arquivos corretamente\n' +'================='*7+'\n\n\n'

DEFAULT_PATH_CONFIG_ABSOLUTE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default_path_config.txt')

print('\n\n'+'=================='*9 + '\nATENÇÃO, o programa apresenta uma pequena margen de erro (~3%) por conta de pequenos erros do algoritimo, é recomendado que se use fotos de folhas dobradas o minimo possivel, e de preferencia com o lado onde o pecíolo é menos visivel\n' + 'escreva "-a" ou "--ajuda" para mais informações no uso do programa.\n' + '=================='*9)

while True:
    
    # pede o comando e separa em command/argument
    command = input("\n\ncomando: ").strip().lower()
    command = command.split(' ')
    
    # consegue o path para a pasta default
    try:
        default_path = ''
        with open(DEFAULT_PATH_CONFIG_ABSOLUTE_PATH, 'r') as default_path_config:
            default_path = default_path_config.read()
    except:
        print("a pasta default ainda não existe, prosseguiremos com a instalação:\n\n ")
        Default()
    
    try:    
        # verifica se é um comando suportado
        if command[0] not in COMMAND_LIST:
            print(COMMAND_NOT_FOUND_MESSAGE)
        
        # -a / --ajuda
        elif command[0] == '-a' or '--ajuda' in command[0]: 
            print('\n\n\n\n\n\n'+HELP_MESSAGE)
            
        # -sed/--scanear-em-default   
        elif command[0] == '-sed' or '--scanear-em-default' in command[0]:
            
            # consegue o path completo do arquivo
            if len(command) == 1:
                command.append(input("caminho do arquivo/pasta a ser scaneado: "))
                
            path = os.path.join(default_path, command[1])
            
            if os.path.isfile(path):
                
                # scaneia a imagem
                result = handler.SearchImg(path)
                
                # verifica se o arquivo existe
                if result[0] == None:
                    print(FILE_NOT_FOUND_MESSAGE)
                    
                # caso exista, realiza a analise :
                else:               
                    # faz o unpacking dos valores
                    result = result[0]         
                    percentages, suspicious, img, imgMap = result
                    
                    # OUTPUT com as informações
                    print("===========================================")
                    print(f'-> folha: {str(percentages['green'])}%')
                    print(f'-> doença: {str(percentages['red'])}%')
                    print(f'-> total: {str(percentages['green'] + percentages['red'])[:7]}%')
                    print("===========================================")
                    
                    # personaliza a mensagem para mostrar o mapa da imagem de acordo com o grau de probabilidade de erro do algoritimo
                    if suspicious:
                        showImgMessage = 'as porcentagens desta imagem estão fora do padrão, deseja ver o mapa da imagem? (digite "s" para "sim"): '
                    else: 
                        showImgMessage = 'deseja ver o mapa da imagem? (digite "s" para "sim"): ' 
                                    
                    showImg = input(showImgMessage).strip().lower()
                    
                    # mostra as imagens caso requerido
                    if showImg == 's' or showImg == 'sim':
                        imgMap.show()
                        img.show()
            
            elif os.path.isdir(path):
                
                # scaneia uma pasta
                def searchFolder(path):
                    
                    for result in handler.SearchImg(os.path.join(path, '*')):
                        results.append(result)
                    for scan_path in os.listdir(path):
                        scan_path = os.path.join(path, scan_path)
                        if os.path.isdir(scan_path):
                            print(f"    scaneando {os.path.basename(scan_path)}")
                            searchFolder(scan_path)
                
                # scaneia path        
                results = []
                for result in handler.SearchImg(os.path.join(path, "*")):
                    results.append(result)
                for scan_path in os.listdir(path):
                    scan_path = os.path.join(path, scan_path)
                    
                    # se scan_path for uma pasta, scaneia os arquivos dentro dele
                    if os.path.isdir(scan_path):
                        print(f"    scaneando {os.path.basename(scan_path)}")
                        searchFolder(scan_path)  
                        
                # caso não existam resultados, OUPUT: mensagem de erro para file not found           
                if results[0] == None:
                    print(FILE_NOT_FOUND_MESSAGE)
                    
                # caso exista, realiza a analise :
                else:
                    WichImage = 1
                    for result in results:
                        percentages, suspicious, img, imgMap = result

                        # OUTPUT com as informações
                        print("===========================================")
                        print(f"{WichImage}º imagem : ")
                        print(f'-> folha: {str(percentages['green'])}%')
                        print(f'-> doença: {str(percentages['red'])}%')
                        print(f'-> total: {str(percentages['green'] + percentages['red'])[:7]}%')
                        print("===========================================")
                        
                        # personaliza a mensagem para mostrar o mapa da imagem de acordo com o grau de probabilidade de erro do algoritimo
                        if suspicious:
                            showImgMessage = 'as porcentagens desta imagem estão fora do padrão, deseja ver o mapa da imagem? (digite "s" para "sim"): '
                        else: 
                            showImgMessage = 'deseja ver o mapa da imagem? (digite "s" para "sim"): ' 
                        
                        # mostra as imagens caso requerido                
                        showImg = input(showImgMessage).strip().lower()
                        if showImg.lower() == 's' or showImg.lower() == 'sim':
                            imgMap.show()
                            img.show()
                            
                        # atualiza qual é a imagem (primeira, segunda, etc)
                        WichImage += 1
                
                
            
        elif command[0] == '-sd' or '--scanear-default' in command[0]:
            
            # scaneia uma pasta
            def searchFolderSD(path):
                for result in handler.SearchImg(os.path.join(path, '*')):
                    results.append(result)
                for scan_path in os.listdir(path):
                    scan_path = os.path.join(path, scan_path)
                    if os.path.isdir(scan_path):
                        print(f"    scaneando {os.path.basename(scan_path)}")
                        searchFolderSD(scan_path)
                        
            # scaneia a imagem
            t1 = time()
            print("\n    scaneando pasta default...")
            
            results = []
            for result in handler.SearchImg(os.path.join(default_path, "*")):
                results.append(result)
            for scan_path in os.listdir(default_path):
                scan_path = os.path.join(default_path, scan_path)
                if os.path.isdir(scan_path):
                    print(f"    scaneando {os.path.basename(scan_path)}")
                    searchFolderSD(scan_path)  
                            
            t2 = time()
            print(f"    {len(results)-1} arquivos encontrados")
            print(f"    scan concluido em {str(t2-t1)[:7]} segundos\n")
            
            # verifica se o arquivo existe
            if results[0] == None:
                print(FILE_NOT_FOUND_MESSAGE)
                
            # caso exista, realiza a analise :
            else:
                WichImage = 1
                for result in results:
                    percentages, suspicious, img, imgMap = result

                    # OUTPUT com as informações
                    print("===========================================")
                    print(f"{WichImage}º imagem : ")
                    print(f'-> folha: {str(percentages['green'])}%')
                    print(f'-> doença: {str(percentages['red'])}%')
                    print(f'-> total: {str(percentages['green'] + percentages['red'])[:7]}%')
                    print("===========================================")
                    
                    # personaliza a mensagem para mostrar o mapa da imagem de acordo com o grau de probabilidade de erro do algoritimo
                    if suspicious:
                        showImgMessage = 'as porcentagens desta imagem estão fora do padrão, deseja ver o mapa da imagem? (digite "s" para "sim"): '
                    else: 
                        showImgMessage = 'deseja ver o mapa da imagem? (digite "s" para "sim"): ' 
                                    
                    showImg = input(showImgMessage)# mostra as imagens caso requerido
                    if showImg.lower() == 's' or showImg.lower() == 'sim':
                        imgMap.show()
                        img.show()
                        
                    # atualiza qual é a imagem (primeira, segunda, etc)
                    WichImage += 1
                    
        elif command[0] == '-mp' or '--mover-pasta' in command[0]:
            
            # consegue o path do arquivo/pasta
            mvPath = ''
            if len(command) == 1:
                mvPath = input('qual o caminho para a pasta? : ')
            else:
                mvPath = command[1]
            
            # move uma pasta para a pasta default
            def moveFolder(Dpath, i):
                
                for path in os.listdir(Dpath):
                    # cria o path absoluto
                    path = os.path.join(Dpath, path)
                    # move caso o path corresponda a um file
                    if os.path.isfile(path) and not os.path.exists(os.path.join(default_path, os.path.basename(path))):
                        print("  "*(i+1)+f"movendo {os.path.basename(path)}")
                        shutil.move(path, default_path)
                    # chama a função recursivamente caso o path corresponda a uma pasta
                    elif os.path.isdir(path):
                        print("  "*i+1 + f"movendo arquivos de {os.path.basename(path)}...")
                        moveFolder(path, i+2)
                print("  "*i+1 + f"mudança dos arquivos de{os.path.basename(Dpath)} terminada")
            
            # impede erros caso o arquivo não exista/qualquer outro erro   
            try:
                print(f"\n  iterando em {mvPath}...")
                for path in os.listdir(mvPath):
                    # cria o path absoluto
                    path = os.path.join(mvPath, path)
                    # move caso o path corresponda a um file
                    if os.path.isfile(path) and not os.path.exists(os.path.join(default_path, os.path.basename(path))):
                        print(f"    movendo {os.path.basename(path)}")
                        shutil.move(path, default_path)
                    # chama "moveFolder" caso o path corresponda a uma pasta
                    elif os.path.isdir(path):
                        print(f"    movendo arquivos de {os.path.basename(path)}...")
                        moveFolder(path, 2)
                
                print("  iteração concluida")           
                print("  arquivos movidos com sucesso")
            except:
                print(FILE_NOT_FOUND_MESSAGE)
                print("ATENÇÃO - verifique se os arquivos desta pasta já existem na pasta default\n" +
                    "caso este seja o caso, os arquivos ainda inexistentes já foram movidos")
                
            # OUPUT uma mensagem de erro caso o arquivo não exista/qualquer erro aconteça

        
        elif command[0] == '-cp' or '--copiar' in command[0]:
                    
            # consegue o path do arquivo/pasta
            cpPath = ''
            if len(command) == 1:
                cpPath = input('qual o caminho para a pasta? : ')
            else:
                cpPath = command[1]
            
            # move uma pasta para a pasta default
            def copyFolder(Dpath, i):
                
                for path in os.listdir(Dpath):
                    # cria o path absoluto
                    path = os.path.join(Dpath, path)
                    # copia caso o path corresponda a um file
                    if os.path.isfile(path):
                        print("  "*(i+1)+f"copiando {os.path.basename(path)}")
                        shutil.copy(path, default_path)
                    # chama a função recursivamente caso o path corresponda a uma pasta
                    elif os.path.isdir(path):
                        print("  "*i+1 + f"copiando arquivos de {os.path.basename(path)}...")
                        copyFolder(path, i+2)
                print("  "*(i-1) + f"copia dos arquivos de {os.path.basename(Dpath)} terminada")
            
            # impede erros caso o arquivo não exista/qualquer outro erro   
            try:            
                print(f"\n  iterando em {cpPath}...")
                for path in os.listdir(cpPath):
                    # cria o path absoluto
                    path = os.path.join(cpPath, path)
                    # move caso o path corresponda a um file
                    if os.path.isfile(path):
                        print(f"    copiando {os.path.basename(path)}")
                        shutil.copy(path, default_path)
                    # chama "moveFolder" caso o path corresponda a uma pasta
                    elif os.path.isdir(path):
                        print(f"    copiando arquivos de {os.path.basename(path)}...")
                        copyFolder(path, 2)
                        
                print("  arquivos copiados com sucesso")
                
            # OUPUT uma mensagem de erro caso o arquivo não exista/qualquer erro aconteça
            except:
                print(FILE_NOT_FOUND_MESSAGE)
        
            
        elif command[0] == "-ls" or "--list" in command[0]:
            
            path = ''
            # se é um path absoluto: 
            if len(command) > 1:
                path = os.path.join(default_path, command[1])
            # se é apenas o nome da pasta
            else:
                inputPath = input("nome do arquivo/caminho relativo (default/caminho_relativo): ").strip()
                
                # procura o nome dentro da pasta
                def LSFolder(Fpath):
                    global path
                    for possible in os.listdir(default_path):
                        # se possible é um mathc, define path com o caminho absoluto de possible
                        if os.path.isdir(os.path.join(Fpath, possible)) and os.path.basename(possible) == inputPath:
                            path = os.path.join(Fpath, possible)
                            break
                        # se possible é uma pasta mas não é um match: 
                        # chama LSFolder recursivamente com o valor absoluto de epossible
                        elif os.path.isdir(os.path.join(Fpath, possible)):
                            LSFolder(os.path.join(Fpath, possible))
                
                # se o path do input não for absoluto ou blank           
                if len(REsplit(r'\\|/', inputPath)) == 1 and inputPath != '':
                    # procura até o path ser achado
                    while not path:
                        for possible in os.listdir(default_path):
                            # define o valor de possible corretamente
                            possible = os.path.join(default_path, possible)
                            # termina se um matching é encontrado
                            if os.path.isdir(possible) and os.path.basename(possible) == inputPath:
                                path = possible
                            # chama LSFolder recursivamente caso ele seja uma pasta mas não um match
                            elif os.path.isdir(possible):
                                LSFolder(possible)
            
            # se o path não for encontrado, ou for blank, é definido como a pasta default
            if path == '':
                path = default_path
            # conta a quantidade de arquivos e pastas separadamente para formatação do output
            counter = Counter(dir=1, file=1)
            try:
                for Lpath in os.listdir(path):
                    # se o path sendo listado é uma pasta:
                    if os.path.isdir(os.path.join(path, Lpath)):
                        print(f'{counter['dir']}º pasta: {Lpath}')
                        counter['dir'] += 1
                    # se o path sendo listado é um arquivo:
                    elif os.path.isfile(os.path.join(path, Lpath)):
                        print(f'{counter['file']}º arquivo: {Lpath}')
                        counter['file'] += 1
                if counter['dir'] == 1 and counter['file'] == 1:
                    print("\nnenhum arquivo encontrado")    
            # se qualquer erro ocorrer, printa a mensagem de erro file-not-found           
            except:
                print(FILE_NOT_FOUND_MESSAGE)            
                    
        
            
        elif command[0] == '-f' or '--fechar' in command[0]:
            exit("\n\nprograma fechado\n\n")    
        
        elif command[0] == '-l' or '--limpar' in command[0]:
            print('\n'*197)
            print('\n\n'+'=================='*9 + '\nATENÇÃO, o programa apresenta uma pequena margen de erro por conta da abreviação e pequenos erros do algoritimo, analise os valores percentuais antes do uso cientifico\n' + 'escreva "-a" ou "--ajuda" para mais informações no uso do programa.\n' + '=================='*9)  
                    
        elif command[0] == '--default':
            if input('escreva "--confirmar--" para prosseguir: ').strip().lower() == "--confirmar--":
                Default()
                
        elif '--manual' in command[0]:           
            print('\n\n' + '=========================='*6)
            print("caminhos de arquivos:")
            print(
                "os caminhos de arquivos são a forma em que o computador acessa os arquivos, "+
                  "estes, são compostos do disco rigido (\"C:\" por exemplo), seguidos pelas pastas, "+
                  "('C:\\Users\\CLIENTE\\Desktop' por exemplo), e ao fim, o nome do arquivo: "+
                  f"('{os.path.abspath(__file__)}' por exemplo).\n"
                  )
            print(
                "algums comandos requerem arquivos para trabalharem, estes, podem ser "+
                  "especificados após o comando: ('-mp C:\\Users\\CLIENTE\\Desktop\\exemplo')\n\n" +
                  "caso não seja especificado, o programa o pedirá para fornecer um caminho de arquivo.\n"
                  )
            print(
                "por fim, vale ressaltar que todos os comandos são. em algum nivel, 'case-sensitive' "+
                "em outras palavras, caso seja escrito '-mv' no lugar de '-mp', ou 'mp' no lugar de '-mp' "+
                "o programa não reconhecerá o comando, além disso, recomendamos o uso precavido de algums "+
                "comandos, como o '--default' pois estes trabalham com as configurações do "+
                "programa, e/ou podem deletar arquivos importantes caso o caminho seja passado de forma "+
                "incorreta.\n"
                )
            print("caso qualquer erro ocorra durante o uso do programa, o programa enviará uma "+
                  "mensagem de erro em linguagem comum, ao invés de fechar, caso isso não aconteça, "+
                  "copie e cole (crtl+c, ctrl+v) todo o conteudo do cmd, e me envie a mensagem, assim como "+
                  "uma descrição sobre oque ouve antes desta acontecer (caso tenha se usado  -l ou --limpar "+
                  "anteriormente, basta subir com o cursor por alguns segundos e encontrara o historico de uso antigo novamente")
            print('\n\n' + '=========================='*6 + '\n\n')

        else:
            print(COMMAND_NOT_FOUND_MESSAGE)
        
        
    except:
        if command[0] == '-f' or '--fechar' in command[0]:
            exit("\n\nprograma fechado\n\n")
        else:
            print("\n"*200)
            exit(">>>>>algum erro ocorreu, o programa foi fechado\n\n\n")
        
        
    
        