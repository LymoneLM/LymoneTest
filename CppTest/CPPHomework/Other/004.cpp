#include<bits/stdc++.h>
using namespace std;
template<class T>
class node
{
public:
	T data;
	node<T>* next;
	operator= ( node &a) const 
	{
		data=a.data;
		next=a.next; 
	}
};

template<class T>
class link
{
private:
	node<T>* head, p;
	int len;
public:
	void print();
	void push(T y);
	void reverse();
	link();
	~link();
};

template<class T>
link<T>::link() :len(0)
{
	head = NULL;
	p = NULL;
};

template<class T> 
void link<T>::push(T y)
{
	if (!head) {
		p = new node<T>;
		p->data = y;
		p->next = NULL;
		head = p;
		len++;
	}
	else {
		p = p->next;
		p = new node<T>;
		p->data = y;
		p->next = NULL;
		len++;
	}
};
template<class T> void link<T>::print()
{
	p = head;
	while (p) {
		cout << p->data << ' ';
		p = p->next;
	}
};
template<class T> void link<T>::reverse()
{
	if (!head) return;
	node<T>* k;
	node<T>* rehead = NULL;
	int relen = len;
	len = 0;
	if (!rehead)
	{
		int i = 0;
		k = head;
		while (i != relen)
		{
			k = k->next;
			i++;
		}
		p = new node<T>;
		p->data = k->data;
		p->next = NULL;
		delete k;
		rehead = p;
		len++;
		relen--;
	}
	else {
		for (; relen != 0; relen--) {
			int i = 0;
			k = head;
			p = p->next;
			while (i != relen)
			{
				k = k->next;
				i++;
			}
			p = new node<T>;
			p->data = k->data;
			p->next = NULL;
			delete k;
			len++;
		}
	}
	head = rehead;

}
template<class T> link<T>::~link()
{
	node<T>* q;
	for (int i = 0; i < len; i++)
	{
		p = head;
		q = p->next;
		while (q->next)
		{
			p = q;
			q = p->next;
		}
		delete q;
		p->next = NULL;
	}
};
int main()
{
	int num1, num2;
	int x;
	double y;
	link<int> a;
	link<double> b;

	cin >> num1 >> num2;

	for (int i = 0; i < num1; i++)
	{
		cin >> x;
		a.push(x);
	}
	for (int i = 0; i < num2; i++)
	{
		cin >> y;
		b.push(y);
	}
	a.print();
	cout << endl;
	b.print();
	cout << endl;
	a.reverse();
	b.reverse();
	a.print();
	cout << endl;
	b.print();
	return 0;
}


