#ifndef LINKLIST_H
#define LINKLIST_H
#include <iostream>
using namespace std;
template <typename T>
class Node
{
	public:
		/* ��������ڵ�Ķ��� */
		T data; // ��ʾ������
		Node<T> *next;  // ��ʾָ���򣬴洢��һ���ڵ��λ��
};
template <typename T>
class LinkList : public Node<T>
{
	private:
		/* ��������Ķ��� */
		Node<T> *head; // ͷ�ڵ�
	public:
		/* ��Ա���������� */
		LinkList(); // ��дĬ�ϵĹ��캯��
		bool Empty(); // �ж������Ƿ�Ϊ��
		int GetLen(); // ��ȡ����ĳ���
		void insert(T elem); // Ĭ�ϲ�������Ŀ�ͷ
		bool insert(int idx, T elem); // �������ָ��λ�ò���Ԫ��
		void remove(T &elem); // Ĭ��ɾ������ĵ�һ��Ԫ�أ������ظ�Ԫ��
		bool remove(int idx, T &elem); // ɾ����ָ��λ�õ�Ԫ��
		bool index(int idx, T &elem); // �ҳ�������ָ��λ�õ�Ԫ��
		int index(bool (*compare(T, T)), T elem); // �ҵ�����������compare��Ԫ��
		void traverse(void (* print)(T &elem)); // ���ڱ�����������
};


/* ����ʵ�ֳ�Ա�����Ķ��� */
template <typename T>
inline LinkList<T>::LinkList()
{
	this -> head = (Node<T> *)malloc(sizeof(Node<T>));
	if (!this -> head)
	{
		cerr << "Error allocating memory!" << endl;
	}
	this -> head -> next = nullptr;
}

template <typename T>
inline bool LinkList<T>::Empty()
{
	if (this -> head == nullptr)
	{
		return true;
	}
	return false;
}

template <typename T>
int LinkList<T>::GetLen()
{
	Node<T> *tmp = this -> head -> next;
	int counter = 0;
	while (tmp)
	{
		counter++;
		tmp = tmp -> next;
	}
	return counter;
}

template <typename T>
inline void LinkList<T>::insert(T elem)
{
	Node<T> *newnode = (Node<T> *)malloc(sizeof(Node<T>));
	newnode -> data = elem;
	newnode -> next = this -> head -> next;
	this -> head -> next = newnode;
}

template <typename T>
bool LinkList<T>::insert(int idx, T elem)
{
	if (idx < 1 || idx > this -> GetLen() + 1)
	{
		cerr << "subscript wrong!" << endl;
		return false;
	}
	int counter = 0;
	Node<T> *newnode = this -> head, *tmp = (Node<T> *)malloc(sizeof(Node<T>));
	while (counter < idx - 1 && newnode -> next != nullptr)
	{
		counter++;
		newnode = newnode -> next;
	}
	tmp -> data = elem;
	tmp -> next = newnode -> next;
	newnode -> next = tmp;
	return true;
}

template <typename T>
void LinkList<T>::remove(T &elem)
{
	Node<T> *tmp = this -> head -> next;
	this -> head -> next = tmp -> next;
	elem = tmp -> data;
	free(tmp);
}

template <typename T>
bool LinkList<T>::remove(int idx, T &elem)
{
	if (idx < 1 || idx > this -> GetLen())
	{
		cerr << "subscript wrong!" << endl;
		return false;
	}
	Node<T> *newnode = this -> head, *tmp;
	int counter = 0;
	while (counter < idx - 1 && newnode -> next != nullptr)
	{
		newnode = newnode -> next;
		counter++;
	}
	tmp = newnode -> next;
	elem = tmp -> data;
	newnode -> next = tmp -> next;
	free(tmp);
	return true;
}

template <typename T>
bool LinkList<T>::index(int idx, T &elem)
{
	if (idx < 1 || idx > this -> GetLen())
	{
		cerr << "subscript wrong!" << endl;
		return false;
	}
	Node<T> *newnode = this -> head -> next;
	int counter = 1;
	while (counter < idx)
	{
		counter++;
		newnode = newnode -> next;
	}
	elem = newnode -> data;
	return true;
}

template <typename T>
int LinkList<T>::index(bool (*compare(T, T)), T elem)
{
	Node<T> *newnode = this -> head;
	int counter = 0;
	while (newnode -> next != nullptr)
	{
		newnode = newnode -> next;
		counter++;
		if (compare(newnode -> data, elem))
		{
			return counter;
		}
	}
	return -1;
}
template <typename T>
void LinkList<T>::traverse(void (* print)(T &elem))
{
	Node<T> *tmp = this -> head -> next;
	while (tmp)
	{
		print(tmp -> data);
		tmp = tmp -> next;
	}
	cout << endl;
}

/* ���ڶ���ǳ�Ա���� */
template <typename T>
void show(LinkList<T> &L)
{
	cout << "length : " << L.GetLen() << endl;
}

template <typename T>
void print(T &elem)
{
	cout << elem << " ";
}
#endif

int main()
{
	LinkList<int> a;
	return 0;
 } 
