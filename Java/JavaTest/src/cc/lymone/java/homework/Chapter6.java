package cc.lymone.java.homework;

interface calculate<T>{
    public T add(T a, T b);
    public T sub(T a, T b);
    public T mul(T a, T b);
    public T div(T a, T b);
}
class Calculate_ implements calculate<Integer>{
    public Integer add(Integer a, Integer b){
        return a+b;
    }
    public Integer sub(Integer a, Integer b){
        return a-b;
    }
    public Integer mul(Integer a, Integer b){
        return a*b;
    }
    public Integer div(Integer a, Integer b){
        return a/b;
    }
}
public class Chapter6 {
    public static void main(String[] args) {
        Calculate_ cal = new Calculate_();
        System.out.println("1 + 2 = " + cal.add(1,2).toString());
        System.out.println("5 - 4 = " + cal.sub(5,4).toString());
        System.out.println("5 * 5 = " + cal.mul(5,5).toString());
        System.out.println("8 / 2 = " + cal.div(8,2).toString());
    }
}
