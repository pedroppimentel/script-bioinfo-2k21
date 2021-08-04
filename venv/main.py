resultados = []

class predictions: 
    def __init__(self, id, alifrom, alito, strand, e_value, score, length): 
        self.id = id
        self.alifrom = alifrom 
        self.alito = alito
        self.strand = strand
        self.e_value = e_value
        self.score = score
        self.length = length
        
class annotation3L: 
    def __init__(self, id, FROM, TO, LENGTH, SENSE): 
        self.id = id
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
                        annotation.id,
                        annotation.FROM,
                        annotation.TO,
                        annotation.LENGTH,
                        annotation.SENSE
                    )
                ),
                pred=(
                    predictions(
                        predict.id,
                        predict.alifrom,   #alifrom
                        predict.alito,   #ali to
                        predict.strand,     #strand
                        predict.e_value, #e_value
                        predict.score,  #score
                        predict.length, #length
                    )
                )
                    
            ))


tabelaFilePath = "../tabelas/tabela-cromo3l-insetos.tbl"
anotacoesFilePath = "../tabelas/Anotacao_Copia_Cromo-3L.txt"
resultadoFilePath = "../resultados/resultadosComparacaoC3LI.txt"
resultadoPredicoesFilePath = "../resultados/predicoesExtraidasC3LI.txt"

filename = tabelaFilePath

with open(filename) as f:
    content = f.readlines()
   
predictionList = [] 

for idx in range(2, 110):
    predictionList.append ( predictions(
        idx,
        content[idx][89:97],   #alifrom
        content[idx][98:106],   #ali to
        content[idx][137],     #strand
        content[idx][143:150], #e_value
        content[idx][152:157],  #score
        content[idx][311:319]  #length
        ))

predictionList.sort(key=lambda x : x.alifrom)
    
filename = anotacoesFilePath

with open(filename) as f:
    content = f.readlines()

annotation3LList = [] 

for idx, item in enumerate(content):
    annotation3LList.append ( annotation3L(
        idx,
        item[ (getIndex(item, "FROM")) : (getLastIndex(item, "FROM"))],   #alifrom
        item[ (getIndex(item, "TO")) : (getLastIndex(item, "TO"))],   #ali to
        item[ (getIndex(item, "LENGTH")) : (getLastIndex(item, "LENGTH"))],     #strand
        item[ (getIndex(item, "SENSE")) : (getLastIndex(item, "SENSE"))],     #strand
        ))
    
annotation3LList.sort(key=lambda x : x.FROM)   

for annotation in annotation3LList:
    for predict in predictionList:
        if((predict.strand == '+' and annotation.SENSE == 'Direct') or 
           (predict.strand == '-' and annotation.SENSE == 'Reverse')):   
            _alifrom = int(predict.alifrom, 10)
            _from = int(annotation.FROM, 10)
            _alito = int(predict.alito, 10)
            _to = int(annotation.TO, 10)
            
            if(_alifrom >= _from and _alito <= _to):
                setFinalResults(annotation, predict)
                
with open(resultadoFilePath, 'w') as frc:
    for res in resultados:
        frc.write('ANNO---FROM--%s---TO--%s---LENGTH--%s---SENSE--%s---CLASSIF--Copia\n' %
                (res.ann.FROM.strip(), res.ann.TO.strip(), res.ann.LENGTH.strip(), res.ann.SENSE.strip()))
        
        if (res.ann.SENSE == "Reverse"):
            frc.write('PRED---FROM--%s---TO--%s---LENGTH--%s---SENSE--%s---VALUE--%s---SCORE--%s---CLASSIF--Copia\n' %
                (res.pred.alito.strip(), res.pred.alifrom.strip(), res.pred.length.strip(), res.pred.strand.strip(), 
                 res.pred.e_value.strip(), res.pred.score.strip())) 
        else:
            frc.write('PRED---FROM--%s---TO--%s---LENGTH--%s---SENSE--%s---VALUE--%s---SCORE--%s---CLASSIF--Copia\n' %
                (res.pred.alifrom.strip(), res.pred.alito.strip(), res.pred.length.strip(), res.pred.strand.strip(), 
                 res.pred.e_value.strip(), res.pred.score.strip()))    
        frc.write('\n')
      
with open(resultadoPredicoesFilePath, 'w') as fpe:
    for pred in predictionList:
      fpe.write('PRED---FROM--%s---TO--%s---LENGTH--%s---SENSE--%s---VALUE--%s---SCORE--%s---CLASSIF--Copia\n' %
                (pred.alifrom.strip(), pred.alito.strip(), pred.length.strip(), pred.strand.strip(), 
                 pred.e_value.strip(), pred.score.strip()))
      fpe.write('\n')      