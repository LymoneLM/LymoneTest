package com.qst.dms.dos;
import java.util.Scanner;
public class DataShow {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int[] data=new int[10];
        for(int i=0;i<data.length;i++){
            System.out.print("情输入第" + ( i + 1 ) + "个采集数据:");
            data[i]=sc.nextInt();
        }
        int i = 0;
        for(int e : data){
            System.out.print(e + " ");
            i++;
            if(i%5==0) {
                System.out.println();
            }
        }
    }
}
