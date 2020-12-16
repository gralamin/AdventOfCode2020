all: answer

answer: answer.o
	g++ -std=c++2a -o answer answer.o

answer.o:
	g++ -std=c++2a -c answer.cpp

clean:
	rm answer.o answer