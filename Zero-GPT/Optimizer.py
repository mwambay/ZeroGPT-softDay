
LINES_PARAGRAPH = 4
LENGHT_LINE = 8
STEP = 500

values = [3854, 1475, 2360, 3639, 344, 145, 7084, 1698, 281, 21926, 249, 80, 723, 192, 2005, 552, 109, 580, 2355, 335, 519, 419, 4824, 579, 583, 356, 162, 4450, 523, 377, 3120, 53, 143, 182, 562, 318, 69, 42985, 200, 804, 635, 335, 752, 671, 178, 42985, 513, 317, 205, 1024, 984, 164, 191, 155, 2643, 223, 1967, 1188, 502, 7274, 855, 1823, 878, 1379, 890, 95, 170, 532, 440, 250, 651, 379, 1018, 418, 1406, 1249, 521, 449, 832, 670, 248, 1149, 271, 4856, 1148, 339, 206, 730, 569, 43577, 1136, 1369, 670, 283, 509, 1708, 758, 722, 334, 291, 1336, 236, 5571, 326, 260, 88, 360, 138, 445, 934, 895, 97, 1806, 85, 45483, 542, 193, 1214, 707, 2216, 265, 169, 2034, 317, 315, 597, 1963, 170, 854, 6420, 5481, 1804, 1218, 488, 93, 746, 288, 88, 826, 176, 129, 88, 45483, 504, 2746]

class Optimizer:
    def __init__(self, perplexity_lines, level_ai) -> None:
        self.perplexity_lines = perplexity_lines
        self.level_ai = level_ai
        self.exclusion_inclusion()
    
    def set_category(self,perplexity):
        return 1 if perplexity <= self.level_ai else 0
    
    
    def exclusion_inclusion(self):
        perplexity_temp = []
        print(len(self.perplexity_lines))
        
        for index_ in range(1, len(self.perplexity_lines)-1):
            print(index_)
            perplexity = self.perplexity_lines[index_]
            
            is_matches_the_antecedent = self.set_category(perplexity) == self.set_category(self.perplexity_lines[index_ - 1])
            is_corresponds_to_the_successor = self.set_category(perplexity) == self.set_category(self.perplexity_lines[index_ + 1])
            
            try:
                is_matches_the_antecedent_pre = self.set_category(perplexity) == self.set_category(self.perplexity_lines[index_ - 2])
                is_corresponds_to_the_successor_after = self.set_category(perplexity) == self.set_category(self.perplexity_lines[index_ + 2])
            except: pass
             
            if is_matches_the_antecedent  and  is_corresponds_to_the_successor:
                
                perplexity_temp.append(perplexity)
                    
            else:
                if is_matches_the_antecedent_pre and  is_corresponds_to_the_successor_after :
                    pass
                
                perplexity_temp.append(perplexity + STEP)
                
        print(perplexity_temp)
        

optimizer = Optimizer(values, 200)
        
