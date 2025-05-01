package com.qst.dms.dos;
import java.util.Scanner;
public class MenuDriver {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        while(true){
            System.out.println("**********************");
            System.out.println("* 1.数据采集 2.数据匹配 *");
            System.out.println("* 3.数据记录 4.数据显示 *");
            System.out.println("* 5.数据发送 0.退出应用 *");
            System.out.println("**********************");

            System.out.print("请输入菜单项（0~5）：");
            int choice = sc.nextInt();
            switch(choice){
                case 1:
                    System.out.println("数据采集中……");
                    break;
                case 2:
                    System.out.println("数据匹配中……");
                    break;
                case 3:
                    System.out.println("数据记录中……");
                    break;
                case 4:
                    System.out.println("数据显示中……");
                    break;
                case 5:
                    System.out.println("数据发送中……");
                    break;
                case 0:
                    System.out.println("程序退出");
                    System.exit(0);

                default:
                    System.out.println("* 请输入正确的菜单项（0~5）");
            }
        }
    }
}
