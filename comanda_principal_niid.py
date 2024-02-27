import os
import glob
import shlex
import subprocess 
import concurrent.futures
from itertools import product

limpa_arquivos_csv= []
padroes =   [
                # 'TESTES/IID/LABELS/*.csv', 
                # 'TESTES/IID/LOG_EVALUATE/*.csv', 
                # 'TESTES/IID/LOG_ACERTOS/*.csv',
                'TESTES/NIID/LABELS/*.csv', 
                'TESTES/NIID/LOG_EVALUATE/*.csv',  
                'TESTES/NIID/LOG_ACERTOS/*.csv',
                'TESTES/NIID/GRAFICOS/*',
                'TESTES/NIID/LABELS/GRAFICOS/*.png',
                'TESTES/NIID/LOG_ACERTOS/GRAFICOS/*.png',

                
            ]

for i in padroes:
    limpa_arquivos_csv.extend(glob.glob(i))

try:
    for arquivo in limpa_arquivos_csv:
        os.remove(arquivo)
    
except subprocess.CalledProcessError as e:
    print(f'Erro: {e}')

arquivos_teste= [
                    'simulacao_principal.py'
                ]


def executar_arquivo(arquivo):

    try:
        modelos = ['DNN', 'CNN']
        niid_iid = ['NIID']        
        ataques = ['ALTERNA_INICIO', 'ATACANTES', 'EMBARALHA', 'INVERTE_TREINANDO', 'INVERTE_SEM_TREINAR', 'INVERTE_CONVEGENCIA', 'ZEROS', 'RUIDO_GAUSSIANO', 'NORMAL']
        data_set = ['MNIST', 'CIFAR10']                        
        alpha_dirichlet = [0.1, 0.5, 1]
        noise_gaussiano = [0.1,0.5,0.8]
        round_inicio = [2, 4, 6, 8]
        per_cents_atacantes = [30,60,80,85,88,90,95]
        
        combinacoes_unicas = set() 

        for i, j, k, l, m, n, o, p in product(niid_iid, ataques, data_set, modelos, round_inicio, per_cents_atacantes, noise_gaussiano, alpha_dirichlet):
            combinacao = (i, j, k, l, m, n, o, p)  
            
            if i == 'IID' and p > 0:
                print('Combinação inválida. A execução será interrompida.')
                continue

            if j != 'RUIDO_GAUSSIANO' and o > 0:
                print('Combinação inválida. A execução será interrompida.')
                continue

            if (k == 'MNIST' and l == 'CNN') or (k == 'CIFAR10' and l == 'DNN'):
                print('Combinação inválida. A execução será interrompida.')
                continue


            if combinacao not in combinacoes_unicas:                  
                combinacoes_unicas.add(combinacao)           
            else:
                continue

            print(f'Executando {arquivo}')                                    
                
            comando = f'python3 {arquivo} --iid_niid {i} --modo_ataque {j} --dataset {k} --modelo_definido {l} --round_inicio {m} --per_cents_atacantes {n} --noise_gaussiano {o} --alpha_dirichlet {p}'
            print(f'\n\n################################################################################################')
            print(f'\n\n{comando}\n\n')
            print(f'################################################################################################\n\n')
            subprocess.run(shlex.split(comando), check=True)

            print(f'Executou com sucesso: {arquivo}')
            
    except subprocess.CalledProcessError as e:
        print(f'Erro: {arquivo}')

max_threads = 1

with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    resultados = list(executor.map(executar_arquivo, arquivos_teste))    
