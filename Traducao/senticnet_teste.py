from senticnet.senticnet import SenticNet

teste = []
sn = SenticNet('pt')
concept_info = sn.concept('amor')
polarity_value = sn.polarity_value('amor')
polarity_intense = sn.polarity_intense('amor')
moodtags = sn.moodtags('amor')
semantics = sn.semantics('amor')
sentics = sn.sentics('amor')

teste.append(concept_info)

print(teste)