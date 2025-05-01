package cc.lymone.java.homework;

class Person {
    private String name;
    private int age;
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public int getAge() {
        return age;
    }
    public void setAge(int age) {
        this.age = age;
    }
    public String toString() {
        return "name:" + name + ", age:" + age ;
    }
}

class Student extends Person {
    private String studentId;
    public Student(String name, int age,String studentId) {
        super(name, age);
        this.studentId = studentId;
    }
    public String getStudentId() {
        return studentId;
    }
    public void setStudentId(String studentId) {
        this.studentId = studentId;
    }
    public String toString() {
        return super.toString() + ", studentId:" + studentId;
    }
}

class Teacher extends Person {
    private String teacherId;
    public Teacher(String name, int age,String teacherId) {
        super(name, age);
        this.teacherId = teacherId;
    }
    public String getTeacherId() {
        return teacherId;
    }
    public void setTeacherId(String teacherId) {
        this.teacherId = teacherId;
    }
    public String toString() {
        return super.toString() + ", teacherId:" + teacherId;
    }
}

public class Chapter5 {
    public static void main(String[] args) {
        Person student1 = new Student("Yang", 20, "08221234");
        Person teacher1 = new Teacher("Jackson", 30, "1234");
        System.out.println(student1);
        System.out.println(teacher1);
    }
}
