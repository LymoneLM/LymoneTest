package cc.lymone.java.homework;

class Book_ {
    private String name;
    private int pages;

    Book_(String name, int pages) {
        this.name = name;
        this.pages = pages;
    }


    public String toString() {
        return "Book [name=" + name + ", pages=" + pages + "]";
    }
}

class BookDemo {
    public static void main(String[] args) {
        Book_ book = new Book_("Java8基础教程", 256);
        System.out.println(book);
    }
}



