class Table {
 	 static void printTable(int n){
 	 	 synchronized (Table.class) { // lock on the class object
             for (int i=1 ; i<=5 ; i++){
                 System.out.println(n * i);
                 try { 
                     Thread.sleep(400); 
                 } catch(InterruptedException e) {
                     e.printStackTrace();
                 }
             }
             System.out.println("------");
         }
     }
}
class MyThread1 extends Thread{
    public void run(){
        Table.printTable(5);    
    }
}
class MyThread2 extends Thread{
    public void run(){
        Table.printTable(100);    
    }
}
class MyThread3 extends Thread{
    public void run(){
        Table.printTable(1000);    
    }
}
public class StaticSyncDemo {
public static void main(String[] args) {
MyThread1 t1 = new MyThread1();
MyThread2 t2 = new MyThread2();
MyThread3 t3 = new MyThread3();
t1.start();
t2.start();
t3.start();
}
}