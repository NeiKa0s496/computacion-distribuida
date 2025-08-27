#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <mpi.h>

#define TAG_LIMITES 1
#define TAG_RESULTADO 2

#define N 100000000

/*
*Codigo auxiliar para el ejercicio de métricas.
*Realiza la suma de los primeros N numeros naturales de forma distribuida
*y lleva registro del tiempo de ejecucion en el nodo 0
*/

int main(int argc, char** argv){
	struct timeval inicio;//nos permiten medir el tiempo de ejecucion
	gettimeofday(&inicio, NULL);//guarda el tiempo al inicio del programa
	
	MPI_Init(&argc, &argv); //inicializa comunicacion
	int size;
	int rank;
	MPI_Comm_size(MPI_COMM_WORLD, &size); //guarda el numero total de nodos
	MPI_Comm_rank(MPI_COMM_WORLD, &rank); //guarda el identificador de este nodo

	int limites[] ={0,0};//indica el rango de numeros que este nodo debe sumar
	
	if (rank == 0) // Nodo Maestro, que reporta el resultado al final
	{
		int tamano = N/size;//el numero de entradas que cada nodo debe sumar
		limites[1] = tamano;

		int destino;
		for (destino=1; destino<size; ++destino){//envia a cada nodo el rango que debe operar
			MPI_Send(limites, 2, MPI_INT, destino, TAG_LIMITES, MPI_COMM_WORLD);
			limites[0] += tamano;
			limites[1] += tamano;
		}
		limites[1] = N+1; //si N no es divisible entre size, el nodo 0 suma el residuo

	}else//nodos esclavos
	{
		MPI_Recv(limites, 2, MPI_INT, 0, TAG_LIMITES, MPI_COMM_WORLD, MPI_STATUS_IGNORE);//recibe el rango que debe operar
	}
	//esta seccion es ejecutada por todos los nodos
	printf("nodo %i sumara de %i a %i\n",rank, limites[0], (limites[1]-1));
	long int sumaNodo=0;//guarda la suma parcial
	int i;
	for (i=limites[0];i<limites[1];++i){
		sumaNodo+=i;
	}
	
	if (rank!=0){ //nodos esclavos envian resultados parciales
		MPI_Send(&sumaNodo, 1, MPI_LONG, 0, TAG_RESULTADO, MPI_COMM_WORLD);
		printf("nodo %i envia resultado de %li\n",rank, sumaNodo);
	}else{ //nodo maestro recibe los resultados
		int origen;
		long int total = sumaNodo;
		for (origen=1; origen<size; ++origen){
			MPI_Recv(&sumaNodo, 1, MPI_LONG, origen, TAG_RESULTADO, MPI_COMM_WORLD, MPI_STATUS_IGNORE);//recibe el resultado de un esclavo
			total+=sumaNodo;
		}

		struct timeval fin;
		gettimeofday(&fin, NULL); //guarda el tiempo al final del programa
		int tiempo = (fin.tv_sec - inicio.tv_sec)* 1000000 + (fin.tv_usec - inicio.tv_usec);//calcula el tiempo transcurrido restando el inicio del fin
		printf("\n\nsuma total: %li  \ntiempo de ejecucion: %i microsegundos\n",total, tiempo); //imprime resultados
	}
	MPI_Finalize();
	return 0;
}