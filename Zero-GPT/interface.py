from typing import Any
import customtkinter
from model import GPT2PPL
from nltk.tokenize import word_tokenize
import time
from threading import Thread
"""
theme = "light" 
customtkinter.set_appearance_mode(theme)"""

MULTIPLICATEUR = 100
MODELS = ['GPT-3.5', 'GPT-4', 'GEMINI']
# Total * part / 100

TIME = 2740

class AnimateLabel(customtkinter.CTkLabel):
    def __init__(self, master, text, font):
        super(master, text)
        self.master = master
        self.text = text
        self.font = font
    def __post_init__(self):
        pass


class Interface:
    def __init__(self) -> None:
        self.window = customtkinter.CTk()
        self.window.title("StopLMM")
        self.window.geometry("1280x800")
        self.window.resizable(False, False)
        self.contenair_title = customtkinter.CTkFrame(self.window, fg_color="transparent")
        self.contenair_title.pack(expand = True)       
        self.contenair = customtkinter.CTkFrame(self.window)
        self.contenair.pack(expand = True)
        self.frame_interaction = customtkinter.CTkFrame(self.contenair, fg_color="transparent")
        self.frame_interaction.grid(row = 0, column = 0, padx = 10)
        self.frame_option = customtkinter.CTkFrame(self.contenair, fg_color="transparent")
        self.frame_option.grid(row = 0, column = 1)
        self.generate_label("  ", 0, self.contenair, column=2)
        self.model = GPT2PPL()
        self.surligner = False


    def rechercher_occurrences(self, mot):
            # Efface toutes les balises de mise en surbrillance précédentes
            #self.input_text.tag_remove("highlight", "1.0", customtkinter.END)

            texte = self.input_text.get("1.0", "end-1c")  # Obtient le texte du widget texte
            mot_a_rechercher = mot  # Obtient le mot à rechercher
            occurrences = []

            # Recherche toutes les occurrences du mot dans le texte
            index = 1.0
            if mot.__len__() != 0:
                while True:
                    index = self.input_text.search(mot_a_rechercher, index, stopindex=customtkinter.END)
                    if not index:
                        break
                    occurrences.append(index)
                    index = self.input_text.index(f"{index}+{len(mot_a_rechercher)}c")
                # Met en surbrillance les occurrences trouvées
                for index in occurrences:
                    self.input_text.tag_add("highlight", index, f"{index}+{len(mot_a_rechercher)}c")
                    
                if occurrences:
                    self.input_text.see(occurrences[0])
                self.input_text.tag_config("highlight", background="gray")

    def typing_effect(self, string1):
        for char in string1:
            self.parameter.tag_config('color_i', foreground = '#666666')
            self.parameter.insert("end",char , "color_i")
            self.parameter.update()
            self.parameter.see("end")
            time.sleep(0.05)

    def on_get(self, event):
        self.input_text.configure(border_color='blue', border_width = 2)
        
    def out_get(self, event):
        self.input_text.configure(border_color='#969696', border_width = 1)
        
    def inference(self):
        result = self.model(self.input_text.get(1.0, customtkinter.END), int(self.critical_level_ai.get()), int(self.critical_level_mixte.get()))
        self.progress.configure(progress_color = "#672DF2")
        self.progress.set(20)
        self.progress.stop()
        self.parameter.delete(1.0, customtkinter.END)
               
        if result.__len__() > 2: 
            get_prob = self.probability_calculation(result[2])
            pbt = get_prob
            print("probabiltys", get_prob)
            
            label = int(result[0].get('label'))  
            verdict = result[-1]
            probability = get_prob[0] if label == 0 else get_prob[1]
            
            if label ==  0 and get_prob[0] < 50:
                probability = get_prob[1]
                verdict = "Texte generé par un Humain."
                
            elif label == 1 and get_prob[1] < 50:
                probability = get_prob[0]
                verdict = "Texte generé par une IA."
                
            elif (get_prob[0] >= 50 and get_prob[0] <= 55) or (get_prob[1] >= 50 and get_prob[1] <= 55):
                
                if get_prob[0] > get_prob[1]:
                    verdict = "Texte Mixte(Ai predominent)"
                    probability = get_prob[0]
                else:  
                    verdict = "Texte Mixte(Humain predominent)"
                    probability = get_prob[1]
                    
            # if label == 1:
            #     verdict = "Texte generé par un Humain."
            # else:
            #     verdict = "Texte generé par une IA."
            self.parameter.tag_config("token", foreground = "blue")
            self.parameter.insert(1.0, "Tokens : ", 'token')
            self.parameter.insert(customtkinter.END, str(len(word_tokenize(self.input_text.get(
                        1.0, customtkinter.END )))))

            self.parameter.tag_config("result", foreground = "green")

            self.parameter.insert(customtkinter.END, "\tResult : ", 'result')        
            #self.parameter.insert(customtkinter.END, verdict + '\t')  
            self.typing_effect(verdict)
            self.parameter.tag_config("prob", foreground = "#993997")
            self.parameter.insert(customtkinter.END, " Probability : ", 'prob') 
            
            if self.surligner:
                for sentence in result[1]:
                    self.rechercher_occurrences(sentence)
                    time.sleep(0.1)
            # diviseur = 0
            # try:
            #     label = int(result[0].get('label'))
            #     diviseur = self.critical_level_ai.get()

            # except TypeError:
            #     diviseur = 1
                
            # try:
            #     probability = ((int(result[0]['Perplexity per line']) * MULTIPLICATEUR) / diviseur ) % diviseur
            # except KeyError:
            #     probability = 0.0
            # print("probability : ",  probability)
            # if label == 1:
            #     probability = float((probability))

            self.parameter.insert(customtkinter.END, str(round(probability, 1)))
            self.probability_ai.set(0)
            self.probability_human.set(0)

            self.graph_progress(self.probability_ai, int(pbt[0]))
            self.graph_progress(self.probability_human, int(pbt[1]))
        else:
            
            self.parameter.tag_config("token", foreground = "blue")
            self.parameter.insert(1.0, "Tokens : None", 'token')

            self.parameter.tag_config("result", foreground = "green")

            self.parameter.insert(customtkinter.END, "\tResult : ", 'result')        
            #self.parameter.insert(customtkinter.END, verdict + '\t')  
            self.typing_effect(result[1])
            self.parameter.tag_config("prob", foreground = "#993997")
            self.parameter.insert(customtkinter.END, " Probability : unavailable", 'prob') 

        return result

    def formule(self, cas_favorable, cas_possible):
        probability_of = (cas_favorable / cas_possible) * 100
        probability_of = round(probability_of, 2)
        
        return probability_of

    def probability_calculation(self, perplexity):
        tab_ai = []
        tab_humain = []
        for per in perplexity:
            if per < self.critical_level_ai.get():
                tab_ai.append(1)
            else:
                tab_humain.append(1)
        cas_possible = sum(tab_humain) + sum(tab_ai)
        
        probability_ai = self.formule(sum(tab_ai), cas_possible)
        probability_huamin = self.formule(sum(tab_humain), cas_possible)
        
        return (probability_ai, probability_huamin)

            
        
    def amorce_infer(self):
        try:
            self.input_text.tag_remove("highlight", "1.0", customtkinter.END)
        except: pass
        
        self.progress.start()
   
        #self.probability_human.set(0.8)
        self.progress.configure(progress_color = "#F27085")
        self.parameter.delete(1.0, customtkinter.END)
        
        self.parameter.tag_config("token", foreground = "blue")
        self.parameter.insert(1.0, "Tokens : ", 'token')
        self.parameter.insert(customtkinter.END, str(len(word_tokenize(self.input_text.get(
                    1.0, customtkinter.END )))))

        self.parameter.tag_config("result", foreground = "green")

        self.parameter.insert(customtkinter.END, "\tResult : ", 'result')        
        self.parameter.insert(customtkinter.END, "None\t")   

        self.parameter.tag_config("prob", foreground = "#993997")
        self.parameter.insert(customtkinter.END, "Probability : ", 'prob')   
        self.parameter.insert(customtkinter.END, "0.0")

        thread_inference = Thread(target=lambda: self.inference())
        thread_inference.start()

    def generate_label(self,text,row, contenair , column = 0):
        self.label_ = customtkinter.CTkLabel(contenair, text=text,  font=("courier", 14))
        self.label_.grid(row=row, column=column,pady=2)
        

    def stop_progress(self, progressbar):
        progressbar.stop()

    def graph_progress(self, progressbar, value):
        progressbar.start()
        temps = (TIME * value) / 100
        self.window.after(int(temps), lambda : self.stop_progress(progressbar))

    def genrate_frame(self, row, contenair = None):
        if contenair is None:
            contenair = self.frame_option
        self.frame_ = customtkinter.CTkFrame(contenair, fg_color="transparent", border_width=1)
        self.frame_.grid(row = row, column=0, pady= 10)
        return self.frame_
         
    def critical_meth_human(self, event):
        
        value_ = int(self.critical_level_human.get())
        self.label_slider_human.configure(text = str(value_))
        
    def critical_meth_ai(self, event):
        
        value_ = int(self.critical_level_ai.get())
        self.label_slider_ai.configure(text = str(value_))

    def critical_meth_mixte(self, event):
        
        value_ = int(self.critical_level_mixte.get())
        self.label_slider_mixte.configure(text = str(value_))
    
    def surligner_text(self):
        if self.surligner:
            self.surligner = False
        else:
            self.surligner = True

    
    def __call__(self, call) -> Any:
        
        label_title = customtkinter.CTkLabel(self.contenair_title, text="StopLLM",  font=("courier", 40))
        label_title.grid(row=0, column=0)
        
        self.generate_label("", 0, self.frame_interaction)

        
        self.input_text = customtkinter.CTkTextbox(self.frame_interaction, width=1000, height=500,  wrap=customtkinter.WORD,insertwidth=8 , font=("courier", 15, 'italic'), corner_radius=0, border_width=1, border_color='gray')
        self.input_text.grid(row=1, column=0)
        self.progress = customtkinter.CTkProgressBar(self.frame_interaction, orientation=customtkinter.HORIZONTAL, width=1000, determinate_speed=5, corner_radius=0, height=3, progress_color= "blue")
        self.progress.grid(row = 2, column = 0)
        self.progress.set(0)

        self.parameter = customtkinter.CTkTextbox(self.frame_interaction, width=1000, height=20, fg_color='transparent', border_width=2, wrap=customtkinter.WORD,insertwidth=2 , corner_radius=0, font=("courier", 15, 'italic'))
        self.parameter.grid(row=3, column=0, pady = 10)


        self.genrate_frame(4, self.frame_interaction)

        self.probability_human = customtkinter.CTkProgressBar(self.frame_, orientation=customtkinter.HORIZONTAL, width=700, determinate_speed=0.5, corner_radius=0, height=8, progress_color= "green")
        self.probability_human.grid(row=0, column=0, pady = 10)
        self.probability_human.set(0)

        self.probability_ai = customtkinter.CTkProgressBar(self.frame_, orientation=customtkinter.HORIZONTAL, width=700, determinate_speed=0.5, corner_radius=0, height=8, progress_color= "red")
        self.probability_ai.grid(row=1, column=0, pady = 10)
        self.probability_ai.set(0)


        self.parameter.tag_config("token", foreground = "blue")
        self.parameter.insert(1.0, "Tokens : ", 'token')
        self.parameter.insert(customtkinter.END, "0")

        self.parameter.tag_config("result", foreground = "green")
        self.parameter.insert(customtkinter.END, "\tResult : ", 'result')   
        self.parameter.insert(customtkinter.END, "None\t")
        
        self.parameter.tag_config("prob", foreground = "#993997")
        self.parameter.insert(customtkinter.END, "Probability : ", 'prob')   
        self.parameter.insert(customtkinter.END, "0.0")
        
        self.parameter.insert(customtkinter.END, "\tModel : ChatGPT-3.5")

                   
        self.submit = customtkinter.CTkButton(self.frame_interaction, text="submit", command= self.amorce_infer)
        self.submit.grid(row=5, column=0)
        self.generate_label("    ", 6, self.frame_interaction, column=0)

        
        # Creation des slider parametriques
        self.label_ = customtkinter.CTkLabel(self.frame_option, text="Custom",  font=("courier", 20, 'bold'))
        self.label_.grid(row=0, column=0,pady=2)
        
        self.genrate_frame(1)
        self.generate_label("Critical Human", 0, self.frame_)
        self.critical_level_human = customtkinter.CTkSlider(self.frame_, to=1000, command=self.critical_meth_human, width=166, height=16, progress_color="blue")
        self.critical_level_human.grid(row=1, column = 0, pady = 10)
        self.critical_level_human.set(500)
        self.label_slider_human = customtkinter.CTkLabel(self.frame_, text=str(int(self.critical_level_human.get())),  font=("courier", 14, 'italic'))
        self.label_slider_human.grid(row=2, column=0,pady=2)

        self.genrate_frame(2)
        self.generate_label("Critical AI", 0, self.frame_)
        self.critical_level_ai = customtkinter.CTkSlider(self.frame_, to=1000, command= self.critical_meth_ai, width=166, height=16, progress_color="blue")
        self.critical_level_ai.grid(row=1, column = 0, pady = 10)
        self.critical_level_ai.set(200)
        self.label_slider_ai = customtkinter.CTkLabel(self.frame_, text=str(int(self.critical_level_ai.get())),  font=("courier", 14, 'italic'))
        self.label_slider_ai.grid(row=2, column=0,pady=2)
        
                
        self.genrate_frame(3)
        self.generate_label("Critical Mixte", 0, self.frame_)
        self.critical_level_mixte = customtkinter.CTkSlider(self.frame_, to=1000, command= self.critical_meth_mixte, width=166, height=16, progress_color="blue")
        self.critical_level_mixte.grid(row=1, column = 0, pady = 10)
        self.critical_level_mixte.set(280)
        self.label_slider_mixte = customtkinter.CTkLabel(self.frame_, text=str(int(self.critical_level_mixte.get())),  font=("courier", 14, 'italic'))
        self.label_slider_mixte.grid(row=2, column=0,pady=2)
        
        self.genrate_frame(4)
        self.surligner_texte_ai = customtkinter.CTkSwitch(self.frame_, text="Surligner" , command=self.surligner_text)
        self.surligner_texte_ai.grid(row = 0, column=0, pady=5)
        
        self.generate_label("Charger fichier", 1, self.frame_)

        self.charger_fichier = customtkinter.CTkOptionMenu(self.frame_, values=["", "pdf", "txt", "word"], width=100 , command=None)
        self.charger_fichier.grid(row = 2, column=0)
        self.generate_label("", 3, self.frame_)
        
        self.input_text.bind("<FocusIn>", self.on_get)
        self.input_text.bind("<FocusOut>", self.out_get)
        self.window.mainloop()

inter = Interface()
inter(True)
