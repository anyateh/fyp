CC=gcc
CFLAGS=-Wall -Wpedantic -g -I/home/takoinspirit/anaconda3/include/python3.9 -I/home/takoinspirit/anaconda3/include/python3.9  -Wno-unused-result -Wsign-compare -march=nocona -mtune=haswell -ftree-vectorize -fPIC -fstack-protector-strong -fno-plt -O3 -ffunction-sections -pipe -isystem /home/takoinspirit/anaconda3/include -fdebug-prefix-map=/croot/python-split_1694437926857/work=/usr/local/src/conda/python-3.9.18 -fdebug-prefix-map=/home/takoinspirit/anaconda3=/usr/local/src/conda-prefix -I/home/takoinspirit/anaconda3/include 
exec_out=python_embed
LD=gcc
LDFLAGS=-L/home/takoinspirit/anaconda3/lib/python3.9/config-3.9-x86_64-linux-gnu -L/home/takoinspirit/anaconda3/lib -lpython3.9 -lcrypt -lpthread -ldl  -lutil -lm -lm 

src_files=src/simple_python_embed.c
obj_files=$(patsubst %.c, %.o, $(src_files))

.PHONY=run clean

$(exec_out): $(obj_files)
	$(LD) $(LDFLAGS) -o $@ $(obj_files)

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

run: $(exec_out)
	env LD_LIBRARY_PATH=/home/takoinspirit/anaconda3/lib ./$(exec_out)

clean:
	-rm $(exec_out)
	-rm $(obj_files)
