all:
	gcc -c -Wall -Werror -fpic libmvcam.c
	gcc -shared -o libmvcam.so libmvcam.o -ldvp -lhzd -lpthread 
clean:
	rm libmvcam.so libmvcam.o
