from random import randint, uniform

#Conjuntos
Jeans = range(20)
Horas = range(1080) #Horas: 0-11 ya que el maximo de horas por maquina es de 12 hrs.
Tallas = range(6) #Tallas: XS, S, M, L, XL, XXL
Metodos = range(8) #Metodos: Seleccion
Maquinarias = range(33) #Maquinarias: 33 maquinas de produccion actual
Maquinaria_eficiente = range(33, 47) #Maquinaria eficiente: Eco-Friendly
Maquinaria_total = range(47)

#Parametros
demanda_diaria_por_talla = {(j,t): randint(2, 4) for j in Jeans for t in Tallas}
presupuesto = 200000000 # $ en CLP
conjunto_metodos_para_cada_jean = {(j): (0,1,2,3,4,5,6,7)  for j in Jeans}
cantidad_max_jeans_por_talla_por_maquina_por_hora = {(j,t,h,m): randint(400, 460)  for j in Jeans for t in Tallas for h in Horas for m in Maquinaria_total} #Maquinas entre 70%-80% de eficiencia
consumo_agua_jean_maquina_talla = {(j,t,m): randint(60, 100) for j in Jeans for t in Tallas for m in Maquinarias}
for maquina in Maquinaria_eficiente:
    for t in Tallas:
        for j in Jeans:
            consumo_agua_jean_maquina_talla[j,t,maquina] = randint(15,25)
'''
consumo_agua_jean_maquina_talla = {
    (0): randint(60, 100),
    (1): randint(60, 100),
    (2): randint(60, 100),
    (3): randint(60, 100),
    (4): randint(60, 100),
    (5): randint(60, 100),
    (6): randint(60, 100),
    (7): randint(60, 100),
    (8): randint(60, 100),
    (9): randint(60, 100),
    (10): randint(60, 100),
    (11): randint(60, 100),
    (12): randint(60, 100),
    (13): randint(60, 100),
    (14): randint(60, 100),
    (15): randint(60, 100),
    (16): randint(60, 100),
    (17): randint(60, 100),
    (18): randint(60, 100),
    (19): randint(60, 100),
    (20): randint(60, 100),
    (21): randint(60, 100),
    (23): randint(60, 100),
    (24): randint(15, 25),
    (25): randint(15, 25),
    (26): randint(15, 25),
    (27): randint(15, 25),
    (28): randint(15, 25),
    (29): randint(15, 25),
    (30): randint(15, 25),
    (31): randint(15, 25)
}
'''
horas_que_tarda_maquina_procesar_jean_talla_metodo = {(m,j,t,p): randint(30, 90) for m in Maquinaria_total for j in Jeans for t in Tallas for p in Metodos}
conjunto_maquinas_por_metodo = {
    (0): (0, 1), #Metodo diseno
    (1): (2, 4),   #Metodo corte
    (2): (3, 4, 5, 6, 7, 8, 9), #Metodo costura y ensamblaje
    (3): (10, 11, 12, 13, 14, 15, 33, 34, 35, 36), #Metodo lavado
    (4): (16, 17, 18, 19, 20, 21, 22, 37, 38, 39, 40), #Metodo tenido
    (5): (23, 24, 25, 26, 41, 42, 43, 44), #Metodo enjuagado
    (6): (27, 28), #Metodo control de calidad
    (7): (29, 30, 31, 32, 45, 46) #Metodo decolorado
}
cantidad_agua_mantencion_por_maquina = {(m): randint(25, 40) for m in Maquinarias}
for m in Maquinaria_eficiente:
    cantidad_agua_mantencion_por_maquina[(m)] = randint(8,15)

#4 Cada metodo p usa cierta cantidad de maquinarias m
#modelo.addConstrs(quicksum(y[m,j,h] for m in conjunto_maquinas_por_metodo for j in Jeans for h in Horas) == 1 for p in conjunto_metodos_para_cada_jean)
