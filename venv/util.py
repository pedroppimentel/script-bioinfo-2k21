#carrega arquivos
filename = "Cromo-3L.fasta"

with open(filename) as f:
    content = f.read().replace('\n', '')

content = content.replace('>3L type=golden_path_region; loc=3L:1..28110227; ID=3L; dbxref=GB:AE014296,GB:AE014296,REFSEQ:NT_037436; MD5=3c3ea06b22af8cc59809dbf8d154791e; length=28110227; release=r6.08; species=Dmel;',
 "")

sequence = ""

for line in content:
    sequence = sequence + line

# with open('Cromo-3L-Remodelado.txt', 'w') as f:
#     print(content, file=f) 

tabela = "tabela.tbl"

with open(tabela) as t:
    content2 = t.readlines()

#define uma classe para a tabela de predicoes
class prediction: 
    def __init__(self, alifrom, alito, strand, e_value, score, length): 
        self.alifrom = alifrom 
        self.alito = alito
        self.strand = strand
        self.e_value = e_value
        self.score = score
        self.length = length
   
# cria uma lista de dados       
predictionList = [] 

#percorre linha a linha do arquivo e atribui os valores na lista de obj
for idx in range(2, 159):
    predictionList.append ( prediction(
        content2[idx][82:90],   #alifrom
        content2[idx][91:99],   #ali to
        content2[idx][130],     #strand
        content2[idx][134:143], #e_value
        content2[idx][144:150],  #score
        content2[idx][297:314]  #length
        ))

predictionList.sort(key=lambda x : x.alifrom)

# j = 0
# for obj in predictionList:
#     j = j + 1
#     print(j, obj.alifrom, obj.alito, obj.strand, obj.e_value, obj.score)

i = 0
with open('Cromo-3L-Remodelado.fasta', 'w') as f:
    for item in predictionList:
        i = i + 1
        #+  " from " + item.alifrom + " to " + item.alito + " strand " + item.strand
        print("seq" + str(i) , file=f) 
        if(item.strand == '+'):
            print(content[int(item.alifrom)-1:int(item.alito)-1], file=f)
        if(item.strand == '-'):
            print(content[int(item.alito)-1:int(item.alifrom)-1], file=f)

# print(content[80:161])
