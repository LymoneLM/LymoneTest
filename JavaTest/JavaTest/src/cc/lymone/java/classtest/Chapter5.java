package cc.lymone.java.classtest;

//class Thread_test extends Thread{
//    @Override
//    public void run() {
////        super.run();
//        while(true)
//            System.out.println("正在执行："+currentThread());
//    }
//}

public class Chapter5 {
    public static void main(String[] args) {
        for(int i=0;i<10;i++){
            new Thread(new Runnable(){
                public void run(){
                    while(true){
                        System.out.println("正在执行："+Thread.currentThread());
                    }
                }
            }).start();
        }

    }
}
