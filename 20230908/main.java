// import java.io.*;
import java.util.ArrayList;

class MaxExample { 
 
  public static void main(String args[]){
    Integer n = 10;
    ArrayList<Integer> arrayRandom = new ArrayList<Integer>(n);

    
    for (int i=0; i<n; i++)
    {
        Integer r = (int)(Math.random()*200) - 100;
        arrayRandom.add(r);
    }
 
    // Вызов метода getMax () для получения максимального значения
    int max = getMax(arrayRandom);
    System.out.println(arrayRandom);
    System.out.println("Maximum Value is: "+max);

  }
 
  //здесь находим максимум
  public static int getMax(ArrayList<Integer> inputArray){ 
    int maxValue = inputArray.get(0);
    for(int i=1; i < inputArray.size(); i++){ 
        if(inputArray.get(i) > maxValue){ 
            maxValue = inputArray.get(i); 
        }
    } 
    return maxValue; 
  }
 
}