CC=gcc
CFLAGS=-I.
DEPS = myrplidar.h
OBJS = main.o
TARGET = rplidar_test
INCLUDE = -I/usr/include/rplidar
LIB = -L/usr/lib -lsl_lidar_sdk -lstdc++ -lpthread

%.o: %.cpp $(DEPS)
	$(CC)  -c $< -o $@ -I/usr/include/rplidar $(CFLAGS) 

%.o: %.c $(DEPS)
	$(CC)  -c $< -o $@ -I/usr/include/rplidar $(CFLAGS) 

all: main.o 
	$(CC) -o $(TARGET) $(OBJS) $(LIB)
