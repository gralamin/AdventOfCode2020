all: answer

answer: answer.o
	g++ -std=c++2a -O3 -o answer answer.o

answer.o:
	g++ -std=c++2a -O3 -c answer.cpp

clean:
	rm answer.o answer