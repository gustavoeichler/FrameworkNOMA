# -*- coding: utf-8 -*-
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.acl.messages import ACLMessage
from pade.behaviours.protocols import FipaContractNetProtocol
from sys import argv
from random import uniform
import numpy as np
import matlab.engine


class CompContNet1(FipaContractNetProtocol):
    '''CompContNet1

       Initial FIPA-ContractNet Behaviour that sends CFP messages
       to other feeder agents asking for restoration proposals.
       This behaviour also analyzes the proposals and selects the
       one it judges to be the best.'''

    def __init__(self, agent, message):
        super(CompContNet1, self).__init__(
            agent=agent, message=message, is_initiator=True)
        self.cfp = message

    def handle_all_proposes(self, proposes):
        """
        """

        super(CompContNet1, self).handle_all_proposes(proposes)

        best_proposer = None
        higher_power = -300.0
        other_proposers = list()
        display_message(self.agent.aid.name, 'Analyzing proposals...')

        i = 1
        Propostas = list()
        for message in proposes:
            Propostas.append(message.content)
        display_message(self.agent.aid.name, f'As propostas enviadas foram {Propostas}')
        eng = matlab.engine.start_matlab()
        saida = eng.MultiAgentSystem(float(Propostas[0]),float(Propostas[1]),float(Propostas[2]))
        
        # logic to select proposals by the higher available power.
        for message in proposes:
            content = message.content
            power = float(content)
            display_message(self.agent.aid.name,
                            'Analisando a proposta {i}'.format(i=i))
            display_message(self.agent.aid.name,
                            'Ganho de Canal: {pot}'.format(pot=power))
            i += 1
            #if power > higher_power:
            #    if best_proposer is not None:
            #        other_proposers.append(best_proposer)

            #    higher_power = power
            #    best_proposer = message.sender
            #else:
            #    other_proposers.append(message.sender)
        
        best_proposer = [proposes[int(saida[1][0])-1], proposes[int(saida[1][1])-1]]
        
        
        for elem in proposes:
            if elem not in best_proposer:
                notpaired = elem.sender
        other_proposers = [notpaired]
        best_proposer = [proposes[int(saida[1][0])-1].sender, proposes[int(saida[1][1])-1].sender]
        display_message(self.agent.aid.name,
                        f'Os usuários pareados foram {best_proposer[0].name.split("@")[0]} e {best_proposer[1].name.split("@")[0]}')
                        

        if other_proposers != []:
            display_message(self.agent.aid.name,
                            'Enviando PROPOSTA_REJEITADA para o usuário não pareado...')
            answer = ACLMessage(ACLMessage.REJECT_PROPOSAL)
            answer.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
            answer.set_content('')
            for agent in other_proposers:
                answer.add_receiver(agent)

            self.agent.send(answer)
        
        if best_proposer != []:
            display_message(self.agent.aid.name,
                               'Enviando PROPOSTA_ACEITA para os usuários pareados...')

            answer = ACLMessage(ACLMessage.ACCEPT_PROPOSAL)
            answer.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
            answer.set_content('OK')
            for agent in best_proposer:
                answer.add_receiver(agent)

            self.agent.send(answer)

    def handle_inform(self, message):
        """
        """
        super(CompContNet1, self).handle_inform(message)

        display_message(self.agent.aid.name, 'INFORM message received')

    def handle_refuse(self, message):
        """
        """
        super(CompContNet1, self).handle_refuse(message)

        display_message(self.agent.aid.name, 'REFUSE message received')

    def handle_propose(self, message):
        """
        """
        super(CompContNet1, self).handle_propose(message)

        display_message(self.agent.aid.name, f'PROPOSTA recebida de: {message.sender.name.split("@")[0]}')


class CompContNet2(FipaContractNetProtocol):
    '''CompContNet2

       FIPA-ContractNet Participant Behaviour that runs when an agent
       receives a CFP message. A proposal is sent and if it is selected,
       the restrictions are analized to enable the restoration.'''

    def __init__(self, agent):
        super(CompContNet2, self).__init__(agent=agent,
                                           message=None,
                                           is_initiator=False)

    def handle_cfp(self, message):
        """
        """
        self.agent.call_later(1.0, self._handle_cfp, message)

    def _handle_cfp(self, message):
        """
        """
        super(CompContNet2, self).handle_cfp(message)
        self.message = message

        display_message(self.agent.aid.name, 'CFP Recebida')

        answer = self.message.create_reply()
        answer.set_performative(ACLMessage.PROPOSE)
        answer.set_content(str(self.agent.pot_disp))
        self.agent.send(answer)
        display_message(self.agent.aid.name,f'O meu ganho de canal é {self.agent.ganho}')

    def handle_reject_propose(self, message):
        """
        """
        super(CompContNet2, self).handle_reject_propose(message)

        display_message(self.agent.aid.name,
                        'mensagem de PROPOSTA_REJEITADA recebida')

    def handle_accept_propose(self, message):
        """
        """
        super(CompContNet2, self).handle_accept_propose(message)

        display_message(self.agent.aid.name,
                        'mensagem de PROPOSTA_ACEITA recebida')

        answer = message.create_reply()
        answer.set_performative(ACLMessage.INFORM)
        answer.set_content('OK')
        self.agent.send(answer)


class AgenteControlador(Agent):

    def __init__(self, aid, participants):
        super(AgenteControlador, self).__init__(aid=aid, debug=False)

        message = ACLMessage(ACLMessage.CFP)
        message.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
        message.set_content('60.0')

        for participant in participants:
            message.add_receiver(AID(name=participant))

        self.call_later(8.0, self.launch_contract_net_protocol, message)

    def launch_contract_net_protocol(self, message):
        comp = CompContNet1(self, message)
        self.behaviours.append(comp)
        comp.on_start()


class AgenteDispositivo(Agent):

    def __init__(self, aid, distancia):
        super(AgenteDispositivo, self).__init__(aid=aid, debug=False)
        eta = 3.6
        self.distancia = distancia
        h = (np.power(np.sqrt(self.distancia),-eta))*(np.random.randn() + 1j*np.random.randn())/np.sqrt(2)
        g = np.power(np.abs(h),2)
        self.ganho = 10*np.log10(g)
        self.pot_disp = self.ganho
        
        comp = CompContNet2(self)

        self.behaviours.append(comp)

if __name__ == "__main__":

    agents_per_process = 1
    c = 0
    agents = list()
    for i in range(agents_per_process):
        port = int(argv[1]) + c        
        k = 1000
        participants = list()

        agent_name = 'AgenteDispositivo1@localhost:{}'.format(port + k)
        participants.append(agent_name)
        agente_part_1 = AgenteDispositivo(AID(name=agent_name), uniform(20.0,30.0))
        agents.append(agente_part_1)

        agent_name = 'AgenteDispositivo2@localhost:{}'.format(port + 2*k)
        participants.append(agent_name)
        agente_part_3 = AgenteDispositivo(AID(name=agent_name), uniform(40.0, 75.0))
        agents.append(agente_part_3)

        agent_name = 'AgenteDispositivo3@localhost:{}'.format( port + 3*k)
        participants.append(agent_name)
        agente_part_1 = AgenteDispositivo(AID(name=agent_name), uniform(75.0, 150.0))
        agents.append(agente_part_1)

        agent_name = 'AgenteControlador@localhost:{}'.format(port)
        agente_init_1 = AgenteControlador(AID(name=agent_name), participants)
        agents.append(agente_init_1)

        c += 1000
    
    start_loop(agents)
