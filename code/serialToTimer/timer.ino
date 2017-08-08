int one[] = {HIGH, LOW, LOW, HIGH, HIGH, HIGH, HIGH};
int two[] = {LOW, LOW, HIGH, LOW, LOW, HIGH, LOW};
int three[] = {LOW, LOW, LOW, LOW, HIGH, HIGH, LOW};
int four[] = {HIGH, LOW, LOW, HIGH, HIGH, LOW, LOW};
int five[] = {LOW, HIGH, LOW, LOW, HIGH, LOW, LOW};
int six[] = {LOW, HIGH, LOW, LOW, LOW, LOW, LOW};
int seven[] = {LOW, LOW, LOW, HIGH, HIGH, HIGH, HIGH};
int eight[] = {LOW, LOW, LOW, LOW, LOW, LOW, LOW};
int nine[] = {LOW, LOW, LOW, LOW, HIGH, LOW, LOW};
int zero[] = {LOW, LOW, LOW, LOW, LOW, LOW, HIGH};
int blank[] = {HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH};
int f[] = {LOW, HIGH, HIGH, HIGH, LOW, LOW, LOW};

int pin[7];
//int pin[] = {10, 11, 5, 6, 7, 9, 8};
int first, second, third;

//setting up the timer
void timerSetup() {
  // put your setup code here, to run once:
  for(int i=0;i<7;i++) {
    pinMode(pin[i], OUTPUT);
  }
  pinMode(first, OUTPUT);
  pinMode(second, OUTPUT);
  pinMode(third, OUTPUT);
}

//setting the pins for the timer
void pinSetup(int inpin[], int frst, int scnd, int thrd)  {
  for(int i=0;i<7;i++)
    pin[i] = inpin[i];
  first = frst;
  second = scnd;
  third = thrd;
}


//function to print one 3-digit number
void numberPrint(int count) {
  int temp;
  temp = count;
  pinSelect(3);
  display1(temp%10);
  delay(7);
  temp /= 10;
  pinSelect(2);
  display1(temp%10);
  delay(7);
  temp /= 10;
  pinSelect(1);
  display1(temp%10);
  delay(7);
}

//function for counter from count passed to zero
void counter(int count) {
  int i;
  while(count>=0) {
     for(i=1;i<=60;i++)
      numberPrint(count);
    count--;
  }
  display1(67);
}

//function to display a digit on a LED
void display1(int n)
{
  int* input;
  
  switch(n)
  {
    case 0:input=zero;
    break;

    case 1:input=one;
    break;

    case 2:input=two;
    break;

    case 3:input=three;
    break;

    case 4:input=four;
    break;

    case 5:input=five;
    break;

    case 6:input=six;
    break;

    case 7:input=seven;
    break;

    case 8:input=eight;
    break;

    case 9:input=nine;
    break;

    case 10:input = f;
    break;
    
    default: input = blank;
    break;

  }
  for(int i=0;i<7;i++)
  {
    digitalWrite(pin[i], input[i]);
  }
  
}

//function for selection of pins in 3-digit LED
void pinSelect(int n) {
  if(n==1)  {
    digitalWrite(first, HIGH);
    digitalWrite(second, LOW);
    digitalWrite(third, LOW);
  } else if(n==2) {
    digitalWrite(first, LOW);
    digitalWrite(second, HIGH);
    digitalWrite(third, LOW);
  } else if(n==3) {
    digitalWrite(first, LOW);
    digitalWrite(second, LOW);
    digitalWrite(third, HIGH);
  }
}

//function to display OFF 
void off()  {
  for(int i=0;i<1000;i++) {
    pinSelect(1);
    display1(0);
    delay(5);
    pinSelect(2);
    display1(10);
    delay(5);
    pinSelect(3);
    display1(10);
    delay(5);
  }
}

