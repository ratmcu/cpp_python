IDIR =../include
CC=gcc
CFLAGS=-I$(IDIR)

ODIR=obj
LDIR =../lib

LIBS=-lm -lpthread

#_DEPS = hellomake.h
#DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = server.o client.o 
OBJ_SERVER = $(patsubst %,$(ODIR)/%,$(_OBJ))

_OBJ = client.o 
OBJ_CLIENT = $(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)


makeall: server client
	
server: $(OBJ_SERVER)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)
	
client: $(OBJ_CLIENT)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)
	
.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~ 
