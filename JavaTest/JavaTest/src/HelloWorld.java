public class HelloWorld {
    /*public static void main(String[] args) {
        for (String a : args) {
            System.out.println(a);
        }
        *//*
        Usb a = new usbDisk();
        a.call();
        *//*
        Son a;
        a.call();

    }*/
    public abstract class AbsObj {
        private String name;

        public AbsObj(String name) {
            this.name = name;
        }

        public String getName() {
            return name;
        }
        public void setName(String name) {
            this.name = name;
        }

        public abstract void call();

        @Override
        public String toString() {
            return super.toString();
        }
    }
    public class AbsObj2 extends AbsObj {
        public AbsObj2(String name) {
            super(name);
        }
        public void call() {
            System.out.println("call2");
        }
    }
    public class AbsObj3 extends AbsObj {
        public AbsObj3(String name) {
            super(name);
        }
        public void call() {
            System.out.println("call3");
        }
    }
    public interface Usb{
        void call();
    }
    public interface Pci{
        void move();
    }
    public static class usbDisk implements Usb,Pci{
        public void call() {
            System.out.println("call4");
        }
        public void move() {
            System.out.println("move");
        }
    }
    public class Father{
        public  void call(){
            System.out.println("call911");
        }
    }
    public class Son extends Father{

    }
    public class MyException extends Exception {

    }
}
