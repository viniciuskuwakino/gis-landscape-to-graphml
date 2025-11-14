from java.awt import Color
from javax.swing import JFrame, JPanel, JButton, JLabel, JOptionPane, JTextField, Box, BoxLayout, JSeparator
from java.awt import Color, Font, Dimension

graph_backup = g

colors = [
    [0, 37, 51],
    [30, 59, 142],
    [0, 143, 229],
    [136, 197, 247],
    [200, 236, 247]
]

cn_colors = [
    [240, 248, 255],
    [224, 255, 255],
    [176, 196, 222],
    [176, 224, 230],
    [173, 216, 230],
    [135, 206, 235],
    [0, 191, 255],
    [0, 0, 255],
    [30, 144, 255],
    [70, 130, 180],
    [0, 0, 205],
    [0, 0, 139],
    [65, 105, 225],
    [0, 0, 128],
    [0, 71, 171]
]

def get_node_by_id(node_id):
    for node in g.nodes:
        node_str = str(node.id)
        if node_str.startswith("n"):
            node_str = node_str[1:]  # remove o primeiro caractere "n"
        if node_str == str(node_id):
            return node
    return None

def bfs(source):
    result = {}
    visited = {}
    queue = []

    # result[0] = [source]
    queue.append([source, 0])
    visited[str(source.id)] = [source, 0]

    while queue:
        s = queue.pop(0)
        
        for i in s[0].neighbors:
            if visited.get(str(i.id)) == None:
                if s[0].altitude > i.altitude:
                    queue.append([i, s[1] + 1])
                    visited[str(i.id)] = [i, s[1] + 1]

    for value in visited.values():
        node = value[0]
        level = value[1] if value[1] <= 4 else 4

        if value[1] not in result:
            result[value[1]] = []

        result[value[1]].append(node)

        node.color = Color(colors[level][0], colors[level][1], colors[level][2])
    

    for key, value in result.items():
        print("Nivel: " + str(key))
        print("Nodes: " + str(value))

def resetar_grafo():
    print(graph_backup)

def cor_por_cn():
    cn_values = []
    for node in g.nodes:
        if node.cn not in cn_values:
            cn_values.append(node.cn)
    
    cn_values = sorted(cn_values)

    for node in g.nodes:
        intensity = cn_values.index(node.cn)
        node.color = Color(cn_colors[intensity][0], cn_colors[intensity][1], cn_colors[intensity][2])

def cor_nos_padrao():
    for node in g.nodes:
        node.color = Color(200, 200, 200)

def cor_arestas_padrao():
    for edge in g.edges:
        edge.color = Color(200, 200, 200)

def adicionar_filtros():
    addFilter((altitude > 100), name = "Filtrar vertices pela altitude")
    addFilter((outdegree > 0), name = "Filtrar vertices pelo grau de saida")
    addFilter((indegree > 0), name = "Filtrar vertices pelo grau de entrada")
    addFilter((cn > 50), name = "Filtrar vertices pelo CN")

def grau_saida():
    for i in g.nodes:
        i.size = 15 + i.outdegree


def grau_entrada():
    for i in g.nodes:
        i.size = 15 + i.indegree


def bellmanford(start, end):
    edges = {}
    nodes = {}
    dist, prev = {}, {}

    for v in g.nodes:
        nodes[str(v.id)] = v
        dist[str(v.id)], prev[str(v.id)] = float('-inf'), None

    dist[str(start.id)] = 0

    for e in g.edges:
        edges[e] = {
            'edge': e,
            'source': e.source,
            'target': e.target,
            'weight': e.weight,
            'color': e.color
        }

	# Bellman-Ford algorithm
    for i in range(len(g.nodes)):
        for e in g.edges:
            if dist[str(e.target.id)] < dist[str(e.source.id)] + e.weight:
                dist[str(e.target.id)] = dist[str(e.source.id)] + e.weight
                prev[str(e.target.id)] = e
 
	# highlight a shortest path with the red color (if one exists)
    if dist[str(end.id)] > float('-inf'):
        e = prev[str(end.id)]
        end.color = Color(105, 245, 12)
        # Color(255, 157, 56)
        while e != None:
            e.color = Color(250, 163, 2)
            e.source.color = Color(250, 163, 2)
            e = prev[str(e.source.id)]

        start.color = Color(219, 26, 26)
 
    return dist[str(end.id)]

def interface():
    frame = JFrame("Painel de Controle - Grafo TCC")
    frame.setSize(400, 650)
    frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
    frame.setLocationRelativeTo(None)

    panel = JPanel()
    panel.setLayout(BoxLayout(panel, BoxLayout.Y_AXIS))
    panel.setBackground(Color(240, 240, 240))

    titulo = JLabel("Selecione uma acao:")
    titulo.setFont(Font("Arial", Font.BOLD, 16))
    titulo.setAlignmentX(0.5)
    panel.add(Box.createVerticalStrut(20))
    panel.add(titulo)
    panel.add(Box.createVerticalStrut(20))

    # Funcoes auxiliares para montar a interface
    def add_botao(nome, acao):
        botao = JButton(nome)
        botao.setAlignmentX(0.5)
        botao.setPreferredSize(Dimension(300, 40))
        botao.setMaximumSize(Dimension(300, 40))
        botao.setFont(Font("Arial", Font.PLAIN, 14))
        botao.addActionListener(lambda e: acao())
        panel.add(botao)
        panel.add(Box.createVerticalStrut(10))

    def add_titulo_secao(texto):
        titulo_secao = JLabel(texto)
        titulo_secao.setFont(Font("Arial", Font.BOLD, 14))
        titulo_secao.setAlignmentX(0.5)
        panel.add(titulo_secao)
        panel.add(Box.createVerticalStrut(10))

    def add_separador():
        panel.add(Box.createVerticalStrut(5))
        separador = JSeparator()
        separador.setAlignmentX(0.5)
        separador.setMaximumSize(Dimension(320, 1))
        panel.add(separador)
        panel.add(Box.createVerticalStrut(15))

    # Botoes simples organizados por secoes
    add_titulo_secao("Medidas")
    add_botao("Centralidade de grau de saida", lambda: (grau_saida(), JOptionPane.showMessageDialog(None, "Funcao grau_saida() executada!")))
    add_botao("Centralidade de grau de entrada", lambda: (grau_entrada(), JOptionPane.showMessageDialog(None, "Funcao grau_entrada() executada!")))

    add_separador()

    add_titulo_secao("Cores")
    add_botao("Cor por CN", lambda: (cor_por_cn(), JOptionPane.showMessageDialog(None, "Funcao cor_por_cn() executada!")))
    add_botao("Cor de nos padrao", lambda: (cor_nos_padrao(), JOptionPane.showMessageDialog(None, "Cor padrao aplicada aos nos!")))
    add_botao("Cor de arestas padrao", lambda: (cor_arestas_padrao(), JOptionPane.showMessageDialog(None, "Cor padrao aplicada as arestas!")))

    add_separador()

    add_titulo_secao("Filtros")
    add_botao("Adicionar filtros", lambda: (adicionar_filtros(), JOptionPane.showMessageDialog(None, "Filtros adicionados com sucesso!")))

    add_separador()

    # -------------------------------
    # MODAL: BFS
    # -------------------------------
    def abrir_modal_bfs():
        modal = JFrame("Executar BFS")
        modal.setSize(350, 180)
        modal.setLocationRelativeTo(None)
        modal.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)

        p = JPanel()
        p.setLayout(BoxLayout(p, BoxLayout.Y_AXIS))
        p.setBackground(Color(245, 245, 245))

        lbl = JLabel("ID do no de origem (exemplo: 228):")
        lbl.setFont(Font("Arial", Font.PLAIN, 14))
        lbl.setAlignmentX(0.5)

        input_origem = JTextField()
        input_origem.setMaximumSize(Dimension(250, 30))
        input_origem.setFont(Font("Arial", Font.PLAIN, 14))

        def executar_bfs():
            raw_id = input_origem.getText()
            node_id = str(raw_id).strip() if raw_id is not None else ""
            print("Valor informado no campo origem:", repr(node_id))
            if node_id == "":
                JOptionPane.showMessageDialog(None, "Digite um ID valido.")
                return
            node = get_node_by_id(node_id)
            
            if node is None:
                JOptionPane.showMessageDialog(None, "No nao encontrado: " + node_id)
                return
            bfs(node)
            JOptionPane.showMessageDialog(None, "BFS executado a partir do no: " + node_id)
            modal.dispose()

        btn_exec = JButton("Executar BFS")
        btn_exec.setAlignmentX(0.5)
        btn_exec.setFont(Font("Arial", Font.BOLD, 14))
        btn_exec.addActionListener(lambda e: executar_bfs())

        p.add(Box.createVerticalStrut(20))
        p.add(lbl)
        p.add(Box.createVerticalStrut(10))
        p.add(input_origem)
        p.add(Box.createVerticalStrut(20))
        p.add(btn_exec)
        p.add(Box.createVerticalStrut(20))

        modal.add(p)
        modal.setVisible(True)

    # -------------------------------
    # MODAL: Bellman-Ford
    # -------------------------------
    def abrir_modal_bellmanford():
        modal = JFrame("Executar Bellman-Ford")
        modal.setSize(350, 220)
        modal.setLocationRelativeTo(None)
        modal.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)

        p = JPanel()
        p.setLayout(BoxLayout(p, BoxLayout.Y_AXIS))
        p.setBackground(Color(245, 245, 245))

        lbl1 = JLabel("ID do no de origem (exemplo: 228):")
        lbl1.setFont(Font("Arial", Font.PLAIN, 14))
        lbl1.setAlignmentX(0.5)

        input_origem = JTextField()
        input_origem.setMaximumSize(Dimension(250, 30))
        input_origem.setFont(Font("Arial", Font.PLAIN, 14))

        lbl2 = JLabel("ID do no de destino (exemplo: 2):")
        lbl2.setFont(Font("Arial", Font.PLAIN, 14))
        lbl2.setAlignmentX(0.5)

        input_destino = JTextField()
        input_destino.setMaximumSize(Dimension(250, 30))
        input_destino.setFont(Font("Arial", Font.PLAIN, 14))

        def executar_bellmanford():
            origem_id = input_origem.getText()
            destino_id = input_destino.getText()
            if origem_id is None or origem_id.strip() == "" or destino_id is None or destino_id.strip() == "":
                JOptionPane.showMessageDialog(None, "Digite ambos os IDs.")
                return
            origem = get_node_by_id(origem_id)
            destino = get_node_by_id(destino_id)
            if origem is None or destino is None:
                JOptionPane.showMessageDialog(None, "Um dos nos nao foi encontrado.")
                return
            dist = bellmanford(origem, destino)
            JOptionPane.showMessageDialog(None, "Bellman-Ford executado!\nDistancia total: " + str(dist))
            modal.dispose()

        btn_exec = JButton("Executar Bellman-Ford")
        btn_exec.setAlignmentX(0.5)
        btn_exec.setFont(Font("Arial", Font.BOLD, 14))
        btn_exec.addActionListener(lambda e: executar_bellmanford())

        p.add(Box.createVerticalStrut(15))
        p.add(lbl1)
        p.add(Box.createVerticalStrut(5))
        p.add(input_origem)
        p.add(Box.createVerticalStrut(10))
        p.add(lbl2)
        p.add(Box.createVerticalStrut(5))
        p.add(input_destino)
        p.add(Box.createVerticalStrut(15))
        p.add(btn_exec)
        p.add(Box.createVerticalStrut(15))

        modal.add(p)
        modal.setVisible(True)

    # Botoes que abrem as modais
    add_titulo_secao("Algoritmos")
    add_botao("Executar BFS", abrir_modal_bfs)
    add_botao("Executar Bellman-Ford", abrir_modal_bellmanford)

    # -------------------------------
    # BOTAO: Fechar
    # -------------------------------
    panel.add(Box.createVerticalStrut(50))
    fechar = JButton("Fechar")
    fechar.setAlignmentX(0.5)
    fechar.setPreferredSize(Dimension(300, 40))
    fechar.setMaximumSize(Dimension(300, 40))
    fechar.setBackground(Color(220, 60, 60))
    fechar.setForeground(Color.white)
    fechar.setFont(Font("Arial", Font.BOLD, 14))
    fechar.addActionListener(lambda e: frame.dispose())
    panel.add(fechar)
    panel.add(Box.createVerticalStrut(20))

    frame.add(panel)
    frame.setVisible(True)


if __name__ == '__main__':
    interface()