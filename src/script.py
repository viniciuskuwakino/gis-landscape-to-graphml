import csv
from csv import DictReader

data_file_path = './data/SoilUse_1.csv'
data_coords_file_path = './data/coords.csv'
output_graphml_file = './output/mainSoilUse.graphml'
output_csv_file = './output/mainSoilUse.csv'

def sem_repeticao(value, solos_dict):
    for i in solos_dict:
        if value['Area_m2'] == solos_dict[i]['Area_m2']:
            if value['Fid_1'] == solos_dict[i]['Fid_1']:
                if value['Last_last'] == solos_dict[i]['Last_last']:
                    return False
    
    return True


def filtrar_repetidos():
    solos_dict = dict()

    with open(data_file_path, encoding='utf8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for index, value in enumerate(csv_reader):
            if not solos_dict:
                solos_dict.update({index: value})
            else:
                if sem_repeticao(value, solos_dict):
                    solos_dict.update({index: value})
    
    return solos_dict


def separar_dicionarios(solos_dict, dicionario_fid_last, dicionario_solos):
    for i in solos_dict:
        if solos_dict[i]['Fid_1'] == solos_dict[i]['Last_last']:
            dicionario_fid_last.update({i: solos_dict[i]})
        else:
            dicionario_solos.update({i: solos_dict[i]})


def novo_chave_valor(index, dicio_principal, dicio_solo, dicio_fid_last):
    aux_dict = dict()
    
    aux_dict['Uso_solo_1'] = dicio_solo['Uso_solo']
    aux_dict['Uso_solo_2'] = dicio_fid_last['Uso_solo']
    aux_dict['Municipio_1'] = dicio_solo['Municipio']
    aux_dict['Municipio_2'] = dicio_fid_last['Municipio']
    aux_dict['Area_m2_1'] = dicio_solo['Area_m2']
    aux_dict['Area_m2_2'] = dicio_fid_last['Area_m2']
    aux_dict['Fid_1'] = dicio_solo['Fid_1']
    aux_dict['Last_last'] = dicio_solo['Last_last']
    aux_dict['Cn_mancha_1'] = dicio_solo['Cn_mancha1']
    aux_dict['Cn_mancha_2'] = dicio_solo['Cn_mancha2']
    aux_dict['Altitude_mancha_1'] = dicio_solo['Altitude_mancha1']
    aux_dict['Altitude_mancha_2'] = dicio_solo['Altitude_mancha2']
    aux_dict['Dif_altitude'] = dicio_solo['Dif_altitude']
    aux_dict['Comprimento'] = dicio_solo['Comprimento']
    aux_dict['Dif_cn'] = dicio_solo['Dif_cn']
    aux_dict['Valoracao'] = dicio_solo['Valoracao']
    
    dicio_principal.update({index: aux_dict})


def unificar_dicionarios(dicionario_principal, dicionario_fid_last, dicionario_solos):
    for i in dicionario_solos:
        for j in dicionario_fid_last:
            if dicionario_solos[i]['Last_last'] == dicionario_fid_last[j]['Last_last']:
                novo_chave_valor(i, dicionario_principal, dicionario_solos[i], dicionario_fid_last[j])
                break


def converter_csv():
    with open(output_csv_file, mode='w', newline='', encoding='utf8') as file:
        new_file = csv.DictWriter(file, fieldnames=dicionario_principal[0].keys())
        new_file.writeheader()

        for index, dicionario in dicionario_principal.items():
            new_file.writerow(dicionario)


def gerar_graphml():
    # Dicionario para adicionar os nós existentes e dados de latitude e longitude
    nodes_dict = {}

    # Atributos dos nós
    node_attributes = [
        ['color', 'string'],
        ['uso_solo', 'string'],
        ['municipio', 'string'],
        ['area', 'double'],
        ['cn', 'int'],
        ['id', 'int'],
        ['altitude', 'double'],
        ['latitude', 'double'],
        ['longitude', 'double'],
    ]

    # Atributos das arestas
    edge_attributes = [
        ['dif_cn', 'int'],
        ['dif_altitude', 'double'],
        ['comprimento', 'double'],
        ['weight', 'double'],
        ['color', 'string']
    ]

    # Retorna o nó ou None
    def get_node(id):
        return nodes_dict.get(id, None)

    def replace_comma(attr):
        return attr.replace(",", ".")

    def add_node(id, attr):
        if get_node(id) is None:
            nodes_dict[id] = attr

    # Adiciona dados das coordenadas de cada nó
    def add_coords():
        with open(data_coords_file_path, encoding='utf8', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for i in csv_reader:
                nodes_dict[i['fid_1']]['Latitude'] = replace_comma(i['COORD_X'])
                nodes_dict[i['fid_1']]['Longitude'] = replace_comma(i['COORD_Y'])

    # Define a cor de acordo com o CN
    def set_color(cn):
        cn_value = int(cn)

        if cn_value < 20: # Azul
            return '#3498DB'
        elif 20 <= cn_value < 40: # Verde
            return '#27AE60'
        elif 40 <= cn_value < 60: # Amarelo
            return '#F4D03F'
        elif 60 <= cn_value < 80: # Laranja
            return '#E67E22'
        else: # Vermelho
            return '#F70C3C'


    # Checa o peso da aresta, pois caso seja 0, a mesma é descartada 
    def check_weight(weight):
        if weight == '0':
            return '0.0001'

        return weight

    # Define se a valoracao é menor, igual ou maior que 0
    def set_val(weight):
        valoracao = int(float(weight))
        
        if valoracao > 0:
            # return 'Increase'
            return '#F70C3C'
        elif valoracao < 0:
            # return 'Decrease'
            return '#3498DB'
        else:
            # return 'Zero'
            return '#85929E'


    # Formatação para inserção de um nó
    def formatted_node(attr):

        if attr['Fid_1'] == attr['Last_last']:
            return f'''<node id="n{attr['n_id']}">
    <data key="cn">{attr['Cn_mancha2']}</data>
    <data key="color">{set_color(attr['Cn_mancha2'])}</data>
    <data key="id">{attr['Last_last']}</data>
    <data key="altitude">{replace_comma(attr['Altitude_mancha2'])}</data>
    <data key="area">{replace_comma(attr['Area_m2'])}</data>
    <data key="municipio">{attr['Municipio']}</data>
    <data key="uso_solo">{attr['Uso_solo']}</data>
    <data key="latitude">{attr['Latitude']}</data>
    <data key="longitude">{attr['Longitude']}</data>
</node>
'''
        else:

            return f'''<node id="n{attr['n_id']}">
    <data key="cn">{attr['Cn_mancha1']}</data>
    <data key="color">{set_color(attr['Cn_mancha1'])}</data>
    <data key="id">{attr['Fid_1']}</data>
    <data key="altitude">{replace_comma(attr['Altitude_mancha1'])}</data>
    <data key="area">{replace_comma(attr['Area_m2'])}</data>
    <data key="municipio">{attr['Municipio']}</data>
    <data key="uso_solo">{attr['Uso_solo']}</data>
    <data key="latitude">{attr['Latitude']}</data>
    <data key="longitude">{attr['Longitude']}</data>
</node>
'''

    def get_source_target(solo):
        node_1 = get_node(solo['Fid_1'])
        node_2 = get_node(solo['Last_last'])

        if node_1['Fid_1'] == node_1['Last_last'] and node_2['Fid_1'] == node_2['Last_last']:
            if node_1['Altitude_mancha2'] > node_2['Altitude_mancha2']:
                source = node_1['n_id']
                target = node_2['n_id']
            else:
                source = node_2['n_id']
                target = node_1['n_id']

        elif node_1['Fid_1'] == node_1['Last_last']:
            if node_1['Altitude_mancha2'] > node_2['Altitude_mancha1']:
                source = node_1['n_id']
                target = node_2['n_id']
            else:
                source = node_2['n_id']
                target = node_1['n_id']

        elif node_2['Fid_1'] == node_2['Last_last']:
            if node_1['Altitude_mancha1'] > node_2['Altitude_mancha2']:
                source = node_1['n_id']
                target = node_2['n_id']
            else:
                source = node_2['n_id']
                target = node_1['n_id']

        else:

            if node_1['Altitude_mancha1'] > node_2['Altitude_mancha1']:
                source = node_1['n_id']
                target = node_2['n_id']
            else:
                source = node_2['n_id']
                target = node_1['n_id']
        
        return source, target


    # Formatação para inserção de uma aresta
    # Peso e Valoracao sao atributos com mesmos valores para melhor
    # visualizacao no Gephi
    def formatted_edge(edge_id, solo):

        weight = replace_comma(solo['Valoracao'])
        source, target = get_source_target(solo)
        

        return f'''<edge id="e{edge_id}" source="n{source}" target="n{target}">
    <data key="comprimento">{replace_comma(solo['Comprimento'])}</data>
    <data key="dif_altitude">{replace_comma(solo['Dif_altitude'])}</data>
    <data key="dif_cn">{solo['Dif_cn']}</data>
    <data key="weight">{check_weight(weight)}</data>
    <data key="color">{set_val(weight)}</data>
</edge>
'''

    with open(output_graphml_file, 'w') as file:

        # Escreva o cabeçalho do arquivo GraphML
        file.write('''<?xml version="1.0" encoding="UTF-8"?>\n<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">''')

        # Adicionar atributos de nos
        for node_attr in node_attributes:
            file.write(f'<key id="{node_attr[0]}" for="node" attr.name="{node_attr[0]}" attr.type="{node_attr[1]}"/>\n')
        
        # Adicionar atributos de arestas
        for edge_attr in edge_attributes:
            file.write(f'<key id="{edge_attr[0]}" for="edge" attr.name="{edge_attr[0]}" attr.type="{edge_attr[1]}"/>\n')


        # Iniciando grafo
        file.write('<graph id="G" edgedefault="directed">\n')
        
        # Adicionar nós num dicionario
        for index, dicionario in solos_dict.items():
            add_node(dicionario['Fid_1'], dicionario)
        
        # Adicionar as coordenadas no dicionario dos nós
        add_coords()

        # Adiciona no arquivo o nó formatado
        node_id = 0
        for fid, attr in nodes_dict.items():
            attr['n_id'] = node_id
            file.write(formatted_node(attr))
            
            node_id += 1


        edge_id = 0
        for i, solo in dicionario_principal.items():
            file.write(formatted_edge(edge_id, solo))
            edge_id += 1


        file.write('</graph>\n')
        file.write('</graphml>\n')

if __name__ == '__main__':
    solos_dict = filtrar_repetidos()

    dicionario_solos = dict()
    dicionario_fid_last = dict()
    dicionario_principal = dict()
    
    separar_dicionarios(solos_dict, dicionario_fid_last, dicionario_solos)
    
    unificar_dicionarios(dicionario_principal, dicionario_fid_last, dicionario_solos)

    converter_csv()

    gerar_graphml()


    