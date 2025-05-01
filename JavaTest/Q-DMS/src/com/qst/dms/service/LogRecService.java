package com.qst.dms.service;

import java.util.Date;
import java.util.Scanner;

import com.qst.dms.entity.LogRec;

public class LogRecService {
    public LogRec inputLog() {
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入ID标识:");
        int id = sc.nextInt();
        Date nowDate = new Date();
        System.out.println("请输入地址:");
        String address = sc.next();
        int type = LogRec.GATHER;

        System.out.println("请输入 登录用户名:");
        String user = sc.next();
        System.out.println("请输入 主机IP:");
        String ip = sc.next();
        System.out.println("请输入登录状态(1/0):");
        int logType = sc.nextInt();
        return new LogRec(id, nowDate, address, type, user, ip, logType);
    }
    public void showLog(LogRec... logRec) {
        for (LogRec log : logRec) {
            if (log != null) {
                System.out.println(log.toString());
            }
        }
    }
}
