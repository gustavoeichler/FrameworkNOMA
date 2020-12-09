function [Saida] = MultiAgentSystem(U1,U2,U3)
%MULTIAGENTSYSTEM Summary of this function goes here
%   Detailed explanation goes here
No = - 39;        %Noise power in dBm
no = (10^-3)*db2pow(No);       %Noise power in linear scale
Possiveis_Pares = db2pow([U1 U2;
                   U1 U3;
                   U2 U1;
                   U2 U3;
                   U3 U1;
                   U3 U2]);
Possiveis_Pares_Nome = {'U1','U2';
                   'U1', 'U3';
                   'U2', 'U1';
                   'U2' ,'U3';
                   'U3', 'U1';
                   'U3', 'U2'};               
               
               
for i = (1: length(Possiveis_Pares))
    g1 = Possiveis_Pares(i,2);
    g2 = Possiveis_Pares(i,1);
    aux = 1;
    index = 1;
    for pt_trans = 22
        for a2 = (0.5:0.001:0.999)
            R_Far(aux,index,i) = log2(1+(((10^-3)*db2pow(pt_trans).*a2.*g1./(((10^-3)*db2pow(pt_trans).*(1-a2).*g1+no)))));
            R_Near(aux,index,i)= log2(1+(((10^-3)*db2pow(pt_trans).*(1-a2).*g2/no)));
            
            R_mean(aux,index,i) = (R_Far(aux,index,i)+R_Near(aux,index,i))/2;
            Fairness_index(aux,index,i) = (R_Far(aux,index,i)+R_Near(aux,index,i))^2/(2*(R_Far(aux,index,i)^2+R_Near(aux,index,i)^2));
            escolha(aux,index,i) = R_mean(aux,index,i)*Fairness_index(aux,index,i);
            aux=1+aux;
        end
        aux = 1;
        index = index+1;
    end
end

[M,Idx] = max(R_mean,[],'all','linear');

[a,b,c] = ind2sub(size(R_mean),Idx);
[MF,IdxF] = max(Fairness_index(:,:,c),[],'all','linear');
[af] = ind2sub(size(Fairness_index(:,:,c)),IdxF);
Potencia =(0.5:0.001:0.999);
Pot = Potencia(af);
Par = Possiveis_Pares_Nome(c,:);
display(Par);
display(Pot);
display(R_Near(af,b,c));
display(R_Far(af,b,c));
display(R_mean(af,b,c));

figure1 = figure;
Plot_R_near = R_Near(:,:,c);
Plot_R_far = R_Far(:,:,c);
Plot_R_mean = R_mean(:,:,c);

plot(linspace(0.5,0.999,length(Potencia)),Plot_R_near);

hold on;
plot(linspace(0.5,0.999,length(Potencia)),Plot_R_far);
hold on;
plot(linspace(0.5,0.999,length(Potencia)),Plot_R_mean);
legend('Near','Far','Mean');
Saida = {1-Pot,Par,Pot};
saveas(figure1,'Plot.jpg')

end

