package cc.lymone.java.homework;

abstract class Fruit_{
    abstract void plant();
}
class Apple_ extends Fruit_{
    void plant() {
        System.out.println("plant Apple tree");
    }
}
class Strawberry extends Fruit_{
    void plant() {
        System.out.println("plant Strawberry bash");
    }
}
public class Chapter6_2 {
    public static void main(String[] args) {
        Fruit_ apple = new Apple_();
        apple.plant();
        Fruit_ strawberry = new Strawberry();
        strawberry.plant();
    }
}
