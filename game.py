Guia de Instalação game.py - Tradução PT-BR
Este guia descreve as modificações necessárias no seu arquivo game.py para integrar o sistema de PING.

1. Inicialização do pingLine e Status isShowPing
Procure a seguinte linha no método __init__ da classe GameWindow:

#Suchen in class GameWindow(ui.ScriptWindow):
self.__ProcessPreservedServerCommand()

Adicione o seguinte código diretamente abaixo. Este código inicializa self.pingLine e uma nova variável self.isShowPing, que armazena o status de visibilidade atual do PING. Observe que a linha SetPosition foi removida aqui, pois a posição será definida dinamicamente.

		self.pingLine = None
		self.isShowPing = True # Adicionado: Controla a visibilidade do PING. Visível por padrão.
		if app.ENABLE_PINGTIME:
			self.pingLine = ui.TextLine()
			self.pingLine.SetFontName(localeInfo.UI_DEF_FONT) # Alterado: Usa a fonte padrão para uma exibição menor.
			self.pingLine.SetFontColor(1.0,1.0,1.0)
			self.pingLine.SetOutline() # Mantém o contorno.
			# Removido: A linha SetPosition aqui. A posição será definida dinamicamente.

2. Limpeza do pingLine ao Fechar
Procure a seguinte linha no método Close da classe GameWindow:

#Suchen in def Close(self):
			self.interface=None

Adicione o seguinte código diretamente abaixo. Isso garante que o objeto pingLine seja liberado corretamente quando a janela for fechada.

		if app.ENABLE_PINGTIME:
			self.pingLine = None

3. Posicionamento Dinâmico do PING
Vamos criar um novo método __UpdatePingPosition que calcula a posição do PING com base na posição do texto de informações do servidor/canal do Mini-Mapa.

A) Adicione o novo método __UpdatePingPosition à classe GameWindow:

Adicione este método em um local apropriado dentro da classe GameWindow, por exemplo, após o método TogglePing ou antes de __BuildKeyDict.

	# Adicionado: Nova função para atualizar dinamicamente a posição do PING.
	def __UpdatePingPosition(self):
		if not app.ENABLE_PINGTIME or not self.pingLine:
			return

		# Tenta acessar o objeto do minimapa e o elemento de texto do servidor/canal.
		# self.interface.wndMiniMap é a instância da classe MiniMap (uiminimap.py)
		# serverInfo é o ui.TextLine dentro de MiniMap que contém o nome do servidor/canal.
		if hasattr(self.interface, 'wndMiniMap') and self.interface.wndMiniMap and \
		   hasattr(self.interface.wndMiniMap, 'serverInfo') and self.interface.wndMiniMap.serverInfo:

			server_info_text_line = self.interface.wndMiniMap.serverInfo

			# Obtém as coordenadas globais (na tela) (x, y) e o tamanho (largura, altura) do texto do canal.
			text_x, text_y = server_info_text_line.GetGlobalPosition()
			text_width, text_height = server_info_text_line.GetTextSize()

			# Calcula a nova posição para a pingLine.
			# A borda esquerda do PING é alinhada com a borda esquerda do texto do canal.
			# O PING é posicionado com uma pequena margem abaixo do texto do canal.
			
			ping_x = text_x
			ping_top_y = text_y + text_height + 3 # 3 pixels de margem abaixo do texto do canal. Ajuste este valor se necessário.

			self.pingLine.SetPosition(ping_x, ping_top_y)
			# Garante que o alinhamento seja à esquerda, caso uma centralização tenha sido definida anteriormente.
			self.pingLine.SetWindowHorizontalAlignLeft() 
			self.pingLine.SetHorizontalAlignLeft()       
			
		else:
			# Fallback: Se o minimapa ou serverInfo não estiverem disponíveis,
			# uma posição fixa é usada para que o PING apareça (ex: durante o carregamento).
			self.pingLine.SetPosition(wndMgr.GetScreenWidth() - 150, 185) # Posição de fallback (ajuste se necessário).
			# Para o fallback, a centralização horizontal pode ser mantida se for uma posição genérica.
			self.pingLine.SetWindowHorizontalAlignCenter() 
			self.pingLine.SetHorizontalAlignCenter()

B) Chame __UpdatePingPosition quando o jogo for aberto:

Procure na classe GameWindow, no método Open, a linha:

#Suchen in def Open(self):
		net.SendEnterGamePacket()

Adicione o seguinte código diretamente abaixo. Isso garante que o PING seja posicionado corretamente após todos os elementos da UI terem sido carregados.

		# Adicionado: Chamada da função de atualização da posição do PING após o carregamento da interface.
		if app.ENABLE_PINGTIME:
			self.__UpdatePingPosition() # Atualiza a posição do PING.
			if self.isShowPing:
				self.pingLine.Show()
			else:
				self.pingLine.Hide()

4. Atualização do Método __BuildDebugInfo
Procure na classe GameWindow, no método __BuildDebugInfo, o bloco:

#Suchen in def __BuildDebugInfo(self):
		self.ViewDistance.SetPosition(0, 0)
		
#Darunter hinzufügen
		if app.ENABLE_PINGTIME:
			self.pingLine.SetWindowHorizontalAlignCenter()
			self.pingLine.SetHorizontalAlignCenter()
			self.pingLine.SetFeather()
			self.pingLine.SetOutline()
			self.pingLine.Show() # Esta linha será alterada

Altere a condição self.pingLine.Show() para um bloco condicional que leve em conta self.isShowPing:

		if app.ENABLE_PINGTIME:
			# Alterado: Define o alinhamento do PING, mas a visibilidade é controlada por isShowPing.
			# A posição do PING agora é gerenciada por __UpdatePingPosition(), então estas linhas podem permanecer ou ser ajustadas conforme desejado.
			# self.pingLine.SetWindowHorizontalAlignCenter() # Estas linhas podem não ser mais necessárias se __UpdatePingPosition as configurar corretamente.
			# self.pingLine.SetHorizontalAlignCenter()       # Recomenda-se testar no jogo.
			self.pingLine.SetFeather()
			self.pingLine.SetOutline()
			# Alterado: A visibilidade agora é controlada por isShowPing.
			if self.isShowPing:
				self.pingLine.Show()
			else:
				self.pingLine.Hide()

5. Adição do Método TogglePing e Atalho de Tecla
A) Adicione o novo método TogglePing à classe GameWindow:

Adicione este método em um local apropriado dentro da classe GameWindow, por exemplo, antes de __BuildKeyDict ou depois de Close.

	# Adicionado: Função para alternar a visibilidade do PING.
	def TogglePing(self):
		if not app.ENABLE_PINGTIME:
			return

		self.isShowPing = not self.isShowPing
		if self.pingLine:
			if self.isShowPing:
				self.pingLine.Show()
			else:
				self.pingLine.Hide()

B) Vincule a tecla 'P' à função TogglePing:

Procure na classe GameWindow, no método __BuildKeyDict, a linha onde você já tinha adicionado o atalho para a tecla 'P':

#Suchen in def __BuildKeyDict(self):
		onPressKeyDict[app.DIK_P]			= lambda : self.TogglePing() # Esta é a linha alvo

Certifique-se de que esta linha se parece com o seguinte para chamar a função TogglePing:

		onPressKeyDict[app.DIK_P]			= lambda : self.TogglePing() # Adicionado: Atalho de tecla para 'P' para alternar o PING.

6. Atualização do Método OnUpdate
Procure na classe GameWindow, no método OnUpdate, o bloco:

#Suchen in def OnUpdate(self):
		self.interface.BUILD_OnUpdate()

#Darunter hinzufügen
		if app.ENABLE_PINGTIME: # Esta linha será alterada
			nPing = app.GetPingTime()
			self.pingLine.SetText("PING: %s" % (nPing))

Altere a condição para garantir que o PING seja atualizado apenas quando deveria estar visível:

		self.interface.BUILD_OnUpdate()

		if app.ENABLE_PINGTIME and self.isShowPing: # Alterado: Atualiza o PING apenas se ENABLE_PINGTIME estiver ativo E isShowPing for True.
			nPing = app.GetPingTime()
			self.pingLine.SetText("PING: %s" % (nPing))

Após salvar essas alterações em seu game.py:

Empacote seu cliente novamente (se o seu fluxo de trabalho isso exigir).

Inicie o jogo.

O PING deve agora aparecer por padrão abaixo do texto do canal do Mini-Mapa e pode ser alternado (exibido/ocultado) pressionando a tecla 'P'. A posição do PING deve se ajustar automaticamente a diferentes resoluções de tela.