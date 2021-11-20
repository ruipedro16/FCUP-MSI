# Activator

Using a [java decompiler](https://github.com/java-decompiler/jd-gui/), we
can decompile the jar file and inspect the source code:

```java
import java.util.Scanner;

public class Activator {
    private static Boolean isValidSerialNumber(String paramString) {
        String[] arrayOfString = paramString.split("-");
        if (arrayOfString.length != 4)
            return Boolean.valueOf(false);
        Integer integer1 = Integer.valueOf(Integer.parseInt(arrayOfString[0], 16));
        Integer integer2 = Integer.valueOf(Integer.parseInt(arrayOfString[1], 16));
        Integer integer3 = Integer.valueOf(Integer.parseInt(arrayOfString[2], 16));
        Integer integer4 = Integer.valueOf(Integer.parseInt(arrayOfString[3], 16));
        if (integer2.intValue() != 4919)
            return Boolean.valueOf(false);
        if (integer1.intValue() + 1337 != 12248)
            return Boolean.valueOf(false);
        if (integer3.intValue() != integer2.intValue() + 33479)
            return Boolean.valueOf(false);
        if (integer4.intValue() != Integer.parseInt("d34d", 16))
            return Boolean.valueOf(false);
        return Boolean.valueOf(true);
    }

    public static void main(String[] paramArrayOfString) {
        System.out.print("Enter Serial Number: ");
        Scanner scanner = new Scanner(System.in);
        String str = scanner.nextLine();
        if (isValidSerialNumber(str).booleanValue()) {
            System.out.println("Success! Here is your flag: TPAS{" + str + "}");
        } else {
            System.out.println("Invalid Serial Number");
        }
    }
}
```

From `String[] arrayOfString = paramString.split("-");`, we know that the serial number is of the form
`A-B-C-D` and from `Integer.parseInt(arrayOfString[0], 16)` we know that these are hexadecimal numbers.

From `if (integer4.intValue() != Integer.parseInt("d34d", 16)) { return Boolean.valueOf(false); }`,
we know that `D` is D34D.

From `if (integer2.intValue() != 4919) { return Boolean.valueOf(false); }` we know the the value of `B`
is 4919, that is, 1337 in hexadecimal.

From `if (integer3.intValue() != integer2.intValue() + 33479) { return Boolean.valueOf(false); } `, we
know the the value of `C` is B + 33479 = 4919 + 33479 = 38398, that is 95FE in hexadecimal.

Finally, from `if (integer1.intValue() + 1337 != 12248) { return Boolean.valueOf(false); }`, we know
that the value of `A` is 12248 - 1337 = 10911, that is 2A9F in hexadecimal. Thus, the serial number
is `2A9F-1337-95FE-D34D`.

We can then get the flag by running `java -jar activator.jar` and providing the serial number:

```
$ java -jar activator.jar

Enter Serial Number: 2A9F-1337-95FE-D34D
Success! Here is your flag: TPAS{2A9F-1337-95FE-D34D}
```
