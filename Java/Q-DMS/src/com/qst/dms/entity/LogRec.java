package com.qst.dms.entity;
import java.util.Date;

public class LogRec {
    private int id;
    private Date time;
    private String address;
    private int type;
    /**
     * Login username
     */
    private String user;
    /**
     * Login user ip
     */
    private String ip;
    /**
     * State of login user
     */
    private int logType;
    /**
     * Constant of login state: LOG_IN LOG_OUT
     */
    public static final int LOG_IN = 1;
    public static final int LOG_OUT = 0;

    //Other Constant
    public static final int GATHER = 1;
    public static final int MATCH = 2;
    public static final int RECORD = 3;
    public static final int SEND = 4;
    public static final int RECEIVE = 5;
    public static final int WRITE = 6;
    public static final int SAVE = 7;

    public int getId() {
        return id;
    }
    public void setId(int id) {
        this.id = id;
    }
    public Date getTime() {
        return time;
    }
    public void setTime(Date time) {
        this.time = time;
    }
    public String getAddress() {
        return address;
    }
    public void setAddress(String address) {
        this.address = address;
    }
    public int getType() {
        return type;
    }
    public void setType(int type) {
        this.type = type;
    }
    public String getUser() {
        return user;
    }
    public void setUser(String user) {
        this.user = user;
    }
    public String getIp() {
        return ip;
    }
    public void setIp(String ip) {
        this.ip = ip;
    }
    public int getLogType() {
        return logType;
    }
    public void setLogType(int logType) {
        this.logType = logType;
    }

    public LogRec(){
    }
    public LogRec(int id, Date time, String address, int type, String user, String ip, int logType) {
        this.id = id;
        this.time = time;
        this.address = address;
        this.type = type;
        this.user = user;
        this.ip = ip;
        this.logType = logType;
    }

    public String toString(){
        return id + "," + time + "," + address + "," + type + "," + user + "," + ip + "," + logType;
    }
}
