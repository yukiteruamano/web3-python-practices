# encoding: utf-8
#!/usr/bin/env python

from web3 import Web3       # Llamamos a la biblioteca de funciones de Web3.py
import os                   # Llamamos a la biblioteca de funciones del sistema operativo


# Función para limpiar pantalla
def clear_screen():

   # Para sistemas Posix (GNU/Linux, MacOS, *BSD)
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        #Para Windows
        _ = os.system('cls')


# Función para conexión al nodo local Geth
def connect_node():
    
    # Configuramos la conexión al nodo local GETH usando el modo HTTP
    # Esto indica al programa donde está ubicado nuestro nodo para que haga conexión al mismo
    print("Conectando con el nodo Geth Local")
    geth_local = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
                
    # Verificamos la conexión al nodo Geth
    if geth_local.isConnected() == True:
        print("Conexión al nodo: Activa\n")
        return geth_local
    else:
        print("Error en la conexión. ¡Conexión abortada!")
        print("Asegurese de que el nodo este ejecutandosé.")
        print("Asegurese de que la dirección y puerto sea correcta, este habilitada la API de conexión HTTP.")
        input("\nPresione Enter para continuar...")
        return 0


# Función para verificar que cadena está usando nuestro nodo
def verify_chain(localnode):
        
    # Comenzamos el proceso de verificar que cadena está usando el nodo
    id_chain = localnode.eth.chain_id()
    
    # Verificamos cada uno de los valores indicados en el EIP-155
    #   1 = Mainnet
    #   2 = Morden (en desuso)
    #   3 = Ropsten (testnet PoW)
    #   4 = Rinkeby
    #   5 = Goërli
    #   42 = Kovan
    #   1337 = Cadena privada de Geth
    
    if id_chain == 1:
        return "Mainnet"
    elif id_chain == 2:
        return "Morden"
    elif id_chain == 3:
        return "Ropsten"
    elif id_chain == 4:
        return "Rinkeby"
    elif id_chain == 5:
        return "Goërli"
    elif id_chain == 42:
        return "Kovan"
    elif id_chain == 1337:
        return "Cadena privada de Geth"
    else:
        return "Error. Cadena no conocida"


# Función para solicitar información al nodo Geth local
def info_eth_blockchain(localnode):

    print("Información del nodo local Geth")
    print("******************************\n")

    # Extraemos la información administrativa del nodo
    # Para poder acceder a este información debemos activar la API "admin"
    node_info = localnode.geth.admin.node_info()
   
    # Info del nodo
    print("Identificador del Nodo: ", node_info['id'])      # ID único de nuestro nodo
    print("Version del nodo: ", localnode.clientVersion)    # Versión de nuestro nodo Geth
    print("Version de API: ", localnode.api)                # Version API usada para la interacción
    print("Dirección IP: ", node_info['ip'])                # Dirección IP de nuestro nodo

    # Imprimimos datos de los forks y bloque genesis
    print("\nInformación de soporte de forks y bloque genesis")
    print("************************************************\n")
    print("Bloque Genesis: ", node_info.protocols.les.genesis)
    print("Bloque Activación Homestead: ", node_info.protocols.les.config.homesteadBlock)
    print("Soporte a DAO Fork: ", node_info.protocols.les.config.daoForkSupport)
    print("Bloque DAO Fork: ", node_info.protocols.les.config.daoForkBlock)
    print("Bloque Activación Byzantium: ", node_info.protocols.les.config.byzantiumBlock)
    print("Bloque Activación Constantinople: ", node_info.protocols.les.config.constantinopleBlock)
    print("Bloque Activación Petersburg: ", node_info.protocols.les.config.petersburgBlock)
    print("Bloque Activación Istambul: ", node_info.protocols.les.config.istanbulBlock)
    print("Bloque Activación Muir Glacier: ", node_info.protocols.les.config.muirGlacierBlock)

    # Imprimimos datos de la red
    print("\nDatos de la red")
    print("***************\n")
    print("Red usada: ", verify_chain(localnode))                                   # Versión de la red usada según EIP-155
    print("Estatus de sincronización: ", localnode.eth.syncing)                     # Status sincronización del nodo
    print("Dificultad actual de la red: ", node_info.protocols.les.difficulty)      # Dificultad de minería de la red
    print("Número del bloque actual: ", localnode.eth.block_number())               # Último número de bloque de la red

    # Usamos la función de conversion fromWei, para que el valor se transforme a gwaei
    print("Precio del Gas: ", localnode.fromWei(localnode.eth.gas_price(), 'gwei'), "gwei")

    input("\nDatos completos. Presione Enter para continuar...")
    menu(localnode)


# Función para chequear si la dirección dada es una dirección válida de Ethereum
def check_address(eth_address, localnode):

    if localnode.isAddress(eth_address) == True:
        return True
    else:
        return False


# Revisamos las transacciones que ha recibido la dirección
def txs_to_addr(localnode, eth_address):
    
    blocks = localnode.eth.block_number()

    # El rastreo de transacciones por este método es muy lento, ya que debe solicitar
    # cada bloque de forma individual y revisar las transacciones de forma individual.
    # Para estos casos, lo mejor es ejecutar un nodo completo, y llevar esta información
    # a una BD de alta velocidad y concurrencia para dar una respuesta más adecuada 
    # de cara al usuario. Por ello, se ha reducido el rango de busqueda a los ultimos
    # 10 bloques de la blockchain en este algoritmo.  
    # Una limitación: solo podemos ver las transacciones de entrada, no las de salidas

    # Reduciendo el rango de busqueda
    blocks_min = blocks - 10

    # Listas de transacciones
    txs_to = []

    # Recorremos transacciones dentro de los bloques
    for i in range(blocks_min, blocks):
        block_explorer = localnode.eth.get_block(i,full_transactions=True)
        block_range = len(block_explorer.transactions)
        for j in range(block_range):   
            if block_explorer.transactions[j].to == eth_address:
                txs_to.append(block_explorer.transactions[j])        

    return txs_to   # Retornamos el listado de transacciones


# Información de una dirección dada
def info_address(localnode):

    # Limpiamos pantalla
    clear_screen()

    print("\nRevisando datos de una dirección")
    print("**********************************\n")

    # Introducción de datos para la dirección
    addr = input("Indica una dirección de Ethereum: ")
    
    # Verificación rápida si la dirección tiene 42 caracteres (dirección estándar)
    if len(addr) == 42:

        # Comenzamos con la conversión de la dirección para iniciar su verificación
        eth_address = localnode.toChecksumAddress(addr)
        
        # Llamamos la función de verificación
        # Devuelve True, si la dirección es válida, False, si la dirección no es válida
        if check_address(eth_address,localnode) == True:
            print(eth_address, "es una dirección válida.")
        else:
            print(eth_address, "es una dirección inválida.")
    else:
        print("Es una dirección con formato invalido, verifique e intente de nuevo.")
        input("\nPresione Enter para continuar...")
        menu(localnode)

    # Imprimimos información de la dirección dada    
    print("\nInformación de dirección: ", eth_address)
    print("***************************************************************************\n")
    print("Saldo de la dirección: ", localnode.fromWei(localnode.eth.get_balance(eth_address), 'ether'), "ETH")
    total_txs = txs_to_addr(localnode, eth_address)
    print("Total de transacciones recibidas (ultimos 10 bloques): ", len(total_txs))
    print("Total de transacciones de la direccion: ", localnode.eth.getTransactionCount(eth_address))

    input("\nDatos completos. Presione Enter para continuar...")
    menu(localnode)


# Información de una transacción
def info_transaction(localnode):

    # Limpiamos pantalla
    clear_screen()

    print("\nRevisando datos de una transacción")
    print("************************************\n")

    # Introducción de datos para la dirección
    tx = input("Indica una transacción de Ethereum a evaluar: ")
    
    # Extrayendo datos de la transacción
    tx_data = localnode.eth.getTransaction(tx)
    
    # Verificando que la transacción es correcta y existe
    if tx_data != 0:
        print("\nTransacción valida")
        print("Datos de la Transacción: ", tx)
        print("Nº de Bloque:", tx_data.blockNumber)
        print("Gas Price:", localnode.fromWei(tx_data.gasPrice, 'gwei'), " gwei")
        print("Valor:", localnode.fromWei(tx_data.value, 'ether'), " ETH")
    
    input("\nDatos completos. Presione Enter para continuar...")
    menu(localnode)


# Menu de la aplicación
def menu(localnode):

    clear_screen()
    
    print("\nInteracción con Nodo Local GETH")
    print("*********************************\n")
    print("1.- Información del nodo")
    print("2.- Información de una dirección")
    print("3.- Información de una transaccion")
    print("0.- Salir")
    opt = int(input("Indique una opción: "))

    if opt == 1:
        clear_screen()
        info_eth_blockchain(localnode)
    elif opt == 2:
        clear_screen()
        info_address(localnode)
    elif opt == 3:
        clear_screen()
        info_transaction(localnode)
    elif opt == 0:
        clear_screen()
        exit()
    else:
        print("\nOpción errada!")
        input("\nPress Enter to continue...")
        clear_screen()
        menu(localnode)


# Inicialización principal
if __name__ == "__main__":
    try:
        
        clear_screen()                  # Limpiamos pantalla 
        localnode = connect_node()      # Conectamos al nodo local
        
        if localnode != 0:
            menu(localnode)
        else:
            print("Error en la conexión. Cerrando programa")
    except:
        print("Error iniciando programa")
        exit()
