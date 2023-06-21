from gurobipy import Model, GRB, quicksum
from random import randint
from datos import *

modelo = Model()
modelo.setParam("TimeLimit", 1800)

#Variables

x = modelo.addVars(Jeans, Tallas, Maquinaria_total, Horas, vtype = GRB.BINARY, name="x_jtmh")
y = modelo.addVars(Maquinaria_total, Jeans, Horas, vtype = GRB.BINARY, name="y_mjh")
w = modelo.addVars(Maquinaria_total, vtype = GRB.BINARY, name="w_m")
z = modelo.addVars(Maquinaria_total, Jeans, Horas, vtype = GRB.BINARY, name="z_mjh")
a = modelo.addVars(Maquinaria_total, vtype = GRB.CONTINUOUS, name="a_m")
b = modelo.addVars(Metodos, Horas, vtype = GRB.BINARY, name="b_ph")
f = modelo.addVars(Horas, vtype = GRB.CONTINUOUS, name="f_h")



#F.O
objetivo = quicksum(x[j,t,m,h] * consumo_agua_jean_maquina_talla[j,t,m] for j in Jeans for t in Tallas for m in Maquinaria_total for h in Horas) + quicksum(cantidad_agua_mantencion_por_maquina[m] * w[m] for m in Maquinaria_total)
modelo.setObjective(objetivo, GRB.MINIMIZE)

#Restricciones

#1 Cada maquina solo puede procesar un diseno de jean j a la vez, independiente de su talla t
modelo.addConstrs(quicksum(y[m,j,h] for j in Jeans) <= 1 for m in Maquinaria_total for h in Horas)

#2 Se debe cumplir con la demanda al final del dia
for p in conjunto_metodos_para_cada_jean[0]:
    for llave_2 in conjunto_maquinas_por_metodo.keys():
        conjunto_2 = conjunto_maquinas_por_metodo[llave_2]
        print(conjunto_metodos_para_cada_jean[0], conjunto_2)
        for m_1 in conjunto_2:
            print(p, m_1)
            modelo.addConstrs((quicksum(x[j,t,m,h] for h in Horas) / horas_que_tarda_maquina_procesar_jean_talla_metodo[m_1,j,t,p]) >= demanda_diaria_por_talla[j,t] for j in Jeans for t in Tallas for m in Maquinaria_total)



#3 No se debe exceder la cantidad maxima de jeans que puede procesar una maquina
modelo.addConstrs(quicksum(x[j,t,m,h] for t in Tallas for j in Jeans for h in Horas) <= quicksum(cantidad_max_jeans_por_talla_por_maquina_por_hora[j,t,h,m] for h in Horas for j in Jeans for t in Tallas) for m in Maquinaria_total)

#4 Para alguna hora h, no puede ocurrir que existan dos o mas metodos p en una sola maquinaria m
for llave_1 in conjunto_maquinas_por_metodo.keys():
    conjunto_1 = conjunto_maquinas_por_metodo[llave_1]
    for m in conjunto_1:
        for llave_2 in conjunto_maquinas_por_metodo.keys():
            conjunto_2 = conjunto_maquinas_por_metodo[llave_2]
            for k in conjunto_2:
                if m != k:
                    pass
                    #modelo.addConstrs(z[m,j,h] == 1 - z[k,j,h] for h in Horas for j in Jeans)


#5 Las maquinas solo pueden estar funcionando un maximo de 12 horas al dia
#modelo.addConstrs(quicksum(x[j,t,m,h] * horas_que_tarda_maquina_procesar_jean_talla_metodo[m,j,t,p] for h in Horas) <= 720 for j in Jeans for t in Tallas for m in Maquinaria_total)

#6 Si un metodo dura mas tiempo que el tiempo restante de trabajo, no se realizara
for llave in conjunto_metodos_para_cada_jean.keys():
    conjunto = conjunto_metodos_para_cada_jean[llave]
    for p in conjunto:
        print(p)
        modelo.addConstrs(b[p,h] * quicksum(horas_que_tarda_maquina_procesar_jean_talla_metodo[m,j,t,p]) <= f[h] for h in Horas)


#7 Si el gasto por el reemplazo de la maquinaria es menor al presupuesto, entonces se implementar
modelo.addConstr(quicksum(a[m] for m in Maquinaria_total) <= presupuesto)

#8 No se pueden producir jeans si es que no se ha usado al menos una m ́aquina
modelo.addConstrs(x[j,t,m,h] <= quicksum(z[m,j,h] for m in Maquinaria_total) for h in Horas)

#9 Para producir un jean, se debe haber realizado al menos un m ́etodo
#for llave in conjunto_metodos_para_cada_jean:
#    for p in conjunto_metodos_para_cada_jean[llave]:
#        modelo.addConstrs(x[j,t,m,h] <= quicksum(b[p,h]) for j in Jeans for t in Tallas for m in Maquinaria_total for h in Horas)


#10 Cada metodo contempla el uso de al menos una maquina (No se puede terminar un metodo sin haber usado ninguna maquina)
#for llave_1 in conjunto_metodos_para_cada_jean.keys():
#    for p in conjunto_metodos_para_cada_jean[llave_1]:
#       for llave_2 in conjunto_maquinas_por_metodo.keys():
#           for m in conjunto_maquinas_por_metodo[llave_2]:
#               modelo.addConstrs(quicksum(z[m,j,h]) < b[p,h] for j in Jeans for h in Horas)

#11 Si una maquina se empieza a utilizar significa que esa maquina se encuentra ocupada hasta que termine su funcionamiento
modelo.addConstrs(z[m,j,h] <= y[m,j,h] for j in Jeans for m in Maquinaria_total for h in Horas)


modelo.update()
modelo.optimize()




