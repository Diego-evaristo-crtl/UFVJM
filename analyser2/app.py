from tkinter import ttk
import ttkbootstrap as ttk
from PIL import Image
from collections import Counter
import os
from colorsys import rgb_to_hls

'''
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
    :Informações para desenvolvedores:                                  .
    .   a analise da foto, como sugerida pela iteração indentada        .    
    .   é ineficiente O(n²), entretanto, necessaria para a analise      .
    .   de todos os pixeis da imagem. o python é uma linguagem          .
    .   ineficiente, e um programa com melhor desempenho poderia        .
    .   ser feito em C, C++, e linguagens do tipo, entretanto,          .
    .   apresentariam maior grau de complexidade, especialmente         .
    .   para o uso de GUI's.                                            .
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
    :Sugestões:                                                         . 
    .   as principais limitações deste programa advém do uso            .    
    .   do python, tkinter, e ou minha própia inexperiencia             .
    .   algumas sugestões que poderiam ser feitas com melhores          .
    .   frameworks (como pyside6) são:                                  .
    .       * vizualização em tempo real do mapa da imagem com          .
    .         objétos canvas (tkinter não apresenta possibilidade       .
    .         de colorir pixeis unicos de forma eficiente)              .
    .       * sistema 'drag and drop' para acesso a arquivos de         .
    .         forma mais user friendly                                  .
    .       * melhora no sistema de analise de pixeis (encontrado       .
    .         dentro da função 'scan' ) para possibilidade de fundos    .
    .         com diferentes cores                                      .
    .       * implementação de uma busca em pastas (facilmente          .
    .         feito com uma função recursiva), o removi pois            .
    .         ao testar, o programa parou de responder por um           .
    .         periodo de tempo.                                         .
    . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
'''

class App(ttk.Window):
    def __init__(self):
        super().__init__('app', 'darkly')
        
        # set's 2 rows and 2 columns for dashboard interface
        self.geometry('700x400')
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)
        
            # creates 4 dashboards get input and give output.
        self.frame1 = ttk.Frame(self) # general program usage
        self.frame2 = ttk.Frame(self) # output/input for files & results
        self.f3 = ttk.Frame(self.frame2)
        self.f4 = ttk.Frame(self.frame2)
        
            # stats for the percentage of contaminated and non-contaminated parts
        self.stats = Counter()
        self.stats['good'] = 0
        self.stats['bad'] = 0
            # saves the imgs to show them
        self.imgs = []
        
        # creates entries and vars to get filename, dictpath, buttons to show images, and labels to output results 
        self.FileVar = ttk.StringVar()
            # get file name
        self.FileEnt = ttk.Entry(self.frame2, 
                                    textvariable=self.FileVar,
                                    width=30,
                                    background='orange'
                                )
        
        self.DirVar = ttk.StringVar()
            # get dictionary location
        self.DirEnt = ttk.Entry(self.frame2,
                                textvariable=self.DirVar,
                                width=30,
                                background='orange'
                                )
        
            # showcase, respectivily, wich parts aren't and are 'contaminated'
        self.LabelGdVar = ttk.StringVar(value='bom: ')
        self.LabelGd = ttk.Label(self.f3, 
                                 textvariable=self.LabelGdVar,
                                 background='grey',
                                 width=15
                                )
        self.LabelBdVar = ttk.StringVar(value='ruim: ')
        self.LabelBd = ttk.Label(self.f3, 
                                 textvariable=self.LabelBdVar,
                                 background='grey',
                                 width=15
                                )        
            # button that scans the images
        scanButton = ttk.Button(self.f4, 
                                text='scanear imagens', 
                                command=lambda: self.scan(self.DirEnt.get(), self.FileEnt.get())
                               )
            # button that shows the image and it's map
        showButton = ttk.Button(self.f4, 
                                text='mostrar imagem & mapa',
                                command=lambda: self.showImg()
                                )
        
        
        self.infoF2Var = ttk.StringVar(value='pasta/arquivo abaixo (respectivamente):')
        infoF2 = ttk.Label(self.frame2, textvariable=self.infoF2Var)

            # packs all the frame2 widgets, aka the interactive ones.
        infoF2.pack(pady=20, padx=50, side='top', expand=True)
        self.DirEnt.pack(pady=5, padx=50, side='top', expand=True)
        self.FileEnt.pack(pady=5, padx=50, side='top', expand=True)
        self.LabelGd.pack(pady=5, padx=50, side='top', expand=True)
        self.LabelBd.pack(pady=5, padx=50, side='top', expand=True)
        showButton.pack(pady=10, padx=3, side='top', expand=True)
        scanButton.pack(pady=10, padx=3, side='top', expand=True)
        
        self.f3.pack(pady=10, padx=30, side='top', expand=True)
        self.f4.pack(pady=10, padx=40, side='top', expand=True)
        
        # creates and packs the frame1 widgets, aka the informative ones.
        PROGRAM_INFO = ttk.Label(self.frame1,
                                 text=
'''
    \tInformações de uso.
    devido a forma como as fotos são analisadas,
    todas devem ter seus fundos dar cor azul.
    Caso necessario, use softwares como paint.
    
    Cada foto é analisada por vez, portanto,
    recomendo que deixe o caminho para a pasta
    onde as fotos estão sendo usadas já escrito,
    e mude apenas o nome do arquivo para escanear.
    
    Lembre-se de colocar o caminho apenas da pasta,
    sem o nome do arquivo, na sua respectiva área,
    e o nome da foto na entrada abaixo. por exemplo:
    para o caminho 'C:documentos/fotos/f1.jpeg' deve
    ser colocado 'C1:documentos/fotos' na primeira
    entrada, e 'f1.jpeg' na segunda.
    
    informações de possivel uso e sugestões de
    aprimoramentos para desenvolvedores podem
    ser vistas nas primeiras linhas de código.
''',
                                 width=50,
                                 font=2
                                 )
        PROGRAM_INFO.pack(expand=True)
        
        
        self.frame1.grid(column=0, row=0, sticky='nw')
        self.frame2.grid(column=1, row=0, sticky='ne')
    
    
    
    def percent(self):
        percentages = {'good':0, 'bad':0}
        for key, value in self.stats.items():
            percentages[key] = (value/self.stats.total()) * 100
        return percentages
       
    # scans the photos
    def scan(self, dirpath, filename):
            # get's path and tests if it is valid
        path = os.path.join(dirpath, filename)
        if not os.path.exists(path) and os.path.isfile(path):
            return           
        
            # creates opens image and creates img map
        img = Image.open(path)
        imgMap = Image.new(img.mode, img.size)
            
            # scans image to fill the img map
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                
                pixel = img.getpixel((x, y)) # get's pixel (RGB)
                
                    # good
                if pixel[1] > pixel[0]-10 and pixel[1] > pixel[2]-10: 
                    self.stats['good'] += 1
                    imgMap.putpixel((x,y), value=(0,255,0))
                
                elif pixel[0] > pixel[1] and pixel[0] > pixel[2]:
                        
                        try: 
                            hsl_pixel = rgb_to_hls(pixel[0], pixel[1], pixel[2]) # get's pixel (HSL)
                                # good
                            if pixel[2] < 150 and (hsl_pixel[1] < 55 or hsl_pixel[2] > 115): 
                                self.stats['good'] +=1
                                imgMap.putpixel((x,y), value=(0,255,0))
                                # bad           
                            else:
                                self.stats['bad'] += 1
                                imgMap.putpixel((x,y), value=(255,0,0))
                        except:
                            self.stats['bad'] += 1
                            imgMap.putpixel((x,y), value=(255,0,0))
                        # none   
                else:
                    imgMap.putpixel((x,y), value=(100,100,255))
                

    
            # gives statistics
        percentages = self.percent()
        self.LabelGdVar.set('bom: '+str(percentages['good'])[:6]+'%')
        self.LabelBdVar.set('ruim: '+str(percentages['bad'])[:6]+'%')
        
        self.imgs = [img, imgMap]
       
    # mostra as imagems salvas em self.imgs    
    def showImg(self):
        try:
            self.imgs[0].show()
            self.imgs[1].show()
        except IndexError:
            pass
        
    # cria e roda o programa            
root = App()
root.mainloop()