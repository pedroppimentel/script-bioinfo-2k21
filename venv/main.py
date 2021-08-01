import json

#define uma classe para a tabela de predicoes
class predictions: 
    def __init__(self, alifrom, alito, strand, e_value, score, length): 
        self.alifrom = alifrom 
        self.alito = alito
        self.strand = strand
        self.e_value = e_value
        self.score = score
        self.length = length
        
#define uma classe para as anotacoes
class annotation3L: 
    def __init__(self, FROM, TO, LENGTH, SENSE): 
        self.FROM = FROM 
        self.TO = TO
        self.LENGTH = LENGTH
        self.SENSE = SENSE

def getIndex(line, field):
    return line.find(field) + len(field) + 2

def getLastIndex(line, field):
    return line.find('-', getIndex(line, field))

class finalResults: 
    def __init__(self, ann, pred): 
        self.ann = ann 
        self.pred = pred 

def setFinalResults(annotation, predict):
  resultados.append (
                    finalResults(
                    ann=(
                        annotation3L(
                            annotation.FROM,
                            annotation.TO,
                            annotation.LENGTH,
                            annotation.SENSE
                        )
                    ),
                    pred=(
                        predictions(
                            predict.alifrom,   #alifrom
                            predict.alito,   #ali to
                            predict.strand,     #strand
                            predict.e_value, #e_value
                            predict.score,  #score
                            predict.length, #length
                        )
                    )
                
        ))

filename = "../predictionsResults.tbl"

with open(filename) as f:
    content = f.readlines()
   
predictionList = [] 

#percorre linha a linha do arquivo e atribui os valores na lista de obj
for idx in range(2, 159):
    predictionList.append ( predictions(
        content[idx][82:90],   #alifrom
        content[idx][91:99],   #ali to
        content[idx][130],     #strand
        content[idx][134:143], #e_value
        content[idx][144:150],  #score
        content[idx][304:312]  #length
        ))

predictionList.sort(key=lambda x : x.alifrom)

# for predict in predictionList:
#    print("PRED---FROM--%2s---TO--%2s---LENGTH--%2s---VALUE--%2s---SCORE--%2s---SENSE--%2s---CLASSIF--Copia" 
#          % (predict.alifrom.strip(), predict.alito.strip(), predict.length.strip(), predict.e_value.strip(), predict.score.strip(), predict.strand.strip()))
    
filename = "../Anotacao_Copia_Cromo-3L.txt"

with open(filename) as f:
    content = f.readlines()

# cria uma lista de dados       
annotation3LList = [] 

#percorre linha a linha do arquivo e atribui os valores na lista de obj
for item in content:
    annotation3LList.append ( annotation3L(
        item[ (getIndex(item, "FROM")) : (getLastIndex(item, "FROM"))],   #alifrom
        item[ (getIndex(item, "TO")) : (getLastIndex(item, "TO"))],   #ali to
        item[ (getIndex(item, "LENGTH")) : (getLastIndex(item, "LENGTH"))],     #strand
        item[ (getIndex(item, "SENSE")) : (getLastIndex(item, "SENSE"))],     #strand
        ))
    
annotation3LList.sort(key=lambda x : x.FROM)   

resultados = []

for annotation in annotation3LList:
    for predict in predictionList:
        if((predict.strand == '+' and annotation.SENSE == 'Direct') or 
           (predict.strand == '-' and annotation.SENSE == 'Reverse')):
        #if(predict.strand == '+' and annotation.SENSE == 'Direct'):    
            _alifrom = int(predict.alifrom, 16)
            _from = int(annotation.FROM, 16)
            _alito = int(predict.alito, 16)
            _to = int(annotation.TO, 16)
            
            if(_alifrom >= _from and _alito <= _to):
                setFinalResults(annotation, predict)
            #elif(_alifrom >= _from and _alito > _to):
            #    setFinalResults(annotation, predict)
            #elif(_alifrom < _from and _alito <= _to):
            #    setFinalResults(annotation, predict)
                
with open('resultadosComparacao.txt', 'w') as frc:
    for resultado in resultados:
      frc.write('ANNO---FROM--%s---TO--%s---LENGTH--%s---SENSE--%s---CLASSIF--Copia\n' %
                (resultado.ann.FROM.strip(), resultado.ann.TO.strip(), resultado.ann.LENGTH.strip(), resultado.ann.SENSE.strip()))
      frc.write('PRED---FROM--%s---TO--%s---LENGTH--%s---SENSE--%s---VALUE--%s---SCORE--%s---CLASSIF--Copia\n' %
                (resultado.pred.alifrom.strip(), resultado.pred.alito.strip(), resultado.pred.length.strip(), resultado.pred.strand.strip(), 
                 resultado.pred.e_value.strip(), resultado.pred.score.strip()))
      frc.write('\n')
      
with open('predicoesExtraidas.txt', 'w') as fpe:
    for pred in predictionList:
      fpe.write('PRED---FROM--%s---TO--%s---LENGTH--%s---SENSE--%s---VALUE--%s---SCORE--%s---CLASSIF--Copia\n' %
                (pred.alifrom.strip(), pred.alito.strip(), pred.length.strip(), pred.strand.strip(), 
                 pred.e_value.strip(), pred.score.strip()))
      fpe.write('\n')      