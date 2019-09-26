// Server side C/C++ program to demonstrate Socket programming 
#include <signal.h>
#include <unistd.h> 
#include <stdio.h> 
#include <sys/socket.h> 
#include <stdlib.h> 
#include <netinet/in.h> 
#include <string.h> 
#define PORT 8080 

#include <pthread.h> 
  
struct name {
	int server_fd;
	int new_socket;
	struct sockaddr_in address; 
	int addrlen;
};
// A normal C function that is executed as a thread  
// when its name is specified in pthread_create() 
void myThreadFun(void *vargp) 
{ 
	int *dat = (int *)vargp;
	while(1)
	{
    	sleep(1); 
		(*dat)++;
    	printf("Printing from the other Thread %d\n", *dat); 
	}
    return NULL; 
}



int init_socket();
void socket_sender(void *vargp)
{

	static int *dat;
	if(vargp != NULL)
	{
		printf("received a valid pointer\n"); 
		dat = (int *)vargp;
	}
	static int ko = 889;
	int new_socket = init_socket();
	char *hello = "Hello from server"; 
	char *buf =  malloc(sizeof(char)*100);
	int se = 0;
	loop:
			sprintf(buf, "{ 'msg': 'Hello message sent' , 'val' : %d}\n", *dat);
			printf(buf);
			se = send(new_socket , buf , strlen(buf) , 0 ); 
			if (se == -1){
				// pthread_t thread_id2; 
				printf("calling self to send again\n"); 
				socket_sender(NULL);
    			// pthread_create(&thread_id2, NULL, &socket_sender, NULL);
			}
			// printf("Hello message sent: %d\n", *dat);
			 
			sleep(1);
	goto loop;
}

int init_socket()
{
	static int server_fd = NULL;
	static int new_socket = NULL;
	static struct sockaddr_in address; 
	int addrlen = sizeof(address);
	if (new_socket) shutdown(	new_socket, SHUT_RDWR);
	if (server_fd) close(server_fd);
	if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) 
	{ 
		perror("socket failed"); 
		exit(EXIT_FAILURE); 
	} 
	address.sin_family = AF_INET; 
	address.sin_addr.s_addr = INADDR_ANY; 
	address.sin_port = htons( PORT ); 
	if (bind(server_fd, (struct sockaddr *)&address, 
								sizeof(address))<0) 
	{ 
		perror("bind failed"); 
		exit(EXIT_FAILURE); 
	} 
	if (listen(server_fd, 3) < 0) 
	{ 
		perror("listen"); 
		exit(EXIT_FAILURE); 
	}
	// new_socket = 0;
	if ((new_socket = accept(server_fd, (struct sockaddr *)&address, 
					(socklen_t*)&addrlen))<0) 
	{ 
		perror("accept"); 
		printf("failed to accept socket connection from client\n");
		// exit(EXIT_FAILURE); 
		// shutdown(	new_socket, SHUT_RDWR);
		// close(server_fd);	
		init_socket();
	} 
	return new_socket;
	// socket_sender(new_socket);
}

void sigpipe_handler(int unused)
{
	// pthread_t thread_id2; 
	printf("waiting in the sigpipe handler for incoming client");
    // printf("Before Thread\n"); 
    // pthread_create(&thread_id2, NULL, &socket_sender, NULL);
	socket_sender(NULL);
}

int main(void)
{
  	sigaction(SIGPIPE, &(struct sigaction){sigpipe_handler}, NULL);
	// socket_sender(init_socket());
	pthread_t thread_id1, thread_id2; 
	int *dat = malloc(sizeof(int));
	*dat = 99;
    printf("Before Thread\n"); 
    pthread_create(&thread_id1, NULL, &myThreadFun, dat); 
	socket_sender(dat);
    // pthread_create(&thread_id2, NULL, &socket_sender, NULL); 
	// socket_sender(init_socket());
    pthread_join(thread_id1, NULL);
	// pthread_join(thread_id2, NULL);
	return 0; 
} 

