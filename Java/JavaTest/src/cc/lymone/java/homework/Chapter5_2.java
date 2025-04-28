package cc.lymone.java.homework;

import java.util.List;
import java.util.Stack;

class Fruit{
    private double weight;
    private String color;
    public Fruit(double weight, String color) {
        this.weight = weight;
        this.color = color;
    }
    public double getWeight() {
        return weight;
    }
    public void setWeight(double weight) {
        this.weight = weight;
    }
    public String getColor() {
        return color;
    }
    public void setColor(String color) {
        this.color = color;
    }
    public String toString() {
        return "Fruit [weight=" + weight + ", color=" + color + "]";
    }
}
class Apple extends Fruit{
    public Apple(double weight, String color) {
        super(weight, color);
    }
    public String toString() {
        return "Apple [weight=" + getWeight() + ", color=" + getColor() + "]";
    }
}
class Orange extends Fruit{
    public Orange(double weight, String color) {
        super(weight, color);
    }
    public String toString() {
        return "Orange [weight=" + getWeight() + ", color=" + getColor() + "]";
    }
}
class Pear extends Fruit{
    public Pear(double weight, String color) {
        super(weight, color);
    }
    public String toString() {
        return "Pear [weight=" + getWeight() + ", color=" + getColor() + "]";
    }
}
class Box{
    List<Fruit> box = new Stack<>();
    public void addFruit(Fruit fruit){
        box.add(fruit);
    }
    public Fruit getFruit(){
        if(box.isEmpty()){
            return null;
        } else {
            return box.removeFirst();
        }
    }
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for(Fruit fruit : box){
            sb.append(fruit).append('\n');
        }
        return sb.toString();
    }
}
public class Chapter5_2 {
    public static void main(String[] args) {
        Fruit apple = new Apple(1.5, "red");
        Fruit orange = new Orange(3.5, "orange");
        Fruit pear = new Pear(2.5, "yellow");
        Box box = new Box();
        box.addFruit(apple);
        box.addFruit(orange);
        box.addFruit(pear);
        System.out.print("Now in box:\n" + box);
        System.out.println("Get fruit from box: " + box.getFruit());
        System.out.print("Now in box:\n" + box);
    }
}
