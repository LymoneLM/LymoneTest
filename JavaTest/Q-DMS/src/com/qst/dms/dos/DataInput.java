package com.qst.dms.dos;
import java.util.Scanner;
public class DataInput {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int[] data = new int[10];
        for (int i = 0; i < data.length; i++) {
            System.out.print("请输入第 " + ( i+1 ) + "个采集数据: ");
            data[i] = sc.nextInt();
        }
        for (int i = 0; i < data.length; i++) {
            System.out.print(data[i] + " ");
        }
        System.out.println();
    }
}
