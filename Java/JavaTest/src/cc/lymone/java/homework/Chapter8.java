package cc.lymone.java.homework;

import java.util.Collections;
import java.util.List;
import java.util.ArrayList;

class Book implements Comparable<Book> {
    private String title;
    private double price;

    public Book(String title, double price) {
        this.title = title;
        this.price = price;
    }
    public String getTitle() {
        return title;
    }
    public double getPrice() {
        return price;
    }
    public void setTitle(String title) {
        this.title = title;
    }
    public void setPrice(double price) {
        this.price = price;
    }
    public int compareTo(Book b) {
        return Double.compare(this.price, b.getPrice());
    }
    public String toString() {
        return "Price:" + price + "\t" + "Title:" + title;
    }
}

public class Chapter8 {
    public static void main(String[] args) {
        List<Book> books = new ArrayList<Book>();
        books.add(new Book("Java Programming", 78.00));
        books.add(new Book("Python Programming", 128.00));
        books.add(new Book("Java Programming", 56.00));
        books.add(new Book("Cpp Programming", 172.00));
        books.add(new Book("C Programming", 99.00));
        books.add(new Book("JavaScript Programming", 88.00));
        books.add(new Book("CSharp Programming", 228.00));
        Collections.sort(books);
        for(Book b : books) {
            System.out.println(b);
        }
    }
}
