CC=g++
CFLAGS=-pthread -std=c++11 -O3 -I $(IDIR)

IDIR =include
ODIR=obj

_DEPS = stdafx.h params.h analysis.h strategy.h dice.h hog.h
DEPS = $(patsubst %,$(IDIR)/%, $(_DEPS))

_OBJ = main.o hog.o strategy.o analysis.o 
OBJ = $(patsubst %,$(ODIR)/%, $(_OBJ))

OUTPUTNAME = bacon
OUTPUTDIR = bin/
HOGCONV = hogconv.py
HOGCONVBIN = hogconv

$(ODIR)/%.o: %.cpp $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

$(OUTPUTNAME) : $(OBJ)
	$(CC) -o $(OUTPUTDIR)$@ $^ $(CFLAGS)

.PHONY: clean install
	
clean:
	rm -rf $(ODIR)/*
	rm -rf .vs
	rm -f bin/*.pdb 2> /dev/null
	rm -f bin/*.iobj 2> /dev/null
	rm -f bin/*.ipdb 2> /dev/null
	rm -f bin/*.ilk 2> /dev/null
	
install:
	rm -f /usr/local/bin/$(OUTPUTNAME)
	cp $(OUTPUTDIR)$(OUTPUTNAME) /usr/local/bin
	cp $(HOGCONV) /usr/local/bin/$(HOGCONVBIN)
	chmod +x /usr/local/bin/$(HOGCONVBIN)

uninstall:
	rm -f /usr/local/bin/$(OUTPUTNAME)
	rm -f /usr/local/bin/$(HOGCONVBIN)
    
install_user:
	rm -f ~/bin/$(OUTPUTNAME)
	cp $(OUTPUTDIR)$(OUTPUTNAME) ~/bin
	cp $(HOGCONV) ~/bin/$(HOGCONVBIN)
	chmod +x ~/bin/$(HOGCONVBIN)
