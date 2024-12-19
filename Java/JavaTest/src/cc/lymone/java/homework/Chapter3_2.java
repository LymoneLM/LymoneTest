package cc.lymone.java.homework;

class Point{
    private double x;
    private double y;
    public Point(double x, double y){
        this.x = x;
        this.y = y;
    }
    public double getX(){
        return x;
    }
    public double getY(){
        return y;
    }
    public void setX(double x){
        this.x = x;
    }
    public void setY(double y){
        this.y = y;
    }
}

class PointDemo{
    public static double distance(Point p1, Point p2){
        double dx = p2.getX() - p1.getX();
        double dy = p2.getY() - p1.getY();
        return Math.sqrt(dx*dx + dy*dy);
    }
    public static void main(String[] args) {
        Point p1 = new Point(11,12);
        Point p2 = new Point(23,34);
        System.out.println("Distance of p1 and p2 is:"+distance(p1,p2));
    }
}

