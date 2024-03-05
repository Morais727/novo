import os
import glob
import shlex
import subprocess 
import concurrent.futures
from itertools import product

arquivos_teste = ['simulacao_principal.py']

def executar_arquivo(arquivo):
    try:
        num_round = [5,5,15]
        total_clients = [5,10,15,20]
        modelos = ['CNN','DNN']
        niid_iid = ['NIID']        
        ataques = ['ALTERNA_INICIO', 'ATACANTES', 'EMBARALHA', 'INVERTE_TREINANDO', 'INVERTE_SEM_TREINAR', 'INVERTE_CONVEGENCIA', 'ZEROS', 'RUIDO_GAUSSIANO', 'NORMAL']
        data_set = ['MNIST', 'CIFAR10']                        
        alpha_dirichlet = [0.1]
        noise_gaussiano = [0.1]
        round_inicio = [2,  8]
        per_cents_atacantes = [30, 60]
       
        combinacoes_unicas = set() 

        for i, j, k, l, m, n, o, p, q, r in product(niid_iid, ataques, data_set, modelos, round_inicio, per_cents_atacantes, noise_gaussiano, alpha_dirichlet, num_round, total_clients):
            combinacao = (i, j, k, l, m, n, o, p, q, r) 
            if i == 'NIID' and p == 0: 
                print('NON IID com Dirichlet = 0')               
                continue

            if i == 'IID' and p > 0: 
                print('IID com Dirichlet > 0', i, p)                
                continue

            if j != 'RUIDO_GAUSSIANO' and o > 0:
                print('RUIDO_GAUSSIANO > 0', j, p)   
                continue

            if (k == 'MNIST' and l == 'CNN') or (k == 'CIFAR10' and l == 'DNN'):
                print("Combinacao incorreta", k, l)
                continue

            if combinacao not in combinacoes_unicas:                  
                combinacoes_unicas.add(combinacao)
            else:
                continue 

            print(f'Executando {arquivo}')                
            comando = f'python3 {arquivo} --iid_niid {i} --modo_ataque {j} --dataset {k} --modelo_definido {l} --round_inicio {m} --per_cents_atacantes {n} --noise_gaussiano {o} --alpha_dirichlet {p} --num_rounds {q} --total_clients {r}'
            print(f'\n\n################################################################################################')
            print(f'\n\n{comando}\n\n')
            print(f'################################################################################################\n\n')
            subprocess.run(shlex.split(comando), check=True)

            print(f'Executou com sucesso: {arquivo}')

    except subprocess.CalledProcessError as e:
        print(f'Erro ao executar o arquivo: {e}')
    except Exception as e:
        print(f'Erro inesperado: {e}')

max_threads = 1
for i in range(50):
    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        resultados = list(executor.map(executar_arquivo, arquivos_teste))
